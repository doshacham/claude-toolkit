# Copyright (c) 2026 Dor Shacham <dorishacham52@gmail.com>. All rights reserved.
# SPDX-License-Identifier: Proprietary

"""Build a flat entity index from merged XML/JSON for validation.

Usage:
    python build_entity_index.py <merged.xml|merged.json> -o <entity_index.json>

Extracts all documented entity names categorized by type for use by
the completeness validator.
"""

import json
import os
import re
import sys
from xml.etree import ElementTree as ET


def build_from_json(filepath: str) -> dict:
    """Build entity index from merged JSON."""
    with open(filepath, "r") as f:
        merged = json.load(f)

    index = {
        "types": [],
        "functions": [],
        "interfaces": [],
        "constants": [],
        "commands": [],
        "patterns": [],
        "files_documented": [],
    }

    type_mapping = {
        "type": "types",
        "struct": "types",
        "class": "types",
        "entity": "types",
        "interface": "interfaces",
        "trait": "interfaces",
        "function": "functions",
        "method": "functions",
        "func": "functions",
        "constant": "constants",
        "const": "constants",
        "const-group": "constants",
        "command": "commands",
        "pattern": "patterns",
    }

    for entity in merged.get("entities", []):
        name = entity.get("name", "")
        etype = entity.get("type", "entity")
        category = type_mapping.get(etype, "types")
        if name and name not in index[category]:
            index[category].append(name)

    for pattern in merged.get("patterns", []):
        name = pattern.get("name", "")
        if name and name not in index["patterns"]:
            index["patterns"].append(name)

    # Extract file paths from entity attributes
    for entity in merged.get("entities", []):
        attrs = entity.get("attributes", {})
        for key in ["file", "path"]:
            if key in attrs:
                path = attrs[key]
                if path and path not in index["files_documented"]:
                    index["files_documented"].append(path)

    # Sort everything
    for key in index:
        index[key] = sorted(set(index[key]))

    # Add summary stats
    total = sum(len(v) for k, v in index.items() if k != "files_documented")
    index["total_symbols"] = total
    index["files_count"] = len(index["files_documented"])

    return index


def build_from_xml(filepath: str) -> dict:
    """Build entity index from merged XML."""
    index = {
        "types": [],
        "functions": [],
        "interfaces": [],
        "constants": [],
        "commands": [],
        "patterns": [],
        "files_documented": [],
    }

    try:
        tree = ET.parse(filepath)
        root = tree.getroot()
    except (ET.ParseError, OSError):
        return index

    type_mapping = {
        "type": "types",
        "struct": "types",
        "class": "types",
        "entity": "types",
        "interface": "interfaces",
        "function": "functions",
        "method": "functions",
        "constant": "constants",
        "command": "commands",
        "pattern": "patterns",
    }

    for elem in root.iter():
        name = elem.get("name", "")
        if not name:
            continue
        category = type_mapping.get(elem.tag, None)
        if category and name not in index[category]:
            index[category].append(name)

        # Track file paths
        for attr in ["file", "path"]:
            if attr in elem.attrib:
                path = elem.get(attr)
                if path and path not in index["files_documented"]:
                    index["files_documented"].append(path)

    for key in index:
        index[key] = sorted(set(index[key]))

    total = sum(len(v) for k, v in index.items() if k != "files_documented")
    index["total_symbols"] = total
    index["files_count"] = len(index["files_documented"])

    return index


def main():
    if len(sys.argv) < 4 or sys.argv[2] != "-o":
        print("Usage: python build_entity_index.py <merged_file> -o <output>",
              file=sys.stderr)
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[3]

    if input_file.endswith(".json"):
        index = build_from_json(input_file)
    elif input_file.endswith(".xml"):
        index = build_from_xml(input_file)
    else:
        print(f"Error: unsupported format {input_file}", file=sys.stderr)
        sys.exit(1)

    os.makedirs(os.path.dirname(output_file) or ".", exist_ok=True)
    with open(output_file, "w") as f:
        json.dump(index, f, indent=2)

    print(f"Entity index: {index['total_symbols']} symbols, "
          f"{index['files_count']} files", file=sys.stderr)


if __name__ == "__main__":
    main()
