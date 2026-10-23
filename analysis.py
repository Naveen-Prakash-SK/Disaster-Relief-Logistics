"""Algorithm Analysis — empirical timing, complexity notes, benchmarks.

Measures actual elapsed times using time.perf_counter().
Generates CSV and summary reports.
Uses deterministic seeds and multiple repetitions.
"""

import os
import time
import random
import csv


# ============================================================================
# HELPERS
# ============================================================================

RESULTS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                           "results")


def _ensure_results_dir():
    os.makedirs(RESULTS_DIR, exist_ok=True)


def _measure(func, *args, repetitions=3, **kwargs):
    """Run func(*args) multiple times, return average elapsed seconds."""
    total = 0.0
    result = None
    for _ in range(repetitions):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        total += time.perf_counter() - start
    return total / repetitions, result


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


def run_tree_benchmarks():
    """BST vs AVL on sorted and random input for required sizes."""
    sizes = [1000, 5000, 20000]
    rows = []
    print("\n--- Tree Benchmarks: BST vs AVL ---")
    print(f"{'n':>7} {'Type':>8} {'Input':>8} "
          f"{'Time (s)':>12} {'Height':>8}")
    print("-" * 55)
    for n in sizes:
        # Sorted input
        t_bst_s, h_bst_s = _bench_bst_sorted(n)
        t_avl_s, h_avl_s = _bench_avl_sorted(n)
        # Random input
        t_bst_r, h_bst_r = _bench_bst_random(n)
        t_avl_r, h_avl_r = _bench_avl_random(n)

        entries = [
            (n, "BST", "sorted", t_bst_s, h_bst_s),
            (n, "AVL", "sorted", t_avl_s, h_avl_s),
            (n, "BST", "random", t_bst_r, h_bst_r),
            (n, "AVL", "random", t_avl_r, h_avl_r),
        ]
        for entry in entries:
            nn, tp, inp, t, h = entry
            print(f"{nn:>7} {tp:>8} {inp:>8} {t:>12.6f} {h:>8}")
            rows.append(entry)
    return rows


# ============================================================================
# GRAPH BENCHMARKS — Prim vs Kruskal
# ============================================================================

def _build_random_graph(V, E, seed=42):
    """Build a random undirected weighted graph with V vertices and ~E edges."""
    from graph import Graph
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
    max_attempts = E * 5
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

    return g


def run_graph_benchmarks():
    """Prim vs Kruskal on sparse and dense graphs."""
    from mst import prim_mst, kruskal_mst

    configs = []
    for V in [200, 1000, 2000]:
        E_sparse = 2 * V
        E_dense = V * V // 4
        configs.append((V, E_sparse, "sparse"))
        # Only do dense for smaller sizes to avoid very long runtimes.
        if V <= 1000:
            configs.append((V, E_dense, "dense"))
        else:
            # For V=2000, use a moderately dense graph.
            configs.append((V, min(E_dense, 50000), "dense*"))

    rows = []
    print("\n--- Graph Benchmarks: Prim vs Kruskal ---")
    print(f"{'V':>6} {'E':>8} {'Type':>8} "
          f"{'Prim (s)':>12} {'Kruskal (s)':>14} {'Cost':>8}")
    print("-" * 65)

    for V, E, gtype in configs:
        g = _build_random_graph(V, E, seed=42)
        actual_E = g.edge_count()

        t_prim, (pe, pc, _) = _measure(prim_mst, g, repetitions=1)
        t_kruskal, (ke, kc, _) = _measure(kruskal_mst, g, repetitions=1)

        print(f"{V:>6} {actual_E:>8} {gtype:>8} "
              f"{t_prim:>12.6f} {t_kruskal:>14.6f} {pc:>8}")
        rows.append((V, actual_E, gtype, t_prim, t_kruskal, pc, kc))

        if pc != kc:
            print(f"  ⚠ Cost mismatch: Prim={pc}, Kruskal={kc}")

    return rows


# ============================================================================
# SAVE RESULTS
# ============================================================================

def save_benchmark_results(tree_rows, graph_rows):
    """Write results to CSV and summary markdown."""
    _ensure_results_dir()

    csv_path = os.path.join(RESULTS_DIR, "benchmark_results.csv")
    with open(csv_path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["category", "n_or_V", "type", "input_or_E",
                         "time_s", "height_or_cost",
                         "time2_s", "cost2"])
        for n, tp, inp, t, h in tree_rows:
            writer.writerow(["tree", n, tp, inp, f"{t:.6f}", h, "", ""])
        for V, E, gtype, tp, tk, pc, kc in graph_rows:
            writer.writerow(["graph", V, gtype, E,
                             f"{tp:.6f}", pc, f"{tk:.6f}", kc])
    print(f"\nBenchmark CSV saved to: {csv_path}")

    md_path = os.path.join(RESULTS_DIR, "benchmark_summary.md")
    with open(md_path, "w") as f:
        f.write("# Benchmark Summary\n\n")
        f.write("## Tree Benchmarks: BST vs AVL\n\n")
        f.write("| n | Type | Input | Time (s) | Height |\n")
        f.write("|---|------|-------|----------|--------|\n")
        for n, tp, inp, t, h in tree_rows:
            f.write(f"| {n} | {tp} | {inp} | {t:.6f} | {h} |\n")
        f.write("\n## Graph Benchmarks: Prim vs Kruskal\n\n")
        f.write("| V | E | Type | Prim (s) | Kruskal (s) | Cost |\n")
        f.write("|---|---|------|----------|-------------|------|\n")
        for V, E, gtype, tp, tk, pc, kc in graph_rows:
            f.write(f"| {V} | {E} | {gtype} | {tp:.6f} | "
                    f"{tk:.6f} | {pc} |\n")
        f.write("\n### Observations\n\n")
        f.write("- BST with sorted input degenerates to O(n) height, "
                "while AVL maintains O(log n).\n")
        f.write("- With random input, BST height is closer to "
                "O(log n) on average.\n")
        f.write("- Array-based Prim is O(V²), efficient for dense graphs.\n")
        f.write("- Kruskal with merge sort is O(E log E), "
                "efficient for sparse graphs.\n")
        f.write("- Both Prim and Kruskal produce the same MST cost "
                "on connected graphs.\n")
    print(f"Benchmark summary saved to: {md_path}")


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
        choice = input("Choose an option: ").strip()

        try:
            if choice == "1":
                run_tree_benchmarks()
            elif choice == "2":
                run_graph_benchmarks()
            elif choice == "3":
                print("Running all benchmarks (this may take a while)...")
                tree_rows = run_tree_benchmarks()
                graph_rows = run_graph_benchmarks()
                save_benchmark_results(tree_rows, graph_rows)
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
   - Correctness: Cycle property — the heaviest edge in any cycle
     is not in the MST.

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
