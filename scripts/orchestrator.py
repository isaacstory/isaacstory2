#!/usr/bin/env python3
"""
Isaac Pipeline Orchestrator

Code orchestrates, Claude processes.
Inverts the architecture: Python script controls workflow, Claude CLI processes files.

Usage:
    ./scripts/orchestrator.py                    # Run all pending (4 workers)
    ./scripts/orchestrator.py --stage 2          # Only PDF -> Markdown
    ./scripts/orchestrator.py --stage 3          # Only Markdown -> JSONL
    ./scripts/orchestrator.py --workers 8        # Use 8 parallel workers
    ./scripts/orchestrator.py --force            # Reprocess all
    ./scripts/orchestrator.py --file HASH        # Process specific file
    ./scripts/orchestrator.py --dry-run          # Show what would run
    ./scripts/orchestrator.py --category Blood   # Only process Blood category
"""

import argparse
import fcntl
import json
import logging
import os
import subprocess
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
from pathlib import Path
from typing import Optional

# Project paths
PROJECT_ROOT = Path(__file__).parent.parent
INVENTORY_PATH = PROJECT_ROOT / "inventory.json"
SCHEMAS_DIR = Path(__file__).parent / "schemas"
PROMPTS_DIR = Path(__file__).parent / "prompts"
MARKDOWN_DIR = PROJECT_ROOT / "markdown"
DATA_DIR = PROJECT_ROOT / "data"
LOG_PATH = Path(__file__).parent / "orchestrator.log"

# Processing config
DEFAULT_WORKERS = 4
CLAUDE_TIMEOUT = 300  # seconds per file (5 minutes for complex documents)
MAX_RETRIES = 2

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | %(levelname)s | %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    handlers=[
        logging.FileHandler(LOG_PATH, encoding='utf-8'),
    ]
)
logger = logging.getLogger(__name__)


class Colors:
    """ANSI color codes for terminal output"""
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    DIM = '\033[2m'


def load_inventory() -> dict:
    """Load inventory.json with file locking"""
    with open(INVENTORY_PATH, 'r') as f:
        fcntl.flock(f.fileno(), fcntl.LOCK_SH)
        data = json.load(f)
        fcntl.flock(f.fileno(), fcntl.LOCK_UN)
    return data


def save_inventory(data: dict) -> None:
    """Save inventory.json with file locking"""
    with open(INVENTORY_PATH, 'w') as f:
        fcntl.flock(f.fileno(), fcntl.LOCK_EX)
        json.dump(data, f, indent=2, ensure_ascii=False)
        fcntl.flock(f.fileno(), fcntl.LOCK_UN)


def get_pending_files(stage: int, category: Optional[str] = None, force: bool = False) -> list:
    """Get files pending processing for a given stage"""
    inventory = load_inventory()
    pending = []

    for file_hash, info in inventory.get("files", {}).items():
        # Filter by category if specified
        if category and info.get("category") != category:
            continue

        pipeline = info.get("pipeline", {})

        if stage == 2:
            # Stage 2: PDF -> Markdown
            if not pipeline.get("organized", {}).get("completed"):
                continue  # Not organized yet
            markdown_info = pipeline.get("markdown", {})
            # Process if: not completed, OR failed (auto-retry), OR force
            if force or not markdown_info.get("completed") or markdown_info.get("failed"):
                pending.append((file_hash, info))

        elif stage == 3:
            # Stage 3: Markdown -> JSONL
            markdown_info = pipeline.get("markdown", {})
            if not markdown_info.get("completed"):
                continue  # Markdown not ready
            jsonl_info = pipeline.get("jsonl", {})
            # Process if: not completed, OR failed (auto-retry), OR force
            if force or not jsonl_info.get("completed") or jsonl_info.get("failed"):
                pending.append((file_hash, info))

    return pending


def load_prompt_template(stage: int) -> str:
    """Load the prompt template for a stage"""
    filename = "pdf_to_markdown.txt" if stage == 2 else "markdown_to_jsonl.txt"
    with open(PROMPTS_DIR / filename, 'r') as f:
        return f.read()


