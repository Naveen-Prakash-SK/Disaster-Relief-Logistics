"""Scenario-aware console menus for all project data structures."""

import math
import os

from scenario import DATA_PATH, Scenario


def _text(prompt, empty=False):
    while True:
        value = input(prompt).strip()
        if value.lower() == "q":
            return None
        if value or empty:
            return value
        print("A value is required (or enter q to cancel).")


def _integer(prompt, minimum=None, maximum=None):
    while True:
        value = input(prompt).strip()
        if value.lower() == "q":
            return None
        try:
            result = int(value)
        except ValueError:
            print("Enter a whole number (or q to cancel).")
            continue
        if minimum is not None and result < minimum:
            print(f"Enter a number >= {minimum}.")
        elif maximum is not None and result > maximum:
            print(f"Enter a number <= {maximum}.")
        else:
            return result


def _number(prompt, minimum=None):
    while True:
        value = input(prompt).strip()
        if value.lower() == "q":
            return None
        try:
            result = float(value)
        except ValueError:
            print("Enter a numeric value (or q to cancel).")
            continue
        if not math.isfinite(result):
            print("Enter a finite numeric value.")
        elif minimum is not None and result < minimum:
            print(f"Enter a number >= {minimum}.")
        else:
            return result


def _confirm(prompt):
    return input(f"{prompt} [y/N]: ").strip().lower() in ("y", "yes")


def _inventory_shape(tree):
    if tree.root is None:
        print("Inventory is empty.")
        return
    print("Supply BST, shown by depth:")
    stack = [(tree.root, 0)]
    while stack:
        node, depth = stack.pop()
        print(f"{'  ' * depth}{node.key}: {node.item_name} "
              f"(quantity={node.quantity})")
        if node.right:
            stack.append((node.right, depth + 1))
        if node.left:
            stack.append((node.left, depth + 1))


def _menu(scenario):
    graph_type = "directed" if scenario.graph.directed else "undirected"
    print("\n" + "=" * 66)
    print("DISASTER RELIEF LOGISTICS — INTERACTIVE CONSOLE")
    print(f"Scenario: {scenario.network_name} | {graph_type} graph | "
          f"{scenario.graph.vertex_count()} vertices")
    print("=" * 66)
    entries = [
        "Guided disaster scenario builder",
        "Location hierarchy (General Tree)", "Supply inventory (BST)",
        "Relief camps (AVL) and expression calculator",
        "Build and view road network", "BFS nearest depot",
        "Dijkstra shortest route", "DFS and connectivity analysis",
        "Prim minimum spanning forest", "Kruskal minimum spanning forest",
        "Scheduling and critical path", "Benchmarking and performance analysis",
        "Save scenario", "Load scenario", "Reset scenario",
        "Testing and diagnostics",
    ]
    for index, label in enumerate(entries, 1):
        print(f"{index:2}. {label}")
    print("17. Exit")


def _builder_action(scenario):
    print("\n--- SCENARIO BUILDER ---")
    print("1. Guided disaster scenario builder")
    print("2. Load demonstration scenario")
    print("0. Return to main menu")
    choice = input("Choose an option: ").strip()
    if choice == "1":
        replacement = _guided_builder()
    elif choice == "2":
        if _has_data(scenario) and not _confirm(
                "Replace current scenario with demonstration data?"):
            print("Demonstration load cancelled.")
            return scenario
        return _sample()
    elif choice == "0":
        return scenario
    else:
        print("Choose a listed action.")
        return scenario
    if replacement is None:
        return scenario
    if _has_data(scenario) and not _confirm("Replace current scenario?"):
        return scenario
    return replacement


