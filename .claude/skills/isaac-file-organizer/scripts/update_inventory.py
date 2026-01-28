#!/usr/bin/env python3
"""
Update inventory with newly categorized files.

Usage:
    python3 update_inventory.py /path/to/inventory.json

Reads JSON from stdin with format:
{
    "entries": [
        {
            "hash": "abc123...",
            "original_name": "old_filename.pdf",
            "destination": "Exams/Blood/new_filename.pdf",
            "category": "Blood"
        }
    ]
}
"""

import sys
import json
from datetime import date

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 update_inventory.py /path/to/inventory.json < entries.json")
        sys.exit(1)

    inventory_path = sys.argv[1]

    # Load existing inventory
    try:
        with open(inventory_path, 'r') as f:
            inventory = json.load(f)
    except FileNotFoundError:
        inventory = {"files": {}}

    # Read new entries from stdin
    entries_data = json.load(sys.stdin)
    entries = entries_data.get("entries", [])

    today = date.today().isoformat()

    # Add new entries
    for entry in entries:
        file_hash = entry.get("hash")
        if file_hash:
            inventory["files"][file_hash] = {
                "original_name": entry.get("original_name"),
                "destination": entry.get("destination"),
                "categorized_date": today,
                "category": entry.get("category")
            }

    # Save updated inventory
    with open(inventory_path, 'w') as f:
        json.dump(inventory, f, indent=2)

    print(f"Added {len(entries)} entries to inventory")

if __name__ == "__main__":
    main()
