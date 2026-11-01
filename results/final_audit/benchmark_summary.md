# Benchmark Summary

Workloads use deterministic seed 42. Repetitions per configuration: 5. Displayed algorithm times are arithmetic means of actual `time.perf_counter()` measurements; setup is excluded from algorithm timings. Results vary by machine and system load.

## Tree Benchmarks: BST vs AVL

| n | Structure | Input order | Insert avg (s) | Search avg (s) | Delete avg (s) | Height after insert |
|---:|---|---|---:|---:|---:|---:|
| 1000 | BST | sorted | 0.029832100 | 0.025869520 | 0.000200840 | 1000.0 |
| 1000 | AVL | sorted | 0.006398200 | 0.000510760 | 0.004721840 | 10.0 |
| 1000 | BST | random | 0.001072340 | 0.000739680 | 0.000880900 | 21.0 |
| 1000 | AVL | random | 0.005893840 | 0.000652580 | 0.004588960 | 12.0 |
| 5000 | BST | sorted | 0.739981340 | 0.647131000 | 0.000853640 | 5000.0 |
| 5000 | AVL | sorted | 0.042084280 | 0.003674820 | 0.025827160 | 13.0 |
| 5000 | BST | random | 0.007508380 | 0.004606580 | 0.005935640 | 28.0 |
| 5000 | AVL | random | 0.036617420 | 0.004065780 | 0.035605420 | 15.0 |
| 20000 | BST | sorted | 23.962120540 | 19.476735180 | 0.006079700 | 20000.0 |
| 20000 | AVL | sorted | 0.172498940 | 0.017115460 | 0.116689400 | 15.0 |
| 20000 | BST | random | 0.036223160 | 0.026581700 | 0.030711200 | 35.0 |
| 20000 | AVL | random | 0.169549580 | 0.019129780 | 0.156670260 | 17.0 |

## Graph Benchmarks: Prim vs Kruskal

| V | E | Type | Density | Setup (s) | Prim avg (s) | Kruskal avg (s) | MST cost | Shallow graph bytes |
|---:|---:|---|---:|---:|---:|---:|---:|---:|
| 200 | 400 | sparse | 0.020101 | 0.002915 | 0.003121020 | 0.001574760 | 5340 | 435456 |
| 200 | 10000 | dense | 0.502513 | 0.049486 | 0.006217540 | 0.053608900 | 343 | 3119464 |
| 1000 | 2000 | sparse | 0.004004 | 0.033953 | 0.074140400 | 0.010076200 | 28937 | 8962048 |
| 1000 | 250000 | dense | 0.500501 | 2.864649 | 0.136533700 | 4.309716440 | 1007 | 38467432 |
| 2000 | 4000 | sparse | 0.002001 | 0.264421 | 0.302145880 | 0.023644580 | 58334 | 35064248 |
| 2000 | 1000000 | dense | 0.500250 | 39.254116 | 0.728643640 | 49.093194580 | 1999 | 153322120 |

Graph memory is a shallow `sys.getsizeof` estimate of the project's graph containers; it excludes referenced vertex, edge, tuple, and numeric objects, plus transient algorithm allocations.

### Observations

- Sorted input shows how an unbalanced BST can degenerate; AVL measurements are accompanied by invariant checks.
- Benchmark graphs are generated as connected graphs with exactly the requested edge count.
- Prim and Kruskal costs were checked on every repetition.