def _testing_menu():
    from tests import last_test_summary, run_tests

    while True:
        print("\n--- TESTING AND DIAGNOSTICS ---")
        print("1. Run all automated tests")
        print("2. Run tree tests")
        print("3. Run graph algorithm tests")
        print("4. Run scheduling tests")
        print("5. Run scenario persistence tests")
        print("6. View last test summary")
        print("7. Return to main menu")
        choice = input("Choose a testing action: ").strip()
        categories = {
            "1": None,
            "2": "tree",
            "3": "graph",
            "4": "scheduling",
            "5": "scenario",
        }
        if choice in categories:
            run_tests(categories[choice])
        elif choice == "6":
            summary = last_test_summary()
            if summary is None:
                print("No test run has been recorded in this session.")
            else:
                print(f"Last run: {summary['category']}")
                print(f"Tests: {summary['tests_run']}; passed: {summary['passed']}; "
                      f"failures: {summary['failures']}; errors: {summary['errors']}")
                print(f"Elapsed: {summary['seconds']:.3f}s; "
                      f"result: {'PASS' if summary['successful'] else 'FAIL'}")
        elif choice == "7":
            return
        else:
            print("Choose an option from 1 to 7.")


def _location_menu(scenario):
    tree = scenario.locations
    while True:
        print(f"\n--- LOCATION HIERARCHY: {tree.root.name} ---")
        print("1 Add region  2 Add district  3 Add shelter")
        print("4 Display  5 Traversals  6 Search  7 Delete subtree  0 Back")
        choice = input("Action: ").strip()
        try:
            if choice == "1":
                name = _text("Region name: ")
                if name is not None:
                    ok, message = tree.add_location(tree.root.name, name, "Region")
                    print(message)
                    if ok:
                        tree.display()
            elif choice in ("2", "3"):
                parent = _text("Parent name: ")
                name = _text("District name: " if choice == "2" else "Shelter name: ")
                if parent is not None and name is not None:
                    kind = "District" if choice == "2" else "Shelter"
                    ok, message = tree.add_location(parent, name, kind)
                    print(message)
                    if ok:
                        tree.display()
            elif choice == "4":
                tree.display()
            elif choice == "5":
                print("Preorder:   ", " -> ".join(tree.preorder()))
                print("Postorder:  ", " -> ".join(tree.postorder()))
                print("Level-order:", " -> ".join(tree.level_order()))
            elif choice == "6":
                name = _text("Location name: ")
                if name is not None:
                    node = tree.find(name)
                    print(f"Found {node!r}." if node else "Location not found.")
            elif choice == "7":
                name = _text("Location/subtree to delete: ")
                if name is not None:
                    ok, message = tree.delete_subtree(name)
                    print(message)
                    if ok:
                        tree.display()
            elif choice in ("0", "q"):
                return
            else:
                print("Choose a listed action.")
        except (ValueError, RecursionError) as exc:
            print(f"Action failed: {exc}")


def _supply_menu(scenario):
    tree = scenario.supplies
    while True:
        print("\n--- SUPPLY INVENTORY (BST) ---")
        print("1 Insert/update  2 Search  3 Delete  4 Min/max")
        print("5 Range  6 Inorder  7 Tree shape/height  0 Back")
        choice = input("Action: ").strip()
        try:
            if choice == "1":
                key = _integer("Supply ID: ")
                name = _text("Supply name: ")
                quantity = _integer("Quantity (>=0): ", minimum=0)
                if key is not None and name is not None and quantity is not None:
                    existed = tree.search(key) is not None
                    tree.insert(key, name, quantity)
                    print("Supply updated." if existed else "Supply added.")
                    _inventory_shape(tree)
            elif choice == "2":
                key = _integer("Supply ID to find: ")
                if key is not None:
                    node = tree.search(key)
                    print(f"{node.key}: {node.item_name}, quantity={node.quantity}"
                          if node else "Supply ID not found.")
            elif choice == "3":
                key = _integer("Supply ID to delete: ")
                if key is not None:
                    print("Deleted." if tree.delete(key) else "Supply ID not found.")
                    _inventory_shape(tree)
            elif choice == "4":
                for label, node in (("Minimum", tree.minimum()),
                                    ("Maximum", tree.maximum())):
                    print(f"{label}: {node.key} {node.item_name} qty={node.quantity}"
                          if node else f"{label}: no supplies.")
            elif choice == "5":
                low = _integer("Inclusive low ID: ")
                high = _integer("Inclusive high ID: ")
                if low is not None and high is not None:
                    rows = tree.range_query(low, high)
                    for node in rows:
                        print(f"{node.key}: {node.item_name} qty={node.quantity}")
                    if not rows:
                        print("No matching supplies.")
            elif choice == "6":
                rows = tree.inorder_iterative()
                for node in rows:
                    print(f"{node.key}: {node.item_name} qty={node.quantity}")
                if not rows:
                    print("Inventory is empty.")
            elif choice == "7":
                _inventory_shape(tree)
                print(f"Height (nodes): {tree.height()}")
            elif choice in ("0", "q"):
                return
            else:
                print("Choose a listed action.")
        except (ValueError, RecursionError) as exc:
            print(f"Action failed: {exc}")


