# Disaster Relief Logistics System

A console-based Data Structures and Algorithms project developed for **DSA Assignment II** at **KPR Institute of Engineering and Technology**.

The system simulates disaster-relief operations using tree structures, graph algorithms, scheduling, and performance analysis. Users can enter their own scenario, execute algorithms on the entered data, and save or reload scenarios using JSON.

## Features

### 1. Location Hierarchy — General Tree
- Create a hierarchy of regions, districts, and shelters.
- Insert, search, and delete locations where supported.
- Display preorder, postorder, and level-order traversals.

### 2. Supply Inventory — Binary Search Tree
- Add and search supply records using unique IDs.
- Update quantities and delete records.
- Find minimum and maximum IDs.
- Perform range queries and inorder traversal.
- Demonstrate the performance limitations of an unbalanced BST.

### 3. Relief-Camp Index — AVL Tree
- Insert, search, and delete camp records.
- Maintain balance using AVL rotations.
- Inspect tree height and balancing behaviour.

### 4. Expression Tree
- Parse and evaluate mathematical expressions.
- Display infix expressions while preserving grouping.
- Handle invalid expressions, undefined variables, and division by zero.

### 5. Graph and Route Planning
- Construct directed or undirected graphs.
- Add and remove connections and inspect adjacency lists and matrices.
- Compare adjacency-list and adjacency-matrix representations.

### 6. Graph Algorithms
- **BFS:** Find routes with the fewest edges and locate the nearest reachable depot.
- **DFS:** Analyse traversal timestamps, edge classifications, and connectivity.
- **Dijkstra:** Calculate weighted shortest paths and display distance tables.
- **Prim and Kruskal:** Construct minimum spanning trees or minimum spanning forests.
- **Union-Find:** Support efficient component merging and cycle checks.

### 7. Scheduling and Critical Path
- Model tasks, durations, and dependencies.
- Perform topological sorting using Kahn's algorithm and DFS.
- Detect dependency cycles.
- Calculate earliest start and finish times and the critical path where supported.

### 8. Scenario Builder and Persistence
- Enter a custom disaster-relief scenario.
- Reuse scenario data across supported structures and algorithms.
- Save and load scenario data using JSON.
- Validate input and handle missing or malformed saved data.

### 9. Benchmarking and Analysis
- Compare BST and AVL behaviour on sorted and random inputs.
- Compare Prim and Kruskal on sparse and dense graphs.
- Record reproducible benchmark workloads using a seed.
- Generate CSV results and benchmark summaries.

### 10. Testing and Diagnostics
- Run the automated test suite from a dedicated testing submenu.
- Run available tree, graph, scheduling, and persistence test groups.
- Inspect actual test results and diagnose failures.

## Technology

- **Language:** Python
- **Data storage:** JSON for saved scenarios
- **Testing:** Python `unittest`
- **Benchmark output:** CSV and Markdown summaries

The project uses manually implemented data structures and algorithms for the assignment requirements rather than relying on external graph or priority-queue libraries.

## Project Structure

```text
DisasterReliefLogistics/
├── main.py
├── console_app.py
├── scenario.py
├── trees.py
├── avl_expression.py
├── graph.py
├── mst.py
├── scheduling.py
├── analysis.py
├── tests.py
├── data/
├── docs/
├── report/
├── results/
├── README.md
└── .gitignore
```

## Installation and Execution

Python 3 is required.

Clone the repository:

```bash
git clone https://github.com/Naveen-Prakash-SK/Disaster-Relief-Logistics.git
cd Disaster-Relief-Logistics
```

Start the application:

```bash
python main.py
```

Run the complete automated test suite:

```bash
python -m unittest -v
```

## Using the Application

1. Start the application.
2. Create a new disaster-relief scenario or use the available sample scenario.
3. Enter locations, supplies, roads, depots, and task dependencies as prompted.
4. Run the relevant tree, graph, or scheduling algorithms.
5. Inspect the computed routes, traversals, spanning forests, and scheduling results.
6. Save the scenario if you want to reuse it later.
7. Open **Testing and Diagnostics** to run automated tests.

The exact options depend on the current application implementation.

## Algorithmic Analysis

The project studies the following theoretical complexities:

| Algorithm or structure | Expected or worst-case time |
|---|---|
| General tree traversal | \(O(n)\) |
| BST search, insertion, deletion | Average \(O(\log n)\); worst \(O(n)\) |
| AVL search, insertion, deletion | \(O(\log n)\) |
| BFS and DFS | \(O(V+E)\) with adjacency lists |
| Array-based Dijkstra | \(O(V^2+E)\) |
| Array-based Prim | \(O(V^2)\) for the array-scan implementation |
| Kruskal | \(O(E\log E)\), dominated by edge sorting |
| Topological sorting | \(O(V+E)\) |

These are theoretical bounds under the corresponding algorithm and representation assumptions. Empirical benchmark timings can vary by machine and workload.

## Reports and Documentation

See the `docs/` directory for function explanations and the `report/` and `results/` directories for project documentation, test reports, and benchmark outputs.

## Team Members

- 25AD101
- 25AD105
- 25AD116
- 25AD203

## Academic Project

**Institution:** KPR Institute of Engineering and Technology  
**Department:** Artificial Intelligence and Data Science  
**Course:** Data Structures and Algorithms  
**Project:** Disaster Relief Logistics System

---

