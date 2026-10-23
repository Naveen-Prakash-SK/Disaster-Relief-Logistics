"""Automated self-tests for Disaster Relief Logistics.

At least 15 automated tests covering all modules.
Uses Python's standard unittest module.
"""

import unittest
import sys
import random


# ============================================================================
# GENERAL TREE TESTS
# ============================================================================

class TestGeneralTree(unittest.TestCase):
    """Tests for GeneralTree (Location Hierarchy)."""

    def setUp(self):
        from trees import GeneralTree
        self.tree = GeneralTree()

    def test_add_region(self):
        ok, msg = self.tree.add_location(
            self.tree.root.name, "TamilNadu", "Region")
        self.assertTrue(ok)
        self.assertIsNotNone(self.tree.find("TamilNadu"))

    def test_add_district_under_region(self):
        self.tree.add_location(self.tree.root.name, "TamilNadu", "Region")
        ok, msg = self.tree.add_location("TamilNadu", "Coimbatore", "District")
        self.assertTrue(ok)

    def test_add_shelter_under_district(self):
        self.tree.add_location(self.tree.root.name, "TamilNadu", "Region")
        self.tree.add_location("TamilNadu", "Coimbatore", "District")
        ok, msg = self.tree.add_location(
            "Coimbatore", "ShelterA", "Shelter")
        self.assertTrue(ok)

    def test_invalid_hierarchy(self):
        self.tree.add_location(self.tree.root.name, "TamilNadu", "Region")
        ok, msg = self.tree.add_location("TamilNadu", "BadShelter", "Shelter")
        self.assertFalse(ok)  # Shelter cannot be direct child of Region

    def test_duplicate_name(self):
        self.tree.add_location(self.tree.root.name, "TamilNadu", "Region")
        ok, msg = self.tree.add_location(
            self.tree.root.name, "TamilNadu", "Region")
        self.assertFalse(ok)

    def test_delete_subtree(self):
        self.tree.add_location(self.tree.root.name, "TamilNadu", "Region")
        self.tree.add_location("TamilNadu", "Coimbatore", "District")
        ok, msg = self.tree.delete_subtree("TamilNadu")
        self.assertTrue(ok)
        self.assertIsNone(self.tree.find("TamilNadu"))
        self.assertIsNone(self.tree.find("Coimbatore"))

    def test_traversals(self):
        self.tree.add_location(self.tree.root.name, "R1", "Region")
        self.tree.add_location(self.tree.root.name, "R2", "Region")
        self.tree.add_location("R1", "D1", "District")

        pre = self.tree.preorder()
        post = self.tree.postorder()
        level = self.tree.level_order()

        self.assertEqual(pre[0], self.tree.root.name)   # root first
        self.assertEqual(post[-1], self.tree.root.name)  # root last
        self.assertEqual(level[0], self.tree.root.name)  # root first


# ============================================================================
# BST TESTS
# ============================================================================