def _expression_calc():
    from avl_expression import (
        build_expression_tree, evaluate_expression, infix_string, infix_to_postfix,
    )
    print("Enter an infix expression; variables are prompted for as needed.")
    text = _text("Expression (for example: distance * rate + toll): ")
    if text is None:
        return
    try:
        postfix = infix_to_postfix(text)
        root = build_expression_tree(postfix)
        print("Postfix:", " ".join(postfix))
        print("Expression tree:", infix_string(root))
        variables = {}
        for token in postfix:
            if token in ("+", "-", "*", "/", "neg"):
                continue
            try:
                float(token)
            except ValueError:
                if token not in variables:
                    value = _number(f"Value for {token}: ")
                    if value is None:
                        return
                    variables[token] = value
        print("Calculated result:", evaluate_expression(root, variables))
    except ValueError as exc:
        print(f"Expression error: {exc}")


def _avl_menu(scenario):
    from avl_expression import AVLTree
    tree = scenario.camps
    while True:
        print("\n--- RELIEF CAMPS (AVL) ---")
        print("1 Add/update  2 Search  3 Delete  4 Display/balance")
        print("5 Rotation log  6 Expression calculator  7 Stress test  0 Back")
        choice = input("Action: ").strip()
        try:
            if choice == "1":
                key = _integer("Camp ID: ")
                name = _text("Camp name: ")
                if key is not None and name is not None:
                    tree.insert(key, name)
                    print(f"Stored camp {key}; AVL height={tree.height()}.")
                    tree.display()
                    print(tree.verify()[1])
                    if tree.rotation_log:
                        print("Most recent rotation:", tree.rotation_log[-1])
            elif choice == "2":
                key = _integer("Camp ID: ")
                if key is not None:
                    node = tree.search(key)
                    print(f"{node.key}: {node.value}" if node else "Camp not found.")
            elif choice == "3":
                key = _integer("Camp ID to delete: ")
                if key is not None:
                    print("Deleted." if tree.delete(key) else "Camp not found.")
                    print(f"New height: {tree.height()}")
                    tree.display()
                    print(tree.verify()[1])
            elif choice == "4":
                if not tree.root:
                    print("No camps entered.")
                stack = [(tree.root, 0)] if tree.root else []
                while stack:
                    node, depth = stack.pop()
                    print(f"{'  ' * depth}{node.key}: {node.value}, "
                          f"height={node.height}, balance={tree._bf(node)}")
                    if node.right:
                        stack.append((node.right, depth + 1))
                    if node.left:
                        stack.append((node.left, depth + 1))
            elif choice == "5":
                print("\n".join(tree.rotation_log) if tree.rotation_log
                      else "No rotations recorded yet.")
            elif choice == "6":
                _expression_calc()
            elif choice == "7":
                result, passed, total = AVLTree.random_stress_test(10000, 42)
                print(f"AVL checks: {passed}/{total}; height={result.height()}.")
            elif choice in ("0", "q"):
                return
            else:
                print("Choose a listed action.")
        except (ValueError, RecursionError) as exc:
            print(f"Action failed: {exc}")


