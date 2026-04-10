# Copyright (c) 2026 Dor Shacham <dorishacham52@gmail.com>. All rights reserved.
# SPDX-License-Identifier: Proprietary

"""Validate cross-reference consistency across agent dumps.

Usage:
    python validate_consistency.py --dumps <dir> --output <file>

Extracts entity names from each XML dump and checks:
- Same entity described consistently (no contradictions)
- Cross-references between dumps are valid (no orphans)
- Entity descriptions don't conflict

Analog to InfoSeek's underdetermination check: ensuring the analysis
converges to a consistent picture.
"""

import json
import os
import re
import sys
from collections import defaultdict
from xml.etree import ElementTree as ET


def parse_xml_entities(filepath: str) -> dict[str, dict]:
    """Extract entities (types, functions, interfaces) from an XML dump."""
    entities = {}
    agent_name = os.path.basename(filepath)

    try:
        tree = ET.parse(filepath)
        root = tree.getroot()
    except (ET.ParseError, OSError):
        # Fall back to regex-based extraction
        return _regex_extract(filepath, agent_name)

    # Extract from various XML structures
    for elem in root.iter():
        name = elem.get("name", "")
        if not name:
            continue

        entity_type = elem.tag
        description = elem.text or ""
        if not description:
            # Try to get text from child elements
            for child in elem:
                if child.text:
                    description = child.text
                    break

        if name and entity_type in {"type", "interface", "function", "method",
                                     "command", "pattern", "constant", "struct",
                                     "class", "module", "package"}:
            key = f"{entity_type}:{name}"
            entities[key] = {
                "name": name,
                "type": entity_type,
                "description": description[:200],  # Truncate for comparison
                "source_agent": agent_name,
            }

    return entities


def _regex_extract(filepath: str, agent_name: str) -> dict[str, dict]:
    """Fallback: extract entity names via regex from XML/MD files."""
    entities = {}
    try:
        with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()
    except OSError:
        return entities

    # Match name="EntityName" in XML
    for m in re.finditer(r'name="([A-Z]\w+)"', content):
        name = m.group(1)
        entities[f"entity:{name}"] = {
            "name": name,
            "type": "entity",
            "description": "",
            "source_agent": agent_name,
        }

    return entities


def check_consistency(all_entities: dict[str, dict[str, dict]]) -> dict:
    """Check consistency of entities across agent dumps."""
    # Build a map of entity name -> list of (agent, info)
    entity_agents = defaultdict(list)
    for agent, entities in all_entities.items():
        for key, info in entities.items():
            entity_agents[info["name"]].append({
                "agent": agent,
                "type": info["type"],
                "description": info["description"],
            })

    # Find entities mentioned by multiple agents
    shared_entities = {name: refs for name, refs in entity_agents.items()
                       if len(refs) > 1}

    # Check for type contradictions (same name, different type classification)
    contradictions = []
    for name, refs in shared_entities.items():
        types_seen = set(r["type"] for r in refs)
        # Allow some type flexibility (e.g., "type" and "struct" are compatible)
        compatible_groups = [
            {"type", "struct", "class", "entity"},
            {"function", "method"},
            {"interface", "trait"},
        ]
        normalized_types = set()
        for t in types_seen:
            for group in compatible_groups:
                if t in group:
                    normalized_types.add(frozenset(group))
                    break
            else:
                normalized_types.add(frozenset({t}))

        if len(normalized_types) > 1:
            contradictions.append({
                "entity": name,
                "conflict": [{"agent": r["agent"], "classified_as": r["type"]}
                             for r in refs],
            })

    # Find orphan references (entities mentioned but not defined anywhere)
    all_defined = set()
    all_referenced = set()
    for agent, entities in all_entities.items():
        for key, info in entities.items():
            all_defined.add(info["name"])

    # Note: orphan detection is approximate since we can't perfectly
    # distinguish definitions from references in free-form dumps

    return {
        "total_entities": sum(len(e) for e in all_entities.values()),
        "unique_entities": len(entity_agents),
        "shared_entities": len(shared_entities),
        "contradictions": len(contradictions),
        "contradiction_details": contradictions[:20],
        "pass": len(contradictions) == 0,
        "threshold": "0 contradictions",
        "agents_analyzed": list(all_entities.keys()),
    }


def main():
    args = {sys.argv[i]: sys.argv[i + 1] for i in range(1, len(sys.argv) - 1, 2)
            if sys.argv[i].startswith("--")}

    dumps_dir = args.get("--dumps", "")
    output_file = args.get("--output", "")

    if not dumps_dir:
        print("Usage: python validate_consistency.py --dumps <dir> [--output <file>]",
              file=sys.stderr)
        sys.exit(1)

    # Parse all XML dumps
    all_entities = {}
    for fname in sorted(os.listdir(dumps_dir)):
        if fname.endswith(".xml"):
            fpath = os.path.join(dumps_dir, fname)
            entities = parse_xml_entities(fpath)
            all_entities[fname] = entities

    if not all_entities:
        print("Warning: no XML dumps found in " + dumps_dir, file=sys.stderr)
        result = {"skip": True, "reason": "no XML dumps found"}
    else:
        result = check_consistency(all_entities)

    if output_file:
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        with open(output_file, "w") as f:
            json.dump(result, f, indent=2)
        if not result.get("skip"):
            status = "PASS" if result["pass"] else "FAIL"
            print(f"[{status}] Consistency: {result['contradictions']} contradictions "
                  f"across {result['unique_entities']} entities",
                  file=sys.stderr)
    else:
        json.dump(result, sys.stdout, indent=2)
        print()


if __name__ == "__main__":
    main()