class TestSupplyBST(unittest.TestCase):
    """Tests for SupplyBST."""

    def setUp(self):
        from trees import SupplyBST
        self.bst = SupplyBST()
        for k, name, qty in [(50, "Water", 100), (30, "Rice", 200),
                              (70, "Blankets", 50), (20, "Tents", 30),
                              (40, "Medicine", 80), (60, "Fuel", 40),
                              (80, "Batteries", 120)]:
            self.bst.insert(k, name, qty)

    def test_search_existing(self):
        node = self.bst.search(50)
        self.assertIsNotNone(node)
        self.assertEqual(node.item_name, "Water")

    def test_search_missing(self):
        self.assertIsNone(self.bst.search(999))

    def test_delete_leaf(self):
        self.assertTrue(self.bst.delete(20))
        self.assertIsNone(self.bst.search(20))

    def test_delete_one_child(self):
        # Delete 30 (has left child 20 and right child 40)
        self.assertTrue(self.bst.delete(30))
        self.assertIsNone(self.bst.search(30))
        # Children should still be reachable.
        self.assertIsNotNone(self.bst.search(20))
        self.assertIsNotNone(self.bst.search(40))

    def test_delete_two_children(self):
        self.assertTrue(self.bst.delete(50))
        self.assertIsNone(self.bst.search(50))
        # Tree should still have all other nodes.
        for k in [30, 70, 20, 40, 60, 80]:
            self.assertIsNotNone(self.bst.search(k))

    def test_minimum_maximum(self):
        self.assertEqual(self.bst.minimum().key, 20)
        self.assertEqual(self.bst.maximum().key, 80)

    def test_successor_predecessor(self):
        succ = self.bst.successor(50)
        self.assertEqual(succ.key, 60)
        pred = self.bst.predecessor(50)
        self.assertEqual(pred.key, 40)

    def test_range_query(self):
        results = self.bst.range_query(30, 60)
        keys = [n.key for n in results]
        self.assertEqual(sorted(keys), [30, 40, 50, 60])

    def test_inorder_sorted(self):
        nodes = self.bst.inorder()
        keys = [n.key for n in nodes]
        self.assertEqual(keys, sorted(keys))

    def test_iterative_traversals_match_recursive(self):
        rec_in = [n.key for n in self.bst.inorder()]
        iter_in = [n.key for n in self.bst.inorder_iterative()]
        self.assertEqual(rec_in, iter_in)

        rec_pre = [n.key for n in self.bst.preorder()]
        iter_pre = [n.key for n in self.bst.preorder_iterative()]
        self.assertEqual(rec_pre, iter_pre)

        rec_post = [n.key for n in self.bst.postorder()]
        iter_post = [n.key for n in self.bst.postorder_iterative()]
        self.assertEqual(rec_post, iter_post)

    def test_height(self):
        h = self.bst.height()
        self.assertGreater(h, 0)
        self.assertLessEqual(h, 7)  # 7 nodes

    def test_sorted_insert_height(self):
        """Insert 1000 sorted keys — height should equal 1000."""
        from trees import SupplyBST
        bst = SupplyBST()
        for k in range(1, 1001):
            bst.insert(k, f"item-{k}", k)
        self.assertEqual(bst.height(), 1000)

    def test_negative_quantity_rejected(self):
        from trees import SupplyBST
        bst = SupplyBST()
        with self.assertRaises(ValueError):
            bst.insert(1, "test", -5)


# ============================================================================
# AVL TREE TESTS
# ============================================================================

class TestAVLTree(unittest.TestCase):
    """Tests for AVLTree."""

    def setUp(self):
        from avl_expression import AVLTree
        self.avl = AVLTree(trace_rotations=True)

    def test_insert_and_search(self):
        self.avl.insert(10, "camp10")
        self.avl.insert(20, "camp20")
        self.avl.insert(5, "camp5")
        self.assertIsNotNone(self.avl.search(10))
        self.assertIsNone(self.avl.search(99))

    def test_ll_rotation(self):
        """Insert keys that trigger an LL (right) rotation."""
        self.avl.rotation_log.clear()
        self.avl.insert(30)
        self.avl.insert(20)
        self.avl.insert(10)  # Should trigger LL rotation.
        ok, msg = self.avl.verify()
        self.assertTrue(ok, msg)
        self.assertTrue(any("LL" in r for r in self.avl.rotation_log),
                        f"Expected LL rotation: {self.avl.rotation_log}")

    def test_rr_rotation(self):
        """Insert keys that trigger an RR (left) rotation."""
        self.avl.rotation_log.clear()
        self.avl.insert(10)
        self.avl.insert(20)
        self.avl.insert(30)  # Should trigger RR rotation.
        ok, msg = self.avl.verify()
        self.assertTrue(ok, msg)
        self.assertTrue(any("RR" in r for r in self.avl.rotation_log),
                        f"Expected RR rotation: {self.avl.rotation_log}")

    def test_lr_rotation(self):
        """Insert keys that trigger an LR rotation."""
        self.avl.rotation_log.clear()
        self.avl.insert(30)
        self.avl.insert(10)
        self.avl.insert(20)  # Should trigger LR.
        ok, msg = self.avl.verify()
        self.assertTrue(ok, msg)
        self.assertTrue(any("LR" in r for r in self.avl.rotation_log),
                        f"Expected LR rotation: {self.avl.rotation_log}")

    def test_rl_rotation(self):
        """Insert keys that trigger an RL rotation."""
        self.avl.rotation_log.clear()
        self.avl.insert(10)
        self.avl.insert(30)
        self.avl.insert(20)  # Should trigger RL.
        ok, msg = self.avl.verify()
        self.assertTrue(ok, msg)
        self.assertTrue(any("RL" in r for r in self.avl.rotation_log),
                        f"Expected RL rotation: {self.avl.rotation_log}")

    def test_delete_and_rebalance(self):
        for k in [50, 25, 75, 10, 30, 60, 80]:
            self.avl.insert(k)
        self.assertTrue(self.avl.delete(10))
        ok, msg = self.avl.verify()
        self.assertTrue(ok, msg)

    def test_verify_after_random_ops(self):
        """10,000 random insert/delete operations."""
        from avl_expression import AVLTree
        tree, passed, total = AVLTree.random_stress_test(10000, seed=42)
        self.assertEqual(passed, total)
        ok, msg = tree.verify()
        self.assertTrue(ok, msg)

    def test_sorted_insert_height(self):
        """AVL with 1000 sorted keys should have O(log n) height."""
        from avl_expression import AVLTree
        avl = AVLTree()
        for k in range(1, 1001):
            avl.insert(k)
        h = avl.height()
        self.assertLessEqual(h, 20)  # O(log 1000) ≈ 10-14