def _graph_menu(scenario):
    from graph import (
        connected_components_undirected, scc_kosaraju,
    )
    graph = scenario.graph
    while True:
        kind = "directed" if graph.directed else "undirected"
        print(f"\n--- ROAD GRAPH ({kind}; V={graph.vertex_count()}, E={graph.edge_count()}) ---")
        print("1 Add vertex  2 Remove vertex  3 Add/update edge  4 Remove edge")
        print("5 Adjacency list  6 Matrix  7 Components/isolation/memory")
        print("8 Change directedness  0 Back")
        choice = input("Action: ").strip()
        try:
            if choice == "1":
                name = _text("Vertex name: ")
                if name is not None:
                    exists = name in graph.adj_list
                    graph.add_vertex(name)
                    print("Already present." if exists else "Vertex added.")
            elif choice == "2":
                name = _text("Vertex to remove: ")
                if name is not None:
                    removed = graph.remove_vertex(name)
                    scenario.depots = [depot for depot in scenario.depots
                                       if depot != name]
                    print("Vertex and its roads removed." if removed
                          else "Vertex not found.")
            elif choice == "3":
                source = _text("From vertex (auto-created): ")
                target = _text("To vertex (auto-created): ")
                if source is None or target is None:
                    continue
                unweighted = input("Unweighted edge (weight 1)? [y/N]: ").strip().lower()
                weight = 1 if unweighted in ("y", "yes") else _number("Edge weight: ")
                if weight is not None:
                    graph.add_edge(source, target, weight)
                    print(f"Stored {source} -> {target}, weight={weight}.")
            elif choice == "4":
                source = _text("From vertex: ")
                target = _text("To vertex: ")
                if source is not None and target is not None:
                    existed = graph.has_edge(source, target)
                    graph.remove_edge(source, target)
                    print("Road removed." if existed else "Road not found.")
            elif choice == "5":
                graph.display_adj_list()
            elif choice == "6":
                graph.display_adj_matrix()
            elif choice == "7":
                components = (scc_kosaraju(graph) if graph.directed else
                              connected_components_undirected(graph))
                print(f"{'Strongly connected' if graph.directed else 'Connected'} components:")
                for group in components:
                    print("  " + ", ".join(group))
                print("Isolated vertices:", ", ".join(
                    vertex for vertex in graph.vertices
                    if not graph.adj_list[vertex]) or "(none)")
                graph.memory_report()
            elif choice == "8":
                directed = input("Directed? [y/N]: ").strip().lower() in ("y", "yes")
                if directed == graph.directed:
                    print("The graph already has that directedness.")
                    continue
                if graph.directed and not directed:
                    print("Warning: each directed road becomes bidirectional. "
                          "Opposing roads must have matching weights.")
                if graph.edge_count() and not _confirm(
                        "Convert active graph and copy its edges?"):
                    continue
                replacement = _converted_graph(graph, directed)
                scenario.graph = graph = replacement
                print("Graph representation changed. MST needs an undirected graph.")
            elif choice in ("0", "q"):
                return
            else:
                print("Choose a listed action.")
        except (ValueError, TypeError) as exc:
            print(f"Graph action failed: {exc}")


def _converted_graph(graph, directed):
    from graph import Graph

    replacement = Graph(directed=directed)
    for vertex in graph.vertices:
        replacement.add_vertex(vertex)

    edges = graph.all_edges()
    if graph.directed and not directed:
        undirected_edges = {}
        for source, target, weight in edges:
            key = tuple(sorted((source, target)))
            if key in undirected_edges and undirected_edges[key] != weight:
                raise ValueError(
                    f"Cannot merge {source!r} and {target!r}: "
                    "opposing road weights differ.")
            undirected_edges[key] = weight
        for (source, target), weight in undirected_edges.items():
            replacement.add_edge(source, target, weight)
    else:
        for source, target, weight in edges:
            replacement.add_edge(source, target, weight)
            if directed and not graph.directed:
                replacement.add_edge(target, source, weight)
    return replacement


