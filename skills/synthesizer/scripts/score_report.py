# Copyright (c) 2026 Dor Shacham <dorishacham52@gmail.com>. All rights reserved.
# SPDX-License-Identifier: Proprietary

"""Compute overall quality score from validation results.

Usage:
    python score_report.py --coverage <file> --completeness <file> --consistency <file> --output <file>

Aggregates coverage, completeness, and consistency scores into a weighted
overall grade with actionable recommendations.

Scoring weights (inspired by InfoSeek's dual validation criteria):
- Coverage:     30% (did we look at the code?)
- Completeness: 30% (did we document what we found?)
- Consistency:  40% (is the analysis internally coherent?)
"""

import json
import os
import sys


def compute_score(coverage: dict, completeness: dict, consistency: dict) -> dict:
    """Compute weighted quality score."""
    scores = {}

    # Coverage score (0-100)
    if coverage.get("skip"):
        scores["coverage"] = {"score": 0, "weight": 0.30, "status": "SKIPPED"}
    else:
        cov_pct = coverage.get("coverage_pct", 0)
        scores["coverage"] = {
            "score": cov_pct,
            "weight": 0.30,
            "status": "PASS" if coverage.get("pass") else "FAIL",
            "detail": f"{coverage.get('covered_files', 0)}/{coverage.get('total_source_files', 0)} files",
        }

    # Completeness score (0-100)
    if completeness.get("skip"):
        scores["completeness"] = {"score": 0, "weight": 0.30, "status": "SKIPPED"}
    else:
        comp_pct = completeness.get("completeness_pct", 0)
        scores["completeness"] = {
            "score": comp_pct,
            "weight": 0.30,
            "status": "PASS" if completeness.get("pass") else "FAIL",
            "detail": f"{completeness.get('documented_symbols', 0)}/{completeness.get('total_symbols', 0)} symbols",
        }

    # Consistency score (binary: 100 if pass, 0 if fail)
    if consistency.get("skip"):
        scores["consistency"] = {"score": 0, "weight": 0.40, "status": "SKIPPED"}
    else:
        contradictions = consistency.get("contradictions", 0)
        cons_score = 100 if contradictions == 0 else max(0, 100 - contradictions * 20)
        scores["consistency"] = {
            "score": cons_score,
            "weight": 0.40,
            "status": "PASS" if consistency.get("pass") else "FAIL",
            "detail": f"{contradictions} contradictions across {consistency.get('unique_entities', 0)} entities",
        }

    # Weighted total
    active_weight = sum(s["weight"] for s in scores.values() if s["status"] != "SKIPPED")
    if active_weight > 0:
        weighted_sum = sum(s["score"] * s["weight"] for s in scores.values()
                          if s["status"] != "SKIPPED")
        # Renormalize if some checks were skipped
        overall = weighted_sum / active_weight
    else:
        overall = 0

    # Grade
    if overall >= 90:
        grade = "A"
    elif overall >= 75:
        grade = "B"
    elif overall >= 60:
        grade = "C"
    elif overall >= 45:
        grade = "D"
    else:
        grade = "F"

    # Recommendations
    recommendations = []
    if scores["coverage"]["status"] == "FAIL":
        uncovered = coverage.get("uncovered_list", [])
        if uncovered:
            top_uncovered = uncovered[:10]
            recommendations.append({
                "priority": "high",
                "area": "coverage",
                "action": f"Read and document {len(uncovered)} uncovered source files",
                "examples": top_uncovered,
            })

    if scores["completeness"]["status"] == "FAIL":
        for cat, info in completeness.get("by_category", {}).items():
            missing = info.get("missing_list", [])
            if missing:
                recommendations.append({
                    "priority": "medium",
                    "area": "completeness",
                    "action": f"Document {info.get('missing', 0)} missing {cat}",
                    "examples": missing[:5],
                })

    if scores["consistency"]["status"] == "FAIL":
        details = consistency.get("contradiction_details", [])
        for c in details[:3]:
            recommendations.append({
                "priority": "critical",
                "area": "consistency",
                "action": f"Resolve contradiction for entity '{c['entity']}'",
                "details": c.get("conflict", []),
            })

    return {
        "overall_score": round(overall, 1),
        "grade": grade,
        "scores": scores,
        "recommendations": recommendations,
        "summary": f"Grade {grade} ({overall:.1f}/100): "
                   f"coverage={scores['coverage']['score']:.0f}%, "
                   f"completeness={scores['completeness']['score']:.0f}%, "
                   f"consistency={scores['consistency']['score']:.0f}%",
    }


def main():
    args = {sys.argv[i]: sys.argv[i + 1] for i in range(1, len(sys.argv) - 1, 2)
            if sys.argv[i].startswith("--")}

    coverage_file = args.get("--coverage", "")
    completeness_file = args.get("--completeness", "")
    consistency_file = args.get("--consistency", "")
    output_file = args.get("--output", "")

    # Load validation results (handle missing files gracefully)
    coverage = {}
    completeness = {}
    consistency = {}

    for filepath, target in [(coverage_file, "coverage"),
                              (completeness_file, "completeness"),
                              (consistency_file, "consistency")]:
        if filepath and os.path.exists(filepath):
            with open(filepath, "r") as f:
                data = json.load(f)
                if target == "coverage":
                    coverage = data
                elif target == "completeness":
                    completeness = data
                else:
                    consistency = data
        else:
            if target == "coverage":
                coverage = {"skip": True, "reason": "file not found"}
            elif target == "completeness":
                completeness = {"skip": True, "reason": "file not found"}
            else:
                consistency = {"skip": True, "reason": "file not found"}

    result = compute_score(coverage, completeness, consistency)

    if output_file:
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        with open(output_file, "w") as f:
            json.dump(result, f, indent=2)
        print(f"\n{'='*60}", file=sys.stderr)
        print(f"  QUALITY SCORECARD: {result['summary']}", file=sys.stderr)
        print(f"{'='*60}", file=sys.stderr)
        if result["recommendations"]:
            print(f"\n  Recommendations ({len(result['recommendations'])}):", file=sys.stderr)
            for rec in result["recommendations"]:
                print(f"    [{rec['priority'].upper()}] {rec['action']}", file=sys.stderr)
        print(file=sys.stderr)
    else:
        json.dump(result, sys.stdout, indent=2)
        print()


if __name__ == "__main__":
    main()
