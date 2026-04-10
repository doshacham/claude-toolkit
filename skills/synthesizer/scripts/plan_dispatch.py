# Copyright (c) 2026 Dor Shacham <dorishacham52@gmail.com>. All rights reserved.
# SPDX-License-Identifier: Proprietary

"""Partition an exploration tree into balanced agent assignments.

Usage:
    python plan_dispatch.py <exploration_tree.json> [--agents N] [--output dispatch_plan.json]

Distributes tree nodes across N agents (default 4), optimizing for:
- Balanced complexity (similar total lines per agent)
- Cohesion (related packages stay together)
- Coverage (every node assigned to exactly one agent)

Inspired by InfoSeek's Planner Agent that decides exploration strategy.
"""

import json
import sys
from collections import defaultdict


def partition_nodes(tree: dict, num_agents: int = 4) -> list[dict]:
    """Partition tree nodes into balanced groups for agent dispatch."""
    nodes = tree.get("nodes", [])
    if not nodes:
        return []

    # Sort nodes by dependency depth (entry points first, then by complexity)
    roots = set(tree.get("roots", []))
    dep_map = {n["id"]: set(n.get("depends_on", [])) for n in nodes}
    node_map = {n["id"]: n for n in nodes}

    # Compute depth via BFS from roots
    depth = {}
    queue = list(roots)
    for r in queue:
        depth[r] = 0
    visited = set(queue)
    while queue:
        current = queue.pop(0)
        for n in nodes:
            if current in n.get("depends_on", []) and n["id"] not in visited:
                depth[n["id"]] = depth.get(current, 0) + 1
                visited.add(n["id"])
                queue.append(n["id"])

    # Assign depth 0 to any unvisited nodes
    for n in nodes:
        if n["id"] not in depth:
            depth[n["id"]] = 0

    # Group by top-level subtree (which root does each node descend from)
    subtree_groups = _group_by_subtree(nodes, roots, dep_map)

    # If we have enough subtrees, assign each to an agent
    if len(subtree_groups) >= num_agents:
        return _assign_subtrees_to_agents(subtree_groups, nodes, node_map, num_agents, tree)

    # Otherwise, partition by balanced complexity
    return _balanced_partition(nodes, num_agents, tree)


def _group_by_subtree(nodes, roots, dep_map):
    """Group nodes by which root subtree they belong to."""
    groups = defaultdict(list)
    node_ids = {n["id"] for n in nodes}

    # BFS from each root to find its subtree
    assigned = set()
    for root in sorted(roots):
        queue = [root]
        while queue:
            current = queue.pop(0)
            if current in assigned or current not in node_ids:
                continue
            assigned.add(current)
            groups[root].append(current)
            # Find nodes that depend on current (reverse direction for tree)
            for nid in node_ids:
                if current in dep_map.get(nid, set()) and nid not in assigned:
                    queue.append(nid)

    # Assign orphans to the largest group
    for n in nodes:
        if n["id"] not in assigned:
            if groups:
                largest = max(groups.keys(), key=lambda k: len(groups[k]))
                groups[largest].append(n["id"])
            else:
                groups["orphan"].append(n["id"])

    return dict(groups)


def _assign_subtrees_to_agents(subtree_groups, nodes, node_map, num_agents, tree):
    """Assign subtree groups to agents, merging small subtrees."""
    # Sort subtrees by total complexity
    subtree_complexity = {}
    for root, members in subtree_groups.items():
        total = sum(node_map.get(m, {}).get("complexity", 0) for m in members)
        subtree_complexity[root] = total

    sorted_subtrees = sorted(subtree_complexity.keys(),
                             key=lambda k: subtree_complexity[k], reverse=True)

    # Greedily assign subtrees to agents (least-loaded-first)
    agents = [{"id": i, "packages": [], "files": [], "complexity": 0, "name": ""}
              for i in range(num_agents)]

    for subtree_root in sorted_subtrees:
        # Find least loaded agent
        least = min(agents, key=lambda a: a["complexity"])
        members = subtree_groups[subtree_root]
        for member_id in members:
            node = node_map.get(member_id, {})
            least["packages"].append(member_id)
            least["files"].extend(node.get("files", []))
            least["complexity"] += node.get("complexity", 0)

    # Generate names
    for agent in agents:
        if agent["packages"]:
            primary = agent["packages"][0]
            agent["name"] = f"branch-{primary.replace('/', '-').replace('.', '-')}"
        else:
            agent["name"] = f"branch-empty-{agent['id']}"

    # Remove empty agents
    agents = [a for a in agents if a["files"]]

    return _format_dispatch_plan(agents, tree)


def _balanced_partition(nodes, num_agents, tree):
    """Partition nodes into balanced groups by complexity."""
    # Sort by complexity descending (largest-first bin packing)
    sorted_nodes = sorted(nodes, key=lambda n: n.get("complexity", 0), reverse=True)

    agents = [{"id": i, "packages": [], "files": [], "complexity": 0, "name": ""}
              for i in range(num_agents)]

    for node in sorted_nodes:
        least = min(agents, key=lambda a: a["complexity"])
        least["packages"].append(node["id"])
        least["files"].extend(node.get("files", []))
        least["complexity"] += node.get("complexity", 0)

    for agent in agents:
        if agent["packages"]:
            primary = agent["packages"][0]
            agent["name"] = f"branch-{primary.replace('/', '-').replace('.', '-')}"

    agents = [a for a in agents if a["files"]]
    return _format_dispatch_plan(agents, tree)


def _format_dispatch_plan(agents, tree):
    """Format agent assignments into dispatch plan."""
    plan = {
        "repo_path": tree.get("repo_path", ""),
        "language": tree.get("language", "unknown"),
        "method": tree.get("method", "unknown"),
        "total_agents": len(agents),
        "total_files": sum(len(a["files"]) for a in agents),
        "agents": [],
    }

    for agent in agents:
        plan["agents"].append({
            "id": agent["id"],
            "name": agent["name"],
            "packages": agent["packages"],
            "files": sorted(set(agent["files"])),
            "file_count": len(set(agent["files"])),
            "complexity": agent["complexity"],
        })

    return plan


def main():
    if len(sys.argv) < 2:
        print("Usage: python plan_dispatch.py <tree.json> [--agents N] [--output FILE]",
              file=sys.stderr)
        sys.exit(1)

    tree_file = sys.argv[1]
    num_agents = 4
    output_file = None

    if "--agents" in sys.argv:
        idx = sys.argv.index("--agents")
        if idx + 1 < len(sys.argv):
            num_agents = int(sys.argv[idx + 1])

    if "--output" in sys.argv:
        idx = sys.argv.index("--output")
        if idx + 1 < len(sys.argv):
            output_file = sys.argv[idx + 1]

    with open(tree_file, "r") as f:
        tree = json.load(f)

    plan = partition_nodes(tree, num_agents)

    if output_file:
        with open(output_file, "w") as f:
            json.dump(plan, f, indent=2)
        print(f"Dispatch plan written to {output_file}", file=sys.stderr)
    else:
        json.dump(plan, sys.stdout, indent=2)
        print()


if __name__ == "__main__":
    main()
