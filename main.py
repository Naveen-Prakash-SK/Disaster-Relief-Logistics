"""Disaster Relief Logistics — main entry point.

Console-based application integrating all DSA modules.
Team 8 | KPR Institute of Engineering and Technology
"""


def show_menu():
    print("\n" + "=" * 52)
    print("       DISASTER RELIEF LOGISTICS SYSTEM")
    print("=" * 52)
    print(" 1. Location hierarchy (General Tree)")
    print(" 2. Relief supply inventory (BST)")
    print(" 3. Relief-camp index (AVL) & Expression calculator")
    print(" 4. Build / view road network (Graph)")
    print(" 5. BFS nearest depot")
    print(" 6. Dijkstra shortest supply route")
    print(" 7. DFS and connectivity analysis")
    print(" 8. Prim minimum spanning forest")
    print(" 9. Kruskal minimum spanning forest")
    print("10. Scheduling and critical path")
    print("11. Timing experiments / benchmarks")
    print("12. Run automated self-tests")
    print("13. Display sample scenario")
    print(" 0. Exit")
    print("-" * 52)


def main():
    while True:
        show_menu()
        choice = input("Choose an option: ").strip()

        try:
            if choice == "1":
                from trees import trees_menu
                trees_menu()
            elif choice == "2":
                from trees import trees_menu
                trees_menu()  # BST is in the same menu
            elif choice == "3":
                from avl_expression import avl_expression_menu
                avl_expression_menu()
            elif choice == "4":
                from graph import graph_menu
                graph_menu()
            elif choice == "5":
                _bfs_nearest_depot()
            elif choice == "6":
                _dijkstra_route()
            elif choice == "7":
                _dfs_analysis()
            elif choice == "8":
                _prim_mst()
            elif choice == "9":
                _kruskal_mst()
            elif choice == "10":
                from scheduling import scheduling_menu
                scheduling_menu()
            elif choice == "11":
                from analysis import analysis_menu
                analysis_menu()
            elif choice == "12":
                from tests import run_tests
                run_tests()
            elif choice == "13":
                _display_sample_scenario()
            elif choice == "0":
                print("Exiting Disaster Relief Logistics. Goodbye!")
                break
            else:
                print("Invalid option. Please choose 0-13.")
        except Exception as exc:
            print(f"Error: {exc}")


# ============================================================================
# Quick-access functions (wrap module calls for menu convenience)
# ============================================================================

def _bfs_nearest_depot():
    """BFS nearest depot from user-specified location."""
    from graph import build_sample_graph, bfs_nearest_depot
    g, _, depots = build_sample_graph()
    print("\nAvailable locations:", ", ".join(g.vertices))
    src = input("Your location: ").strip()
    depot, path, edges = bfs_nearest_depot(g, src, depots)
    if depot is None:
        print("No reachable depot found from that location.")
    else:
        print(f"Nearest depot: {depot} ({edges} edges)")
        print(f"Route: {' -> '.join(path)}")


def _dijkstra_route():
    """Dijkstra shortest weighted route."""
    from graph import build_sample_graph, dijkstra_path
    g, _, _ = build_sample_graph()
    print("\nAvailable locations:", ", ".join(g.vertices))
    src = input("Source: ").strip()
    dst = input("Destination: ").strip()
    try:
        path, dist = dijkstra_path(g, src, dst, verbose=True)
        if path is None:
            print(f"\nNo path from '{src}' to '{dst}' (unreachable).")
        else:
            print(f"\nShortest distance: {dist}")
            print(f"Path: {' -> '.join(path)}")
    except ValueError as e:
        print(f"Error: {e}")


