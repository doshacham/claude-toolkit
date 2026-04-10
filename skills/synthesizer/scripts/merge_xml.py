# Copyright (c) 2026 Dor Shacham <dorishacham52@gmail.com>. All rights reserved.
# SPDX-License-Identifier: Proprietary

"""Merge multiple XML agent dumps into a unified structure.

Usage:
    python merge_xml.py <dumps_dir> -o <output_file>

Parses all XML dumps, deduplicates entities, resolves cross-references,
and produces a single merged XML file.

Analog to InfoSeek's Refiner Agent that condenses multiple search results.
"""

import json
import os
import re
import sys
from collections import defaultdict
from xml.etree import ElementTree as ET


def parse_dump(filepath: str) -> dict:
    """Parse an XML dump file and extract structured data."""
    result = {
        "source": os.path.basename(filepath),
        "area": "",
        "entities": [],
        "patterns": [],
        "data_flows": [],
        "borrowable_ideas": [],
        "raw_sections": {},
    }

    try:
        tree = ET.parse(filepath)
        root = tree.getroot()
        result["area"] = root.get("area", "")
    except (ET.ParseError, OSError) as e:
        # Fall back to text extraction
        result["parse_error"] = str(e)
        result["entities"] = _extract_entities_from_text(filepath)
        return result

    # Walk the tree and extract entities
    for elem in root.iter():
        name = elem.get("name", "")
        if not name:
            continue

        entity = {
            "name": name,
            "type": elem.tag,
            "attributes": dict(elem.attrib),
            "text": (elem.text or "").strip()[:500],
            "source": result["source"],
        }

        if elem.tag in {"pattern", "design-pattern"}:
            result["patterns"].append(entity)
        elif elem.tag in {"flow", "data-flow"}:
            result["data_flows"].append(entity)
        elif elem.tag in {"idea", "borrowable-idea"}:
            result["borrowable_ideas"].append(entity)
        else:
            result["entities"].append(entity)

    # Extract raw section content
    for child in root:
        tag = child.tag
        content = ET.tostring(child, encoding="unicode", method="xml")
        result["raw_sections"][tag] = content

    return result


def _extract_entities_from_text(filepath: str) -> list[dict]:
    """Fallback entity extraction from raw text."""
    entities = []
    try:
        with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()
    except OSError:
        return entities

    for m in re.finditer(r'name="([^"]+)"', content):
        entities.append({
            "name": m.group(1),
            "type": "entity",
            "source": os.path.basename(filepath),
        })

    return entities


def merge_dumps(dumps: list[dict]) -> dict:
    """Merge multiple parsed dumps into a unified structure."""
    # Deduplicate entities by name
    entity_map = defaultdict(list)
    for dump in dumps:
        for entity in dump.get("entities", []):
            entity_map[entity["name"]].append(entity)

    # Pick the richest description for each entity
    merged_entities = []
    for name, occurrences in entity_map.items():
        # Prefer the one with the longest text
        best = max(occurrences, key=lambda e: len(e.get("text", "")))
        best["mentioned_in"] = list(set(e.get("source", "") for e in occurrences))
        best["mention_count"] = len(occurrences)
        merged_entities.append(best)

    # Collect all patterns
    all_patterns = []
    pattern_names = set()
    for dump in dumps:
        for p in dump.get("patterns", []):
            if p["name"] not in pattern_names:
                pattern_names.add(p["name"])
                all_patterns.append(p)

    # Collect all data flows
    all_flows = []
    for dump in dumps:
        all_flows.extend(dump.get("data_flows", []))

    # Collect borrowable ideas
    all_ideas = []
    idea_names = set()
    for dump in dumps:
        for idea in dump.get("borrowable_ideas", []):
            if idea["name"] not in idea_names:
                idea_names.add(idea["name"])
                all_ideas.append(idea)

    # Build cross-references
    cross_refs = []
    for name, occurrences in entity_map.items():
        if len(occurrences) > 1:
            sources = list(set(e.get("source", "") for e in occurrences))
            cross_refs.append({
                "entity": name,
                "referenced_in": sources,
                "count": len(occurrences),
            })

    return {
        "sources": [d.get("source", "") for d in dumps],
        "areas": [d.get("area", "") for d in dumps],
        "total_entities": len(merged_entities),
        "total_patterns": len(all_patterns),
        "total_flows": len(all_flows),
        "total_ideas": len(all_ideas),
        "total_cross_references": len(cross_refs),
        "entities": merged_entities,
        "patterns": all_patterns,
        "data_flows": all_flows,
        "borrowable_ideas": all_ideas,
        "cross_references": cross_refs,
        "raw_sections": {d.get("source", ""): d.get("raw_sections", {}) for d in dumps},
    }


