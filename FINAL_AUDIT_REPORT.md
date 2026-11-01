# Final Audit Report — Disaster Relief Logistics

## 1. Project Information

| Item | Details |
|---|---|
| Project | Disaster Relief Logistics System |
| Assignment | Data Structures and Algorithms — Assignment II |
| Team | 8 |
| Team members | 25AD101, 25AD105, 25AD116, 25AD203 |
| Problem statement | Plan relief supply and shelter connectivity after a disaster. |
| Runtime used for verification | Python 3.14.0 on Windows |
| Main implementation technologies | Python standard library, `unittest`, JSON, CSV |
| External algorithm libraries | None used for the required data structures and algorithms |

No assignment PDF was present in the repository. This audit therefore uses the
requirements in the supplied task description. The implementation and reports
are organized as follows:

| Area | Main files |
|---|---|
| Console entry and shared scenario | [main.py](./main.py), [console_app.py](./console_app.py), [scenario.py](./scenario.py) |
| Trees and expressions | [trees.py](./trees.py), [avl_expression.py](./avl_expression.py) |
| Graph and route algorithms | [graph.py](./graph.py), [mst.py](./mst.py) |
| Task scheduling | [scheduling.py](./scheduling.py) |
| Benchmarking and automated tests | [analysis.py](./analysis.py), [tests.py](./tests.py) |
| Documentation and reports | [README.md](./README.md), [docs/](./docs/), [report/](./report/) |
| Persistent data and existing results | [data/](./data/), [results/](./results/) |
| New audit evidence | [results/final_audit/](./results/final_audit/) |

## 2. Team 8 Requirement Verification

| Assigned concept | Implementation | Status | Evidence |
|---|---|---|---|
| Unit III — General Tree: Region → District → Shelter | [trees.py](./trees.py) | PASS | Hierarchy validation, insertion, subtree deletion and traversal tests; display implementation inspected. |
| Unit III — BST: supply stock management | [trees.py](./trees.py) | PASS | Search, update, deletion, bounds, range and traversal tests. |
| Unit III — AVL: relief-camp index | [avl_expression.py](./avl_expression.py) | PASS | Rotation, deletion, invariant and 10,000-operation stress tests. |
| Unit IV — Dijkstra: supply routes | [graph.py](./graph.py) | PASS | Shortest-path tests, negative-weight rejection and route/distance-table code inspection. |
| Unit IV — MST: connecting shelters | [mst.py](./mst.py) | PASS | Prim/Kruskal agreement checks on connected graphs and forest tests on disconnected graphs. |
| Unit IV — BFS: nearest depot | [graph.py](./graph.py) | PASS | Edge-count route and nearest-depot tests. |
| Unit V — Greedy correctness arguments | [report/project_report.md](./report/project_report.md), [report/complexity_analysis.md](./report/complexity_analysis.md), [analysis.py](./analysis.py) | PASS | Dijkstra induction argument and MST cut-property argument are documented. |

## 3. Complete Assignment Rubric Audit

Status meanings: **PASS** = verified by source inspection and/or execution;
**PARTIAL** = present but limited or not fully verified; **FAIL** = requested
capability is missing.

