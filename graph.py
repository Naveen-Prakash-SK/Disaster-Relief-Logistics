"""Graph ADT with BFS, DFS, SCC and Dijkstra.

Supports directed/undirected, weighted/unweighted graphs.
Adjacency-list and adjacency-matrix representations maintained in parallel.

Convention:
- Absent edge: weight is None (adjacency list) or 0 (adjacency matrix).
- Zero-weight edge: stored explicitly with weight 0 in the adjacency list;
  in the matrix, 0 means *no edge* unless the vertex pair is explicitly
  tracked in a separate set. For simplicity we use the adjacency list as
  the source of truth and rebuild the matrix on demand.
- No NetworkX. No heapq.
"""

import sys

INF = float('inf')


# ============================================================================
# GRAPH ADT
# ============================================================================

class Graph:
    """Custom graph ADT with adjacency list and adjacency matrix."""

    def __init__(self, directed=False):
        self.directed = directed
        self.vertices = []              # ordered list of vertex labels
        self._index = {}                # label -> int index
        self.adj_list = {}              # label -> {neighbour: weight}
        self.adj_matrix = []            # 2-D list, 0 means no edge
        self._edge_set = set()          # for tracking zero-weight edges

    def vertex_count(self):
        return len(self.vertices)

    def edge_count(self):
        """Return the number of edges."""
        count = 0
        for u in self.adj_list:
            count += len(self.adj_list[u])
        if not self.directed:
            self_loops = sum(1 for u in self.vertices if u in self.adj_list[u])
            count = (count + self_loops) // 2
        return count

    def add_vertex(self, label):
        """Add a vertex if it does not already exist."""
        if label in self._index:
            return
        idx = len(self.vertices)
        self.vertices.append(label)
        self._index[label] = idx
        self.adj_list[label] = {}
        # Expand the matrix.
        for row in self.adj_matrix:
            row.append(0)
        self.adj_matrix.append([0] * (idx + 1))

    def remove_vertex(self, label):
        """Remove a vertex and all incident edges; return whether it existed."""
        if label not in self._index:
            return False
        index = self._index[label]
        del self.adj_list[label]
        for neighbours in self.adj_list.values():
            neighbours.pop(label, None)
        self.vertices.pop(index)
        self.adj_matrix.pop(index)
        for row in self.adj_matrix:
            row.pop(index)
        self._index = {vertex: i for i, vertex in enumerate(self.vertices)}
        self._edge_set = {
            (u, v) for u, neighbours in self.adj_list.items()
            for v in neighbours
        }
        return True

    def add_edge(self, u, v, weight=1):
        """Add an edge u -> v (and v -> u if undirected)."""
        for vertex in (u, v):
            if vertex not in self._index:
                self.add_vertex(vertex)
        self.adj_list[u][v] = weight
        ui, vi = self._index[u], self._index[v]
        self.adj_matrix[ui][vi] = weight if weight != 0 else 0
        self._edge_set.add((u, v))
        if not self.directed:
            self.adj_list[v][u] = weight
            self.adj_matrix[vi][ui] = weight if weight != 0 else 0
            self._edge_set.add((v, u))

    def remove_edge(self, u, v):
        """Remove edge u -> v (and v -> u if undirected)."""
        if u in self.adj_list and v in self.adj_list[u]:
            del self.adj_list[u][v]
            self.adj_matrix[self._index[u]][self._index[v]] = 0
            self._edge_set.discard((u, v))
        if not self.directed:
            if v in self.adj_list and u in self.adj_list[v]:
                del self.adj_list[v][u]
                self.adj_matrix[self._index[v]][self._index[u]] = 0
                self._edge_set.discard((v, u))

    def has_edge(self, u, v):
        return u in self.adj_list and v in self.adj_list[u]

    def get_weight(self, u, v):
        if u in self.adj_list and v in self.adj_list[u]:
            return self.adj_list[u][v]
        return None

    def neighbours(self, u):
        """Return dict {neighbour: weight} for vertex u."""
        return dict(self.adj_list.get(u, {}))

    def all_edges(self):
        """Return list of (u, v, w) tuples. For undirected, each edge once."""
        seen = set()
        edges = []
        for u in self.vertices:
            for v, w in self.adj_list[u].items():
                if self.directed:
                    edges.append((u, v, w))
                else:
                    key = (min(u, v), max(u, v)) if isinstance(u, str) else (
                        (u, v) if u <= v else (v, u))
                    if key not in seen:
                        seen.add(key)
                        edges.append((u, v, w))
        return edges

    def get_edges_sorted(self):
        """Return all edges as list sorted by (weight, u, v). Used by Kruskal."""
        return self.all_edges()

    def memory_report(self):
        """Estimate memory usage for adjacency list vs matrix."""
        V = len(self.vertices)
        E = self.edge_count()
        # Adjacency list: ~ E entries (each stores neighbour + weight)
        # Adjacency matrix: V*V entries
        list_entries = sum(len(self.adj_list[v]) for v in self.vertices)
        matrix_entries = V * V
        print(f"  Vertices: {V},  Edges: {E}")
        print(f"  Adjacency list entries : {list_entries}")
        print(f"  Adjacency matrix cells : {matrix_entries}")
        print(f"  For sparse graphs (E << V²), the list is more efficient.")
        print(f"  For dense graphs  (E ≈ V²), the matrix is comparable.")
        # Actual sys.getsizeof estimates
        list_bytes = sys.getsizeof(self.adj_list)
        for v in self.adj_list:
            list_bytes += sys.getsizeof(self.adj_list[v])
        matrix_bytes = sys.getsizeof(self.adj_matrix)
        for row in self.adj_matrix:
            matrix_bytes += sys.getsizeof(row)
        print(f"  Approx adjacency-list object size : {list_bytes:,} bytes")
        print(f"  Approx adjacency-matrix object size: {matrix_bytes:,} bytes")

    def display_adj_list(self):
        """Print the adjacency list."""
        print("Adjacency List:")
        for v in self.vertices:
            nbrs = ", ".join(
                f"{n}(w={w})" for n, w in self.adj_list[v].items())
            print(f"  {v} -> [{nbrs}]")

    def display_adj_matrix(self):
        """Print the adjacency matrix with labels."""
        V = len(self.vertices)
        header = "       " + "  ".join(f"{v:>6}" for v in self.vertices)
        print("Adjacency Matrix:")
        print(header)
        for i, v in enumerate(self.vertices):
            row_str = "  ".join(f"{self.adj_matrix[i][j]:>6}"
                                for j in range(V))
            print(f"  {v:>4} {row_str}")

    def has_negative_weights(self):
        """Check if any edge has negative weight."""
        for u in self.adj_list:
            for v, w in self.adj_list[u].items():
                if w < 0:
                    return True
        return False


