# Benchmark Summary

## Tree Benchmarks: BST vs AVL

| n | Type | Input | Time (s) | Height |
|---|------|-------|----------|--------|
| 1000 | BST | sorted | 0.029987 | 1000 |
| 1000 | AVL | sorted | 0.005719 | 10 |
| 1000 | BST | random | 0.001083 | 21 |
| 1000 | AVL | random | 0.005388 | 12 |
| 5000 | BST | sorted | 0.868481 | 5000 |
| 5000 | AVL | sorted | 0.048282 | 13 |
| 5000 | BST | random | 0.010080 | 28 |
| 5000 | AVL | random | 0.041708 | 15 |
| 20000 | BST | sorted | 14.123166 | 20000 |
| 20000 | AVL | sorted | 0.196684 | 15 |
| 20000 | BST | random | 0.036776 | 35 |
| 20000 | AVL | random | 0.195560 | 17 |

## Graph Benchmarks: Prim vs Kruskal

| V | E | Type | Prim (s) | Kruskal (s) | Cost |
|---|---|------|----------|-------------|------|
| 200 | 400 | sparse | 0.003163 | 0.002285 | 5340 |
| 200 | 10000 | dense | 0.006497 | 0.089671 | 343 |
| 1000 | 2000 | sparse | 0.080498 | 0.014704 | 28937 |
| 1000 | 250000 | dense | 0.142490 | 5.617302 | 1007 |
| 2000 | 4000 | sparse | 0.379895 | 0.044830 | 58334 |
| 2000 | 50000 | dense* | 0.339965 | 0.662416 | 5782 |

### Observations

- BST with sorted input degenerates to O(n) height, while AVL maintains O(log n).
- With random input, BST height is closer to O(log n) on average.
- Array-based Prim is O(V²), efficient for dense graphs.
- Kruskal with merge sort is O(E log E), efficient for sparse graphs.
- Both Prim and Kruskal produce the same MST cost on connected graphs.