| Unit | Requirement | Implementation file | Verification method | Status | Remarks |
|---|---|---|---|---|---|
| III | General-tree insertion, subtree deletion and display | [trees.py](./trees.py) | Source inspection; insertion/deletion tests | PASS | Enforces Network → Region → District → Shelter. |
| III | Preorder, postorder and level-order traversals | [trees.py](./trees.py) | Source inspection and traversal test | PASS | General-tree preorder/postorder are recursive; level-order is iterative. |
| III | Recursive and iterative traversals where required | [trees.py](./trees.py) | Source inspection; recursive/iterative BST traversal equivalence test | PASS | BST has recursive traversals and explicit iterative alternatives. |
| III | BST insertion, search and leaf/one-child/two-child deletion | [trees.py](./trees.py), [tests.py](./tests.py) | Tests for each deletion shape; one-child test corrected to create a genuine one-child node | PASS | BST implementation itself required no change. |
| III | BST minimum and maximum | [trees.py](./trees.py), [tests.py](./tests.py) | Unit test | PASS |  |
| III | BST successor and predecessor | [trees.py](./trees.py), [tests.py](./tests.py) | Unit test | PASS | Also handles a key that is not present by returning the nearest candidate. |
| III | BST range query | [trees.py](./trees.py), [tests.py](./tests.py) | Inclusive-range unit test and skewed-tree test | PASS |  |
| III | Compare BST and AVL heights for 1,000 sorted IDs | [analysis.py](./analysis.py), [results/final_audit/tree_benchmark_results.csv](./results/final_audit/tree_benchmark_results.csv) | Five measured sorted-input runs | PASS | At n=1,000: BST height 1,000; AVL height 10. |
| III | AVL insertion and deletion | [avl_expression.py](./avl_expression.py), [tests.py](./tests.py) | Insert/search, delete/rebalance and random-operation tests | PASS |  |
| III | LL, RR, LR and RL rotations | [avl_expression.py](./avl_expression.py), [tests.py](./tests.py) | Four targeted rotation tests | PASS |  |
| III | Rotation trace | [avl_expression.py](./avl_expression.py), [tests.py](./tests.py) | Rotation-log assertions and menu implementation | PASS |  |
| III | `verify()` checks ordering, stored heights and balance factors | [avl_expression.py](./avl_expression.py), [tests.py](./tests.py) | Invariant checker invoked after 10,000 stress operations and in benchmarks | PASS |  |
| III | At least 10,000 random insert/delete stress operations | [avl_expression.py](./avl_expression.py), [tests.py](./tests.py) | Fixed-seed 10,000-operation test; verifies after every operation | PASS | Operations are a random mix of inserts and deletes. |
| III | Expression tree construction from postfix | [avl_expression.py](./avl_expression.py), [tests.py](./tests.py) | Construction and malformed-input tests | PASS |  |
| III | Expression evaluation and minimal-parenthesis infix | [avl_expression.py](./avl_expression.py), [tests.py](./tests.py) | Numeric/variable evaluation and grouping tests | PASS |  |
| III | Invalid postfix and division-by-zero handling | [avl_expression.py](./avl_expression.py), [tests.py](./tests.py) | Expected `ValueError` tests | PASS |  |
| IV | Directed/undirected and weighted/unit-weight graphs | [graph.py](./graph.py), [tests.py](./tests.py) | Graph construction and workflow tests | PASS | Default edge weight 1 represents an unweighted edge. |
| IV | Adjacency-list and adjacency-matrix representations | [graph.py](./graph.py) | Source inspection; representation display and consistency tests | PASS | Both are maintained together. |
| IV | Ability to switch between list-only and matrix-only representations | [graph.py](./graph.py), [console_app.py](./console_app.py) | Menu/API inspection | FAIL | The UI displays either representation and can change directedness, but does not select which representation backs the graph. |
| IV | Compare memory usage of the two representations | [graph.py](./graph.py), [analysis.py](./analysis.py) | Inspected `memory_report()` and benchmark memory fields | PARTIAL | Reported values are shallow Python-container estimates, not total or peak memory. |
| IV | BFS shortest route by number of edges and nearest depot | [graph.py](./graph.py), [tests.py](./tests.py) | Shortest-edge route, unreachable route and nearest-depot tests | PASS | BFS optimizes edge count, not weight. |
| IV | DFS discovery and finishing times | [graph.py](./graph.py), [tests.py](./tests.py) | Timestamp assertions | PASS |  |
| IV | DFS tree, back, forward and cross edge classes | [graph.py](./graph.py), [tests.py](./tests.py) | Directed test exercises all four labels | PASS |  |
| IV | Connected components and strongly connected components | [graph.py](./graph.py), [tests.py](./tests.py) | Disconnected graph and directed SCC tests | PASS |  |
| IV | Topological sorting with Kahn and DFS | [scheduling.py](./scheduling.py), [tests.py](./tests.py) | Acyclic DAG tests for both algorithms | PASS |  |
| IV | Cycle detection that prints/reports a cycle | [scheduling.py](./scheduling.py), [console_app.py](./console_app.py), [tests.py](./tests.py) | Cycle-path unit test and output path inspection | PASS |  |
| IV | Critical path and earliest start times for DAG tasks | [scheduling.py](./scheduling.py), [tests.py](./tests.py) | Critical-path and earliest-start tests | PASS | Cyclic schedules are rejected. |
| IV | Array-based Dijkstra with path and distance table | [graph.py](./graph.py), [console_app.py](./console_app.py), [tests.py](./tests.py) | Shortest-path tests and verbose-table code inspection | PASS | The verbose form prints estimates for every vertex at each selection. |
| IV | Demonstrate a concrete Dijkstra failure on negative edges | [graph.py](./graph.py), [tests.py](./tests.py) | Demo code inspection; rejection test | PARTIAL | The menu prints a counterexample explanation; it does not execute a flawed Dijkstra run against that graph. Correct `dijkstra()` rejects negative weights. |
| IV | Array-based Prim | [mst.py](./mst.py) | Source inspection and repeated benchmark execution | PASS | No heap/priority-queue library is used. |
| IV | Kruskal with manual edge sorting | [mst.py](./mst.py), [tests.py](./tests.py) | Manual merge-sort weight and tie-order tests; dense benchmark | PASS | Merge sort is bottom-up and uses one auxiliary reference array. |
| IV | Union-Find path compression and union by rank | [mst.py](./mst.py), [tests.py](./tests.py) | Source inspection and union/find tests | PASS |  |
| IV | Prim/Kruskal costs agree on connected graphs | [analysis.py](./analysis.py), [results/final_audit/graph_benchmark_results.csv](./results/final_audit/graph_benchmark_results.csv) | Every algorithm repetition checked for all six connected workloads | PASS | All recorded costs match. |
| IV | Disconnected graphs yield minimum spanning forests | [mst.py](./mst.py), [tests.py](./tests.py) | Disconnected sample graph test | PASS | Both algorithms return component lists. |
| V | Dijkstra correctness argument | [report/project_report.md](./report/project_report.md), [analysis.py](./analysis.py) | Reviewed documented induction argument | PASS | Assumes all edge weights are non-negative. |
| V | Explain Dijkstra's negative-edge limitation | [graph.py](./graph.py), [report/project_report.md](./report/project_report.md) | Negative-weight guard, test and documented explanation | PASS |  |
| V | Prim or Kruskal correctness proof via cut/cycle property | [report/project_report.md](./report/project_report.md), [analysis.py](./analysis.py) | Reviewed Prim cut-property proof and Kruskal safe-edge note | PASS |  |
| V | Non-recursive complexity derivations | [report/complexity_analysis.md](./report/complexity_analysis.md) | Reviewed BFS, Dijkstra, Prim, Kruskal derivations | PASS |  |
| V | Recursive complexity derivations | [report/complexity_analysis.md](./report/complexity_analysis.md) | Reviewed tree traversal, BST and AVL derivations | PASS |  |
| V | BST best, average and worst cases | [report/complexity_analysis.md](./report/complexity_analysis.md) | Reviewed analysis and benchmark evidence | PARTIAL | Best/worst recurrences are given; average O(log n) is stated for random BSTs without a full expected-height derivation. |
| V | AVL height proof with N(h)=N(h−1)+N(h−2)+1 | [report/complexity_analysis.md](./report/complexity_analysis.md) | Recurrence and logarithmic bound reviewed | PASS |  |
| V | Big-O, Big-Omega and Big-Theta | [report/complexity_analysis.md](./report/complexity_analysis.md) | Formal array-Dijkstra bounds reviewed | PASS |  |
| V | Union-Find amortized analysis | [report/complexity_analysis.md](./report/complexity_analysis.md), [analysis.py](./analysis.py) | Inverse-Ackermann discussion reviewed | PASS |  |
| V | Comparison-sort lower bound for Kruskal | [report/complexity_analysis.md](./report/complexity_analysis.md) | Decision-tree lower-bound discussion reviewed | PASS |  |
| V | Empirical BST versus AVL comparison | [analysis.py](./analysis.py), [results/final_audit/tree_benchmark_results.csv](./results/final_audit/tree_benchmark_results.csv) | Five repetitions at all requested sizes and orders | PASS | Includes insert, search, delete, heights and AVL verification. |
| V | Prim versus Kruskal on sparse and dense graphs | [analysis.py](./analysis.py), [results/final_audit/graph_benchmark_results.csv](./results/final_audit/graph_benchmark_results.csv) | Five repetitions on six workloads | PASS | Includes the complete 2,000-vertex, 1,000,000-edge dense graph. |
| Common | Empty/single-vertex, invalid input and scenario save/load | [tests.py](./tests.py), [scenario.py](./scenario.py) | Suite plus focused empty-graph Dijkstra/Prim/Kruskal and single-vertex MST checks | PASS | Malformed scenarios, invalid hierarchy, missing endpoints and JSON round-trips are covered. |
| Common | Application launch | [main.py](./main.py), [console_app.py](./console_app.py) | `17` piped to `python main.py`; clean menu and exit observed | PASS |  |

