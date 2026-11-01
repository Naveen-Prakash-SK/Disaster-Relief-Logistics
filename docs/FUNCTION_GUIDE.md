# Function Guide — Disaster Relief Logistics

This guide describes the public operations used by the application. Labels and
IDs are strings and integers in the interactive menus; algorithm functions
usually accept the same labels as graph or task nodes. A **node** return value
is the actual manually implemented tree node, not a copy.

## General Tree (`trees.py`)

| Function | Purpose, inputs, and result |
|---|---|
| `GeneralTree(root_name: str = "Disaster Relief Network")` | Creates a location hierarchy with a Network root. |
| `find(name: str, node: GeneralTreeNode | None = None) -> GeneralTreeNode | None` | Depth-first search by globally unique name. Returns the first matching node or `None`. |
| `add_location(parent_name: str, name: str, location_type: str) -> tuple[bool, str]` | Adds only allowed links: Network→Region→District→Shelter. Reports duplicate, missing-parent, or invalid-hierarchy errors without changing the tree. |
| `delete_subtree(name: str) -> tuple[bool, str]` | Deletes the named node and its descendants; the root is protected. |
| `preorder()`, `postorder()`, `level_order() -> list[str]` | Return names in the named traversal order. Pre/postorder use recursion; level-order uses a list queue. |

**How it works:** Each node owns a list of children. Search and modification
walk the hierarchy until the target name is found; traversal visits each node
once. With `n` locations, search/add/delete are `O(n)` worst case; traversals
are `O(n)` time and `O(h)` recursive stack for depth `h` (level order uses
`O(n)` queue space).

**Example:** Add `TamilNadu` under the root, then `Coimbatore` under it:
`add_location(root_name, "TamilNadu", "Region")` followed by
`add_location("TamilNadu", "Coimbatore", "District")`. Option 1 runs these
operations and displays the updated hierarchy.

## Binary Search Tree (`trees.py`)

| Function | Purpose, inputs, and result |
|---|---|
| `SupplyBST.insert(key: int, item_name: str, quantity: int) -> None` | Adds a supply. An existing key updates that record; negative quantity raises `ValueError`. |
| `search(key: int) -> BSTNode | None` | Finds one record by supply ID. |
| `delete(key: int) -> bool` | Iteratively deletes a leaf, one-child node, or two-child node using its inorder successor. |
| `minimum()`, `maximum() -> BSTNode | None` | Return the smallest/largest ID record. |
| `successor(key: int)`, `predecessor(key: int) -> BSTNode | None` | Return the closest larger/smaller key, whether or not `key` exists. |
| `range_query(low: int, high: int) -> list[BSTNode]` | Iteratively returns records in inclusive ID range, sorted by ID; reversed bounds return an empty list. |
| `inorder()`, `preorder()`, `postorder()`, `level_order() -> list[BSTNode]` | Recursive/queue-based traversal helpers. |
| `inorder_iterative()`, `preorder_iterative()`, `postorder_iterative()`, `level_order_iterative()` | Explicit stack/queue alternatives; the console uses iterative listing for skewed trees. |
| `height() -> int` | Returns height measured in nodes (empty tree is 0), iteratively. |

**How it works:** A comparison sends each operation left for a smaller key or
right for a larger key. Operation time is `O(h)` where `h` is tree height;
worst case is `O(n)` for sorted insertions. Range query is `O(h + k)` in the
usual case, where `k` records are returned, and `O(n)` worst case. Traversal
is `O(n)` time. Iterative traversal uses `O(h)` stack or `O(n)` queue space.

**Example:** Insert `(101, "Water", 500)`, then
`range_query(100, 110)` returns the record. Option 2 exposes insertion/update,
search, deletion, min/max, range, ordered inventory, and tree shape.

## AVL Tree (`avl_expression.py`)