def _bfs(scenario):
    from graph import bfs_nearest_depot, bfs_path
    graph = scenario.graph
    print("BFS minimizes the number of edges, not total edge weight.")
    print("Vertices:", ", ".join(graph.vertices) or "(empty)")
    source = _text("Starting location: ")
    if source is None:
        return
    if source not in graph.adj_list:
        print(f"Unknown start vertex '{source}'.")
        return
    raw = input("Depot vertices (comma-separated; blank uses saved depots): ").strip()
    depots = ([item.strip() for item in raw.split(",") if item.strip()]
              if raw else scenario.depots)
    if not depots:
        print("No depots selected or saved.")
        return
    missing = [depot for depot in depots if depot not in graph.adj_list]
    if missing:
        print("Not graph vertices:", ", ".join(missing))
        return
    depot, path, edges = bfs_nearest_depot(graph, source, depots)
    if depot is None:
        print("No selected depot is reachable.")
    else:
        print(f"Nearest depot: {depot}, edge count={edges}")
        print("Route:", " -> ".join(path))
    target = _text("Optional destination to route to (blank skips): ", empty=True)
    if target:
        if target not in graph.adj_list:
            print("Destination is not a graph vertex.")
        else:
            path, length = bfs_path(graph, source, target)
            print(f"Route: {' -> '.join(path)} ({length} edges)"
                  if path else "Destination is unreachable.")


def _dijkstra(scenario):
    from graph import INF, dijkstra, dijkstra_path, demonstrate_negative_weight_failure
    graph = scenario.graph
    source = _text("Source vertex: ")
    target = _text("Destination vertex: ")
    if source is None or target is None:
        return
    if source not in graph.adj_list or target not in graph.adj_list:
        print("Source and destination must be existing vertices.")
        return
    try:
        distances, parents = dijkstra(graph, source, verbose=True)
    except ValueError as exc:
        print(f"Dijkstra rejected this graph: {exc}")
        print("The algorithm's result is not valid when negative edges exist.")
        if _confirm("Show the negative-edge failure explanation?"):
            demonstrate_negative_weight_failure()
        return
    print("\nFinal distance table:")
    for vertex in graph.vertices:
        dist = distances[vertex]
        print(f"{vertex:>20} | {dist if dist != INF else 'unreachable':>12} "
              f"| predecessor={parents[vertex]}")
    path, distance = dijkstra_path(graph, source, target)
    print(f"Shortest route: {' -> '.join(path)} (weight {distance})"
          if path else "Destination is unreachable.")


def _dfs(scenario):
    from graph import (
        connected_components_undirected, dfs_full, scc_kosaraju,
    )
    graph = scenario.graph
    if not graph.vertices:
        print("The graph is empty.")
        return
    start = _text("Start vertex (blank means all components): ", empty=True)
    if start is None:
        return
    if start and start not in graph.adj_list:
        print("Unknown start vertex.")
        return
    discovery, finish, parent, types, order = dfs_full(graph, start=start or None)
    print("DFS order:", " -> ".join(order))
    for vertex in order:
        print(f"{vertex}: discover={discovery[vertex]}, finish={finish[vertex]}, "
              f"parent={parent[vertex]}")
    print("Edge classification:")
    for edge, kind in types.items():
        print(f"  {edge[0]} -> {edge[1]}: {kind}")
    groups = (scc_kosaraju(graph) if graph.directed else
              connected_components_undirected(graph))
    print("Strongly connected components:" if graph.directed
          else "Connected components:")
    for group in groups:
        print("  " + ", ".join(group))
    print("Isolated vertices:", ", ".join(
        v for v in graph.vertices if not graph.adj_list[v]) or "(none)")