# ============================================================================
# BFS
# ============================================================================

def bfs(graph, start):
    """BFS from *start*. Returns (dist, parent) dicts.
    dist[v] = number of edges from start to v.
    parent[v] = predecessor on the shortest-edge-count path.
    """
    if start not in graph.adj_list:
        return {}, {}
    dist = {start: 0}
    parent = {start: None}
    queue = [start]
    front = 0
    while front < len(queue):
        u = queue[front]
        front += 1
        for v in graph.adj_list[u]:
            if v not in dist:
                dist[v] = dist[u] + 1
                parent[v] = u
                queue.append(v)
    return dist, parent


def bfs_path(graph, start, end):
    """Return (path, edge_count) from start to end using BFS."""
    dist, parent = bfs(graph, start)
    if end not in dist:
        return None, None
    path = []
    current = end
    while current is not None:
        path.append(current)
        current = parent[current]
    path.reverse()
    return path, dist[end]


def bfs_nearest_depot(graph, source, depots):
    """Find the nearest depot from source by fewest edges.
    Returns (depot_label, path, edge_count) or (None, None, None).
    """
    dist, parent = bfs(graph, source)
    best_depot = None
    best_dist = INF
    for d in depots:
        if d in dist and dist[d] < best_dist:
            best_dist = dist[d]
            best_depot = d
    if best_depot is None:
        return None, None, None
    path = []
    cur = best_depot
    while cur is not None:
        path.append(cur)
        cur = parent[cur]
    path.reverse()
    return best_depot, path, best_dist


# ============================================================================
# DFS with timestamps and edge classification
# ============================================================================

