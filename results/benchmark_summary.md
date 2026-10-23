# Benchmark Summary

Workloads use deterministic seed 42. Each displayed time is a single `time.perf_counter()` sample, not an average; elapsed times vary by machine and system load. Reproduce with the benchmark command in `README.md`.

## Tree Benchmarks: BST vs AVL

| n | Type | Input | Time (s) | Height |
|---|------|-------|----------|--------|
| 500 | BST | sorted | 0.010806 | 500 |
| 500 | AVL | sorted | 0.002518 | 9 |
| 500 | BST | random | 0.000461 | 19 |
| 500 | AVL | random | 0.002371 | 11 |
| 1000 | BST | sorted | 0.037275 | 1000 |
| 1000 | AVL | sorted | 0.006983 | 10 |
| 1000 | BST | random | 0.000996 | 21 |
| 1000 | AVL | random | 0.008640 | 12 |

## Graph Benchmarks: Prim vs Kruskal

| V | E | Type | Prim (s) | Kruskal (s) | Cost |
|---|---|------|----------|-------------|------|
| 50 | 100 | sparse | 0.000381 | 0.000684 | 1283 |
| 50 | 625 | dense | 0.000402 | 0.004141 | 300 |
| 100 | 200 | sparse | 0.000795 | 0.000931 | 2381 |
| 100 | 2500 | dense | 0.001218 | 0.018395 | 323 |

### Observations

- BST with sorted input degenerates to O(n) height, while AVL maintains O(log n).
- With random input, BST height is closer to O(log n) on average.
- Array-based Prim is O(V^2), efficient for dense graphs.
- Kruskal with merge sort is O(E log E), efficient for sparse graphs.
- Both Prim and Kruskal produce the same MST cost on connected graphs.
