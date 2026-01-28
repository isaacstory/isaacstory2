#!/usr/bin/env python3
"""
Scan dropbasket folder and compute file hashes.
Outputs JSON with file info for processing.

Usage:
    python3 scan_dropbasket.py /path/to/dropbasket /path/to/inventory.json
"""

import sys
import os
import json
import hashlib
from pathlib import Path

def compute_hash(filepath):
    """Compute SHA256 hash of file."""
    sha256 = hashlib.sha256()
    with open(filepath, 'rb') as f:
        for chunk in iter(lambda: f.read(8192), b''):
            sha256.update(chunk)
    return sha256.hexdigest()

def scan_folder(folder_path):
    """Recursively scan folder for files."""
    files = []
    for root, dirs, filenames in os.walk(folder_path):
        # Skip hidden folders
        dirs[:] = [d for d in dirs if not d.startswith('.')]
        for filename in filenames:
            if filename.startswith('.'):
                continue
            filepath = os.path.join(root, filename)
            files.append({
                'path': filepath,
                'name': filename,
                'relative_path': os.path.relpath(filepath, folder_path)
            })
    return files

def load_inventory(inventory_path):
    """Load existing inventory or create empty one."""
    if os.path.exists(inventory_path):
        with open(inventory_path, 'r') as f:
            return json.load(f)
    return {"files": {}}

def main():
    if len(sys.argv) < 3:
        print("Usage: python3 scan_dropbasket.py /path/to/dropbasket /path/to/inventory.json")
        sys.exit(1)

    dropbasket_path = sys.argv[1]
    inventory_path = sys.argv[2]

    # Load inventory
    inventory = load_inventory(inventory_path)
    known_hashes = set(inventory.get("files", {}).keys())

    # Scan files
    files = scan_folder(dropbasket_path)

    results = {
        "new_files": [],
        "duplicates": [],
        "total_scanned": len(files)
    }

    for file_info in files:
        file_hash = compute_hash(file_info['path'])
        file_info['hash'] = file_hash

        if file_hash in known_hashes:
            existing = inventory["files"][file_hash]
            file_info['duplicate_of'] = existing.get('destination', existing.get('original_name'))
            results['duplicates'].append(file_info)
        else:
            results['new_files'].append(file_info)

    print(json.dumps(results, indent=2))

if __name__ == "__main__":
    main()