def load_schema(stage: int) -> dict:
    """Load the JSON schema for a stage"""
    filename = "markdown_output.json" if stage == 2 else "jsonl_output.json"
    with open(SCHEMAS_DIR / filename, 'r') as f:
        return json.load(f)


def build_prompt_stage2(file_hash: str, info: dict, template: str) -> str:
    """Build the prompt for PDF -> Markdown conversion"""
    pdf_path = PROJECT_ROOT / info["destination"]
    return template.format(
        pdf_path=str(pdf_path),
        category=info.get("category", "Unknown"),
        document_hash=file_hash
    )


def build_prompt_stage3(file_hash: str, info: dict, template: str) -> str:
    """Build the prompt for Markdown -> JSONL conversion"""
    # Determine markdown file path
    destination = info["destination"]
    markdown_path = MARKDOWN_DIR / Path(destination).with_suffix('.md').name

    # Try to find the actual markdown file
    category_path = Path(destination).parent
    filename = Path(destination).stem + ".md"
    possible_path = MARKDOWN_DIR / category_path / filename

    if possible_path.exists():
        markdown_path = possible_path

    source_path = PROJECT_ROOT / destination

    # Read markdown content directly to include in prompt
    markdown_content = ""
    if markdown_path.exists():
        with open(markdown_path, 'r') as f:
            markdown_content = f.read()

    # Build prompt with markdown content embedded
    base_prompt = template.format(
        markdown_path=str(markdown_path),
        category=info.get("category", "Unknown"),
        document_hash=file_hash,
        source_path=str(source_path)
    )

    # Append the actual markdown content
    return f"{base_prompt}\n\n---\nMARKDOWN CONTENT TO PARSE:\n---\n\n{markdown_content}"


def run_claude(prompt: str, schema: dict, allowed_tools: list = None, timeout: int = CLAUDE_TIMEOUT) -> dict:
    """
    Run Claude CLI with the given prompt and schema.

    Returns:
        dict with 'success', 'output', and optionally 'error'
    """
    cmd = [
        "claude",
        "-p", prompt,
        "--output-format", "json"
    ]

    # Add JSON schema constraint
    schema_str = json.dumps(schema)
    cmd.extend(["--json-schema", schema_str])

    # Add allowed tools if specified
    if allowed_tools:
        cmd.extend(["--allowedTools", ",".join(allowed_tools)])

    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=timeout,
            cwd=str(PROJECT_ROOT)
        )

        if result.returncode != 0:
            return {
                "success": False,
                "error": f"Claude CLI error: {result.stderr}"
            }

        # Parse the JSON output
        try:
            response = json.loads(result.stdout)

            # Claude CLI wraps output in metadata - extract the actual result
            if "result" in response:
                result_text = response["result"]

                # Find JSON block - Claude may include text before/after the JSON
                json_start = result_text.find("```json")
                if json_start != -1:
                    result_text = result_text[json_start + 7:]  # Skip ```json
                    json_end = result_text.find("```")
                    if json_end != -1:
                        result_text = result_text[:json_end]
                elif result_text.startswith("```"):
                    result_text = result_text[3:]
                    json_end = result_text.find("```")
                    if json_end != -1:
                        result_text = result_text[:json_end]

                result_text = result_text.strip()

                # Parse the actual JSON content
                output = json.loads(result_text)
                return {"success": True, "output": output}
            else:
                # Direct JSON output (no wrapper)
                return {"success": True, "output": response}
        except json.JSONDecodeError as e:
            return {
                "success": False,
                "error": f"Invalid JSON output: {e}\nRaw output: {result.stdout[:500]}"
            }

    except subprocess.TimeoutExpired:
        return {"success": False, "error": f"Timeout after {timeout}s"}
    except Exception as e:
        return {"success": False, "error": str(e)}


def validate_stage2_output(output: dict) -> tuple[bool, str]:
    """Validate Stage 2 output"""
    if not output:
        return False, "Empty output"

    if "markdown" not in output:
        return False, "Missing 'markdown' field"

    if not output["markdown"] or len(output["markdown"]) < 50:
        return False, "Markdown content too short"

    metadata = output.get("metadata", {})
    if not metadata.get("document_date"):
        return False, "Missing metadata.document_date"

    if not metadata.get("provider"):
        return False, "Missing metadata.provider"

    return True, ""


