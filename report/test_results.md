# Test Results

## Test Execution

**Command:** `python -m unittest -v`

**Total Tests:** 80
**Passed:** 80
**Failed:** 0  
**Errors:** 0  
**Time:** 5.621 seconds (final workspace run).

## Detailed Results

### TestAVLTree (8 tests)
| Test | Status |
|------|--------|
| test_delete_and_rebalance | ✓ OK |
| test_insert_and_search | ✓ OK |
| test_ll_rotation | ✓ OK |
| test_lr_rotation | ✓ OK |
| test_rl_rotation | ✓ OK |
| test_rr_rotation | ✓ OK |
| test_sorted_insert_height | ✓ OK |
| test_verify_after_random_ops (10,000 ops) | ✓ OK |

### TestDisjointSet (2 tests)
| Test | Status |
|------|--------|
| test_union_find | ✓ OK |
| test_union_same_set | ✓ OK |

### TestEmptyStructures (4 tests)
| Test | Status |
|------|--------|
| test_empty_avl | ✓ OK |
| test_empty_bst | ✓ OK |
| test_empty_expression | ✓ OK |
| test_empty_graph | ✓ OK |

### TestExpressionTree (8 tests)
| Test | Status |
|------|--------|
| test_complex_expression | ✓ OK |
| test_division_by_zero | ✓ OK |
| test_invalid_postfix_extra_operands | ✓ OK |
| test_invalid_postfix_too_few_operands | ✓ OK |
| test_infix_preserves_right_child_grouping | ✓ OK |
| test_infix_expression_unary_and_invalid_input | ✓ OK |
| test_simple_expression | ✓ OK |
| test_undefined_variable | ✓ OK |

### TestGeneralTree (7 tests)
| Test | Status |
|------|--------|
| test_add_district_under_region | ✓ OK |
| test_add_region | ✓ OK |
| test_add_shelter_under_district | ✓ OK |
| test_delete_subtree | ✓ OK |
| test_duplicate_name | ✓ OK |
| test_invalid_hierarchy | ✓ OK |
| test_traversals | ✓ OK |

### TestGraph (15 tests)
| Test | Status |
|------|--------|
| test_bfs_dijkstra_agree_uniform_weight | ✓ OK |
| test_bfs_nearest_depot | ✓ OK |
| test_bfs_route_length | ✓ OK |
| test_bfs_unreachable | ✓ OK |
| test_connected_components | ✓ OK |
| test_dfs_timestamps | ✓ OK |
| test_dijkstra_negative_weight_rejected | ✓ OK |
| test_dijkstra_shortest_path | ✓ OK |
| test_dijkstra_unreachable | ✓ OK |
| test_edge_exists | ✓ OK |
| test_scc_directed | ✓ OK |
| test_sample_graph_conditions | ✓ OK |
| test_undirected_self_loop_count | ✓ OK |
| test_remove_vertex_cleans_incident_edges | ✓ OK |
| test_vertex_count | ✓ OK |

### TestMST (5 tests)
| Test | Status |
|------|--------|
| test_disconnected_forest | ✓ OK |
| test_equal_weights | ✓ OK |
| test_merge_sort_edges | ✓ OK |
| test_prim_kruskal_agree | ✓ OK |
| test_single_vertex | ✓ OK |

### TestScheduling (6 tests)
| Test | Status |
|------|--------|
| test_critical_path | ✓ OK |
| test_cycle_detection | ✓ OK |
| test_dfs_topo_acyclic | ✓ OK |
| test_earliest_start_times | ✓ OK |
| test_kahn_acyclic | ✓ OK |
| test_empty_critical_path | ✓ OK |

### TestSupplyBST (14 tests)
All 14 supply BST tests passed, including the regression test that performs
iterative traversal, range query and deletion on a 1,500-node skewed tree.

### Workflow and persistence tests

Seven scenario persistence tests validate JSON round-trip, invalid records,
structural reconstruction and task-name normalization. One benchmark test
checks custom sizes, deterministic seed and CSV metadata. One interactive
workflow class includes tests for bidirectional-preserving graph conversion,
conflicting directed-edge weights, and building/saving/restarting/loading a
scenario before calculating a route.

## Coverage Summary

| Module | Tests | All Pass |
|--------|-------|----------|
| trees.py (General Tree) | 7 | ✓ |
| trees.py (BST) | 14 | ✓ |
| avl_expression.py (AVL) | 8 | ✓ |
| avl_expression.py (Expr) | 8 | ✓ |
| graph.py (Graph + algos) | 15 | ✓ |
| mst.py (Prim + Kruskal) | 5 | ✓ |
| scheduling.py | 6 | ✓ |
| mst.py (Union-Find) | 2 | ✓ |
| Edge cases | 4 | ✓ |
| Scenario persistence | 7 | ✓ |
| Benchmark configuration | 1 | ✓ |
| Interactive workflow and graph conversion | 3 | ✓ |
| **Total** | **80** | **✓** |
