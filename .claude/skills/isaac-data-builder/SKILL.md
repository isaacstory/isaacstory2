---
name: isaac-data-builder
command: /isaac-data
description: Generate JSONL database files from Isaac's clinical documents. This is Stage 3 of the Isaac Clinical Document Pipeline. Creates granular JSONL records from markdown files - one row per test result or medication, not per document.
---

# Isaac Data Builder (Stage 3 of Pipeline)

Convert markdown files to structured JSONL database files for querying.

## Pipeline Context

This is **Stage 3** of the Isaac Clinical Document Pipeline:
```
dropbasket/ → [Organize] → categorized folders → [Markdown] → markdown/ → [JSONL] → data/
```

**Prerequisites**: Run `/isaac-markdown` (Stage 2) first to generate markdown files.

## Key Insight: Granular Records

**One row per test result, not per document.** A blood panel with 50 tests generates 50 JSONL rows. This enables:
- Searching for specific tests (e.g., "TSH" → all TSH results across time)
- Filtering by status (all abnormal results)
- Tracking values over time
- Flexible querying by any field

## Output Files

All files go to `isaacstory2/data/`:

| File | Content | Row Type |
|------|---------|----------|
| `exam_results.jsonl` | Lab test results | One per test value |
| `prescriptions.jsonl` | Medications | One per medication |
| `documents.jsonl` | Source documents | One per document |
| `catalog.json` | Summary statistics | Single JSON file |

## Workflow Overview

1. **Scan inventory** for files with `pipeline.jsonl.completed = false`
2. **Batch files** for parallel processing (5-10 per batch)
3. **Spawn sub-agents** to extract records from each file:
   - Parse markdown/PDF content
   - Generate granular JSONL records
   - Return array of record objects
4. **Append records** to appropriate JSONL files
5. **Update inventory** with `pipeline.jsonl.completed = true`
6. **Rebuild catalog.json** with summary statistics
7. **Report results** to user

## JSONL Schemas

### exam_results.jsonl - One row per test result

```json
{
  "id": "result_20230914_tsh_001",
  "document_hash": "abc123...",
  "document_date": "2023-09-14",
  "category": "Blood",
  "test_name": "TSH",
  "test_name_normalized": "tsh",
  "value": 3.8,
  "value_text": "3.8",
  "unit": "mUI/L",
  "reference_min": 0.7,
  "reference_max": 6.0,
  "reference_text": "0.70 a 6.0",
  "status": "normal",
  "lab": "OswaldoCruz",
  "physician": "Dr. Rogerio",
  "source_file": "Exams/Blood/20230914_OswaldoCruz_Sangue.pdf",
  "markdown_file": "markdown/Exams/Blood/20230914_OswaldoCruz_Sangue.md",
  "page": 2
}
```

### prescriptions.jsonl - One row per medication

```json
{
  "id": "rx_20240529_lteanina_001",
  "document_hash": "def456...",
  "document_date": "2024-05-29",
  "medication_name": "L-Teanina + GABA + Memantina",
  "medication_normalized": "lteanina_gaba_memantina",
  "components": ["L-Teanina 500mg", "GABA 500mg", "Memantina 5mg"],
  "form": "Solucao Oral",
  "dosage": "30 doses",
  "frequency": "3x ao dia",
  "instructions": "se sedar reduzir a dose",
  "prescriber": "Dr. Rogerio",
  "specialty": "Neurologia",
  "active": true,
  "source_file": "Prescriptions/Medications/20240529_DrRogerio_Suplementos.pdf",
  "markdown_file": "markdown/Prescriptions/Medications/20240529_DrRogerio_Suplementos.md"
}
```

### documents.jsonl - One row per source document

```json
{
  "id": "doc_abc123",
  "hash": "abc123...",
  "category": "Blood",
  "subcategory": "Hemograma",
  "document_date": "2023-09-14",
  "provider": "OswaldoCruz",
  "physician": "Dr. Rogerio",
  "source_file": "Exams/Blood/20230914_OswaldoCruz_Sangue.pdf",
  "markdown_file": "markdown/Exams/Blood/20230914_OswaldoCruz_Sangue.md",
  "result_count": 47,
  "abnormal_count": 3,
  "file_type": "pdf",
  "language": "pt",
  "processed_date": "2026-01-28"
}
```

### catalog.json - Summary statistics

```json
{
  "generated": "2026-01-28T12:00:00Z",
  "stats": {
    "total_documents": 136,
    "total_exam_results": 2450,
    "total_prescriptions": 180,
    "documents_by_category": {
      "Blood": 18,
      "Medications": 33,
      "Metabolic_GreatPlains": 13
    },
    "date_range": {
      "earliest": "2018-11-01",
      "latest": "2025-06-09"
    }
  },
  "categories": [
    {"name": "Blood", "count": 18, "result_count": 850},
    {"name": "Medications", "count": 33, "prescription_count": 180}
  ]
}
```

## Sub-Agent Processing

For each file, spawn a sub-agent with this prompt template:

```
You are extracting structured data from a clinical document for database storage.

File: {filepath}
Category: {category}
Document Hash: {hash}

TASK:
1. Read the document (markdown preferred, PDF as fallback)
2. Extract GRANULAR records - one per test result or medication
3. Return array of JSONL-ready objects

IMPORTANT:
- Each test result = separate record
- Each medication = separate record
- Normalize test names to lowercase_underscore format
- Parse numeric values and reference ranges
- Flag abnormal values with status: "high", "low", or "abnormal"
- Include all metadata (dates, providers, units)

Output format: Return a JSON object:
{
  "records": [
    {...}, {...}, ...
  ],
  "document_summary": {
    "record_count": N,
    "abnormal_count": N,
    "subcategory": "..."
  }
}
```

## Category Processing Rules

### Blood/Stool_GI/Urine/Metabolic_GreatPlains
- Extract each test result as separate record
- Include reference ranges and status
- Normalize test names

### Medications
- Extract each medication as separate record
- Parse dosage, frequency, form
- Mark as active/inactive based on document date

### Genetic
- Extract each variant as separate record
- Include classification and gene information

### Imaging/Consultations/Assessments
- Generate document summary record
- Extract key findings as structured data

## Updating Inventory

After successful JSONL generation:

```python
inventory["files"][hash]["pipeline"]["jsonl"] = {
    "completed": True,
    "record_id": "doc_abc123"
}
```

## Rebuilding catalog.json

After each batch, recalculate:
1. Count total records in each JSONL file
2. Count documents by category
3. Find date range
4. Update catalog.json with fresh statistics

## Error Handling

- If extraction fails: Keep `jsonl.completed = false`, retry next run
- Duplicate records: Use document_hash to detect and skip
- Missing markdown: Fall back to reading original PDF

## Running the Skill

When invoked:
1. Load inventory and filter for `jsonl.completed = false`
2. Ensure markdown files exist (suggest running Stage 2 if missing)
3. Process in batches using parallel sub-agents
4. Show progress: "Extracting records from batch 1/14..."
5. Rebuild catalog.json
6. Report summary: "Added 450 exam results, 25 medications"

## ID Generation

Format: `{type}_{date}_{name}_{sequence}`

Examples:
- `result_20230914_tsh_001`
- `rx_20240529_cbd_001`
- `doc_abc123def4`

## Validation

Before writing records, validate:
- Required fields present
- Date format valid (YYYY-MM-DD)
- Numeric values parseable
- Reference ranges logical (min < max)