def validate_stage3_output(output: dict) -> tuple[bool, str]:
    """Validate Stage 3 output"""
    if not output:
        return False, "Empty output"

    if "records" not in output:
        return False, "Missing 'records' field"

    if not isinstance(output["records"], list):
        return False, "'records' must be an array"

    # Validate each record has required fields
    for i, record in enumerate(output["records"]):
        if not record.get("type"):
            return False, f"Record {i} missing 'type'"
        if not record.get("id"):
            return False, f"Record {i} missing 'id'"

    return True, ""


def write_markdown_file(file_hash: str, info: dict, output: dict) -> str:
    """Write markdown file and return the path"""
    destination = info["destination"]
    category_path = Path(destination).parent
    filename = Path(destination).stem + ".md"

    output_dir = MARKDOWN_DIR / category_path
    output_dir.mkdir(parents=True, exist_ok=True)

    output_path = output_dir / filename

    with open(output_path, 'w') as f:
        f.write(output["markdown"])

    return str(output_path.relative_to(PROJECT_ROOT))


def append_jsonl_records(records: list, category: str) -> int:
    """Append records to appropriate JSONL files. Returns count written."""
    DATA_DIR.mkdir(exist_ok=True)

    count = 0

    for record in records:
        record_type = record.get("type", "document")

        # Determine output file based on record type
        if record_type == "exam_result":
            output_file = DATA_DIR / "exam_results.jsonl"
        elif record_type == "prescription":
            output_file = DATA_DIR / "prescriptions.jsonl"
        elif record_type == "variant":
            output_file = DATA_DIR / "genetic_variants.jsonl"
        else:
            output_file = DATA_DIR / "documents.jsonl"

        # Append record
        with open(output_file, 'a') as f:
            f.write(json.dumps(record, ensure_ascii=False) + "\n")

        count += 1

    return count


def process_file_stage2(file_hash: str, info: dict, template: str, schema: dict, dry_run: bool = False) -> dict:
    """Process a single file for Stage 2 (PDF -> Markdown)"""
    filename = info.get("original_name", "unknown")
    result = {
        "hash": file_hash,
        "file": filename,
        "stage": 2,
        "status": "pending",
        "start_time": time.time()
    }

    logger.info(f"Stage2 START | {filename} | hash={file_hash[:16]}...")

    if dry_run:
        result["status"] = "dry_run"
        result["message"] = f"Would process: {info['destination']}"
        logger.info(f"Stage2 DRY_RUN | {filename}")
        return result

    try:
        # Build prompt
        prompt = build_prompt_stage2(file_hash, info, template)

        # Run Claude
        claude_result = run_claude(prompt, schema, allowed_tools=["Read"])

        if not claude_result["success"]:
            result["status"] = "failed"
            result["error"] = claude_result["error"]
            logger.error(f"Stage2 FAILED | {filename} | Claude error: {claude_result['error'][:100]}")
            return result

        output = claude_result["output"]

        # Validate output
        valid, error = validate_stage2_output(output)
        if not valid:
            result["status"] = "validation_failed"
            result["error"] = error
            logger.error(f"Stage2 VALIDATION_FAILED | {filename} | {error}")
            return result

        # Write markdown file
        output_path = write_markdown_file(file_hash, info, output)

        result["status"] = "ok"
        result["output_path"] = output_path
        result["metadata"] = output.get("metadata", {})
        result["duration"] = time.time() - result["start_time"]

        logger.info(f"Stage2 OK | {filename} | {result['duration']:.1f}s | output={output_path}")

    except Exception as e:
        result["status"] = "error"
        result["error"] = str(e)
        logger.error(f"Stage2 ERROR | {filename} | {str(e)}")

    return result


