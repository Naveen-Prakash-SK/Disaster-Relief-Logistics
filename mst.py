"""Minimum Spanning Tree / Forest: Prim (array-based) and Kruskal.

- Prim: O(V²) array scan, no heap.
- Kruskal: manual merge-sort for edges, union-find with path compression
  and union by rank.
- Handles disconnected graphs → minimum spanning forest.
- No heapq. No built-in sort for the required edge-sort step.
"""

INF = float('inf')


# ============================================================================
# DISJOINT-SET (Union-Find) — path compression + union by rank
# ============================================================================

class DisjointSet:
    """Union-Find with path compression and union by rank."""

    def __init__(self, items):
        self.parent = {item: item for item in items}
        self.rank = {item: 0 for item in items}

    def find(self, item):
        """Find with path compression."""
        root = item
        while self.parent[root] != root:
            root = self.parent[root]
        # Path compression
        while self.parent[item] != root:
            next_item = self.parent[item]
            self.parent[item] = root
            item = next_item
        return root

    def union(self, a, b):
        """Union by rank. Returns True if a merge happened."""
        root_a = self.find(a)
        root_b = self.find(b)
        if root_a == root_b:
            return False
        if self.rank[root_a] < self.rank[root_b]:
            root_a, root_b = root_b, root_a
        self.parent[root_b] = root_a
        if self.rank[root_a] == self.rank[root_b]:
            self.rank[root_a] += 1
        return True


# ============================================================================
# MANUAL MERGE SORT for edges — O(E log E)
# ============================================================================

def merge_sort_edges(edges):
    """Sort a list of (u, v, weight) tuples by weight using merge sort.
    This is the manual sorting implementation required by the assignment.
    Ties broken by (u, v) for determinism.
    """
    if len(edges) <= 1:
        return list(edges)

    mid = len(edges) // 2
    left = merge_sort_edges(edges[:mid])
    right = merge_sort_edges(edges[mid:])

    merged = []
    i = j = 0
    while i < len(left) and j < len(right):
        # Compare by weight, then by (u, v) for stability.
        lw = (left[i][2], str(left[i][0]), str(left[i][1]))
        rw = (right[j][2], str(right[j][0]), str(right[j][1]))
        if lw <= rw:
            merged.append(left[i])
            i += 1
        else:
            merged.append(right[j])
            j += 1
    merged.extend(left[i:])
    merged.extend(right[j:])
    return merged


# ============================================================================
# PRIM'S ALGORITHM — array-based, O(V²)
# ============================================================================

def prim_mst(graph, start=None):
    """Array-based Prim. No heap / priority queue.

    Returns (mst_edges, total_cost, components).
    mst_edges: list of (u, v, weight)
    components: list of lists of vertices in each tree of the forest.

    For disconnected graphs, runs Prim from each unvisited component.
    """
    vertices = graph.vertices
    if not vertices:
        return [], 0, []

    in_mst = {v: False for v in vertices}
    key = {v: INF for v in vertices}
    parent = {v: None for v in vertices}
    parent_weight = {v: 0 for v in vertices}

    mst_edges = []
    total_cost = 0
    components = []

    # Process all components (handles disconnected graphs).
    for start_vertex in vertices:
        if in_mst[start_vertex]:
            continue

        # Initialise this component's Prim run.
        comp_vertices = []
        key[start_vertex] = 0
        if start is not None and not in_mst[start]:
            key[start] = 0
            start_vertex = start
            start = None  # only use the hint once

        for _ in range(len(vertices)):
            # Array scan: pick the unvisited vertex with minimum key.
            u = None
            for v in vertices:
                if not in_mst[v]:
                    if u is None or key[v] < key[u]:
                        u = v
            if u is None or key[u] == INF:
                break
            in_mst[u] = True
            comp_vertices.append(u)

            if parent[u] is not None:
                mst_edges.append((parent[u], u, parent_weight[u]))
                total_cost += parent_weight[u]

            # Update keys of adjacent vertices.
            for v, w in graph.adj_list[u].items():
                if not in_mst[v] and w < key[v]:
                    key[v] = w
                    parent[v] = u
                    parent_weight[v] = w

        if comp_vertices:
            components.append(comp_vertices)

    return mst_edges, total_cost, components


# ============================================================================
# KRUSKAL'S ALGORITHM — merge-sort + union-find
# ============================================================================

def kruskal_mst(graph):
    """Kruskal using manual merge sort and union-find.

    Returns (mst_edges, total_cost, components).
    """
    vertices = graph.vertices
    if not vertices:
        return [], 0, []

    edges = graph.all_edges()
    sorted_edges = merge_sort_edges(edges)

    ds = DisjointSet(vertices)
    mst_edges = []
    total_cost = 0

    for u, v, w in sorted_edges:
        if ds.union(u, v):
            mst_edges.append((u, v, w))
            total_cost += w

    # Determine components from the disjoint-set.
    comp_map = {}
    for v in vertices:
        root = ds.find(v)
        comp_map.setdefault(root, []).append(v)
    components = list(comp_map.values())

    return mst_edges, total_cost, components


# ============================================================================
# Console menu
# ============================================================================

def mst_menu():
    """Interactive MST menu."""
    from graph import build_sample_graph
    g, _, _ = build_sample_graph()

    while True:
        print("\n--- MINIMUM SPANNING TREE / FOREST ---")
        print("1. Run Prim's algorithm")
        print("2. Run Kruskal's algorithm")
        print("3. Compare Prim and Kruskal results")
        print("4. Display current graph edges")
        print("5. MST explanation")
        print("0. Return to main menu")
        choice = input("Choose an MST action (enter the displayed number): ").strip()

        try:
            if choice == "1":
                edges, cost, comps = prim_mst(g)
                print(f"\nPrim's MST — total cost: {cost}")
                print("Edges selected:")
                for u, v, w in edges:
                    print(f"  {u} -- {v}  (weight {w})")
                print(f"Components ({len(comps)}):")
                for i, c in enumerate(comps, 1):
                    print(f"  {i}: {', '.join(c)}")
            elif choice == "2":
                edges, cost, comps = kruskal_mst(g)
                print(f"\nKruskal's MST — total cost: {cost}")
                print("Edges selected:")
                for u, v, w in edges:
                    print(f"  {u} -- {v}  (weight {w})")
                print(f"Components ({len(comps)}):")
                for i, c in enumerate(comps, 1):
                    print(f"  {i}: {', '.join(c)}")
            elif choice == "3":
                pe, pc, _ = prim_mst(g)
                ke, kc, _ = kruskal_mst(g)
                print(f"Prim  total cost: {pc}  ({len(pe)} edges)")
                print(f"Kruskal total cost: {kc}  ({len(ke)} edges)")
                if pc == kc:
                    print("✓ Both algorithms agree on total MST cost.")
                else:
                    print("✗ Mismatch — investigate the graph.")
            elif choice == "4":
                edges = g.all_edges()
                print(f"Graph has {g.vertex_count()} vertices, "
                      f"{g.edge_count()} edges:")
                for u, v, w in edges:
                    print(f"  {u} -- {v}  (weight {w})")
            elif choice == "5":
                print("\nMST algorithms apply to undirected, weighted graphs.")
                print("Prim grows a single tree greedily (cut property).")
                print("Kruskal selects globally cheapest edges (cycle property).")
                print("For disconnected graphs, both produce a minimum")
                print("spanning forest — one tree per component.")
            elif choice == "0":
                break
            else:
                print("Invalid option.")
        except Exception as exc:
            print("Error:", exc)
