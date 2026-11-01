"""Algorithm analysis, repeated empirical benchmarks, and complexity notes."""

import os
import time
import random
import csv
import sys


# ============================================================================
# HELPERS
# ============================================================================

RESULTS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                           "results")
FINAL_AUDIT_DIR = os.path.join(RESULTS_DIR, "final_audit")
DEFAULT_REPETITIONS = 5


def _ensure_results_dir(directory):
    os.makedirs(directory, exist_ok=True)


def _statistics(samples):
    return {
        "avg": sum(samples) / len(samples),
        "min": min(samples),
        "max": max(samples),
    }


def _new_benchmark_tree(structure):
    if structure == "BST":
        from trees import SupplyBST
        return SupplyBST()
    from avl_expression import AVLTree
    return AVLTree()


def _insert_benchmark_key(tree, structure, key):
    if structure == "BST":
        tree.insert(key, f"s{key}", key)
    else:
        tree.insert(key, f"c{key}")


def _measure_tree_case(n, structure, input_order, keys, repetitions, seed):
    insert_samples = []
    search_samples = []
    delete_samples = []
    delete_setup_samples = []
    heights = []

    for _ in range(repetitions):
        tree = _new_benchmark_tree(structure)
        started = time.perf_counter()
        for key in keys:
            _insert_benchmark_key(tree, structure, key)
        insert_samples.append(time.perf_counter() - started)
        heights.append(tree.height())

        if structure == "AVL":
            valid, message = tree.verify()
            if not valid:
                raise RuntimeError(f"AVL invariant check failed: {message}")

        started = time.perf_counter()
        for key in keys:
            tree.search(key)
        search_samples.append(time.perf_counter() - started)

        delete_tree = _new_benchmark_tree(structure)
        started = time.perf_counter()
        for key in keys:
            _insert_benchmark_key(delete_tree, structure, key)
        delete_setup_samples.append(time.perf_counter() - started)

        started = time.perf_counter()
        for key in keys:
            delete_tree.delete(key)
        delete_samples.append(time.perf_counter() - started)
        if delete_tree.root is not None:
            raise RuntimeError(
                f"{structure} deletion benchmark left nodes behind.")
        if structure == "AVL":
            valid, message = delete_tree.verify()
            if not valid:
                raise RuntimeError(
                    f"AVL invariant check failed after deletion: {message}")

    metrics = {}
    for operation, samples in (
            ("insert", insert_samples), ("search", search_samples),
            ("delete", delete_samples),
            ("delete_setup", delete_setup_samples)):
        for statistic, value in _statistics(samples).items():
            metrics[f"{operation}_{statistic}_s"] = value
    return {
        "n": n,
        "structure": structure,
        "input_order": input_order,
        **metrics,
        "height_after_insert_avg": sum(heights) / len(heights),
        "height_after_insert_min": min(heights),
        "height_after_insert_max": max(heights),
        "avl_verified": structure == "AVL",
        "seed": seed,
        "repetitions": repetitions,
    }


# ============================================================================
# TREE BENCHMARKS — BST vs AVL
# ============================================================================

def _bench_bst_sorted(n):
    """Insert n sorted keys into BST, return (insert_time, height)."""
    from trees import SupplyBST
    bst = SupplyBST()
    start = time.perf_counter()
    for k in range(1, n + 1):
        bst.insert(k, f"s{k}", k)
    elapsed = time.perf_counter() - start
    h = bst.height()
    return elapsed, h


def _bench_avl_sorted(n):
    """Insert n sorted keys into AVL, return (insert_time, height)."""
    from avl_expression import AVLTree
    avl = AVLTree()
    start = time.perf_counter()
    for k in range(1, n + 1):
        avl.insert(k, f"c{k}")
    elapsed = time.perf_counter() - start
    h = avl.height()
    return elapsed, h


def _bench_bst_random(n, seed=42):
    """Insert n random keys into BST, return (insert_time, height)."""
    from trees import SupplyBST
    rng = random.Random(seed)
    keys = rng.sample(range(1, n * 10), n)
    bst = SupplyBST()
    start = time.perf_counter()
    for k in keys:
        bst.insert(k, f"s{k}", k)
    elapsed = time.perf_counter() - start
    h = bst.height()
    return elapsed, h