def process_file_stage3(file_hash: str, info: dict, template: str, schema: dict, dry_run: bool = False) -> dict:
    """Process a single file for Stage 3 (Markdown -> JSONL)"""
    filename = info.get("original_name", "unknown")
    result = {
        "hash": file_hash,
        "file": filename,
        "stage": 3,
        "status": "pending",
        "start_time": time.time()
    }

    logger.info(f"Stage3 START | {filename} | hash={file_hash[:16]}...")

    if dry_run:
        result["status"] = "dry_run"
        result["message"] = f"Would process: {info['destination']}"
        logger.info(f"Stage3 DRY_RUN | {filename}")
        return result

    try:
        # Build prompt
        prompt = build_prompt_stage3(file_hash, info, template)

        # Run Claude
        claude_result = run_claude(prompt, schema, allowed_tools=["Read"])

        if not claude_result["success"]:
            result["status"] = "failed"
            result["error"] = claude_result["error"]
            logger.error(f"Stage3 FAILED | {filename} | Claude error: {claude_result['error'][:100]}")
            return result

        output = claude_result["output"]

        # Validate output
        valid, error = validate_stage3_output(output)
        if not valid:
            result["status"] = "validation_failed"
            result["error"] = error
            logger.error(f"Stage3 VALIDATION_FAILED | {filename} | {error}")
            return result

        # Append records to JSONL files
        record_count = append_jsonl_records(output["records"], info.get("category"))

        result["status"] = "ok"
        result["record_count"] = record_count
        result["summary"] = output.get("document_summary", {})
        result["duration"] = time.time() - result["start_time"]

        logger.info(f"Stage3 OK | {filename} | {result['duration']:.1f}s | records={record_count}")

    except Exception as e:
        result["status"] = "error"
        result["error"] = str(e)
        logger.error(f"Stage3 ERROR | {filename} | {str(e)}")

    return result


def update_inventory_result(result: dict) -> None:
    """Update inventory with processing result"""
    inventory = load_inventory()
    file_info = inventory["files"].get(result["hash"])

    if not file_info:
        return

    stage_key = "markdown" if result["stage"] == 2 else "jsonl"

    if result["status"] == "ok":
        file_info["pipeline"][stage_key] = {
            "completed": True,
            "timestamp": datetime.now().isoformat(),
            "output_path": result.get("output_path"),
            "record_count": result.get("record_count"),
            "duration": result.get("duration")
        }
    else:
        # Track failures
        current = file_info["pipeline"].get(stage_key, {})
        attempts = current.get("attempts", 0) + 1
        file_info["pipeline"][stage_key] = {
            "completed": False,
            "failed": True,
            "error": result.get("error", "Unknown error"),
            "attempts": attempts,
            "last_attempt": datetime.now().isoformat()
        }

    save_inventory(inventory)


def display_header(stage: int, total: int, workers: int):
    """Display the header with stage info"""
    stage_name = "PDF -> Markdown" if stage == 2 else "Markdown -> JSONL"
    print(f"\n{Colors.BOLD}{Colors.CYAN}╔══════════════════════════════════════════════════════════════════╗{Colors.ENDC}")
    print(f"{Colors.BOLD}{Colors.CYAN}║  Isaac Pipeline - Stage {stage}: {stage_name:<35}║{Colors.ENDC}")
    print(f"{Colors.BOLD}{Colors.CYAN}╠══════════════════════════════════════════════════════════════════╣{Colors.ENDC}")
    print(f"{Colors.CYAN}║  Files pending: {total:<48}║{Colors.ENDC}")
    print(f"{Colors.CYAN}║  Workers: {workers:<53}║{Colors.ENDC}")
    print(f"{Colors.BOLD}{Colors.CYAN}╚══════════════════════════════════════════════════════════════════╝{Colors.ENDC}\n")


def display_progress(completed: int, total: int, ok: int, failed: int, current_files: list):
    """Display progress bar and status"""
    pct = (completed / total * 100) if total > 0 else 0
    bar_width = 40
    filled = int(bar_width * completed / total) if total > 0 else 0
    bar = '█' * filled + '░' * (bar_width - filled)

    print(f"\r{Colors.BOLD}Progress: [{bar}] {completed}/{total} ({pct:.1f}%){Colors.ENDC}", end="")
    print(f"  {Colors.GREEN}✓ {ok}{Colors.ENDC} | {Colors.RED}✗ {failed}{Colors.ENDC}", end="")

    if current_files:
        current = current_files[0] if len(current_files) == 1 else f"{len(current_files)} files"
        print(f"  | Processing: {current[:30]}", end="")

    print("        ", end="\r")