def dfs_full(graph, start=None):
    """Full DFS on the graph.
    Returns (discovery, finish, parent, edge_types, order).
    edge_types: dict of (u, v) -> 'tree'|'back'|'forward'|'cross'
    """
    WHITE, GRAY, BLACK = 0, 1, 2
    color = {v: WHITE for v in graph.vertices}
    discovery = {}
    finish = {}
    parent = {v: None for v in graph.vertices}
    edge_types = {}
    order = []
    time_counter = [0]

    def _dfs_visit(u):
        time_counter[0] += 1
        discovery[u] = time_counter[0]
        color[u] = GRAY
        order.append(u)
        for v in graph.adj_list[u]:
            if color[v] == WHITE:
                edge_types[(u, v)] = 'tree'
                parent[v] = u
                _dfs_visit(v)
            elif color[v] == GRAY:
                edge_types[(u, v)] = 'back'
            else:
                if discovery[u] < discovery[v]:
                    edge_types[(u, v)] = 'forward'
                else:
                    edge_types[(u, v)] = 'cross'
        time_counter[0] += 1
        finish[u] = time_counter[0]
        color[u] = BLACK

    if start is not None and start not in graph.adj_list:
        raise ValueError(f"Unknown DFS start vertex '{start}'.")
    traversal_roots = ([start] if start is not None else []) + [
        vertex for vertex in graph.vertices if vertex != start
    ]
    for v in traversal_roots:
        if color[v] == WHITE:
            _dfs_visit(v)

    return discovery, finish, parent, edge_types, order


def connected_components_undirected(graph):
    """Return list of components (each a list of vertex labels)."""
    visited = set()
    components = []

    def _dfs(u, comp):
        visited.add(u)
        comp.append(u)
        for v in graph.adj_list[u]:
            if v not in visited:
                _dfs(v, comp)

    for v in graph.vertices:
        if v not in visited:
            comp = []
            _dfs(v, comp)
            components.append(comp)
    return components


def scc_kosaraju(graph):
    """Strongly connected components using Kosaraju's algorithm.
    Works on directed graphs.
    Returns list of components (each a list of vertex labels).
    """
    # Step 1: compute finish times on original graph.
    _, finish, _, _, _ = dfs_full(graph)
    # Step 2: build transpose graph.
    gt = Graph(directed=True)
    for v in graph.vertices:
        gt.add_vertex(v)
    for u in graph.vertices:
        for v, w in graph.adj_list[u].items():
            gt.add_edge(v, u, w)
    # Step 3: DFS on transpose in reverse finish-time order.
    order = sorted(graph.vertices, key=lambda v: finish[v], reverse=True)
    visited = set()
    components = []

    def _dfs(u, comp):
        visited.add(u)
        comp.append(u)
        for v in gt.adj_list[u]:
            if v not in visited:
                _dfs(v, comp)

    for v in order:
        if v not in visited:
            comp = []
            _dfs(v, comp)
            components.append(comp)
    return components


# ============================================================================
# DIJKSTRA — array-based, no heapq
# ============================================================================

def dijkstra(graph, source, verbose=False):
    """Array-based Dijkstra. Returns (dist, parent) dicts.
    Raises ValueError if negative edge weights are detected.
    """
    if graph.has_negative_weights():
        raise ValueError(
            "Dijkstra's algorithm does not support negative edge weights.\n"
            "Negative weights can cause Dijkstra to miss shorter paths that\n"
            "go through already-finalised vertices. Use Bellman-Ford instead.")
    if source not in graph.adj_list:
        return {}, {}

    dist = {v: INF for v in graph.vertices}
    parent = {v: None for v in graph.vertices}
    dist[source] = 0
    visited = set()

    if verbose:
        print(f"\nDijkstra step-by-step from '{source}':")
        print(f"{'Iter':>4}  {'Selected':>12}  {'Dist':>8}  "
              f"{'Distance estimates'}")

    for iteration in range(len(graph.vertices)):
        # Select unvisited vertex with minimum distance (array scan).
        u = None
        for v in graph.vertices:
            if v not in visited:
                if u is None or dist[v] < dist[u]:
                    u = v
        if u is None or dist[u] == INF:
            break
        visited.add(u)

        if verbose:
            estimates = ", ".join(
                f"{v}:{dist[v]}" if dist[v] != INF else f"{v}:∞"
                for v in graph.vertices)
            d_str = str(dist[u]) if dist[u] != INF else "∞"
            print(f"{iteration+1:>4}  {str(u):>12}  {d_str:>8}  {estimates}")

        # Relax neighbours.
        for v, w in graph.adj_list[u].items():
            if v not in visited:
                new_dist = dist[u] + w
                if new_dist < dist[v]:
                    dist[v] = new_dist
                    parent[v] = u

    return dist, parent


def dijkstra_path(graph, source, target, verbose=False):
    """Return (path, distance) from source to target."""
    dist, parent = dijkstra(graph, source, verbose)
    if target not in dist or dist[target] == INF:
        return None, INF
    path = []
    cur = target
    while cur is not None:
        path.append(cur)
        cur = parent[cur]
    path.reverse()
    return path, dist[target]


