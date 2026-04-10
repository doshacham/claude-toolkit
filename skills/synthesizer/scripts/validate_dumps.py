# Copyright (c) 2026 Dor Shacham <dorishacham52@gmail.com>. All rights reserved.
# SPDX-License-Identifier: Proprietary

"""Validate that raw agent dumps exist and meet minimum quality thresholds.

Usage:
    python validate_dumps.py <dumps_dir>

Checks:
- Expected XML and MD files exist
- XML files are well-formed
- Files meet minimum size thresholds (not empty/trivial)
- Paired XML/MD files have matching names
"""

import os
import sys
from xml.etree import ElementTree as ET


MIN_XML_BYTES = 5000    # 5KB minimum — trivial dumps are useless
MIN_MD_BYTES = 3000     # 3KB minimum


def validate(dumps_dir: str) -> dict:
    """Validate dump files in the given directory."""
    issues = []
    xml_files = []
    md_files = []

    if not os.path.isdir(dumps_dir):
        return {"valid": False, "issues": [f"Directory not found: {dumps_dir}"]}

    for fname in sorted(os.listdir(dumps_dir)):
        fpath = os.path.join(dumps_dir, fname)
        if not os.path.isfile(fpath):
            continue

        size = os.path.getsize(fpath)

        if fname.endswith(".xml"):
            xml_files.append(fname)
            if size < MIN_XML_BYTES:
                issues.append(f"{fname}: too small ({size} bytes, min {MIN_XML_BYTES})")
            else:
                # Check well-formedness
                try:
                    ET.parse(fpath)
                except ET.ParseError as e:
                    issues.append(f"{fname}: malformed XML ({e})")

        elif fname.endswith(".md"):
            md_files.append(fname)
            if size < MIN_MD_BYTES:
                issues.append(f"{fname}: too small ({size} bytes, min {MIN_MD_BYTES})")

    # Check for paired files
    xml_bases = {f.rsplit(".", 1)[0] for f in xml_files}
    md_bases = {f.rsplit(".", 1)[0] for f in md_files}

    xml_only = xml_bases - md_bases
    md_only = md_bases - xml_bases

    for base in xml_only:
        issues.append(f"{base}.xml has no matching .md file")
    for base in md_only:
        issues.append(f"{base}.md has no matching .xml file")

    if not xml_files:
        issues.append("No XML dump files found")

    return {
        "valid": len(issues) == 0,
        "xml_files": len(xml_files),
        "md_files": len(md_files),
        "paired": len(xml_bases & md_bases),
        "issues": issues,
    }


def main():
    if len(sys.argv) < 2:
        print("Usage: python validate_dumps.py <dumps_dir>", file=sys.stderr)
        sys.exit(1)

    result = validate(sys.argv[1])

    if result["valid"]:
        print(f"OK: {result['xml_files']} XML + {result['md_files']} MD files, "
              f"{result['paired']} paired", file=sys.stderr)
    else:
        print(f"ISSUES FOUND:", file=sys.stderr)
        for issue in result["issues"]:
            print(f"  - {issue}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