## 4. Tree Benchmark Results

The measurements below are arithmetic averages over five repetitions. Seed:
42. Search visits every inserted key once in insertion order. Deletion removes
all keys in that same order; consequently sorted BST deletion removes the
current root repeatedly and should not be interpreted as a random-deletion
workload. Tree initialization for deletion is timed separately and excluded
from deletion time. Heights are measured after insertion. AVL invariants were
checked after insertion and deletion on every repetition.

| n | Input order | BST insert (s) | BST search (s) | BST delete (s) | BST height | AVL insert (s) | AVL search (s) | AVL delete (s) | AVL height |
|---:|---|---:|---:|---:|---:|---:|---:|---:|---:|
| 1,000 | Sorted | 0.029832 | 0.025870 | 0.000201 | 1,000 | 0.006398 | 0.000511 | 0.004722 | 10 |
| 1,000 | Random | 0.001072 | 0.000740 | 0.000881 | 21 | 0.005894 | 0.000653 | 0.004589 | 12 |
| 5,000 | Sorted | 0.739981 | 0.647131 | 0.000854 | 5,000 | 0.042084 | 0.003675 | 0.025827 | 13 |
| 5,000 | Random | 0.007508 | 0.004607 | 0.005936 | 28 | 0.036617 | 0.004066 | 0.035605 | 15 |
| 20,000 | Sorted | 23.962121 | 19.476735 | 0.006080 | 20,000 | 0.172499 | 0.017115 | 0.116689 | 15 |
| 20,000 | Random | 0.036223 | 0.026582 | 0.030711 | 35 | 0.169550 | 0.019130 | 0.156670 | 17 |