| Function | Purpose, inputs, and result |
|---|---|
| `AVLTree.insert(key, value=None) -> None` | Inserts or updates a key and rotates to restore balance. |
| `delete(key) -> bool` | Removes a key and rebalances ancestors. |
| `search(key) -> AVLNode | None` | Iterative key lookup. |
| `inorder() -> list[AVLNode]` | Returns nodes sorted by key. |
| `height() -> int` | Returns stored root height; empty tree is 0. |
| `verify() -> tuple[bool, str]` | Checks key ordering, stored heights, and balance factors. |
| `random_stress_test(n_ops: int = 10000, seed: int = 42)` | Performs seeded random insert/delete and calls `verify()` after every operation. Returns `(tree, verified_count, operation_count)`. |

**How it works:** Each node stores its height. After insert/delete, the tree
checks `height(left) - height(right)` and applies LL, RR, LR, or RL rotations.
Search/insert/delete are `O(log n)`; traversal and verification are `O(n)`.
The randomized stress test is `O(m log n)` expected for `m` operations.

**Example:** Insert keys `30, 20, 10`; the LL imbalance causes a right rotation.
Option 3 shows height, balance factors, and rotation history.

## Expression Tree (`avl_expression.py`)

| Function | Purpose, inputs, and result |
|---|---|
| `infix_to_postfix(expression: str) -> list[str]` | Tokenizes arithmetic infix text and applies operator precedence/parentheses; supports unary minus as `neg`. Invalid tokens or syntax raise `ValueError`. |
| `build_expression_tree(postfix_tokens: list[str]) -> ExpressionNode` | Builds a binary expression tree using an operand stack. Rejects malformed postfix input. |
| `evaluate_expression(root, variables: dict[str, int | float] | None = None) -> float` | Recursively evaluates operators and variable leaves. Raises `ValueError` for unknown variables or division by zero. It never calls `eval()`. |
| `infix_string(root) -> str` | Produces an infix form with parentheses when needed to preserve the operation tree. |

**How it works:** Infix conversion uses an operator stack in `O(t)` time and
space for `t` tokens. Tree construction, evaluation, and formatting each visit
`O(t)` nodes and use `O(t)` worst-case stack/recursion space.

**Example:** `infix_to_postfix("distance * rate + toll")` returns
`["distance", "rate", "*", "toll", "+"]`. The console prompts for each variable
and displays the tree expression and computed value.

## Graph ADT (`graph.py`)

| Function | Purpose, inputs, and result |
|---|---|
| `Graph(directed: bool = False)` | Creates a manual graph with adjacency list, adjacency matrix, and ordered labels. |
| `add_vertex(label) -> None` | Adds a vertex if it is not already present. Matrix expansion costs `O(V)`. |
| `remove_vertex(label) -> bool` | Removes a vertex and all incident edges, then rebuilds matrix indices. `O(V² + E)` due to matrix/list cleanup. |
| `add_edge(u, v, weight=1) -> None` | Adds or updates an edge; undirected graphs store both directions. Missing endpoints are automatically added. |
| `remove_edge(u, v) -> None` | Removes the directed edge or both undirected copies if present. |
| `has_edge(u, v) -> bool`, `get_weight(u, v)`, `neighbours(u) -> dict` | Edge inspection helpers. `neighbours` returns a shallow copy. |
| `all_edges() -> list[tuple]` | Returns directed arcs or one copy of each undirected edge. |
| `vertex_count()`, `edge_count() -> int`; `has_negative_weights() -> bool` | Graph counts and Dijkstra precondition helper. |
| `display_adj_list()`, `display_adj_matrix()`, `memory_report() -> None` | Print graph representations and approximate Python container sizes. |

An adjacency-list edge update is average `O(1)`. Matrix storage is `O(V²)`;
the adjacency list is `O(V + E)`. A zero-weight edge exists in the adjacency
list even though the displayed matrix uses zero for both absent and zero-weight
edges.

## BFS (`graph.py`)