# ============================================================================
# EXPRESSION TREE TESTS
# ============================================================================

class TestExpressionTree(unittest.TestCase):
    """Tests for expression tree construction, evaluation and infix."""

    def test_simple_expression(self):
        from avl_expression import (build_expression_tree,
                                     evaluate_expression, infix_string)
        root = build_expression_tree(["3", "4", "+"])
        self.assertAlmostEqual(evaluate_expression(root), 7.0)
        self.assertEqual(infix_string(root), "3 + 4")

    def test_complex_expression(self):
        from avl_expression import (build_expression_tree,
                                     evaluate_expression, infix_string)
        # distance rate * toll + → (distance * rate) + toll
        root = build_expression_tree(
            ["distance", "rate", "*", "toll", "+"])
        result = evaluate_expression(
            root, {"distance": 10, "rate": 5, "toll": 3})
        self.assertAlmostEqual(result, 53.0)

    def test_division_by_zero(self):
        from avl_expression import build_expression_tree, evaluate_expression
        root = build_expression_tree(["5", "0", "/"])
        with self.assertRaises(ValueError):
            evaluate_expression(root)

    def test_invalid_postfix_too_few_operands(self):
        from avl_expression import build_expression_tree
        with self.assertRaises(ValueError):
            build_expression_tree(["5", "+"])

    def test_invalid_postfix_extra_operands(self):
        from avl_expression import build_expression_tree
        with self.assertRaises(ValueError):
            build_expression_tree(["5", "3", "2", "+"])

    def test_undefined_variable(self):
        from avl_expression import build_expression_tree, evaluate_expression
        root = build_expression_tree(["x", "y", "+"])
        with self.assertRaises(ValueError):
            evaluate_expression(root, {"x": 1})


# ============================================================================
# GRAPH AND BFS TESTS
# ============================================================================