Minimum and maximum measurements for each timed operation are in
[tree_benchmark_results.csv](./results/final_audit/tree_benchmark_results.csv).
The sorted-BST insertion/search growth and height demonstrate degeneration;
the AVL heights remain small and its invariants passed throughout. On random
inputs the BST inserts faster in this implementation, while AVL search remains
competitive and its height is bounded.

## 5. Graph Benchmark Results

Each graph was generated once per configuration; graph setup is measured
separately. Prim and Kruskal used the same connected undirected graph for each
configuration, and each algorithm ran five times. Density is E divided by
V(V−1)/2. Memory is the measured shallow size of project graph containers;
it excludes referenced edge/vertex objects and transient algorithm memory.

| V | E | Workload | Density | Setup (s) | Prim avg (s) | Kruskal avg (s) | Prim/Kruskal cost | Shallow graph bytes |
|---:|---:|---|---:|---:|---:|---:|---:|---:|
| 200 | 400 | Sparse | 0.020101 | 0.002915 | 0.003121 | 0.001575 | 5,340 / 5,340 | 435,456 |
| 200 | 10,000 | Dense | 0.502513 | 0.049486 | 0.006218 | 0.053609 | 343 / 343 | 3,119,464 |
| 1,000 | 2,000 | Sparse | 0.004004 | 0.033953 | 0.074140 | 0.010076 | 28,937 / 28,937 | 8,962,048 |
| 1,000 | 250,000 | Dense | 0.500501 | 2.864649 | 0.136534 | 4.309716 | 1,007 / 1,007 | 38,467,432 |
| 2,000 | 4,000 | Sparse | 0.002001 | 0.264421 | 0.302146 | 0.023645 | 58,334 / 58,334 | 35,064,248 |
| 2,000 | 1,000,000 | Dense | 0.500250 | 39.254116 | 0.728644 | 49.093195 | 1,999 / 1,999 | 153,322,120 |