def _bench_avl_random(n, seed=42):
    """Insert n random keys into AVL, return (insert_time, height)."""
    from avl_expression import AVLTree
    rng = random.Random(seed)
    keys = rng.sample(range(1, n * 10), n)
    avl = AVLTree()
    start = time.perf_counter()
    for k in keys:
        avl.insert(k, f"c{k}")
    elapsed = time.perf_counter() - start
    h = avl.height()
    return elapsed, h


def run_tree_benchmarks(sizes=None, seed=42,
                        repetitions=DEFAULT_REPETITIONS):
    """BST vs AVL for requested sizes using a reproducible random seed."""
    if sizes is None:
        sizes = [1000, 5000, 20000]
    if repetitions < 1:
        raise ValueError("repetitions must be at least 1.")
    rows = []
    print("\n--- Tree Benchmarks: BST vs AVL ---")
    print(f"Average timings over {repetitions} repetitions; "
          "setup for deletion is excluded from deletion time.")
    print(f"{'n':>7} {'Type':>8} {'Input':>8} {'Insert avg (s)':>15} "
          f"{'Search avg (s)':>15} {'Delete avg (s)':>15} {'Height':>8}")
    print("-" * 85)
    for n in sizes:
        if n < 1:
            raise ValueError("Tree sizes must be positive.")
        sorted_keys = list(range(1, n + 1))
        random_keys = random.Random(seed).sample(range(1, n * 10 + 1), n)
        for input_order, keys in (
                ("sorted", sorted_keys), ("random", random_keys)):
            for structure in ("BST", "AVL"):
                row = _measure_tree_case(
                    n, structure, input_order, keys, repetitions, seed)
                print(f"{n:>7} {structure:>8} {input_order:>8} "
                      f"{row['insert_avg_s']:>15.6f} "
                      f"{row['search_avg_s']:>15.6f} "
                      f"{row['delete_avg_s']:>15.6f} "
                      f"{row['height_after_insert_avg']:>8.1f}")
                rows.append(row)
    return rows


# ============================================================================
# GRAPH BENCHMARKS — Prim vs Kruskal
# ============================================================================

def _build_random_graph(V, E, seed=42):
    """Build a connected random graph with exactly V vertices and E edges."""
    from graph import Graph
    max_edges = V * (V - 1) // 2
    if V < 1 or E < max(0, V - 1) or E > max_edges:
        raise ValueError(
            f"Cannot build a connected simple graph with V={V}, E={E}.")
    rng = random.Random(seed)
    g = Graph(directed=False)
    for i in range(V):
        g.add_vertex(f"v{i}")

    # First, ensure connectivity with a spanning tree.
    vertices = list(range(V))
    rng.shuffle(vertices)
    edge_set = set()
    for i in range(1, V):
        u, v = vertices[i - 1], vertices[i]
        w = rng.randint(1, 100)
        key = (min(u, v), max(u, v))
        if key not in edge_set:
            edge_set.add(key)
            g.add_edge(f"v{u}", f"v{v}", w)

    # Add remaining edges.
    attempts = 0
    max_attempts = max(E * 10, V * 100)
    while len(edge_set) < E and attempts < max_attempts:
        u = rng.randint(0, V - 1)
        v = rng.randint(0, V - 1)
        if u != v:
            key = (min(u, v), max(u, v))
            if key not in edge_set:
                edge_set.add(key)
                w = rng.randint(1, 100)
                g.add_edge(f"v{u}", f"v{v}", w)
        attempts += 1

    if len(edge_set) != E:
        raise RuntimeError(
            f"Generated {len(edge_set)} of {E} requested graph edges.")
    return g


def _graph_container_bytes(graph):
    """Approximate shallow Python container sizes (not a full heap profile)."""
    size = sys.getsizeof(graph.vertices) + sys.getsizeof(graph._index)
    size += sys.getsizeof(graph.adj_list) + sys.getsizeof(graph._edge_set)
    size += sys.getsizeof(graph.adj_matrix)
    size += sum(sys.getsizeof(neighbours)
                for neighbours in graph.adj_list.values())
    size += sum(sys.getsizeof(row) for row in graph.adj_matrix)
    return size