class TestGraph(unittest.TestCase):
    """Tests for Graph ADT, BFS, DFS, SCC and Dijkstra."""

    def setUp(self):
        from graph import Graph, build_sample_graph
        self.g, self.dg, self.depots = build_sample_graph()

    def test_vertex_count(self):
        self.assertEqual(self.g.vertex_count(), 14)

    def test_edge_exists(self):
        self.assertTrue(self.g.has_edge("DepotA", "RegionNorth"))
        self.assertFalse(self.g.has_edge("DepotA", "IsolatedX"))

    def test_bfs_route_length(self):
        from graph import bfs_path
        path, edges = bfs_path(self.g, "DepotA", "ShelterN1a")
        self.assertIsNotNone(path)
        self.assertEqual(edges, 3)  # DepotA -> RegionNorth -> DistrictN1 -> ShelterN1a

    def test_bfs_unreachable(self):
        from graph import bfs_path
        path, edges = bfs_path(self.g, "DepotA", "IsolatedX")
        self.assertIsNone(path)

    def test_bfs_nearest_depot(self):
        from graph import bfs_nearest_depot
        depot, path, edges = bfs_nearest_depot(
            self.g, "ShelterN1a", self.depots)
        self.assertIn(depot, self.depots)

    def test_dfs_timestamps(self):
        from graph import dfs_full
        disc, fin, _, _, _ = dfs_full(self.g)
        for v in self.g.vertices:
            self.assertIn(v, disc)
            self.assertIn(v, fin)
            self.assertLess(disc[v], fin[v])

    def test_connected_components(self):
        from graph import connected_components_undirected
        comps = connected_components_undirected(self.g)
        self.assertEqual(len(comps), 2)  # main + isolated pair

    def test_scc_directed(self):
        from graph import scc_kosaraju
        comps = scc_kosaraju(self.dg)
        self.assertGreater(len(comps), 0)

    def test_dijkstra_shortest_path(self):
        from graph import dijkstra_path
        path, dist = dijkstra_path(self.g, "DepotA", "ShelterN1a")
        self.assertIsNotNone(path)
        self.assertEqual(path[0], "DepotA")
        self.assertEqual(path[-1], "ShelterN1a")
        # DepotA(10)RegionNorth(5)DistrictN1(3)ShelterN1a = 18
        self.assertEqual(dist, 18)

    def test_dijkstra_unreachable(self):
        from graph import dijkstra_path
        path, dist = dijkstra_path(self.g, "DepotA", "IsolatedX")
        self.assertIsNone(path)

    def test_dijkstra_negative_weight_rejected(self):
        from graph import Graph, dijkstra
        g = Graph(directed=False)
        g.add_edge("A", "B", -1)
        with self.assertRaises(ValueError):
            dijkstra(g, "A")

    def test_bfs_dijkstra_agree_uniform_weight(self):
        """On a graph where every edge has weight 1, BFS and Dijkstra
        should find paths of equal length."""
        from graph import Graph, bfs_path, dijkstra_path
        g = Graph(directed=False)
        for u, v in [("A", "B"), ("B", "C"), ("A", "C"),
                     ("C", "D"), ("D", "E")]:
            g.add_edge(u, v, 1)
        bfs_p, bfs_e = bfs_path(g, "A", "E")
        dij_p, dij_d = dijkstra_path(g, "A", "E")
        self.assertEqual(bfs_e, int(dij_d))


# ============================================================================
# MST TESTS
# ============================================================================

class TestMST(unittest.TestCase):
    """Tests for Prim and Kruskal."""

    def setUp(self):
        from graph import build_sample_graph
        self.g, _, _ = build_sample_graph()

    def test_prim_kruskal_agree(self):
        from mst import prim_mst, kruskal_mst
        _, pc, _ = prim_mst(self.g)
        _, kc, _ = kruskal_mst(self.g)
        self.assertEqual(pc, kc)

    def test_disconnected_forest(self):
        from mst import prim_mst, kruskal_mst
        _, _, p_comps = prim_mst(self.g)
        _, _, k_comps = kruskal_mst(self.g)
        self.assertEqual(len(p_comps), 2)  # main + isolated
        self.assertEqual(len(k_comps), 2)

    def test_single_vertex(self):
        from graph import Graph
        from mst import prim_mst, kruskal_mst
        g = Graph(directed=False)
        g.add_vertex("X")
        _, pc, _ = prim_mst(g)
        _, kc, _ = kruskal_mst(g)
        self.assertEqual(pc, 0)
        self.assertEqual(kc, 0)

    def test_equal_weights(self):
        """All edges same weight — MST should use V-1 edges."""
        from graph import Graph
        from mst import prim_mst, kruskal_mst
        g = Graph(directed=False)
        for v in ["A", "B", "C", "D"]:
            g.add_vertex(v)
        for u, v in [("A", "B"), ("B", "C"), ("C", "D"),
                     ("A", "C"), ("B", "D")]:
            g.add_edge(u, v, 5)
        pe, pc, _ = prim_mst(g)
        ke, kc, _ = kruskal_mst(g)
        self.assertEqual(len(pe), 3)
        self.assertEqual(len(ke), 3)
        self.assertEqual(pc, 15)
        self.assertEqual(kc, 15)

    def test_merge_sort_edges(self):
        from mst import merge_sort_edges
        edges = [("A", "B", 5), ("C", "D", 1), ("E", "F", 3)]
        sorted_e = merge_sort_edges(edges)
        weights = [e[2] for e in sorted_e]
        self.assertEqual(weights, [1, 3, 5])


