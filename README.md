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
- **Expression Calculator**: Infix/postfix → expression tree → safe evaluation + infix
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
├── console_app.py       # Shared-state interactive menus and guided builder
├── scenario.py          # In-memory scenario and JSON persistence
├── trees.py             # General Tree + BST
├── avl_expression.py    # AVL Tree + Expression Tree
├── graph.py             # Graph ADT, BFS, DFS, SCC, Dijkstra
├── mst.py               # Prim, Kruskal, Union-Find, merge sort
├── scheduling.py        # Topological sort, cycle detection, critical path
├── analysis.py          # Benchmarks and complexity analysis
├── tests.py             # Automated unittest suite
├── README.md            # This file
├── report/              # Project report and documentation
│   ├── project_report.md
│   ├── pseudocode.md
│   ├── complexity_analysis.md
│   └── test_results.md
├── results/             # Benchmark output
│   ├── benchmark_results.csv
│   └── benchmark_summary.md
└── docs/
    └── FUNCTION_GUIDE.md
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
python -m unittest -v
```

### Run Benchmarks Only
```bash
python -c "from analysis import run_tree_benchmarks, run_graph_benchmarks, save_benchmark_results; t = run_tree_benchmarks(seed=42); g = run_graph_benchmarks(seed=42); save_benchmark_results(t, g, seed=42)"
```
Or use menu option **12** and enter safe sizes and a seed.

## Menu Options

| # | Feature | Module |
|---|---------|--------|
| 1 | Guided scenario builder; offers manual entry or demonstration data | console_app.py |
| 2 | Edit, display/search, traverse and delete location subtrees | trees.py |
| 3 | Supply insert/update/search/delete, min/max/range/list/tree shape | trees.py |
| 4 | Manage AVL camps and expression calculator | avl_expression.py |
| 5 | Add/remove graph vertices/edges and inspect road network | graph.py |
| 6 | BFS to selected or saved depots (fewest edges) | graph.py |
| 7 | Array-based Dijkstra shortest route | graph.py |
| 8 | DFS timestamps, classifications, components/SCC | graph.py |
| 9 | Prim minimum spanning forest on active undirected graph | mst.py |
| 10 | Kruskal minimum spanning forest on active undirected graph | mst.py |
| 11 | Add tasks/dependencies; topological orders and critical path | scheduling.py |
| 12 | BST/AVL and Prim/Kruskal benchmarks with configurable seed/sizes | analysis.py |
| 13–15 | Save, load, and reset active scenario | scenario.py |
| 16 | Testing and diagnostics submenu | tests.py |
| 17 | Exit | console_app.py |

The testing submenu runs all tests or tree, graph, scheduling, and scenario
persistence categories on request; it can also display the last actual test
summary from the current application session. Tests are not run at startup.

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

## Guided scenario and persistence

Start with an empty scenario, then select **1**, followed by guided entry.
The builder collects a
network name, hierarchical locations, supplies, camp IDs, directed or
undirected road vertices/connections and weights, depot vertices, task
durations, and dependencies. These same in-memory structures are used by all
algorithm options.

Select **13** to save JSON records to `data/scenario.json`. If the file exists,
the program asks before overwriting. After restarting with `python main.py`,
select **14** to load it; malformed input is reported without replacing the
active scenario. **15** resets only in-memory data after confirmation. The
program starts normally if there is no saved file.

Text/numeric prompts accept `q` to cancel. Blank depot selection uses the
saved depot list. Benchmarks limit sizes to 5,000 tree nodes and 500 graph
vertices. Enter finite edge weights; Dijkstra refuses negative weights.

### Example custom scenario

Choose option **1**, then guided entry, and enter a small network:

```text
Network name: North Relief
Regions: 1; Region: North; Districts: 1; District: River Town
Shelters: 1; Shelter: School Shelter
Supply records: 1; ID: 10; Name: Water; Quantity: 50
Camps: 1; ID: 21; Name: Camp One
Directed graph: no
Vertices: Depot, School Shelter
Road: Depot -> School Shelter, weight 7
Depots: Depot
Tasks: Assess (3), Deliver (4); dependency: Assess -> Deliver
```

Choose **6**, enter `School Shelter`, and leave depot selection blank: BFS
reports the route to `Depot` in one edge. Choose **7** with source `Depot` and
destination `School Shelter`: Dijkstra reports weight 7. Choose **13** to save;
after restarting, choose **14** and rerun the route to verify the restored
graph.

See [docs/FUNCTION_GUIDE.md](docs/FUNCTION_GUIDE.md) for public function
signatures, examples, algorithms, complexities, and data-structure details.

## Team

| Reg. No. | Name |
|----------|------|
| 25AD101 | (To be filled) |
| 25AD105 | (To be filled) |
| 25AD116 | (To be filled) |
| 25AD203 | (To be filled) |
