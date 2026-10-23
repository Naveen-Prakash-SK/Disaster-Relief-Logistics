# Disaster Relief Logistics — Project Report

**DSA Assignment II — Project-Based Assessment**  
**Team 8 | KPR Institute of Engineering and Technology**  
**Department of Artificial Intelligence and Data Science**  
**II Year, Section C | Course: Data Structures and Algorithms**

---

## 1. Title and Project Details

| Field | Details |
|-------|---------|
| Title | Disaster Relief Logistics System |
| Team | 8 |
| Members | 25AD101, 25AD105, 25AD116, 25AD203 |
| Language | Python 3.14.0 |
| Platform | Windows, VS Code |
| Submission | November 2026 |

---

## 2. Abstract and Problem Statement

### Abstract
This project implements a console-based disaster relief management system using fundamental data structures and algorithms. The system manages hierarchical location data (regions, districts, shelters), relief supply inventory, relief-camp indexing, road network modelling, route planning, minimum-cost connectivity, task scheduling and critical-path analysis. All data structures and algorithms are implemented from scratch without external libraries.

### Problem Statement
During natural disasters, coordinating relief efforts requires efficient management of:
- **Location hierarchies** (which shelters belong to which districts and regions)
- **Supply tracking** (fast lookup, update and range queries on inventory)
- **Route planning** (finding shortest/fewest-edge routes between depots and shelters)
- **Network connectivity** (minimum-cost infrastructure to connect all shelters)
- **Task scheduling** (ordering relief operations respecting dependencies)

---

## 3. Objectives and Proposed System

### Objectives
1. Implement General Tree, BST, AVL Tree and Expression Tree
2. Implement Graph ADT with adjacency list and matrix representations
3. Implement BFS, DFS, Dijkstra, Prim and Kruskal algorithms
4. Implement topological sorting, cycle detection and critical-path analysis
5. Provide correctness arguments and complexity analysis
6. Validate through automated testing and empirical benchmarks

### Proposed System
A modular console application with 17 main-menu actions plus an exit option. The menu operates on one shared scenario and supports guided entry and JSON save/load. Each module is independently testable.

---

## 4. Data Structures and Design

### Architecture

```
main.py ──┬── console_app.py     (Shared interactive scenario)
          ├── scenario.py       (Validation and JSON persistence)
          ├── trees.py           (General Tree + BST)
          ├── avl_expression.py  (AVL Tree + Expression Tree)
          ├── graph.py           (Graph ADT, BFS, DFS, SCC, Dijkstra)
          ├── mst.py             (Prim, Kruskal, Union-Find)
          ├── scheduling.py      (Topological Sort, Critical Path)
          ├── analysis.py        (Benchmarks, Complexity Notes)
          └── tests.py           (80 Automated Tests)
```

### Data Structures

| Structure | Purpose | Module |
|-----------|---------|--------|
| General Tree | Location hierarchy (Region → District → Shelter) | trees.py |
| BST | Supply inventory indexed by integer ID | trees.py |
| AVL Tree | Relief-camp index with guaranteed O(log n) | avl_expression.py |
| Expression Tree | Postfix expression evaluation | avl_expression.py |
| Graph (adj list + matrix) | Road network | graph.py |
| Disjoint Set (Union-Find) | Kruskal's MST | mst.py |
| Task DAG | Scheduling dependencies | scheduling.py |

---

## 5. Algorithms and Pseudocode

See [pseudocode.md](pseudocode.md) for detailed pseudocode of:
- AVL deletion with rebalancing
- Array-based Dijkstra
- Union-Find with path compression

### Algorithm Summary

| Algorithm | Design Technique | Time Complexity |
|-----------|-----------------|-----------------|
| BST operations | Divide & Conquer | O(h) per op |
| AVL insert/delete | Divide & Conquer + Rebalancing | O(log n) |
| BFS | Exhaustive Search | O(V + E) |
| DFS | Exhaustive Search | O(V + E) |
| Dijkstra (array) | Greedy | O(V²) |
| Prim (array) | Greedy | O(V²) |
| Kruskal | Greedy + Union-Find | O(E log E) |
| Topological Sort | BFS/DFS-based | O(V + E) |

---

## 6. Correctness Arguments and Proofs

### Dijkstra Correctness
**Claim:** Array-based Dijkstra correctly finds shortest paths from a source when all edge weights are non-negative.

