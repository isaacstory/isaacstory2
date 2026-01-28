# CLAUDE.md

## Project Overview

Isaac Clinical Document Pipeline - A document processing system for organizing and extracting structured data from medical records of Isaac (autistic child).

## Repository Structure

```
isaacstory2/
├── dropbasket/           # Incoming unprocessed files
├── Exams/                # Categorized exam documents
│   ├── Blood/
│   ├── Stool_GI/
│   ├── Urine/
│   ├── Genetic/
│   ├── Imaging/
│   ├── Metabolic_GreatPlains/
│   ├── Specialty/
│   ├── Assessments/
│   └── Requests/
├── Prescriptions/
│   ├── Medications/
│   └── Nutrition/
├── Consultations/
├── Tracking/
├── Newborn/
├── _duplicates/          # Duplicate files detected by hash
├── markdown/             # Generated markdown files (Stage 2 output)
├── data/                 # JSONL database files (Stage 3 output)
├── inventory.json        # Master file inventory with pipeline status
└── scripts/
    ├── orchestrator.py   # Main pipeline controller
    ├── prompts/          # Prompt templates for Claude
    └── schemas/          # JSON schemas for output validation
```

## Pipeline Architecture

The system processes clinical documents through 3 stages:

```
dropbasket/ → [Stage 1: Organize] → categorized folders
           → [Stage 2: Markdown] → markdown/
           → [Stage 3: JSONL]    → data/
```

### Stage 1: File Organization (`/isaac-organize`)
- Scans `dropbasket/` for new files
- Computes SHA256 hash to detect duplicates
- Categorizes files using Claude sub-agents
- Moves to appropriate folders with standardized names
- Updates `inventory.json`

### Stage 2: PDF → Markdown (`/isaac-markdown`)
- Reads PDFs from categorized folders
- Extracts structured data using category-specific templates
- Generates markdown files in `markdown/` directory
- Templates in `.claude/skills/isaac-markdown-generator/references/templates/`

### Stage 3: Markdown → JSONL (`/isaac-data`)
- Parses markdown files into structured records
- Outputs to `data/` as JSONL files:
  - `exam_results.jsonl`
  - `prescriptions.jsonl`
  - `genetic_variants.jsonl`
  - `documents.jsonl`

## Key Files

### `inventory.json` (v2.0 schema)
Master inventory tracking all files and their pipeline status:
```json
{
  "version": "2.0",
  "files": {
    "sha256hash": {
      "original_name": "filename.pdf",
      "destination": "Exams/Blood/20230914_OswaldoCruz_Hemograma.pdf",
      "category": "Blood",
      "pipeline": {
        "organized": {"completed": true, "timestamp": "2025-01-28"},
        "markdown": {"completed": false, "output_path": null},
        "jsonl": {"completed": false, "record_id": null}
      },
      "metadata": {
        "document_date": "2023-09-14",
        "provider": "OswaldoCruz",
        "has_abnormal_values": false
      }
    }
  }
}
```

### `scripts/orchestrator.py`
Main pipeline controller. Usage:
```bash
./scripts/orchestrator.py                    # Run all pending (4 workers)
./scripts/orchestrator.py --stage 2          # Only PDF -> Markdown
./scripts/orchestrator.py --stage 3          # Only Markdown -> JSONL
./scripts/orchestrator.py --workers 8        # Use 8 parallel workers
./scripts/orchestrator.py --force            # Reprocess all
./scripts/orchestrator.py --file HASH        # Process specific file
./scripts/orchestrator.py --dry-run          # Show what would run
./scripts/orchestrator.py --category Blood   # Only process Blood category
```

## Document Categories

| Category | Description |
|----------|-------------|
| Blood | Blood tests (hemograms, hormones, vitamins) |
| Stool_GI | Stool and gastrointestinal tests |
| Urine | Urine analysis |
| Genetic | Genetic variant reports |
| Imaging | EEG, MRI, X-rays |
| Metabolic_GreatPlains | Great Plains organic acids, metabolic panels |
| Specialty | Specialist exams (audiology, ophthalmology) |
| Assessments | ATEC scores, developmental assessments |
| Requests | Exam request forms |
| Medications | Prescriptions, supplements, CBD protocols |
| Nutrition | Diet plans, food guidance |
| Consultations | Doctor visit notes |
| Tracking | Growth charts, progress tracking |
| Newborn | Birth and early infancy documents |

## Filename Convention

```
YYYYMMDD_Provider_Description[_ALTERADO].ext
```
- `YYYYMMDD`: Document date
- `Provider`: Lab or doctor name (OswaldoCruz, DraSimone, GreatPlains)
- `Description`: Brief type (Hemograma, Prescricao, PlanoAlimentar)
- `_ALTERADO`: Suffix indicating abnormal results

## Skills

Skills are defined in `.claude/skills/`:

- **isaac-file-organizer**: `/isaac-organize` - Stage 1 file organization
- **isaac-markdown-generator**: `/isaac-markdown` - Stage 2 markdown generation

## Development

### Running the Pipeline
```bash
# Full pipeline
./scripts/orchestrator.py

# Single stage
./scripts/orchestrator.py --stage 2

# Dry run to preview
./scripts/orchestrator.py --dry-run
```

### Adding New Document Types
1. Add category to `references/categories.md`
2. Create template in `references/templates/`
3. Update category mapping in SKILL.md
4. Update orchestrator prompts if needed

## Notes

- All documents are in Portuguese (Brazil)
- Clinical context is autism-related treatments and monitoring
- Files are deduplicated by SHA256 hash
- Pipeline uses parallel sub-agents for efficiency (configurable workers)
- Output validation uses JSON schemas in `scripts/schemas/`
