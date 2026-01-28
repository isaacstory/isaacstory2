---
name: isaac-markdown-generator
command: /isaac-markdown
description: Generate structured markdown files from Isaac's clinical documents. This is Stage 2 of the Isaac Clinical Document Pipeline. Reads PDFs from categorized folders and generates markdown files with extracted data using category-specific templates.
---

# Isaac Markdown Generator (Stage 2 of Pipeline)

Convert categorized clinical documents to structured markdown files.

## Pipeline Context

This is **Stage 2** of the Isaac Clinical Document Pipeline:
```
dropbasket/ → [Organize] → categorized folders → [Markdown] → markdown/ → [JSONL] → data/
```

**Prerequisites**: Run `/isaac-organize` (Stage 1) first to categorize files.
**Next Stage**: Run `/isaac-data` (Stage 3) to generate JSONL database files.

## Workflow Overview

1. **Scan inventory** for files with `pipeline.markdown.completed = false`
2. **Batch files** into groups of 5-10 for parallel processing
3. **Spawn sub-agents** to process each file:
   - Read PDF/document content
   - Extract structured data based on category
   - Apply category-specific template
   - Return markdown content
4. **Write markdown files** to `markdown/{category_path}/`
5. **Update inventory** with `pipeline.markdown.completed = true`
6. **Report results** to user

## Paths

- **Source**: Files from `Exams/`, `Prescriptions/`, `Consultations/`, etc.
- **Output**: `isaacstory2/markdown/{mirrors source tree}`
- **Inventory**: `isaacstory2/inventory.json`
- **Templates**: `.claude/skills/isaac-markdown-generator/references/templates/`

## Category to Template Mapping

| Category | Template | Description |
|----------|----------|-------------|
| Blood | blood_exam.md | Blood tests with values table, reference ranges |
| Stool_GI | stool_exam.md | Stool/GI tests |
| Urine | urine_exam.md | Urine analysis |
| Genetic | genetic_report.md | Genetic variants, classifications |
| Imaging | imaging_report.md | EEG, MRI, X-ray findings |
| Metabolic_GreatPlains | metabolic_panel.md | Great Plains markers |
| Specialty | specialty_exam.md | Specialist exams |
| Assessments | assessment.md | ATEC, developmental assessments |
| Requests | exam_request.md | Exam requests/solicitations |
| Medications | prescription.md | Medications, supplements, CBD |
| Nutrition | nutrition_plan.md | Diet plans, food guidance |
| Consultations | consultation.md | Doctor visit notes |
| Tracking | tracking.md | Growth charts, tracking data |
| Newborn | newborn.md | Birth/early documents |

## Sub-Agent Processing

For each file, spawn a sub-agent with this prompt template:

```
You are processing a clinical document for Isaac's medical records.

File: {filepath}
Category: {category}
Template: {template_name}

TASK:
1. Read the document content
2. Extract structured data according to the template format
3. Return the completed markdown content

TEMPLATE STRUCTURE:
{template_content}

IMPORTANT:
- Extract ALL data visible in the document
- Preserve exact values, units, and reference ranges
- Note any abnormal values with ⚠️ flag
- Include document metadata (date, provider, lab)
- Return ONLY the completed markdown, no explanation

Output format: Return a JSON object:
{
  "markdown": "the completed markdown content",
  "extracted_data": {
    "document_date": "YYYY-MM-DD",
    "provider": "name",
    "test_count": N,
    "abnormal_count": N
  }
}
```

## Batch Processing Strategy

```
Files pending: N
Batch size: 5 files (to manage context)
Process: spawn 5 sub-agents in parallel → collect results → write files → next batch
```

## Updating Inventory

After successful markdown generation:

```python
inventory["files"][hash]["pipeline"]["markdown"] = {
    "completed": True,
    "output_path": "markdown/Exams/Blood/20230914_OswaldoCruz_Sangue.md",
    "template_version": "1.0"
}
```

## Error Handling

- If PDF is unreadable: Log error, skip file, continue with batch
- If extraction fails: Keep `markdown.completed = false`, retry on next run
- Low confidence extraction: Add `<!-- LOW_CONFIDENCE -->` comment in markdown

## Running the Skill

When invoked:
1. Load inventory and filter for `markdown.completed = false`
2. Group files by category for efficient template reuse
3. Process in batches using parallel sub-agents
4. Show progress: "Processing batch 1/14 (10 files)..."
5. Report summary at end

## Supported File Types

- **PDF**: Primary format, read with PDF reader
- **JPEG/PNG**: Read as image, use vision for extraction
- **DOCX**: Read with document parser
- **XLSX**: Read spreadsheet data

## Output Example

For a blood test file, markdown output looks like:

```markdown
# Blood Test Results

**Date**: 2023-09-14
**Provider**: Oswaldo Cruz Laboratory
**Patient**: Isaac

## Test Results

| Test | Value | Unit | Reference | Status |
|------|-------|------|-----------|--------|
| TSH | 3.8 | mUI/L | 0.7-6.0 | Normal |
| Hemoglobin | 11.2 | g/dL | 11.5-14.5 | ⚠️ Low |
...

## Summary

- Total tests: 47
- Abnormal results: 3
- Notable findings: Hemoglobin slightly below reference range

---
*Generated from: Exams/Blood/20230914_OswaldoCruz_Sangue.pdf*
*Template version: blood_exam 1.0*
```
