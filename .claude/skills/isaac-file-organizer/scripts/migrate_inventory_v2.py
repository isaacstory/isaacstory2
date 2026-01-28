#!/usr/bin/env python3
"""Migrate inventory.json to v2.0 schema with pipeline tracking."""
import json
import os
from datetime import datetime

INVENTORY_PATH = "/Users/tony/isaacstory/isaacstory2/inventory.json"

def migrate_inventory():
    # Load existing inventory
    with open(INVENTORY_PATH, 'r', encoding='utf-8') as f:
        inventory = json.load(f)

    # Check if already migrated
    if inventory.get("version") == "2.0":
        print("Inventory already at version 2.0")
        return

    # Create new structure
    new_inventory = {
        "version": "2.0",
        "files": {},
        "template_versions": {
            "blood_exam": "1.0",
            "prescription": "1.0",
            "metabolic_panel": "1.0",
            "genetic_report": "1.0",
            "nutrition_plan": "1.0",
            "imaging_report": "1.0",
            "consultation": "1.0",
            "stool_exam": "1.0",
            "assessment": "1.0",
            "exam_request": "1.0",
            "specialty_exam": "1.0",
            "urine_exam": "1.0",
            "tracking": "1.0",
            "newborn": "1.0"
        }
    }

    # Migrate each file entry
    for hash_key, file_data in inventory.get("files", {}).items():
        # Parse existing data
        original_name = file_data.get("original_name", "")
        destination = file_data.get("destination", "")
        categorized_date = file_data.get("categorized_date", "")
        category = file_data.get("category", "")

        # Extract document date from filename (YYYYMMDD format)
        doc_date = None
        if destination:
            filename = os.path.basename(destination)
            if filename[:8].isdigit():
                doc_date = f"{filename[:4]}-{filename[4:6]}-{filename[6:8]}"

        # Extract provider from filename
        provider = None
        if destination:
            filename = os.path.basename(destination)
            parts = filename.split('_')
            if len(parts) >= 2:
                provider = parts[1]

        # Create new entry with pipeline tracking
        new_inventory["files"][hash_key] = {
            "original_name": original_name,
            "destination": destination,
            "category": category,
            "pipeline": {
                "organized": {
                    "completed": True,
                    "timestamp": categorized_date
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
                "has_abnormal_values": "_ALTERADO" in destination if destination else False
            }
        }

    # Save migrated inventory
    with open(INVENTORY_PATH, 'w', encoding='utf-8') as f:
        json.dump(new_inventory, f, indent=2, ensure_ascii=False)

    print(f"Migrated {len(new_inventory['files'])} files to inventory v2.0")
    return new_inventory

if __name__ == "__main__":
    migrate_inventory()