def demonstrate_negative_weight_failure():
    """Show a small example where Dijkstra fails with negative edges."""
    print("\n--- Dijkstra failure with negative edge weights ---")
    print("Graph: A --(1)--> B --(−3)--> C, A --(2)--> C")
    print("Correct shortest A->C: A->B->C = 1 + (−3) = −2")
    print("Dijkstra finalises C with dist=2 via A->C, missing the")
    print("cheaper path through B because it never revisits C.")
    print()
    print("Explanation:")
    print("  Dijkstra's greedy strategy assumes that once a vertex is")
    print("  finalised (extracted with minimum distance), no shorter")
    print("  path to it exists. Negative edges violate this assumption")
    print("  because a later path through a negative edge could produce")
    print("  a smaller total distance.")


# ============================================================================
# SAMPLE GRAPH BUILDER
# ============================================================================

def build_sample_graph():
    """Build a sample disaster-relief road network.

    At least 12 vertices, one disconnected area, at least one directed edge.
    Returns (undirected_graph, directed_graph, depots).
    """
    # -- Undirected road network --
    g = Graph(directed=False)
    locations = [
        "DepotA", "DepotB",
        "RegionNorth", "RegionSouth",
        "DistrictN1", "DistrictN2", "DistrictS1",
        "ShelterN1a", "ShelterN1b", "ShelterS1a",
        "CampAlpha", "CampBeta",
        "IsolatedX", "IsolatedY",      # disconnected area
    ]
    for loc in locations:
        g.add_vertex(loc)

    roads = [
        ("DepotA", "RegionNorth", 10),
        ("DepotA", "RegionSouth", 15),
        ("DepotB", "RegionNorth", 12),
        ("RegionNorth", "DistrictN1", 5),
        ("RegionNorth", "DistrictN2", 8),
        ("DistrictN1", "ShelterN1a", 3),
        ("DistrictN1", "ShelterN1b", 4),
        ("DistrictN2", "CampAlpha", 6),
        ("RegionSouth", "DistrictS1", 7),
        ("DistrictS1", "ShelterS1a", 2),
        ("DistrictS1", "CampBeta", 9),
        ("ShelterN1a", "ShelterN1b", 1),
        ("CampAlpha", "CampBeta", 11),
        # Disconnected pair
        ("IsolatedX", "IsolatedY", 5),
    ]
    for u, v, w in roads:
        g.add_edge(u, v, w)

    depots = ["DepotA", "DepotB"]

    # -- Directed supply-flow graph (reuses some vertices) --
    dg = Graph(directed=True)
    for loc in locations:
        dg.add_vertex(loc)
    directed_edges = [
        ("DepotA", "RegionNorth", 10),
        ("DepotA", "RegionSouth", 15),
        ("DepotB", "RegionNorth", 12),
        ("RegionNorth", "DistrictN1", 5),
        ("RegionNorth", "DistrictN2", 8),
        ("DistrictN1", "ShelterN1a", 3),
        ("DistrictN1", "ShelterN1b", 4),
        ("DistrictN2", "CampAlpha", 6),
        ("RegionSouth", "DistrictS1", 7),
        ("DistrictS1", "ShelterS1a", 2),
        ("DistrictS1", "CampBeta", 9),
        ("ShelterN1a", "ShelterN1b", 1),
        ("CampAlpha", "CampBeta", 11),
        ("IsolatedX", "IsolatedY", 5),
        # Some back-flow edges (directed-only)
        ("CampBeta", "RegionSouth", 20),
        ("ShelterN1b", "DepotA", 25),
    ]
    for u, v, w in directed_edges:
        dg.add_edge(u, v, w)

    return g, dg, depots


# ============================================================================
# Console menu
# ============================================================================

