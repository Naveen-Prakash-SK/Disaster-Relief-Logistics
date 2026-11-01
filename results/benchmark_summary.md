# Benchmark Summary

Workloads use deterministic seed 54. Repetitions per configuration: 5. Displayed algorithm times are arithmetic means of actual `time.perf_counter()` measurements; setup is excluded from algorithm timings. Results vary by machine and system load.

## Tree Benchmarks: BST vs AVL

| n | Structure | Input order | Insert avg (s) | Search avg (s) | Delete avg (s) | Height after insert |
|---:|---|---|---:|---:|---:|---:|
| 5000 | BST | sorted | 0.645210020 | 0.499381740 | 0.000948960 | 5000.0 |
| 5000 | AVL | sorted | 0.021753800 | 0.001638560 | 0.014204140 | 13.0 |
| 5000 | BST | random | 0.004035320 | 0.002676020 | 0.002728380 | 27.0 |
| 5000 | AVL | random | 0.018690580 | 0.001818080 | 0.015421540 | 15.0 |

## Graph Benchmarks: Prim vs Kruskal

| V | E | Type | Density | Setup (s) | Prim avg (s) | Kruskal avg (s) | MST cost | Shallow graph bytes |
|---:|---:|---|---:|---:|---:|---:|---:|---:|
| 1000 | 2000 | sparse | 0.004004 | 0.015558 | 0.038489560 | 0.005251280 | 29007 | 8962664 |
| 1000 | 250000 | dense | 0.500501 | 2.050899 | 0.247668880 | 3.455934080 | 1003 | 38467432 |

Graph memory is a shallow `sys.getsizeof` estimate of the project's graph containers; it excludes referenced vertex, edge, tuple, and numeric objects, plus transient algorithm allocations.

### Observations

- Sorted input shows how an unbalanced BST can degenerate; AVL measurements are accompanied by invariant checks.
- Benchmark graphs are generated as connected graphs with exactly the requested edge count.
- Prim and Kruskal costs were checked on every repetition.