**Proof (by induction on the number of finalised vertices):**
- **Base:** The source has distance 0, which is correct.
- **Inductive step:** Assume all k finalised vertices have correct shortest distances. The (k+1)-th vertex u is selected with minimum tentative distance d[u]. Any alternative path to u must pass through an unfinalised vertex w. Since w is unfinalised, d[w] ≥ d[u]. The sub-path from w to u adds non-negative weight, so the total ≥ d[w] ≥ d[u]. Thus d[u] is correct.
- **Failure with negative edges:** If an edge (w, u) has negative weight, d[w] + weight(w,u) could be < d[u] even after u is finalised.

### Prim Correctness (Cut Property)
**Theorem:** For any cut of the graph, the minimum-weight edge crossing the cut belongs to some MST.

**Proof:** Let T be an MST. If the minimum crossing edge e = (u,v) is not in T, adding e creates a cycle. This cycle contains another cut-crossing edge e'. Since w(e) ≤ w(e'), replacing e' with e gives a spanning tree of no greater weight that includes e. It is therefore also an MST, proving that some MST contains the minimum crossing edge.

### AVL Height Bound
**Claim:** An AVL tree with n nodes has height h = O(log n).

**Proof:** Let N(h) be the minimum number of nodes in an AVL tree of height h.
- N(0) = 0, N(1) = 1
- N(h) = N(h-1) + N(h-2) + 1

Since N(h) > N(h-2) + N(h-2) = 2·N(h-2), we get N(h) > 2^(h/2).
Therefore n ≥ N(h) > 2^(h/2), giving h < 2·log₂(n) = O(log n).

---

## 7. Complexity Derivations and Recurrences

See [complexity_analysis.md](complexity_analysis.md) for complete derivations.

### Tree Traversal
T(n) = T(k) + T(n-1-k) + O(1)  →  T(n) = O(n)

### BST Insertion
- Best: T(n) = T(n/2) + O(1) → O(log n) (balanced)
- Worst: T(n) = T(n-1) + O(1) → O(n) (sorted input)
- Average: O(log n) for random keys