def _mst(scenario, algorithm):
    from mst import (
        DisjointSet, kruskal_mst, merge_sort_edges, prim_mst,
    )
    graph = scenario.graph
    if graph.directed:
        print("MST algorithms require an undirected graph.")
        return
    if algorithm == "Prim":
        edges, cost, components = prim_mst(graph)
        running = 0
        print("Prim selects the cheapest edge connecting the current tree to an unvisited vertex.")
        for source, target, weight in edges:
            running += weight
            print(f"Select {source} -- {target} ({weight}); running total={running}")
    else:
        edges, cost, components = kruskal_mst(graph)
        print("Kruskal accepts edges that join different components.")
        sets = DisjointSet(graph.vertices)
        running = 0
        for source, target, weight in merge_sort_edges(graph.all_edges()):
            if sets.union(source, target):
                running += weight
                print(f"Select {source} -- {target} ({weight}); running total={running}")
            else:
                print(f"Reject {source} -- {target} ({weight}); would form a cycle")
    comparison_edges, comparison_cost, _ = (
        kruskal_mst(graph) if algorithm == "Prim" else prim_mst(graph)
    )
    print(f"{algorithm}: {len(edges)} edges, total weight={cost}.")
    other = "Kruskal" if algorithm == "Prim" else "Prim"
    print(f"{other}: {len(comparison_edges)} edges, "
          f"total weight={comparison_cost}; costs "
          f"{'agree' if cost == comparison_cost else 'differ'}.")
    print(f"Forest components: {len(components)}")
    for component in components:
        print("  " + ", ".join(component))
    print("Disconnected graph: this is a minimum spanning forest."
          if len(components) > 1 else "Connected graph: this is a spanning tree.")


def _schedule(scenario):
    from scheduling import (
        critical_path, detect_cycle, earliest_start_times,
        topological_sort_dfs, topological_sort_kahn,
    )
    dag = scenario.tasks
    while True:
        print("\n--- SCHEDULING ---")
        print("1 Add/update task  2 Add prerequisite  3 List dependencies")
        print("4 Both topological sorts  5 Timings/critical path  6 Cycle check  0 Back")
        choice = input("Action: ").strip()
        try:
            if choice == "1":
                name = _text("Task name: ")
                duration = _number("Duration >= 0: ", minimum=0)
                if name is not None and duration is not None:
                    dag.add_task(name, duration)
                    print(f"Stored task '{name}'.")
            elif choice == "2":
                before = _text("Prerequisite task: ")
                after = _text("Dependent task: ")
                if before is not None and after is not None:
                    if before not in dag._index or after not in dag._index:
                        print("Add both tasks with durations before linking them.")
                        continue
                    dag.add_dependency(before, after)
                    print(f"Stored dependency {before} -> {after}.")
            elif choice == "3":
                for task in dag.tasks:
                    print(f"{task} ({dag.duration[task]}) -> "
                          f"{', '.join(dag.adj[task]) or '(none)'}")
                if not dag.tasks:
                    print("No tasks have been entered.")
            elif choice == "4":
                ko, kv = topological_sort_kahn(dag)
                do, dv, cycle = topological_sort_dfs(dag)
                print("Kahn:", " -> ".join(ko) or "(empty)")
                print("DFS: ", " -> ".join(do) or "(empty)")
                print("Valid schedule." if kv and dv else
                      "No valid schedule; cycle: " + " -> ".join(cycle))
            elif choice == "5":
                if not dag.tasks:
                    print("Add tasks first.")
                    continue
                path, total, starts = critical_path(dag)
                _, order = earliest_start_times(dag)
                for task in order:
                    print(f"{task}: start={starts[task]}, "
                          f"finish={starts[task] + dag.duration[task]}")
                print(f"Critical path: {' -> '.join(path)}; duration={total}.")
            elif choice == "6":
                found, cycle = detect_cycle(dag)
                print("Cycle: " + " -> ".join(cycle) if found
                      else "No cycle; the dependency schedule is feasible.")
            elif choice in ("0", "q"):
                return
            else:
                print("Choose a listed action.")
        except ValueError as exc:
            print(f"Schedule error: {exc}")