All six graph sizes hit their exact requested edge counts; no cap was applied.
Prim and Kruskal returned matching costs in every repetition. These
measurements show the expected pattern on these workloads: Kruskal is faster
on the larger sparse graphs, while array-based Prim is much faster on dense
graphs. Per-run minima and maxima are in
[graph_benchmark_results.csv](./results/final_audit/graph_benchmark_results.csv).

## 6. Automated Test Results

**Command:** `python -m unittest -v`

**Final result:** 86 tests run, 86 passed, 0 failures, 0 errors, in 5.207 s.

| Test class | Count | Coverage examples |
|---|---:|---|
| TestGeneralTree | 7 | Hierarchy constraints, subtree deletion and traversals |
| TestSupplyBST | 14 | Search, all deletion shapes, range, min/max and skewed tree |
| TestAVLTree | 8 | Four rotations, deletion, invariant and 10,000 random operations |
| TestExpressionTree | 8 | Evaluation, infix grouping, malformed expressions and division by zero |
| TestGraph | 16 | BFS, DFS times/classes, connectivity, SCC, Dijkstra and negative weights |
| TestMST | 5 | Prim/Kruskal, disconnected forest, equal weights and manual sort |
| TestScheduling | 6 | Both topological sorts, cycle, earliest starts and critical path |
| TestDisjointSet | 2 | Union/find behavior |
| TestEmptyStructures | 4 | Empty BST, AVL, expression and graph |
| TestScenarioPersistence | 7 | JSON round-trip, validation and reconstruction |
| TestBenchmarkConfiguration | 1 | Repetitions, exact requested graph edges, seed and CSV metadata |
| TestInteractiveScenarioWorkflow | 8 | Builder, directedness conversion, save/restart/load and route |
| **Total** | **86** | **All passed** |

Supplemental runtime checks also confirmed empty-graph Dijkstra/Prim/Kruskal
results and a single-vertex MST. Full test results are recorded in
[report/test_results.md](./report/test_results.md).

## 7. Correctness and Complexity Verification

- Dijkstra's correctness argument uses induction on finalized vertices and
  states the non-negative-weight precondition in
  [report/project_report.md](./report/project_report.md). The implementation
  rejects negative weights.
- Prim's cut-property proof is documented in the project report. Kruskal uses
  manual merge sort and Union-Find; the analysis notes its safe-edge/cut
  property.
- [report/complexity_analysis.md](./report/complexity_analysis.md) derives
  BFS, array-based Dijkstra, Prim, Kruskal, tree traversal, BST and AVL bounds.
- The AVL minimum-node recurrence
  `N(h) = N(h-1) + N(h-2) + 1`, inverse-Ackermann Union-Find analysis, and
  comparison-sorting lower bound are present.
- Big-O, Big-Omega and Big-Theta are explicitly demonstrated for
  array-based Dijkstra.
- The expected O(log n) height for random BSTs is stated, but a full
  expected-height derivation is not included.

## 8. Issues Found and Corrections

| File(s) | Issue | Correction | Verification |
|---|---|---|---|
| [analysis.py](./analysis.py) | Existing benchmarks took one sample, omitted tree search/deletion, and capped the 2,000-vertex dense workload at 50,000 edges. | Added five-repetition averages/minima/maxima, search/deletion measurements, separate setup timing, exact-edge validation, full default sizes, and dedicated final-audit outputs. | Ran all 12 tree and six graph configurations; CSV assertions confirm 5 repetitions and exactly 1,000,000 dense edges at V=2,000. |
| [mst.py](./mst.py) | Recursive merge sort made repeated list slices and temporary lists impractical for the required million-edge workload. | Replaced it with a bottom-up manual merge sort using one auxiliary reference array while retaining deterministic weight/endpoint ordering. | Sort order and ties tested; full dense Kruskal benchmark completed five times and matched Prim. |
| [console_app.py](./console_app.py) | Interactive benchmark size limits/defaults did not allow required assignment sizes and described timings as single-run. | Updated defaults and limits to 1,000/5,000/20,000 tree nodes and 200/1,000/2,000 graph vertices; updated timing description. | Application startup smoke test and final test suite passed. |
| [tests.py](./tests.py) | The test named for one-child BST deletion actually deleted a node with two children; DFS category and benchmark expectations also needed direct coverage. | Corrected the deletion setup and added all-four DFS edge-category, merge-sort tie-order, repeated-run and exact edge-count assertions. | All 86 tests pass. |
| [README.md](./README.md), [docs/FUNCTION_GUIDE.md](./docs/FUNCTION_GUIDE.md) | Benchmark documentation described the old caps/output and did not give the assignment-sized reproduction command. | Documented the full run command, sizes, repetition count, dedicated output directory and memory estimate caveat. | Documentation claims cross-checked against the run and generated files. |
| [report/project_report.md](./report/project_report.md), [report/test_results.md](./report/test_results.md) | Existing report figures were stale (80 tests, single-run timings and capped dense graph). | Updated test totals, current benchmark highlights, dense-graph result and limitations. | Counts and selected values match the final test output and audit CSVs. |