def _mst_samples(algorithm, graph, repetitions):
    samples = []
    costs = []
    for _ in range(repetitions):
        started = time.perf_counter()
        _, cost, components = algorithm(graph)
        samples.append(time.perf_counter() - started)
        if len(components) != 1:
            raise RuntimeError("The generated benchmark graph is disconnected.")
        costs.append(cost)
    return samples, costs


def run_graph_benchmarks(vertex_sizes=None, seed=42,
                         repetitions=DEFAULT_REPETITIONS):
    """Prim vs Kruskal on sparse and dense graphs for requested sizes."""
    from mst import prim_mst, kruskal_mst

    if vertex_sizes is None:
        vertex_sizes = [200, 1000, 2000]
    if repetitions < 1:
        raise ValueError("repetitions must be at least 1.")
    configs = []
    for V in vertex_sizes:
        if V < 5:
            raise ValueError("Graph benchmark sizes must be at least 5.")
        E_sparse = 2 * V
        E_dense = V * V // 4
        configs.append((V, E_sparse, "sparse"))
        configs.append((V, E_dense, "dense"))

    rows = []
    print("\n--- Graph Benchmarks: Prim vs Kruskal ---")
    print(f"Average algorithm timings over {repetitions} repetitions; "
          "graph setup excluded.")
    print(f"{'V':>6} {'E':>9} {'Type':>8} {'Prim avg (s)':>14} "
          f"{'Kruskal avg (s)':>16} {'MST cost':>12} {'Density':>10}")
    print("-" * 85)

    for V, E, gtype in configs:
        setup_started = time.perf_counter()
        g = _build_random_graph(V, E, seed=seed)
        setup_s = time.perf_counter() - setup_started
        actual_E = g.edge_count()
        if actual_E != E:
            raise RuntimeError(
                f"Expected {E} edges but generated {actual_E}.")
        memory_bytes = _graph_container_bytes(g)
        prim_samples, prim_costs = _mst_samples(prim_mst, g, repetitions)
        kruskal_samples, kruskal_costs = _mst_samples(
            kruskal_mst, g, repetitions)
        if prim_costs != kruskal_costs:
            raise RuntimeError(
                f"Prim and Kruskal costs differ for V={V}, E={E}.")
        prim_stats = _statistics(prim_samples)
        kruskal_stats = _statistics(kruskal_samples)
        mst_cost = prim_costs[0]
        possible_edges = V * (V - 1) // 2
        density = actual_E / possible_edges
        row = {
            "vertices": V,
            "edges": actual_E,
            "graph_type": gtype,
            "density": density,
            "setup_s": setup_s,
            "memory_bytes_shallow": memory_bytes,
            "prim_avg_s": prim_stats["avg"],
            "prim_min_s": prim_stats["min"],
            "prim_max_s": prim_stats["max"],
            "kruskal_avg_s": kruskal_stats["avg"],
            "kruskal_min_s": kruskal_stats["min"],
            "kruskal_max_s": kruskal_stats["max"],
            "mst_cost_prim": mst_cost,
            "mst_cost_kruskal": mst_cost,
            "costs_match": True,
            "seed": seed,
            "repetitions": repetitions,
        }
        print(f"{V:>6} {actual_E:>9} {gtype:>8} "
              f"{row['prim_avg_s']:>14.6f} "
              f"{row['kruskal_avg_s']:>16.6f} "
              f"{mst_cost:>12} {density:>10.6f}")
        rows.append(row)

    return rows


# ============================================================================
# SAVE RESULTS
# ============================================================================

TREE_FIELDS = [
    "n", "structure", "input_order",
    "insert_avg_s", "insert_min_s", "insert_max_s",
    "search_avg_s", "search_min_s", "search_max_s",
    "delete_avg_s", "delete_min_s", "delete_max_s",
    "delete_setup_avg_s", "delete_setup_min_s", "delete_setup_max_s",
    "height_after_insert_avg", "height_after_insert_min",
    "height_after_insert_max", "avl_verified", "seed", "repetitions",
]
GRAPH_FIELDS = [
    "vertices", "edges", "graph_type", "density", "setup_s",
    "memory_bytes_shallow", "prim_avg_s", "prim_min_s", "prim_max_s",
    "kruskal_avg_s", "kruskal_min_s", "kruskal_max_s",
    "mst_cost_prim", "mst_cost_kruskal", "costs_match", "seed",
    "repetitions",
]