def write_merged_xml(merged: dict, output_path: str):
    """Write merged data as XML."""
    root = ET.Element("merged-analysis")
    root.set("sources", str(len(merged["sources"])))
    root.set("entities", str(merged["total_entities"]))

    # Metadata
    meta = ET.SubElement(root, "metadata")
    for src in merged["sources"]:
        ET.SubElement(meta, "source").text = src
    for area in merged["areas"]:
        ET.SubElement(meta, "area").text = area

    # Entities
    entities_elem = ET.SubElement(root, "entities")
    for entity in merged["entities"]:
        elem = ET.SubElement(entities_elem, entity.get("type", "entity"))
        elem.set("name", entity.get("name", ""))
        elem.set("mention-count", str(entity.get("mention_count", 1)))
        if entity.get("text"):
            elem.text = entity["text"]
        if entity.get("mentioned_in"):
            elem.set("mentioned-in", ",".join(entity["mentioned_in"]))

    # Patterns
    patterns_elem = ET.SubElement(root, "design-patterns")
    for pattern in merged["patterns"]:
        elem = ET.SubElement(patterns_elem, "pattern")
        elem.set("name", pattern.get("name", ""))
        elem.set("source", pattern.get("source", ""))
        if pattern.get("text"):
            elem.text = pattern["text"]

    # Data flows
    flows_elem = ET.SubElement(root, "data-flows")
    for flow in merged["data_flows"]:
        elem = ET.SubElement(flows_elem, "flow")
        elem.set("name", flow.get("name", ""))
        if flow.get("text"):
            elem.text = flow["text"]

    # Cross-references
    xrefs_elem = ET.SubElement(root, "cross-references")
    for xref in merged["cross_references"]:
        elem = ET.SubElement(xrefs_elem, "reference")
        elem.set("entity", xref["entity"])
        elem.set("count", str(xref["count"]))
        elem.set("sources", ",".join(xref["referenced_in"]))

    # Borrowable ideas
    ideas_elem = ET.SubElement(root, "borrowable-ideas")
    for idea in merged["borrowable_ideas"]:
        elem = ET.SubElement(ideas_elem, "idea")
        elem.set("name", idea.get("name", ""))
        if idea.get("text"):
            elem.text = idea["text"]

    # Write with indentation
    ET.indent(root, space="  ")
    tree = ET.ElementTree(root)
    tree.write(output_path, encoding="unicode", xml_declaration=True)


def main():
    if len(sys.argv) < 4 or sys.argv[2] != "-o":
        print("Usage: python merge_xml.py <dumps_dir> -o <output_file>", file=sys.stderr)
        sys.exit(1)

    dumps_dir = sys.argv[1]
    output_file = sys.argv[3]

    # Parse all XML dumps
    dumps = []
    for fname in sorted(os.listdir(dumps_dir)):
        if fname.endswith(".xml"):
            fpath = os.path.join(dumps_dir, fname)
            dump = parse_dump(fpath)
            dumps.append(dump)
            print(f"  Parsed {fname}: {len(dump['entities'])} entities", file=sys.stderr)

    if not dumps:
        print("Error: no XML dumps found in " + dumps_dir, file=sys.stderr)
        sys.exit(1)

    # Merge
    merged = merge_dumps(dumps)
    print(f"\n  Merged: {merged['total_entities']} entities, "
          f"{merged['total_cross_references']} cross-references", file=sys.stderr)

    # Write
    write_merged_xml(merged, output_file)
    print(f"  Output: {output_file}", file=sys.stderr)

    # Also write JSON version for entity index building
    json_output = output_file.replace(".xml", ".json")
    with open(json_output, "w") as f:
        json.dump(merged, f, indent=2)


if __name__ == "__main__":
    main()