def display_result(result: dict):
    """Display a single result"""
    status = result["status"]
    filename = result["file"][:40]
    duration = result.get("duration", 0)

    if status == "ok":
        extra = ""
        if result.get("record_count"):
            extra = f" ({result['record_count']} records)"
        print(f"  {Colors.GREEN}✓{Colors.ENDC} {filename} ({duration:.1f}s){extra}")
    elif status == "dry_run":
        print(f"  {Colors.BLUE}○{Colors.ENDC} {filename} (dry run)")
    else:
        error = result.get("error", "Unknown")[:60]
        print(f"  {Colors.RED}✗{Colors.ENDC} {filename}: {error}")


def display_summary(results: list, stage: int, elapsed: float):
    """Display final summary"""
    ok = sum(1 for r in results if r["status"] == "ok")
    failed = sum(1 for r in results if r["status"] in ("failed", "error", "validation_failed"))
    dry_run = sum(1 for r in results if r["status"] == "dry_run")

    stage_name = "PDF -> Markdown" if stage == 2 else "Markdown -> JSONL"

    print(f"\n{Colors.BOLD}{'='*60}{Colors.ENDC}")
    print(f"{Colors.BOLD}Stage {stage}: {stage_name} - Complete{Colors.ENDC}")
    print(f"{'='*60}")
    print(f"  Total processed: {len(results)}")
    print(f"  {Colors.GREEN}Successful: {ok}{Colors.ENDC}")
    if failed > 0:
        print(f"  {Colors.RED}Failed: {failed}{Colors.ENDC}")
    if dry_run > 0:
        print(f"  {Colors.BLUE}Dry run: {dry_run}{Colors.ENDC}")
    print(f"  Time elapsed: {elapsed:.1f}s")

    if ok > 0 and elapsed > 0:
        rate = ok / elapsed * 60
        print(f"  Rate: {rate:.1f} files/min")

    print()


def run_stage(stage: int, workers: int, category: Optional[str], force: bool,
              dry_run: bool, file_hash: Optional[str] = None, verbose: bool = False):
    """Run a processing stage"""
    stage_name = "PDF->Markdown" if stage == 2 else "Markdown->JSONL"
    logger.info(f"{'='*60}")
    logger.info(f"STAGE {stage} ({stage_name}) STARTING | workers={workers} | category={category or 'all'} | force={force}")

    # Get pending files
    if file_hash:
        inventory = load_inventory()
        info = inventory["files"].get(file_hash)
        if not info:
            print(f"{Colors.RED}Error: File hash not found: {file_hash}{Colors.ENDC}")
            return
        pending = [(file_hash, info)]
    else:
        pending = get_pending_files(stage, category, force)

    if not pending:
        print(f"{Colors.YELLOW}No files pending for Stage {stage}{Colors.ENDC}")
        return

    # Load template and schema
    template = load_prompt_template(stage)
    schema = load_schema(stage)

    # Display header
    display_header(stage, len(pending), workers)

    # Choose processor function
    processor = process_file_stage2 if stage == 2 else process_file_stage3

    results = []
    start_time = time.time()
    current_files = []

    # Process files
    if workers == 1 or file_hash:
        # Sequential processing
        for i, (fhash, info) in enumerate(pending):
            current_files = [info.get("original_name", fhash[:8])]
            display_progress(i, len(pending),
                           sum(1 for r in results if r["status"] == "ok"),
                           sum(1 for r in results if r["status"] not in ("ok", "dry_run")),
                           current_files)

            result = processor(fhash, info, template, schema, dry_run)
            results.append(result)

            if not dry_run:
                update_inventory_result(result)

            if verbose:
                print()  # New line before result
                display_result(result)
    else:
        # Parallel processing with ThreadPoolExecutor
        with ThreadPoolExecutor(max_workers=workers) as executor:
            # Submit all tasks
            future_to_hash = {
                executor.submit(processor, fhash, info, template, schema, dry_run): (fhash, info)
                for fhash, info in pending
            }

            # Process completed tasks
            for future in as_completed(future_to_hash):
                fhash, info = future_to_hash[future]

                try:
                    result = future.result()
                    results.append(result)

                    if not dry_run:
                        update_inventory_result(result)

                    # Update display
                    display_progress(len(results), len(pending),
                                   sum(1 for r in results if r["status"] == "ok"),
                                   sum(1 for r in results if r["status"] not in ("ok", "dry_run")),
                                   [])

                    if verbose:
                        print()
                        display_result(result)

                except Exception as e:
                    results.append({
                        "hash": fhash,
                        "file": info.get("original_name", "unknown"),
                        "stage": stage,
                        "status": "error",
                        "error": str(e)
                    })

    # Final display
    print()  # Clear progress line

    if not verbose:
        # Show all results at the end
        print(f"\n{Colors.BOLD}Results:{Colors.ENDC}")
        for result in results:
            display_result(result)

    # Summary
    elapsed = time.time() - start_time
    display_summary(results, stage, elapsed)

    # Log summary
    ok = sum(1 for r in results if r["status"] == "ok")
    failed = sum(1 for r in results if r["status"] in ("failed", "error", "validation_failed"))
    logger.info(f"STAGE {stage} COMPLETE | total={len(results)} | ok={ok} | failed={failed} | elapsed={elapsed:.1f}s")

    return results