No correctness failure in the production data-structure operations was found
by the final suite. Existing `data/scenario.json`,
`data/scenarios/1.json`, and historical benchmark files were not changed.

## 9. Remaining Gaps

1. There is no selectable adjacency-list-only versus adjacency-matrix-only
   graph mode. Both representations are stored together; displaying one or
   changing directedness is not a representation switch.
2. Graph memory results are shallow container estimates, not full heap or
   peak-memory measurements.
3. The negative-edge menu item explains the failure scenario but does not
   execute an intentionally incorrect Dijkstra implementation; the real
   implementation correctly rejects negative weights.
4. The average-case BST height is asserted rather than fully derived.
5. Recursive DFS, SCC, connected-components, and recursive tree helpers have
   not been stress-tested at depths beyond Python's recursion limit.
6. No original assignment PDF was found locally, so alignment to any
   requirements outside the supplied rubric remains unverified.
7. Individual member names, contributions and percentages were not supplied;
   the team must complete the contribution table before submission.

## 10. Final Rubric Assessment

Across the 48 rows in the complete rubric table: **44 PASS, 3 PARTIAL,
1 FAIL**. The project is operational and its core assigned algorithms are
implemented, tested and benchmarked at the requested sizes. It is **not a
claim of complete rubric compliance** because the representation-switching
requirement is missing and three areas remain partial.

Before submission:

- Confirm whether the assignment specifically requires selectable graph
  storage representations; implement and test that mode if required.
- Decide whether the Dijkstra negative-edge demonstration must show an
  actual failing run or whether the current explanation is acceptable.
- Expand the memory measurement and BST average-case analysis if the rubric
  expects those to be rigorous.
- Add the actual team member names and agreed contribution details.
- Compare against the original assignment PDF if the team has a copy.

## 11. Team Contribution Table

| Register number | Name | Contribution | Percentage |
|---|---|---|---|
| 25AD101 | Awaiting confirmation | Awaiting confirmation | Awaiting confirmation |
| 25AD105 | Awaiting confirmation | Awaiting confirmation | Awaiting confirmation |
| 25AD116 | Awaiting confirmation | Awaiting confirmation | Awaiting confirmation |
| 25AD203 | Awaiting confirmation | Awaiting confirmation | Awaiting confirmation |

No individual contributions or percentages have been inferred.

## 12. Evidence and Reproducibility

Commands and checks performed:

```text
python -m unittest -v
python -m py_compile analysis.py console_app.py mst.py tests.py
python -c "import analysis; analysis.run_final_audit_benchmarks()"
"17" | python main.py
git diff --check
```

The final benchmark command used seed 42, five repetitions, the required tree
sizes 1,000/5,000/20,000 and graph sizes 200/1,000/2,000. The graph generator
checked exact edge counts and connectedness; Prim and Kruskal cost equality
was asserted on every repetition.

Generated benchmark evidence:

- [tree_benchmark_results.csv](./results/final_audit/tree_benchmark_results.csv)
- [graph_benchmark_results.csv](./results/final_audit/graph_benchmark_results.csv)
- [benchmark_summary.md](./results/final_audit/benchmark_summary.md)

Test evidence: [report/test_results.md](./report/test_results.md). No
screenshots were created. Existing scenario JSON and historical benchmark
files were preserved.
