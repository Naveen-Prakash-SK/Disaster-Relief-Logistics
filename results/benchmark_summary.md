# Benchmark Summary

Workloads use deterministic seed 42. Each displayed time is a single `time.perf_counter()` sample, not an average; elapsed times vary by machine and system load. Reproduce with the benchmark command in `README.md`.

## Tree Benchmarks: BST vs AVL

| n | Type | Input | Time (s) | Height |
|---|------|-------|----------|--------|
| 1000 | BST | sorted | 0.032684 | 1000 |
| 1000 | AVL | sorted | 0.007379 | 10 |
| 1000 | BST | random | 0.001781 | 21 |
| 1000 | AVL | random | 0.009604 | 12 |
| 5000 | BST | sorted | 0.892764 | 5000 |
| 5000 | AVL | sorted | 0.046385 | 13 |
| 5000 | BST | random | 0.008043 | 28 |
| 5000 | AVL | random | 0.051774 | 15 |
| 20000 | BST | sorted | 13.358428 | 20000 |
| 20000 | AVL | sorted | 0.185719 | 15 |
| 20000 | BST | random | 0.036685 | 35 |
| 20000 | AVL | random | 0.195739 | 17 |

## Graph Benchmarks: Prim vs Kruskal

| V | E | Type | Prim (s) | Kruskal (s) | Cost |
|---|---|------|----------|-------------|------|
| 200 | 400 | sparse | 0.004157 | 0.003964 | 5340 |
| 200 | 10000 | dense | 0.006723 | 0.083455 | 343 |
| 1000 | 2000 | sparse | 0.086595 | 0.012993 | 28937 |
| 1000 | 250000 | dense | 0.147201 | 6.450146 | 1007 |
| 2000 | 4000 | sparse | 0.380274 | 0.041227 | 58334 |
| 2000 | 50000 | dense* | 0.332871 | 0.637205 | 5782 |

### Observations

- BST with sorted input degenerates to O(n) height, while AVL maintains O(log n).
- With random input, BST height is closer to O(log n) on average.
- Array-based Prim is O(V^2), efficient for dense graphs.
- Kruskal with merge sort is O(E log E), efficient for sparse graphs.
- Both Prim and Kruskal produce the same MST cost on connected graphs.