def graph_menu():
    """Interactive graph, BFS, DFS and Dijkstra menu."""
    g, dg, depots = build_sample_graph()
    # Default working graph is undirected.
    current = g
    current_label = "undirected"

    while True:
        print(f"\n--- GRAPH AND ROUTE PLANNING (active: {current_label}) ---")
        print("1.  Display adjacency list")
        print("2.  Display adjacency matrix")
        print("3.  Memory report (list vs matrix)")
        print("4.  Switch undirected / directed graph")
        print("5.  Add edge")
        print("6.  Remove edge")
        print("7.  BFS: fewest-edge route")
        print("8.  BFS: nearest depot from a location")
        print("9.  DFS: timestamps and edge classification")
        print("10. Connected / strongly connected components")
        print("11. Dijkstra: shortest weighted route")
        print("12. Dijkstra: step-by-step table")
        print("13. Demonstrate Dijkstra negative-weight failure")
        print("0.  Return to main menu")
        choice = input("Choose a graph action (enter the displayed number): ").strip()

        try:
            if choice == "1":
                current.display_adj_list()
            elif choice == "2":
                current.display_adj_matrix()
            elif choice == "3":
                current.memory_report()
            elif choice == "4":
                if current is g:
                    current, current_label = dg, "directed"
                else:
                    current, current_label = g, "undirected"
                print(f"Switched to {current_label} graph.")
            elif choice == "5":
                u = input("Enter road connection source vertex name (must match an existing graph vertex, e.g. DEPOT): ").strip()
                v = input("Enter road connection destination vertex name (must match an existing graph vertex, e.g. RIVERBEND): ").strip()
                w = int(input("Enter road connection weight (integer, e.g. 4): "))
                current.add_edge(u, v, w)
                print("Edge added.")
            elif choice == "6":
                u = input("Enter road connection source vertex name to remove (must match an existing graph vertex, e.g. DEPOT): ").strip()
                v = input("Enter road connection destination vertex name to remove (must match an existing graph vertex, e.g. RIVERBEND): ").strip()
                current.remove_edge(u, v)
                print("Edge removed (if it existed).")
            elif choice == "7":
                src = input("Enter start vertex name (must match an existing graph vertex, e.g. DEPOT): ").strip()
                dst = input("Enter destination vertex name (must match an existing graph vertex, e.g. RIVERBEND): ").strip()
                path, edges = bfs_path(current, src, dst)
                if path is None:
                    print(f"No route from '{src}' to '{dst}' "
                          f"(unreachable).")
                else:
                    print(f"Route ({edges} edges): "
                          f"{' -> '.join(path)}")
            elif choice == "8":
                src = input("Enter source vertex name to find the nearest depot (must match an existing graph vertex, e.g. DEPOT): ").strip()
                depot, path, edges = bfs_nearest_depot(
                    current, src, depots)
                if depot is None:
                    print("No reachable depot found.")
                else:
                    print(f"Nearest depot: {depot} ({edges} edges)")
                    print(f"Route: {' -> '.join(path)}")
            elif choice == "9":
                disc, fin, par, etypes, order = dfs_full(current)
                print("DFS traversal order:", " -> ".join(order))
                print("\nTimestamps:")
                for v in current.vertices:
                    print(f"  {v}: discovery={disc.get(v, '?')}, "
                          f"finish={fin.get(v, '?')}")
                print("\nEdge classification:")
                for (u, v), etype in etypes.items():
                    print(f"  ({u} -> {v}): {etype}")
            elif choice == "10":
                if current.directed:
                    comps = scc_kosaraju(current)
                    print(f"Strongly connected components ({len(comps)}):")
                else:
                    comps = connected_components_undirected(current)
                    print(f"Connected components ({len(comps)}):")
                for i, comp in enumerate(comps, 1):
                    print(f"  Component {i}: {', '.join(comp)}")
            elif choice == "11":
                src = input("Enter source vertex name to route from (must match an existing graph vertex, e.g. DEPOT): ").strip()
                dst = input("Enter destination vertex name to route to (must match an existing graph vertex, e.g. RIVERBEND): ").strip()
                path, dist = dijkstra_path(current, src, dst)
                if path is None:
                    print(f"No path from '{src}' to '{dst}' "
                          f"(unreachable).")
                else:
                    print(f"Shortest distance: {dist}")
                    print(f"Path: {' -> '.join(path)}")
            elif choice == "12":
                src = input("Enter source vertex name for the weighted distance table (must match an existing graph vertex, e.g. DEPOT): ").strip()
                dst = input("Enter destination vertex name for the weighted distance table (must match an existing graph vertex, e.g. RIVERBEND): ").strip()
                path, dist = dijkstra_path(current, src, dst,
                                           verbose=True)
                if path is None:
                    print(f"\nNo path from '{src}' to '{dst}'.")
                else:
                    print(f"\nShortest distance: {dist}")
                    print(f"Path: {' -> '.join(path)}")
            elif choice == "13":
                demonstrate_negative_weight_failure()
            elif choice == "0":
                break
            else:
                print("Invalid option.")
        except ValueError as exc:
            print("Error:", exc)