def _write_csv(path, rows, fields):
    with open(path, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def save_benchmark_results(tree_rows, graph_rows, seed=42, output_dir=None):
    """Write measured benchmark data; a supplied directory gets audit names."""
    directory = RESULTS_DIR if output_dir is None else output_dir
    _ensure_results_dir(directory)
    if output_dir is None:
        combined_path = os.path.join(directory, "benchmark_results.csv")
        with open(combined_path, "w", newline="", encoding="utf-8") as file:
            fields = ["category"] + TREE_FIELDS + GRAPH_FIELDS
            writer = csv.DictWriter(file, fieldnames=fields)
            writer.writeheader()
            writer.writerows(
                {"category": "tree", **row} for row in tree_rows)
            writer.writerows(
                {"category": "graph", **row} for row in graph_rows)
        print(f"\nBenchmark CSV saved to: {combined_path}")
    else:
        tree_path = os.path.join(directory, "tree_benchmark_results.csv")
        graph_path = os.path.join(directory, "graph_benchmark_results.csv")
        _write_csv(tree_path, tree_rows, TREE_FIELDS)
        _write_csv(graph_path, graph_rows, GRAPH_FIELDS)
        print(f"\nTree benchmark CSV saved to: {tree_path}")
        print(f"Graph benchmark CSV saved to: {graph_path}")

    md_path = os.path.join(directory, "benchmark_summary.md")
    repetitions = sorted({
        row["repetitions"] for row in tree_rows + graph_rows
    })
    with open(md_path, "w", encoding="utf-8") as file:
        file.write("# Benchmark Summary\n\n")
        file.write(f"Workloads use deterministic seed {seed}. "
                   f"Repetitions per configuration: "
                   f"{', '.join(map(str, repetitions))}. Displayed "
                   "algorithm times are arithmetic means of actual "
                   "`time.perf_counter()` measurements; setup is excluded "
                   "from algorithm timings. Results vary by machine and "
                   "system load.\n\n")
        file.write("## Tree Benchmarks: BST vs AVL\n\n")
        file.write("| n | Structure | Input order | Insert avg (s) | "
                   "Search avg (s) | Delete avg (s) | Height after insert |\n")
        file.write("|---:|---|---|---:|---:|---:|---:|\n")
        for row in tree_rows:
            file.write(
                f"| {row['n']} | {row['structure']} | "
                f"{row['input_order']} | {row['insert_avg_s']:.9f} | "
                f"{row['search_avg_s']:.9f} | {row['delete_avg_s']:.9f} | "
                f"{row['height_after_insert_avg']:.1f} |\n")
        file.write("\n## Graph Benchmarks: Prim vs Kruskal\n\n")
        file.write("| V | E | Type | Density | Setup (s) | Prim avg (s) | "
                   "Kruskal avg (s) | MST cost | Shallow graph bytes |\n")
        file.write("|---:|---:|---|---:|---:|---:|---:|---:|---:|\n")
        for row in graph_rows:
            file.write(
                f"| {row['vertices']} | {row['edges']} | "
                f"{row['graph_type']} | {row['density']:.6f} | "
                f"{row['setup_s']:.6f} | {row['prim_avg_s']:.9f} | "
                f"{row['kruskal_avg_s']:.9f} | "
                f"{row['mst_cost_prim']} | "
                f"{row['memory_bytes_shallow']} |\n")
        file.write("\nGraph memory is a shallow `sys.getsizeof` estimate of "
                   "the project's graph containers; it excludes referenced "
                   "vertex, edge, tuple, and numeric objects, plus transient "
                   "algorithm allocations.\n\n")
        file.write("### Observations\n\n")
        file.write("- Sorted input shows how an unbalanced BST can degenerate; "
                   "AVL measurements are accompanied by invariant checks.\n")
        file.write("- Benchmark graphs are generated as connected graphs with "
                   "exactly the requested edge count.\n")
        file.write("- Prim and Kruskal costs were checked on every repetition.\n")
    print(f"Benchmark summary saved to: {md_path}")


def run_final_audit_benchmarks(repetitions=DEFAULT_REPETITIONS, seed=42):
    """Run and save the full required benchmark sizes to the audit folder."""
    tree_rows = run_tree_benchmarks(
        [1000, 5000, 20000], seed=seed, repetitions=repetitions)
    graph_rows = run_graph_benchmarks(
        [200, 1000, 2000], seed=seed, repetitions=repetitions)
    save_benchmark_results(
        tree_rows, graph_rows, seed=seed, output_dir=FINAL_AUDIT_DIR)
    return tree_rows, graph_rows


# ============================================================================
# Console menu
# ============================================================================

def analysis_menu():
    """Interactive analysis and benchmarking menu."""
    while True:
        print("\n--- ALGORITHM ANALYSIS AND BENCHMARKS ---")
        print("1. Run tree benchmarks (BST vs AVL)")
        print("2. Run graph benchmarks (Prim vs Kruskal)")
        print("3. Run all benchmarks and save results")
        print("4. Complexity notes")
        print("0. Return to main menu")
        choice = input("Choose an analysis action (enter the displayed number): ").strip()

        try:
            if choice == "1":
                run_tree_benchmarks()
            elif choice == "2":
                run_graph_benchmarks()
            elif choice == "3":
                print("Running all benchmarks (this may take a while)...")
                tree_rows = run_tree_benchmarks()
                graph_rows = run_graph_benchmarks()
                save_benchmark_results(tree_rows, graph_rows, seed=42)
            elif choice == "4":
                _print_complexity_notes()
            elif choice == "0":
                break
            else:
                print("Invalid option.")
        except Exception as exc:
            print("Error:", exc)
            import traceback
            traceback.print_exc()


def _print_complexity_notes():
    """Print complexity analysis summary."""
    print("""
=== COMPLEXITY ANALYSIS SUMMARY ===

1. BFS (adjacency list): O(V + E)
   - Each vertex enqueued/dequeued once: O(V).
   - Each adjacency list scanned once: total O(E) across all vertices.

2. Array-based Dijkstra: O(V² + E) ≈ O(V²)
   - V iterations, each scanning V vertices to find minimum: O(V²).
   - Relaxation of all edges: O(E). Since E ≤ V², overall O(V²).
   - Design technique: Greedy.
   - Correctness: At each step, the vertex with minimum tentative
     distance is finalised. This is correct when all weights are
     non-negative (greedy-choice property).
   - Fails with negative weights: a finalised vertex might be
     reachable via a shorter path through a later negative edge.

3. Array-based Prim: O(V²)
   - V iterations, each scanning V vertices to find minimum key: O(V²).
   - Edge relaxation: O(E). Since E ≤ V², overall O(V²).
   - Correctness: Cut property — the lightest edge crossing any cut
     is in some MST.

4. Kruskal: O(E log E)
   - Edge sorting (merge sort): O(E log E).
   - Union-Find operations: nearly O(E α(V)) ≈ O(E).
   - Correctness: Each selected lightest edge crossing the current
     component cut is safe by the cut property.

5. BST insertion: O(h) per operation.
   - Best case: balanced tree, h = O(log n).
   - Worst case: sorted input, h = O(n).
   - Average case (random): h = O(log n).
   - Recurrence: T(n) = T(n/2) + O(1) → O(log n) best/average.

6. AVL insertion: O(log n) per operation.
   - Height h = O(log n) guaranteed.
   - N(h) = N(h-1) + N(h-2) + 1 ≥ 2·N(h-2)
     → N(h) ≥ 2^(h/2) → h ≤ 2·log₂(n) = O(log n).

7. Tree traversal: T(n) = T(k) + T(n-1-k) + O(1) → O(n).
   Each node visited exactly once.

=== UNION-FIND AMORTIZED ANALYSIS ===

With path compression and union by rank:
- A sequence of m operations on n elements: O(m · α(n))
  where α is the inverse Ackermann function.
- α(n) ≤ 4 for all practical n, so effectively O(m).

=== COMPARISON-BASED SORTING LOWER BOUND ===

Any comparison-based sort requires Ω(n log n) comparisons in the
worst case. This applies to the edge sort in Kruskal's algorithm:
Ω(E log E) is a lower bound. Since log E = O(log V²) = O(log V),
this is also Ω(E log V).
""")