def _dfs_analysis():
    """DFS timestamps and connectivity."""
    from graph import (build_sample_graph, dfs_full,
                       connected_components_undirected,
                       scc_kosaraju)
    g, dg, _ = build_sample_graph()

    print("\n--- DFS on undirected graph ---")
    disc, fin, _, etypes, order = dfs_full(g)
    print("DFS order:", " -> ".join(order))
    print("\nTimestamps:")
    for v in g.vertices:
        print(f"  {v}: d={disc.get(v, '?')}, f={fin.get(v, '?')}")
    print("\nEdge classification:")
    for (u, v), et in etypes.items():
        print(f"  ({u} -> {v}): {et}")

    comps = connected_components_undirected(g)
    print(f"\nConnected components ({len(comps)}):")
    for i, c in enumerate(comps, 1):
        print(f"  {i}: {', '.join(c)}")

    print("\n--- SCC on directed graph (Kosaraju) ---")
    sccs = scc_kosaraju(dg)
    print(f"Strongly connected components ({len(sccs)}):")
    for i, c in enumerate(sccs, 1):
        print(f"  {i}: {', '.join(c)}")


def _prim_mst():
    """Run Prim's MST."""
    from graph import build_sample_graph
    from mst import prim_mst
    g, _, _ = build_sample_graph()
    edges, cost, comps = prim_mst(g)
    print(f"\nPrim's MST — total cost: {cost}")
    print("Edges selected:")
    for u, v, w in edges:
        print(f"  {u} -- {v}  (weight {w})")
    print(f"Components ({len(comps)}):")
    for i, c in enumerate(comps, 1):
        print(f"  {i}: {', '.join(c)}")


def _kruskal_mst():
    """Run Kruskal's MST."""
    from graph import build_sample_graph
    from mst import kruskal_mst
    g, _, _ = build_sample_graph()
    edges, cost, comps = kruskal_mst(g)
    print(f"\nKruskal's MST — total cost: {cost}")
    print("Edges selected:")
    for u, v, w in edges:
        print(f"  {u} -- {v}  (weight {w})")
    print(f"Components ({len(comps)}):")
    for i, c in enumerate(comps, 1):
        print(f"  {i}: {', '.join(c)}")


def _display_sample_scenario():
    """Display the full sample disaster relief scenario."""
    from trees import GeneralTree, SupplyBST
    from graph import build_sample_graph
    from mst import prim_mst, kruskal_mst

    print("\n" + "=" * 52)
    print("       SAMPLE DISASTER RELIEF SCENARIO")
    print("=" * 52)

    # Location hierarchy.
    print("\n--- Location Hierarchy ---")
    tree = GeneralTree()
    locations = [
        (tree.root.name, "TamilNadu", "Region"),
        (tree.root.name, "Kerala", "Region"),
        ("TamilNadu", "Coimbatore", "District"),
        ("TamilNadu", "Chennai", "District"),
        ("Kerala", "Wayanad", "District"),
        ("Coimbatore", "ShelterA", "Shelter"),
        ("Coimbatore", "ShelterB", "Shelter"),
        ("Chennai", "ShelterC", "Shelter"),
        ("Wayanad", "ShelterD", "Shelter"),
    ]
    for parent, name, ltype in locations:
        tree.add_location(parent, name, ltype)
    tree.display()

    print("\nTraversals:")
    print("  Preorder:", " -> ".join(tree.preorder()))
    print("  Postorder:", " -> ".join(tree.postorder()))
    print("  Level-order:", " -> ".join(tree.level_order()))

    # Supply BST.
    print("\n--- Supply Inventory (BST) ---")
    bst = SupplyBST()
    supplies = [
        (101, "Water Bottles", 500),
        (102, "Rice Bags", 200),
        (103, "Blankets", 150),
        (104, "Medicine Kits", 80),
        (105, "Tents", 60),
        (106, "Fuel Cans", 40),
        (107, "Batteries", 300),
    ]
    for sid, name, qty in supplies:
        bst.insert(sid, name, qty)
    print("Supplies (inorder):")
    for node in bst.inorder():
        print(f"  ID={node.key} | {node.item_name} | Qty={node.quantity}")
    print(f"BST height: {bst.height()}")

    # Road network.
    print("\n--- Road Network ---")
    g, _, depots = build_sample_graph()
    g.display_adj_list()

    # MST.
    print("\n--- Minimum Spanning Tree ---")
    pe, pc, _ = prim_mst(g)
    ke, kc, _ = kruskal_mst(g)
    print(f"Prim  cost: {pc}")
    print(f"Kruskal cost: {kc}")
    print(f"Agreement: {'Yes' if pc == kc else 'No'}")


if __name__ == "__main__":
    main()
