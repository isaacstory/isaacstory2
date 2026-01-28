---
name: isaac-file-organizer
command: /isaac-organize
description: Organize Isaac's clinical files from the dropbasket folder into a structured hierarchy. Use this skill when the user asks to "organize files", "sort the dropbasket", "file the clinical documents", or similar requests about organizing Isaac's medical/clinical documentation. The skill uses parallel sub-agents to categorize files, tracks file hashes to detect duplicates, and maintains an inventory of processed files. This is Stage 1 of the 3-stage Isaac Clinical Document Pipeline.
---

# Isaac File Organizer (Stage 1 of Pipeline)

Organize clinical files from `dropbasket/` into structured folders by type.

## Pipeline Context

This is **Stage 1** of the Isaac Clinical Document Pipeline:
```
dropbasket/ → [Organize] → categorized folders → [Markdown] → markdown/ → [JSONL] → data/
```

After files are organized, run `/isaac-markdown` (Stage 2) to generate structured markdown files.

## Workflow Overview

1. **Scan** dropbasket for files
2. **Check duplicates** against inventory (by hash)
3. **Categorize** new files using parallel sub-agents
4. **Move** files to appropriate folders
5. **Update** inventory with new entries (v2.0 schema with pipeline tracking)
6. **Report** results to user

## Paths

- **Dropbasket**: `isaacstory2/dropbasket/`
- **Inventory**: `isaacstory2/inventory.json`
- **Duplicates folder**: `isaacstory2/_duplicates/`

## Step 1: Scan and Hash

Scan all files in `dropbasket/` (including `Exams/` and `Prescriptions/` subfolders).

For each file, compute SHA256 hash:
```bash
shasum -a 256 "/path/to/file" | cut -d' ' -f1
```

## Step 2: Check Inventory for Duplicates

Load `inventory.json` (v2.0 schema with pipeline tracking).

Structure:
```json
{
  "version": "2.0",
  "files": {
    "abc123hash": {
      "original_name": "20230914 - Exame Sangue.pdf",
      "destination": "Exams/Blood/20230914_OswaldoCruz_Hemograma.pdf",
      "category": "Blood",
      "pipeline": {
        "organized": {"completed": true, "timestamp": "2025-01-28"},
        "markdown": {"completed": false, "output_path": null, "template_version": null},
        "jsonl": {"completed": false, "record_id": null}
      },
      "metadata": {
        "document_date": "2023-09-14",
        "provider": "OswaldoCruz",
        "has_abnormal_values": false
      }
    }
  },
  "template_versions": {"blood_exam": "1.0", "prescription": "1.0", ...}
}
```

If hash exists in inventory → move file to `_duplicates/` folder with note.

## Step 3: Categorize Using Sub-agents

For each NEW file (not in inventory), spawn a sub-agent to determine:
1. **Category** (see references/categories.md)
2. **Standardized filename** (format: `YYYYMMDD_Provider_Description.ext`)

**Sub-agent prompt template:**
```
Categorize this clinical file for Isaac (autistic child).

File: {filename}
Path: {filepath}

Read the file if needed to determine content. Then respond with JSON:
{
  "category": "one of: Blood, Stool_GI, Urine, Genetic, Imaging, Metabolic_GreatPlains, Specialty, Assessments, Requests, Medications, Nutrition, Consultations, Tracking, Newborn",
  "standardized_name": "YYYYMMDD_Provider_Description.ext",
  "confidence": "high/medium/low",
  "notes": "any relevant notes"
}

Category definitions are in references/categories.md.
Filename format: YYYYMMDD_Provider_Description.ext
- Extract date from filename or document content
- Provider = doctor name or lab (DraSimone, OswaldoCruz, GreatPlains, etc.)
- Description = brief type (Hemograma, Prescricao, PlanoAlimentar, etc.)
- Preserve _ALTERADO suffix if present (indicates abnormal results)
```

**Spawn sub-agents in parallel** (batch of 5-10 at a time) for efficiency.

## Step 4: Move Files

Based on categorization results, move files to target structure.

Target folder structure (see references/folder-structure.md):
```
isaacstory2/
├── Exams/
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
└── _duplicates/
```

Move command:
```bash
mkdir -p "target/folder" && mv "source" "target/folder/newname"
```

## Step 5: Update Inventory

After successful move, add entry to `inventory.json` with v2.0 schema:
```python
from datetime import datetime

# Extract document date from filename (YYYYMMDD format)
doc_date = None
filename = os.path.basename(destination)
if filename[:8].isdigit():
    doc_date = f"{filename[:4]}-{filename[4:6]}-{filename[6:8]}"

# Extract provider from filename
provider = None
parts = filename.split('_')
if len(parts) >= 2:
    provider = parts[1]

inventory["files"][hash] = {
    "original_name": original_filename,
    "destination": relative_path_from_isaacstory2,
    "category": category,
    "pipeline": {
        "organized": {
            "completed": True,
            "timestamp": datetime.now().strftime("%Y-%m-%d")
        },
        "markdown": {
            "completed": False,
            "output_path": None,
            "template_version": None
        },
        "jsonl": {
            "completed": False,
            "record_id": None
        }
    },
    "metadata": {
        "document_date": doc_date,
        "provider": provider,
        "has_abnormal_values": "_ALTERADO" in destination
    }
}
```

Save updated inventory.

## Step 6: Report Results

Summarize for user:
- Files processed: X
- Files moved: Y (list with old → new paths)
- Duplicates found: Z (list)
- Errors: any issues encountered

## Handling Edge Cases

**Low confidence categorization**: Ask user to confirm before moving.

**Unreadable files**: Note in report, leave in dropbasket.

**Existing file at destination**: Append `_2`, `_3` etc. to filename.

## Running the Skill

When user invokes this skill:
1. Confirm the dropbasket path with user
2. Run the workflow
3. Present results and ask if any corrections needed