def _benchmarks():
    from analysis import (
        run_graph_benchmarks, run_tree_benchmarks, save_benchmark_results,
    )
    print("Timings are empirical, single-run samples; reported complexity is theoretical.")
    print("Limits: 5,000 tree nodes; 500 graph vertices.")
    try:
        tree_input = input("Tree sizes comma-separated [1000,2000,5000]: ").strip()
        graph_input = input("Graph vertex sizes [100,250,500]: ").strip()
        tree_sizes = ([int(x.strip()) for x in tree_input.split(",")]
                      if tree_input else [1000, 2000, 5000])
        graph_sizes = ([int(x.strip()) for x in graph_input.split(",")]
                       if graph_input else [100, 250, 500])
        if any(not 1 <= size <= 5000 for size in tree_sizes):
            raise ValueError("Tree sizes must be from 1 through 5000.")
        if any(not 2 <= size <= 500 for size in graph_sizes):
            raise ValueError("Graph sizes must be from 2 through 500.")
    except ValueError as exc:
        print(f"Invalid size: {exc}")
        return
    seed = _integer("Seed [42]: ", minimum=0)
    tree_rows = run_tree_benchmarks(tree_sizes, seed=42 if seed is None else seed)
    graph_rows = run_graph_benchmarks(graph_sizes, seed=42 if seed is None else seed)
    save_benchmark_results(tree_rows, graph_rows, seed=42 if seed is None else seed)


def _guided_builder():
    from graph import Graph
    result_name = _text("Network name: ")
    if result_name is None:
        return None
    result = Scenario(result_name)

    def locations_under(parent, kind, count):
        for _ in range(count):
            name = _text(f"{kind} under {parent}: ")
            if name is None:
                raise InterruptedError
            ok, message = result.locations.add_location(parent, name, kind)
            if not ok:
                raise ValueError(message)
            if kind == "Region":
                count_d = _integer(f"District count in {name}: ", minimum=0)
                if count_d is None:
                    raise InterruptedError
                locations_under(name, "District", count_d)
            elif kind == "District":
                count_s = _integer(f"Shelter count in {name}: ", minimum=0)
                if count_s is None:
                    raise InterruptedError
                locations_under(name, "Shelter", count_s)

    try:
        count = _integer("Region count: ", minimum=0)
        if count is None:
            return None
        locations_under(result.locations.root.name, "Region", count)
        count = _integer("Supply record count: ", minimum=0)
        if count is None:
            return None
        for _ in range(count):
            key = _integer("Supply ID: ")
            name = _text("Supply name: ")
            quantity = _integer("Quantity >= 0: ", minimum=0)
            if key is None or name is None or quantity is None:
                raise InterruptedError
            if result.supplies.search(key):
                raise ValueError(f"Duplicate supply ID {key}.")
            result.supplies.insert(key, name, quantity)
        count = _integer("Relief camp count: ", minimum=0)
        if count is None:
            return None
        for _ in range(count):
            key = _integer("Camp ID: ")
            name = _text("Camp name: ")
            if key is None or name is None:
                raise InterruptedError
            if result.camps.search(key):
                raise ValueError(f"Duplicate camp ID {key}.")
            result.camps.insert(key, name)
        directed = input("Directed road graph? [y/N]: ").strip().lower() in ("y", "yes")
        result.graph = Graph(directed=directed)
        count = _integer("Road-graph vertex count (max 1000): ",
                         minimum=0, maximum=1000)
        if count is None:
            return None
        for _ in range(count):
            vertex = _text("Vertex name: ")
            if vertex is None:
                raise InterruptedError
            if vertex in result.graph.adj_list:
                raise ValueError(f"Duplicate graph vertex '{vertex}'.")
            result.graph.add_vertex(vertex)
        count = _integer("Road/connection count (max 100000): ",
                         minimum=0, maximum=100000)
        if count is None:
            return None
        for _ in range(count):
            source = _text("From vertex: ")
            target = _text("To vertex: ")
            weight = _number("Weight: ")
            if source is None or target is None or weight is None:
                raise InterruptedError
            if source not in result.graph.adj_list or target not in result.graph.adj_list:
                raise ValueError("Both edge endpoints must be entered graph vertices.")
            result.graph.add_edge(source, target, weight)
        count = _integer("Depot count: ", minimum=0)
        if count is None:
            return None
        for _ in range(count):
            depot = _text("Depot vertex: ")
            if depot is None:
                raise InterruptedError
            if depot not in result.graph.adj_list:
                raise ValueError(f"Depot '{depot}' is not a graph vertex.")
            if depot in result.depots:
                raise ValueError(f"Duplicate depot '{depot}'.")
            result.depots.append(depot)
        count = _integer("Task count: ", minimum=0)
        if count is None:
            return None
        for _ in range(count):
            name = _text("Task name: ")
            duration = _number("Task duration >= 0: ", minimum=0)
            if name is None or duration is None:
                raise InterruptedError
            if name in result.tasks._index:
                raise ValueError(f"Duplicate task '{name}'.")
            result.tasks.add_task(name, duration)
        count = _integer("Dependency count: ", minimum=0)
        if count is None:
            return None
        for _ in range(count):
            before = _text("Prerequisite task: ")
            after = _text("Dependent task: ")
            if before is None or after is None:
                raise InterruptedError
            if before not in result.tasks._index or after not in result.tasks._index:
                raise ValueError("Dependencies must refer to entered tasks.")
            result.tasks.add_dependency(before, after)
    except InterruptedError:
        print("Entry cancelled; active scenario was preserved.")
        return None
    except ValueError as exc:
        print(f"Scenario rejected; active scenario was preserved: {exc}")
        return None
    print(f"Created scenario '{result.network_name}'.")
    return result