| Function | Purpose, inputs, and result |
|---|---|
| `bfs(graph: Graph, start) -> tuple[dict, dict]` | Returns edge-count distances and predecessor map reachable from `start`; unknown source returns two empty dictionaries. |
| `bfs_path(graph, start, end) -> tuple[list | None, int | None]` | Reconstructs a minimum-edge path or returns `(None, None)`. |
| `bfs_nearest_depot(graph, source, depots) -> tuple[vertex | None, list | None, int | None]` | Selects the reachable supplied depot with minimum edge count. |

BFS uses a queue with a front index, visiting each reachable vertex/edge once:
`O(V + E)` time and `O(V)` space. Edge count is not weighted travel cost.
Example: in `Depot—Town—Shelter`, BFS returns the three-vertex route and two
edges. Options 5 and graph submenu route actions use the user's active graph.

## DFS (`graph.py`)

| Function | Purpose, inputs, and result |
|---|---|
| `dfs_full(graph, start=None) -> (discovery, finish, parent, edge_types, order)` | Runs DFS from the requested start first, then covers any remaining components. Unknown start raises `ValueError`. |
| `connected_components_undirected(graph) -> list[list]` | Groups vertices in an undirected graph. |
| `scc_kosaraju(graph) -> list[list]` | Finds strongly connected components in a directed graph using Kosaraju's two traversals. |

DFS is `O(V + E)` plus recursion stack `O(V)`. This implementation's SCC
ordering sorts finishing times, so it takes `O(V log V + E)` time and `O(V+E)`
extra space. Option 7 prints discovery/finish times, parents, edge labels,
components, and isolated vertices.

## Dijkstra (`graph.py`)

| Function | Purpose, inputs, and result |
|---|---|
| `dijkstra(graph, source, verbose=False) -> (distances, parents)` | Array-scan single-source shortest paths. Raises `ValueError` if any graph edge is negative. Unknown source returns empty maps. |
| `dijkstra_path(graph, source, target, verbose=False) -> (path | None, distance)` | Reconstructs the shortest path; unreachable targets return `(None, infinity)`. |

Each iteration scans the vertex array to choose the next minimum-distance
unvisited vertex, then relaxes adjacent edges. Time is `O(V² + E)` (`O(V²)` for
a simple graph) and auxiliary space is `O(V)`. Example: `Depot—(7)—Shelter`
returns distance 7. Option 6 shows the actual distance table and predecessors.

## Prim (`mst.py`)

`prim_mst(graph: Graph, start=None) -> (edges, total_cost, components)` uses
vertex arrays/dictionaries to scan for the least key (no heap). It restarts at
each unvisited component and returns a minimum spanning forest when the graph
is disconnected. For an undirected graph, time is `O(V² + E)` = `O(V²)` and
auxiliary space is `O(V)`. Each returned edge joins the current tree to a new
vertex. Option 8 prints chosen edges and running cost.

## Kruskal and Union-Find (`mst.py`)

| Function | Purpose, inputs, and result |
|---|---|
| `merge_sort_edges(edges: list[tuple]) -> list[tuple]` | Manual merge sort by `(weight, string(u), string(v))`; returns a new sorted list. |
| `DisjointSet(items)` | Creates one set per item, with parent and rank maps. |
| `find(item) -> root` | Finds and path-compresses the component representative. |
| `union(a, b) -> bool` | Merges distinct roots by rank; `False` means both were already connected. |
| `kruskal_mst(graph: Graph) -> (edges, total_cost, components)` | Sorts edges manually, accepts only component-joining edges, and returns a forest. |

Merge sort costs `O(E log E)` time and `O(E)` peak extra space. Union-Find costs
amortized `O(E α(V))` for the edge scan, where `α` grows so slowly it is at
most a small constant in practice. Total is `O(E log E)`; working space is
`O(V + E)`. Option 9 prints accepted and cycle-rejected edges. MST operations
are only valid on undirected graphs; disconnected results are forests.