### AVL Insertion
T(n) = T(n') + O(1) where n' ≤ n-1 and h = O(log n) → O(log n)

### Non-Recursive Algorithms
| Algorithm | Time | Space |
|-----------|------|-------|
| BFS | O(V + E) | O(V) |
| Dijkstra (array) | O(V² + E) ≈ O(V²) | O(V) |
| Prim (array) | O(V²) | O(V) |
| Kruskal | O(E log E + E·α(V)) ≈ O(E log E) | O(V + E) |

---

## 8. Testing Methodology and Test Results

See [test_results.md](test_results.md) for complete test output.

### Summary
- **80 automated tests** across 12 test classes
- All tests pass (0 failures, 0 errors)
- Tests cover: General Tree, BST, AVL, Expression Tree, Graph/BFS/DFS/SCC/Dijkstra, MST, Scheduling, Union-Find, Empty structures

### Test Categories
| Class | Tests | Coverage |
|-------|-------|----------|
| TestGeneralTree | 7 | Insert, hierarchy validation, delete, traversals |
| TestSupplyBST | 14 | Search, delete cases, min/max, range query, iterative traversals and skewed-tree operations |
| TestAVLTree | 8 | All rotations, delete rebalance, stress test |
| TestExpressionTree | 8 | Evaluation, infix grouping, unary minus, errors |
| TestGraph | 15 | BFS, DFS, Dijkstra, SCC, disconnected graph and graph representation conditions |
| TestMST | 5 | Prim/Kruskal agreement, disconnected, merge sort |
| TestScheduling | 6 | Topological sort, cycle detection, critical path, empty DAG |
| TestDisjointSet | 2 | Union-find correctness |
| TestEmptyStructures | 4 | Edge cases |
| TestScenarioPersistence | 7 | JSON round-trip, validation, graph/task reconstruction |
| TestBenchmarkConfiguration | 1 | Custom sizes, seed and CSV metadata |
| TestInteractiveScenarioWorkflow | 3 | Guided entry, persistence, routes and graph conversion |

---

## 9. Benchmark Tables and Interpretation

### Tree Benchmarks: BST vs AVL

| n | Type | Input | Time (s) | Height |
|---|------|-------|----------|--------|
| 1,000 | BST | sorted | 0.032684 | 1,000 |
| 1,000 | AVL | sorted | 0.007379 | 10 |
| 1,000 | BST | random | 0.001781 | 21 |
| 1,000 | AVL | random | 0.009604 | 12 |
| 5,000 | BST | sorted | 0.892764 | 5,000 |
| 5,000 | AVL | sorted | 0.046385 | 13 |
| 5,000 | BST | random | 0.008043 | 28 |
| 5,000 | AVL | random | 0.051774 | 15 |
| 20,000 | BST | sorted | 13.358428 | 20,000 |
| 20,000 | AVL | sorted | 0.185719 | 15 |
| 20,000 | BST | random | 0.036685 | 35 |
| 20,000 | AVL | random | 0.195739 | 17 |

**Observations:**
- BST with sorted input shows O(n) height degradation (degenerate linked list)
- AVL maintains O(log n) height regardless of input order
- BST sorted insertion time grows quadratically; AVL remains near-linear
- With random input, BST height is reasonable but AVL is consistently lower

### Graph Benchmarks: Prim vs Kruskal

| V | E | Type | Prim (s) | Kruskal (s) | Cost |
|---|---|------|----------|-------------|------|
| 200 | 400 | sparse | 0.004157 | 0.003964 | 5,340 |
| 200 | 10,000 | dense | 0.006723 | 0.083455 | 343 |
| 1,000 | 2,000 | sparse | 0.086595 | 0.012993 | 28,937 |
| 1,000 | 250,000 | dense | 0.147201 | 6.450146 | 1,007 |
| 2,000 | 4,000 | sparse | 0.380274 | 0.041227 | 58,334 |
| 2,000 | 50,000 | dense* | 0.332871 | 0.637205 | 5,782 |

**Observations:**
- Array-based Prim is O(V²) — time depends on V, not E. Better for dense graphs.
- Kruskal is O(E log E) — fast for sparse graphs, slow when E is large.
- Both produce identical MST costs, confirming correctness.
- For V=1000 dense: Prim (0.147201s) outperforms Kruskal (6.450146s).
- These are single-run timings on deterministic inputs; elapsed times vary by environment and system load.

---

## 10. Sample Application Output

### Launching the Application
```
python main.py
```

### Menu
```
==================================================================
DISASTER RELIEF LOGISTICS — INTERACTIVE CONSOLE
Scenario: Disaster Relief Network | undirected graph | 0 vertices
==================================================================
 1. Guided disaster scenario builder
 2. Location hierarchy (General Tree)
 3. Supply inventory (BST)
 4. Relief camp index (AVL) and expression tree
 5. Build and view road network
 6. BFS nearest depot
 7. Dijkstra shortest route
 8. DFS and connectivity analysis
 9. Prim minimum spanning forest
10. Kruskal minimum spanning forest
11. Scheduling and critical path
12. Benchmarking and performance analysis
13. Save scenario
14. Load scenario
15. Reset scenario
16. Testing and diagnostics
17. Exit
```

This menu was observed by launching `python main.py` with `0` as input.
The automated workflow test separately verifies building and saving a
scenario, restarting, loading it, and calculating a route.

---

## 11. Limitations and Conclusion

### Limitations
1. Dense graph benchmarks for V=2000 use reduced edge count (50,000 instead of 1,000,000) to keep runtime practical
2. Recursive BST traversal helpers may hit Python's recursion limit on highly skewed trees; interactive display, range query and deletion are iterative.
3. No graphical visualisation — text-based output only (as specified)
4. Sample data is synthetic; real disaster data would require external integration

### Conclusion
The system successfully demonstrates all required data structures and algorithms:
- Trees (General, BST, AVL, Expression) with correct operations and verified invariants
- Graph algorithms (BFS, DFS, SCC, Dijkstra, Prim, Kruskal) on a realistic sample network
- Scheduling with topological sort, cycle detection and critical path
- Empirical benchmarks confirming theoretical complexity predictions
- 80 automated tests covering data structures, algorithms, persistence and interactive workflows

The modular architecture allows independent testing and extension of each component.

---

## 12. Team Contribution Table

| Reg. No. | Name | Contribution | Percentage |
|----------|------|-------------|------------|
| 25AD101 | (To be filled) | (To be updated by team) | — |
| 25AD105 | (To be filled) | (To be updated by team) | — |
| 25AD116 | (To be filled) | (To be updated by team) | — |
| 25AD203 | (To be filled) | (To be updated by team) | — |

> **Note:** This table should be updated by team members with their actual contributions before submission.