# ============================================================================
# SCHEDULING TESTS
# ============================================================================

class TestScheduling(unittest.TestCase):
    """Tests for topological sorting, cycle detection and critical path."""

    def test_kahn_acyclic(self):
        from scheduling import build_sample_acyclic_dag, topological_sort_kahn
        dag = build_sample_acyclic_dag()
        order, is_dag = topological_sort_kahn(dag)
        self.assertTrue(is_dag)
        self.assertEqual(len(order), len(dag.tasks))

    def test_dfs_topo_acyclic(self):
        from scheduling import build_sample_acyclic_dag, topological_sort_dfs
        dag = build_sample_acyclic_dag()
        order, is_dag, cycle = topological_sort_dfs(dag)
        self.assertTrue(is_dag)
        self.assertEqual(cycle, [])

    def test_cycle_detection(self):
        from scheduling import build_sample_cyclic_dag, detect_cycle
        dag = build_sample_cyclic_dag()
        has_cycle, cycle = detect_cycle(dag)
        self.assertTrue(has_cycle)
        self.assertGreater(len(cycle), 0)

    def test_critical_path(self):
        from scheduling import build_sample_acyclic_dag, critical_path
        dag = build_sample_acyclic_dag()
        path, duration, est = critical_path(dag)
        self.assertGreater(duration, 0)
        self.assertIn("AssessDamage", path)
        self.assertIn("FinalReport", path)

    def test_earliest_start_times(self):
        from scheduling import (build_sample_acyclic_dag,
                                earliest_start_times)
        dag = build_sample_acyclic_dag()
        est, order = earliest_start_times(dag)
        self.assertEqual(est["AssessDamage"], 0)


# ============================================================================
# UNION-FIND TESTS
# ============================================================================

class TestDisjointSet(unittest.TestCase):
    """Tests for union-find."""

    def test_union_find(self):
        from mst import DisjointSet
        ds = DisjointSet(["a", "b", "c", "d"])
        self.assertTrue(ds.union("a", "b"))
        self.assertTrue(ds.union("c", "d"))
        self.assertEqual(ds.find("a"), ds.find("b"))
        self.assertNotEqual(ds.find("a"), ds.find("c"))
        self.assertTrue(ds.union("b", "c"))
        self.assertEqual(ds.find("a"), ds.find("d"))

    def test_union_same_set(self):
        from mst import DisjointSet
        ds = DisjointSet([1, 2, 3])
        ds.union(1, 2)
        self.assertFalse(ds.union(1, 2))  # Already same set


# ============================================================================
# EMPTY STRUCTURE TESTS
# ============================================================================

class TestEmptyStructures(unittest.TestCase):
    """Tests for edge cases with empty data structures."""

    def test_empty_bst(self):
        from trees import SupplyBST
        bst = SupplyBST()
        self.assertIsNone(bst.search(1))
        self.assertIsNone(bst.minimum())
        self.assertIsNone(bst.maximum())
        self.assertEqual(bst.height(), 0)
        self.assertFalse(bst.delete(1))

    def test_empty_avl(self):
        from avl_expression import AVLTree
        avl = AVLTree()
        self.assertIsNone(avl.search(1))
        self.assertFalse(avl.delete(1))
        ok, msg = avl.verify()
        self.assertTrue(ok)

    def test_empty_graph(self):
        from graph import Graph, bfs
        g = Graph()
        d, p = bfs(g, "nonexistent")
        self.assertEqual(d, {})

    def test_empty_expression(self):
        from avl_expression import build_expression_tree
        with self.assertRaises(ValueError):
            build_expression_tree([])


# ============================================================================
# TEST RUNNER
# ============================================================================

def run_tests():
    """Run all tests with verbose output, callable from the main menu."""
    print("\n=== Running Automated Self-Tests ===\n")
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    test_classes = [
        TestGeneralTree,
        TestSupplyBST,
        TestAVLTree,
        TestExpressionTree,
        TestGraph,
        TestMST,
        TestScheduling,
        TestDisjointSet,
        TestEmptyStructures,
    ]
    for cls in test_classes:
        suite.addTests(loader.loadTestsFromTestCase(cls))

    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    print(f"\nTests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    return result