## Scheduling (`scheduling.py`)

| Function | Purpose, inputs, and result |
|---|---|
| `TaskDAG.add_task(label: str, duration: number = 1) -> None` | Adds a task or updates its duration. |
| `add_dependency(prerequisite, task) -> None` | Adds an arc prerequisite→task; existing labels are auto-created with default duration 1 in the data-structure API. The application asks users to define tasks first. |
| `topological_sort_kahn(dag) -> (order, is_dag)` | Queue-based topological order; a partial order and `False` indicate a cycle. |
| `topological_sort_dfs(dag) -> (order, is_dag, cycle)` | DFS-based order or one detected cycle. |
| `detect_cycle(dag) -> (bool, cycle)` | Reports cycle presence and path. |
| `earliest_start_times(dag) -> (start_times, order)` | Computes earliest task starts; raises `ValueError` on cycles. |
| `critical_path(dag) -> (path, duration, start_times)` | Returns a longest-duration path through the DAG; empty DAG returns `([], 0, {})`. |

Topological sorting and earliest starts take `O(V + E)`. Critical-path
backtracking first builds predecessor lists, so it is also `O(V + E)` time and
space. Option 10 builds/edits tasks and dependencies and rejects cyclic
schedules.

## Benchmarking (`analysis.py`)

| Function | Purpose, inputs, and result |
|---|---|
| `run_tree_benchmarks(sizes=None, seed=42, repetitions=5) -> list[dict]` | Measures insertion, successful search, and deletion for BST and AVL with sorted and seeded random keys. Defaults to `1000, 5000, 20000`; each row includes average/minimum/maximum timings, deletion setup time, height, and AVL verification. |
| `run_graph_benchmarks(vertex_sizes=None, seed=42, repetitions=5) -> list[dict]` | Builds connected seeded graphs with the exact requested edge count and measures Prim/Kruskal. Defaults to `200, 1000, 2000`; no dense-size cap is applied. |
| `save_benchmark_results(tree_rows, graph_rows, seed=42, output_dir=None) -> None` | Writes measured CSV data and a Markdown summary. A supplied output directory writes separate tree and graph CSV files. |
| `run_final_audit_benchmarks(repetitions=5, seed=42)` | Runs all assignment benchmark sizes and writes the separated CSVs and summary to `results/final_audit/`. |

Measurements use `time.perf_counter()` and are empirical, machine/load
dependent averages; setup is excluded from graph algorithm timings. The graph
memory measurement is a shallow container-size estimate rather than total or
peak process memory. The console accepts up to 20,000 tree nodes and 2,000
graph vertices, with an optional random seed.

## Scenario Records (`scenario.py`)

| Function | Purpose, inputs, and result |
|---|---|
| `Scenario(network_name: str)` | Owns the shared location tree, supply BST, camp AVL, active road graph, depot labels, and task DAG used by every menu action. |
| `to_dict() -> dict` / `from_dict(data: dict) -> Scenario` | Convert to and validate JSON-friendly records; reconstructs the manual structures and rejects malformed records. |
| `save(path=DATA_PATH, overwrite=False) -> None` | Writes atomically and refuses overwrite by default. The console saves successive snapshots as `data/scenarios/1.json`, `2.json`, and so on. |
| `load(path=DATA_PATH) -> Scenario` | Reads, parses, validates, and reconstructs a scenario. |
| `sample() -> Scenario` | Builds the explicitly labelled demonstration data. |

Example:

```python
from scenario import Scenario

scenario = Scenario.sample()
scenario.save()                 # saves to data/scenario.json; raises if it exists
restored = Scenario.load()
```

The console's **Save Scenario** action creates the next available numbered file
under `data/scenarios/`. **Load Scenario** lists these files in numeric order
and also offers the existing `data/scenario.json` as a legacy save when present.
Loading does not serialize Python object internals, and malformed input leaves
the active scenario intact.
