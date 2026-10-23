# Complexity Analysis

## 1. Non-Recursive Algorithm Analysis

### BFS — O(V + E)

**Derivation:**
- Initialisation: O(V) to set up distance/parent structures
- Main loop: Each vertex is enqueued and dequeued at most once → O(V)
- For each dequeued vertex u, we examine all neighbours → total edge scans = O(E)
- Total: O(V) + O(E) = **O(V + E)**

**Space:** O(V) for the queue, distance and parent arrays.

**When to use:** Unweighted graphs or when only edge-count distance matters. The adjacency-list implementation ensures O(V + E) time. With adjacency matrix, BFS becomes O(V²) as each vertex's row must be fully scanned.

---

### Array-Based Dijkstra — O(V²)

**Derivation:**
- Outer loop: V iterations (one vertex finalised per iteration)
- Find minimum (array scan): O(V) per iteration → O(V²) total
- Relaxation: Each edge relaxed at most once → O(E) total
- Since E ≤ V(V-1)/2 for simple graphs, E = O(V²)
- Total: O(V²) + O(E) = **O(V² + E) ≈ O(V²)**

**Space:** O(V) for dist, parent, visited arrays.

**When to prefer:**
- Dense graphs (E ≈ V²): Array Dijkstra is O(V²) vs O(V² log V) for heap-based
- Sparse graphs (E ≈ V): Heap-based O((V + E) log V) = O(V log V) is better

---

### Array-Based Prim — O(V²)

**Derivation:**
- V iterations, each scanning V vertices for minimum key → O(V²)
- Each edge examined during relaxation → O(E) total
- Total: **O(V²)**

**Space:** O(V) for key, parent, in_mst arrays.

**Same preference as Dijkstra:** O(V²) is optimal for dense graphs.

---

### Kruskal — O(E log E)

**Derivation:**
- Edge sorting (merge sort): O(E log E)
  - Merge sort recurrence: T(E) = 2T(E/2) + O(E) → O(E log E)
- Union-Find operations: O(E · α(V)) where α is inverse Ackermann
  - Practically O(E) since α(V) ≤ 4 for all practical V
- Total: **O(E log E + E · α(V)) ≈ O(E log E)**

Note: Since E ≤ V², log E ≤ 2 log V, so O(E log E) = O(E log V).

**When to prefer:** Sparse graphs where E = O(V). Kruskal becomes O(V log V).

---

## 2. Recursive Algorithm Analysis

### Tree Traversal — O(n)

**Recurrence:** T(n) = T(k) + T(n-1-k) + c  (left subtree k nodes, right n-1-k nodes)

**Proof (substitution):**
- Guess T(n) = an + b
- T(n) = a·k + b + a·(n-1-k) + b + c = a·n - a + 2b + c
- For T(n) = an + b: an + b = an - a + 2b + c → a = b + c
- Choose b = 0, a = c → T(n) = cn = **O(n)**

Each of the n nodes is visited exactly once.

---

### BST Insertion

**Best case (balanced):**
- T(n) = T(n/2) + O(1)
- By Master Theorem: a=1, b=2, f(n)=O(1), log_b(a) = 0
- Case 2: T(n) = **O(log n)**

**Worst case (sorted input):**
- T(n) = T(n-1) + O(1)
- T(n) = O(1) · n = **O(n)**

**Average case (random input):**
- Expected height of random BST is O(log n)
- Average insertion: **O(log n)**

---

### AVL Insertion — O(log n)

**Recurrence:** T(n) = T(n') + O(1) where n' < n

The AVL tree has height h = O(log n), so the insertion traverses at most h levels. At each level, O(1) work is done (comparison + possible rotation).

**T(n) = O(h) = O(log n)**

---

### AVL Height Proof — h = O(log n)

**Minimum-node recurrence:**
Let N(h) = minimum nodes in an AVL tree of height h.
- N(0) = 0
- N(1) = 1
- N(h) = N(h-1) + N(h-2) + 1

**Lower bound:**
N(h) = N(h-1) + N(h-2) + 1 > N(h-2) + N(h-2) = 2·N(h-2)

Solving: N(h) > 2^(h/2)

Therefore: n ≥ N(h) > 2^(h/2)

Taking logarithms: h/2 < log₂(n) → **h < 2·log₂(n) = O(log n)**

For n = 1000: h ≤ 2 × 10 = 20 (our measured AVL height: 10, well within bound).

---

## 3. Asymptotic Notation and Proofs

### Formal Asymptotic Proof

**Theorem:** Array-based Dijkstra is Θ(V²) for dense graphs.

**Proof of O(V²):** (Upper bound)
- V outer iterations × V inner scan = V² comparisons in find-minimum
- Plus O(E) for relaxation, E ≤ V² → Total ≤ c₁V² for some constant c₁
- Therefore T(V, E) = O(V²) ✓

**Proof of Ω(V²):** (Lower bound)
- The find-minimum loop always scans V vertices each of V iterations
- Even with E = 0 edges, the algorithm performs V × V comparisons
- Therefore T(V, E) ≥ c₂V² for some constant c₂
- Therefore T(V, E) = Ω(V²) ✓

**Conclusion:** T(V, E) = **Θ(V²)** for the array-based implementation.

---

### Union-Find Amortized Analysis

**With path compression and union by rank:**

**Theorem (Tarjan):** A sequence of m Find/Union operations on n elements takes O(m · α(n)) time, where α is the inverse Ackermann function.

**Key insights:**
1. **Union by rank** ensures tree height ≤ log n
2. **Path compression** flattens the tree during Find, amortizing future operations
3. Combined, the amortized cost per operation is α(n), which is ≤ 4 for all practical values of n (up to 2^65536)

**In Kruskal's context:** E Union/Find operations on V elements → O(E · α(V)) ≈ O(E) total.

---

### Comparison-Based Sorting Lower Bound

**Theorem:** Any comparison-based sorting algorithm requires Ω(n log n) comparisons in the worst case.

**Proof (decision-tree argument):**
- n! possible permutations → decision tree has n! leaves
- A binary tree with L leaves has height ≥ log₂(L)
- Height ≥ log₂(n!) = Ω(n log n) (by Stirling's approximation)

**Application to Kruskal:** Sorting E edges requires Ω(E log E) comparisons. Our merge sort achieves O(E log E), which is optimal.

---

## 4. Sparse vs Dense Graph Analysis

| | Array Dijkstra | Heap Dijkstra | Prim (array) | Kruskal |
|---|---|---|---|---|
| **Time** | O(V²) | O((V+E) log V) | O(V²) | O(E log E) |
| **Sparse (E≈V)** | O(V²) | O(V log V) | O(V²) | O(V log V) |
| **Dense (E≈V²)** | O(V²) | O(V² log V) | O(V²) | O(V² log V) |

**Conclusion:**
- For **sparse** graphs: Heap-based Dijkstra and Kruskal are preferable
- For **dense** graphs: Array-based Dijkstra/Prim are preferable (simpler, same complexity)
- Our project uses array-based implementations as required by the assignment