def _has_data(scenario):
    return bool(scenario.locations.root.children or scenario.supplies.root
                or scenario.camps.root or scenario.graph.vertices
                or scenario.tasks.tasks)


def _save(scenario):
    overwrite = False
    if os.path.exists(DATA_PATH):
        if not _confirm(f"Overwrite existing '{DATA_PATH}'?"):
            print("Save cancelled.")
            return
        overwrite = True
    try:
        scenario.save(DATA_PATH, overwrite=overwrite)
        print(f"Saved scenario to {DATA_PATH}.")
    except (OSError, ValueError) as exc:
        print(f"Save failed: {exc}")


def _load(scenario):
    if _has_data(scenario) and not _confirm("Replace current in-memory scenario?"):
        return scenario
    try:
        result = Scenario.load(DATA_PATH)
        print(f"Loaded '{result.network_name}' from {DATA_PATH}.")
        return result
    except (OSError, ValueError) as exc:
        print(f"Load failed; active scenario is unchanged: {exc}")
        return scenario


def _sample():
    sample = Scenario.sample()
    print("Loaded demonstration data into the active scenario.")
    print("Sample data (not user-entered):")
    sample.locations.display()
    print(f"Supply records: {len(sample.supplies.inorder_iterative())}")
    print(f"Relief camps: {len(sample.camps.inorder())}")
    print(f"Road graph: V={sample.graph.vertex_count()}, "
          f"E={sample.graph.edge_count()}, depots={', '.join(sample.depots)}")
    print(f"Tasks: {', '.join(sample.tasks.tasks)}")
    return sample


def _reset(scenario):
    if not _confirm("Discard all in-memory data?"):
        print("Reset cancelled.")
        return scenario
    name = _text("New network name: ")
    return Scenario(name or "Disaster Relief Network")


def main():
    scenario = Scenario()
    while True:
        _menu(scenario)
        choice = input("Choose an option: ").strip()
        try:
            if choice == "1":
                scenario = _builder_action(scenario)
            elif choice == "2":
                _location_menu(scenario)
            elif choice == "3":
                _supply_menu(scenario)
            elif choice == "4":
                _avl_menu(scenario)
            elif choice == "5":
                _graph_menu(scenario)
            elif choice == "6":
                _bfs(scenario)
            elif choice == "7":
                _dijkstra(scenario)
            elif choice == "8":
                _dfs(scenario)
            elif choice == "9":
                _mst(scenario, "Prim")
            elif choice == "10":
                _mst(scenario, "Kruskal")
            elif choice == "11":
                _schedule(scenario)
            elif choice == "12":
                _benchmarks()
            elif choice == "13":
                _save(scenario)
            elif choice == "14":
                scenario = _load(scenario)
            elif choice == "15":
                scenario = _reset(scenario)
            elif choice == "16":
                _testing_menu()
            elif choice == "17":
                print("Exiting Disaster Relief Logistics. Goodbye!")
                return
            else:
                print("Choose an option from 1 to 17.")
        except (ValueError, OSError, RecursionError) as exc:
            print(f"Action failed: {exc}")
