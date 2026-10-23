# Pseudocode — Required Algorithms

## 1. AVL Deletion with Rebalancing

```
FUNCTION AVL-DELETE(node, key):
    IF node IS NULL:
        RETURN (NULL, False)
    
    IF key < node.key:
        node.left, deleted ← AVL-DELETE(node.left, key)
    ELSE IF key > node.key:
        node.right, deleted ← AVL-DELETE(node.right, key)
    ELSE:
        deleted ← True
        IF node.left IS NULL:
            RETURN (node.right, True)
        IF node.right IS NULL:
            RETURN (node.left, True)
        // Two children: replace with inorder successor
        successor ← MINIMUM(node.right)
        node.key ← successor.key
        node.value ← successor.value
        node.right, _ ← AVL-DELETE(node.right, successor.key)
    
    RETURN (REBALANCE(node), deleted)

FUNCTION REBALANCE(node):
    UPDATE-HEIGHT(node)
    bf ← BALANCE-FACTOR(node)   // height(left) - height(right)
    
    IF bf > 1:
        IF BALANCE-FACTOR(node.left) < 0:
            // LR case
            node.left ← ROTATE-LEFT(node.left)
        RETURN ROTATE-RIGHT(node)        // LL case
    
    IF bf < -1:
        IF BALANCE-FACTOR(node.right) > 0:
            // RL case
            node.right ← ROTATE-RIGHT(node.right)
        RETURN ROTATE-LEFT(node)         // RR case
    
    RETURN node

FUNCTION ROTATE-RIGHT(z):
    y ← z.left
    t3 ← y.right
    y.right ← z
    z.left ← t3
    UPDATE-HEIGHT(z)
    UPDATE-HEIGHT(y)
    RETURN y

FUNCTION ROTATE-LEFT(z):
    y ← z.right
    t2 ← y.left
    y.left ← z
    z.right ← t2
    UPDATE-HEIGHT(z)
    UPDATE-HEIGHT(y)
    RETURN y
```

---

## 2. Array-Based Dijkstra

```
FUNCTION DIJKSTRA(graph, source):
    // Precondition: all edge weights ≥ 0
    IF graph has negative weights:
        RAISE Error("Negative weights not supported")
    
    FOR each vertex v IN graph:
        dist[v] ← ∞
        parent[v] ← NULL
    dist[source] ← 0
    visited ← empty set
    
    REPEAT V times:
        // Array scan: find unvisited vertex with minimum distance
        u ← NULL
        FOR each vertex v IN graph:
            IF v NOT IN visited AND (u IS NULL OR dist[v] < dist[u]):
                u ← v
        
        IF u IS NULL OR dist[u] = ∞:
            BREAK
        
        ADD u TO visited
        
        // Relax all neighbours of u
        FOR each neighbour v of u with weight w:
            IF v NOT IN visited:
                new_dist ← dist[u] + w
                IF new_dist < dist[v]:
                    dist[v] ← new_dist
                    parent[v] ← u
    
    RETURN dist, parent
```

**Complexity:** O(V²) — V iterations × V-scan per iteration.

---

## 3. Union-Find with Path Compression and Union by Rank

```
STRUCTURE DisjointSet:
    parent: dictionary mapping item → parent item
    rank: dictionary mapping item → integer rank

FUNCTION MAKE-SET(items):
    FOR each item x IN items:
        parent[x] ← x
        rank[x] ← 0

FUNCTION FIND(x):
    // Find root with path compression
    root ← x
    WHILE parent[root] ≠ root:
        root ← parent[root]
    // Path compression: make all nodes point directly to root
    WHILE parent[x] ≠ root:
        next ← parent[x]
        parent[x] ← root
        x ← next
    RETURN root

FUNCTION UNION(a, b):
    root_a ← FIND(a)
    root_b ← FIND(b)
    IF root_a = root_b:
        RETURN False    // Already in same set
    // Union by rank: attach shorter tree under taller tree
    IF rank[root_a] < rank[root_b]:
        SWAP(root_a, root_b)
    parent[root_b] ← root_a
    IF rank[root_a] = rank[root_b]:
        rank[root_a] ← rank[root_a] + 1
    RETURN True
```

**Amortized Complexity:** O(α(n)) per operation, where α is the inverse Ackermann function. Practically O(1) per operation.

---

## 4. Kruskal's Algorithm

```
FUNCTION KRUSKAL-MST(graph):
    edges ← all edges of graph as (u, v, weight) tuples
    MERGE-SORT(edges) by weight    // O(E log E) manual merge sort
    ds ← MAKE-SET(all vertices)
    mst_edges ← empty list
    total_cost ← 0
    
    FOR each (u, v, w) IN sorted edges:
        IF FIND(u) ≠ FIND(v):     // Not in same component
            UNION(u, v)
            ADD (u, v, w) TO mst_edges
            total_cost ← total_cost + w
    
    RETURN mst_edges, total_cost
```

---

## 5. Prim's Algorithm (Array-Based)

```
FUNCTION PRIM-MST(graph):
    FOR each vertex v:
        key[v] ← ∞
        parent[v] ← NULL
        in_mst[v] ← False
    key[start] ← 0
    
    REPEAT V times:
        // Array scan: pick unvisited vertex with minimum key
        u ← vertex with minimum key[u] where in_mst[u] = False
        IF u IS NULL OR key[u] = ∞:
            BREAK
        in_mst[u] ← True
        IF parent[u] ≠ NULL:
            ADD edge (parent[u], u, key[u]) to MST
        
        // Update keys of adjacent vertices
        FOR each neighbour v of u with weight w:
            IF NOT in_mst[v] AND w < key[v]:
                key[v] ← w
                parent[v] ← u
    
    RETURN MST edges, total cost
```

---

## 6. BFS

```
FUNCTION BFS(graph, source):
    dist[source] ← 0
    parent[source] ← NULL
    queue ← [source]
    front ← 0
    
    WHILE front < length(queue):
        u ← queue[front]
        front ← front + 1
        FOR each neighbour v of u:
            IF v NOT IN dist:
                dist[v] ← dist[u] + 1
                parent[v] ← u
                APPEND v TO queue
    
    RETURN dist, parent
```

---

## 7. Topological Sort (Kahn's Algorithm)

```
FUNCTION KAHN-TOPO-SORT(dag):
    in_deg ← compute in-degree for each vertex
    queue ← all vertices with in_deg = 0
    order ← empty list
    front ← 0
    
    WHILE front < length(queue):
        u ← queue[front]
        front ← front + 1
        APPEND u TO order
        FOR each successor v of u:
            in_deg[v] ← in_deg[v] - 1
            IF in_deg[v] = 0:
                APPEND v TO queue
    
    IF length(order) ≠ number of vertices:
        RETURN order, False   // Cycle exists
    RETURN order, True
```
