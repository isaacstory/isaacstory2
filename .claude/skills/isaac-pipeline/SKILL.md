---
name: isaac-pipeline
command: /isaac-pipeline
description: Run the complete Isaac Clinical Document Pipeline - all 3 stages sequentially. Organizes files from dropbasket, generates markdown, and builds JSONL database. Use this for full processing of new documents or reprocessing existing ones.
---

# Isaac Clinical Document Pipeline

Run all 3 stages of the document processing pipeline.

## Pipeline Overview

```
dropbasket/ → [Stage 1] → categorized folders → [Stage 2] → markdown/ → [Stage 3] → data/
              Organize       Exams/Blood/...      Markdown     markdown/...    JSONL      data/*.jsonl
```

## Commands

| Command | Description |
|---------|-------------|
| `/isaac-pipeline` | Run all stages (default) |
| `/isaac-pipeline --force` | Reprocess all files |
| `/isaac-pipeline --from-stage 2` | Start from specific stage |
| `/isaac-pipeline --category Blood` | Process only specific category |

## Arguments

- `--force`: Reprocess all files, ignoring completion status
- `--from-stage N`: Start from stage N (1, 2, or 3)
- `--category X`: Only process files in category X
- `--dry-run`: Show what would be processed without making changes

## Workflow

### Default Run (no arguments)

1. **Check dropbasket** for new files
2. **Stage 1 - Organize**: Process files in dropbasket
   - Skip if dropbasket is empty
3. **Stage 2 - Markdown**: Generate markdown for files with `markdown.completed = false`
   - Skip if no files pending
4. **Stage 3 - JSONL**: Build database records for files with `jsonl.completed = false`
   - Skip if no files pending
5. **Report summary**

### With --force

Resets pipeline status and reprocesses everything:
1. Reset `pipeline.markdown.completed = false` for all files
2. Reset `pipeline.jsonl.completed = false` for all files
3. Run stages 2 and 3

### With --from-stage N

Start from a specific stage:
- `--from-stage 1`: Full pipeline (same as default)
- `--from-stage 2`: Skip organize, run markdown + JSONL
- `--from-stage 3`: Skip organize and markdown, run JSONL only

## Stage Summaries

### Stage 1: Organize (`/isaac-organize`)
- Scans `dropbasket/` for files
- Computes hash to detect duplicates
- Categorizes using AI
- Moves to structured folders
- Updates inventory

### Stage 2: Markdown (`/isaac-markdown`)
- Reads categorized PDFs
- Extracts structured data
- Applies category templates
- Writes markdown to `markdown/`
- Updates inventory

### Stage 3: JSONL (`/isaac-data`)
- Parses markdown files
- Extracts granular records
- Appends to JSONL files
- Rebuilds catalog.json
- Updates inventory

## Pipeline Status Check

Before running, show status:

```
Pipeline Status:
├── Stage 1 (Organize): 136 files completed, 0 pending in dropbasket
├── Stage 2 (Markdown): 0 completed, 136 pending
└── Stage 3 (JSONL):    0 completed, 136 pending

Ready to run stages 2 and 3.
Proceed? [Y/n]
```

## Error Handling

- If a stage fails, stop and report
- Allow `--continue-on-error` to proceed despite failures
- Failed files are marked and can be retried

## Progress Reporting

Show live progress:

```
Isaac Pipeline - Running all stages

Stage 1: Organize
  └── No new files in dropbasket

Stage 2: Markdown (136 files)
  ├── Batch 1/14: Processing...
  ├── Batch 2/14: Processing...
  └── Complete: 136 markdown files generated

Stage 3: JSONL (136 files)
  ├── Batch 1/14: Extracting records...
  ├── Batch 2/14: Extracting records...
  └── Complete: 2,450 exam results, 180 prescriptions

Summary:
  ├── Files processed: 136
  ├── Markdown generated: 136
  ├── JSONL records created: 2,630
  └── Catalog updated: data/catalog.json
```

## Usage Examples

```bash
# Full pipeline for new documents
/isaac-pipeline

# Reprocess everything after template updates
/isaac-pipeline --force

# Just rebuild the JSONL database
/isaac-pipeline --from-stage 3

# Process only blood tests
/isaac-pipeline --category Blood

# Check what would be processed
/isaac-pipeline --dry-run
```

## Files Modified

After a full run:
- `inventory.json`: Updated pipeline status for all files
- `markdown/*`: Generated markdown files
- `data/exam_results.jsonl`: Test results
- `data/prescriptions.jsonl`: Medications
- `data/documents.jsonl`: Document metadata
- `data/catalog.json`: Summary statistics

## Execution Implementation

When this skill is invoked:

1. Parse command arguments
2. Load inventory and calculate pipeline status
3. Show status and confirm with user (unless `--yes`)
4. Execute stages sequentially:

```
# Stage 1
if dropbasket has files:
    invoke /isaac-organize skill

# Stage 2
files_pending_markdown = [f for f in inventory if not f.pipeline.markdown.completed]
if files_pending_markdown or --force:
    invoke /isaac-markdown skill

# Stage 3
files_pending_jsonl = [f for f in inventory if not f.pipeline.jsonl.completed]
if files_pending_jsonl or --force:
    invoke /isaac-data skill
```

5. Generate final summary report