def main():
    parser = argparse.ArgumentParser(
        description="Isaac Pipeline Orchestrator - Code orchestrates, Claude processes",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s                    # Run all pending files through both stages
  %(prog)s --stage 2          # Only run Stage 2 (PDF -> Markdown)
  %(prog)s --stage 3          # Only run Stage 3 (Markdown -> JSONL)
  %(prog)s --workers 8        # Use 8 parallel workers
  %(prog)s --force            # Reprocess all files
  %(prog)s --file abc123      # Process specific file hash
  %(prog)s --dry-run          # Show what would be processed
  %(prog)s --category Blood   # Only process Blood category
        """
    )

    parser.add_argument("--stage", type=int, choices=[2, 3],
                       help="Run only specified stage (2: PDF->MD, 3: MD->JSONL)")
    parser.add_argument("--workers", "-w", type=int, default=DEFAULT_WORKERS,
                       help=f"Number of parallel workers (default: {DEFAULT_WORKERS})")
    parser.add_argument("--force", "-f", action="store_true",
                       help="Reprocess all files, ignoring completion status")
    parser.add_argument("--file", dest="file_hash",
                       help="Process specific file by hash")
    parser.add_argument("--dry-run", "-n", action="store_true",
                       help="Show what would be processed without running")
    parser.add_argument("--category", "-c",
                       help="Only process files in specified category")
    parser.add_argument("--verbose", "-v", action="store_true",
                       help="Show detailed progress for each file")

    args = parser.parse_args()

    # Validate paths
    if not INVENTORY_PATH.exists():
        print(f"{Colors.RED}Error: inventory.json not found at {INVENTORY_PATH}{Colors.ENDC}")
        sys.exit(1)

    # Ensure output directories exist
    MARKDOWN_DIR.mkdir(exist_ok=True)
    DATA_DIR.mkdir(exist_ok=True)

    print(f"{Colors.BOLD}{Colors.HEADER}")
    print("╔════════════════════════════════════════╗")
    print("║     Isaac Pipeline Orchestrator        ║")
    print("║   Code orchestrates, Claude processes  ║")
    print("╚════════════════════════════════════════╝")
    print(f"{Colors.ENDC}")

    stages_to_run = [args.stage] if args.stage else [2, 3]

    for stage in stages_to_run:
        run_stage(
            stage=stage,
            workers=args.workers,
            category=args.category,
            force=args.force,
            dry_run=args.dry_run,
            file_hash=args.file_hash,
            verbose=args.verbose
        )


if __name__ == "__main__":
    main()
