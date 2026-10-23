# Disaster Relief Logistics

**DSA Assignment II — Project-Based Assessment**  
**Team 8 | KPR Institute of Engineering and Technology**  
**Department of Artificial Intelligence and Data Science**  
**II Year, Section C**

## Overview

A console-based disaster relief management system that organizes regions, districts, shelters, relief camps, depots, supply inventory and road networks. The system implements core data structures (General Tree, BST, AVL Tree, Expression Tree) and graph algorithms (BFS, DFS, Dijkstra, Prim, Kruskal) from scratch in Python.

## Features

- **Location Hierarchy** (General Tree): Region → District → Shelter management
- **Supply Inventory** (BST): Insert, delete, search, range query, traversals
- **Relief-Camp Index** (AVL Tree): Self-balancing BST with all rotations
- **Expression Calculator**: Postfix → expression tree → evaluation + infix
- **Road Network** (Graph ADT): Adjacency list & matrix, directed/undirected
- **BFS**: Fewest-edge routes, nearest depot search
- **DFS**: Timestamps, edge classification, connected/strongly-connected components
- **Dijkstra**: Shortest weighted paths (array-based, no heapq)
- **Prim & Kruskal MST**: Minimum spanning forest, disconnected graph support
- **Scheduling**: Topological sort (Kahn + DFS), cycle detection, critical path
- **Benchmarks**: Empirical timing with CSV/markdown output

## Folder Structure

```
DisasterReliefLogistics/
├── main.py              # Application entry point, integrated menu
├── trees.py             # General Tree + BST
├── avl_expression.py    # AVL Tree + Expression Tree
├── graph.py             # Graph ADT, BFS, DFS, SCC, Dijkstra
├── mst.py               # Prim, Kruskal, Union-Find, merge sort
├── scheduling.py        # Topological sort, cycle detection, critical path
├── analysis.py          # Benchmarks and complexity analysis
├── tests.py             # 62 automated tests (unittest)
├── README.md            # This file
├── report/              # Project report and documentation
│   ├── project_report.md
│   ├── pseudocode.md
│   ├── complexity_analysis.md
│   └── test_results.md
└── results/             # Benchmark output
    ├── benchmark_results.csv
    └── benchmark_summary.md
```

## Requirements

- **Python 3.10+** (tested with Python 3.14.0)
- **No external dependencies** — uses only the Python standard library
- Compatible with Windows and VS Code terminal

## How to Run

### Launch the Application
```bash
python main.py
```

### Run Automated Tests
```bash
python -m unittest tests -v
```

### Run Benchmarks Only
```bash
python -c "from analysis import run_tree_benchmarks, run_graph_benchmarks, save_benchmark_results; t = run_tree_benchmarks(); g = run_graph_benchmarks(); save_benchmark_results(t, g)"
```
Or use menu option **11** from the application.

## Menu Options

| # | Feature | Module |
|---|---------|--------|
| 1 | Location hierarchy (General Tree) | trees.py |
| 2 | Relief supply inventory (BST) | trees.py |
| 3 | Relief-camp index (AVL) & Expression calculator | avl_expression.py |
| 4 | Build / view road network | graph.py |
| 5 | BFS nearest depot | graph.py |
| 6 | Dijkstra shortest supply route | graph.py |
| 7 | DFS and connectivity analysis | graph.py |
| 8 | Prim minimum spanning forest | mst.py |
| 9 | Kruskal minimum spanning forest | mst.py |
| 10 | Scheduling and critical path | scheduling.py |
| 11 | Timing experiments | analysis.py |
| 12 | Run automated self-tests | tests.py |
| 13 | Display sample scenario | main.py |

## Design Restrictions

1. All trees, graphs and algorithms are manually implemented
2. No NetworkX, heapq, or built-in priority queue
3. Array-based Dijkstra and Prim (no heap)
4. Edge sorting in Kruskal uses a manually-coded merge sort
5. No `eval()` for expression evaluation
6. Deterministic test data with fixed random seeds

## Algorithm Notes

- **Dijkstra** rejects negative edge weights with an explanatory error
- **BFS** finds fewest-edge routes (not shortest weighted distance)
- **Prim** and **Kruskal** produce matching MST costs on connected graphs
- **AVL** tree is verified after every operation in the stress test
- **Expression tree** detects invalid postfix, division by zero, undefined variables

## Team

| Reg. No. | Name |
|----------|------|
| 25AD101 | (To be filled) |
| 25AD105 | (To be filled) |
| 25AD116 | (To be filled) |
| 25AD203 | (To be filled) |
