"""Topological Sorting, Cycle Detection and Critical Path.

- Kahn's algorithm (BFS-based topological sort)
- DFS-based topological sort
- Cycle detection with cycle reporting
- Earliest start time and critical path (longest path in a DAG)
"""


# ============================================================================
# TASK DAG REPRESENTATION
# ============================================================================

class TaskDAG:
    """Directed graph of tasks with durations, used for scheduling."""

    def __init__(self):
        self.tasks = []                 # ordered list of task labels
        self._index = {}                # label -> position
        self.adj = {}                   # task -> [successor tasks]
        self.duration = {}              # task -> duration

    def add_task(self, label, duration=1):
        if label in self._index:
            self.duration[label] = duration
            return
        self._index[label] = len(self.tasks)
        self.tasks.append(label)
        self.adj[label] = []
        self.duration[label] = duration

    def add_dependency(self, prerequisite, task):
        """prerequisite must finish before task can start."""
        for t in (prerequisite, task):
            if t not in self._index:
                self.add_task(t)
        if task not in self.adj[prerequisite]:
            self.adj[prerequisite].append(task)

    def in_degree(self):
        deg = {t: 0 for t in self.tasks}
        for u in self.tasks:
            for v in self.adj[u]:
                deg[v] += 1
        return deg


# ============================================================================
# TOPOLOGICAL SORT — KAHN'S ALGORITHM (BFS)
# ============================================================================

def topological_sort_kahn(dag):
    """Kahn's BFS-based topological sort.
    Returns (order, is_dag).
    If a cycle exists, order will be partial and is_dag will be False.
    """
    in_deg = dag.in_degree()
    queue = [t for t in dag.tasks if in_deg[t] == 0]
    front = 0
    order = []

    while front < len(queue):
        u = queue[front]
        front += 1
        order.append(u)
        for v in dag.adj[u]:
            in_deg[v] -= 1
            if in_deg[v] == 0:
                queue.append(v)

    is_dag = len(order) == len(dag.tasks)
    return order, is_dag


# ============================================================================
# TOPOLOGICAL SORT — DFS
# ============================================================================

def topological_sort_dfs(dag):
    """DFS-based topological sort.
    Returns (order, is_dag, cycle_if_any).
    cycle_if_any is a list of task labels forming the cycle (if detected).
    """
    WHITE, GRAY, BLACK = 0, 1, 2
    color = {t: WHITE for t in dag.tasks}
    order = []
    parent = {t: None for t in dag.tasks}
    cycle = []

    def _dfs(u):
        color[u] = GRAY
        for v in dag.adj[u]:
            if color[v] == GRAY:
                # Back edge found — extract cycle.
                cyc = [v, u]
                p = u
                while p != v:
                    p = parent[p]
                    if p is None:
                        break
                    cyc.append(p)
                cyc.reverse()
                cycle.extend(cyc)
                return False
            if color[v] == WHITE:
                parent[v] = u
                if not _dfs(v):
                    return False
        color[u] = BLACK
        order.append(u)
        return True

    for t in dag.tasks:
        if color[t] == WHITE:
            if not _dfs(t):
                return [], False, cycle

    order.reverse()
    return order, True, []


# ============================================================================
# CYCLE DETECTION
# ============================================================================

def detect_cycle(dag):
    """Detect a cycle and return (has_cycle, cycle_path)."""
    _, is_dag, cycle = topological_sort_dfs(dag)
    if is_dag:
        return False, []
    return True, cycle


# ============================================================================
# EARLIEST START TIME AND CRITICAL PATH
# ============================================================================

def earliest_start_times(dag):
    """Compute earliest start time for each task in a DAG.
    Returns (est_dict, order) or raises ValueError if a cycle exists.
    """
    order, is_dag = topological_sort_kahn(dag)
    if not is_dag:
        raise ValueError("Cycle detected — cannot compute earliest "
                         "start times.")
    est = {t: 0 for t in dag.tasks}
    for u in order:
        for v in dag.adj[u]:
            candidate = est[u] + dag.duration[u]
            if candidate > est[v]:
                est[v] = candidate
    return est, order


def critical_path(dag):
    """Compute the critical path (longest path) in a DAG.
    Returns (path, total_duration, est_dict).
    """
    if not dag.tasks:
        return [], 0, {}
    est, order = earliest_start_times(dag)
    # The task with the highest (est + duration) finishes last.
    end_times = {t: est[t] + dag.duration[t] for t in dag.tasks}
    last_task = max(dag.tasks, key=lambda t: end_times[t])
    total_duration = end_times[last_task]

    # Trace the critical path backwards.
    predecessors = {task: [] for task in dag.tasks}
    for source in dag.tasks:
        for target in dag.adj[source]:
            predecessors[target].append(source)
    path = [last_task]
    current = last_task
    while True:
        # Find a predecessor on the critical path.
        found = False
        for predecessor in predecessors[current]:
            if est[predecessor] + dag.duration[predecessor] == est[current]:
                path.append(predecessor)
                current = predecessor
                found = True
                break
        if not found:
            break

    path.reverse()
    return path, total_duration, est


# ============================================================================
# SAMPLE DATA
# ============================================================================

def build_sample_acyclic_dag():
    """An acyclic task dependency graph with durations.
    Represents relief operation phases.
    """
    dag = TaskDAG()
    tasks_data = [
        ("AssessDamage",    3),
        ("SecureArea",      2),
        ("SetupComms",      1),
        ("DeployTeams",     4),
        ("DistributeFood",  5),
        ("MedicalAid",      3),
        ("BuildShelters",   6),
        ("RestorePower",    4),
        ("FinalReport",     2),
    ]
    for label, dur in tasks_data:
        dag.add_task(label, dur)

    dependencies = [
        ("AssessDamage", "SecureArea"),
        ("AssessDamage", "SetupComms"),
        ("SecureArea", "DeployTeams"),
        ("SetupComms", "DeployTeams"),
        ("DeployTeams", "DistributeFood"),
        ("DeployTeams", "MedicalAid"),
        ("DeployTeams", "BuildShelters"),
        ("DistributeFood", "RestorePower"),
        ("MedicalAid", "RestorePower"),
        ("BuildShelters", "FinalReport"),
        ("RestorePower", "FinalReport"),
    ]
    for pre, task in dependencies:
        dag.add_dependency(pre, task)

    return dag


def build_sample_cyclic_dag():
    """A dependency graph that deliberately contains a cycle."""
    dag = TaskDAG()
    for label, dur in [("A", 2), ("B", 3), ("C", 1), ("D", 4)]:
        dag.add_task(label, dur)
    dag.add_dependency("A", "B")
    dag.add_dependency("B", "C")
    dag.add_dependency("C", "A")   # creates cycle A -> B -> C -> A
    dag.add_dependency("A", "D")
    return dag


# ============================================================================
# Console menu
# ============================================================================

def scheduling_menu():
    """Interactive scheduling menu."""
    acyclic = build_sample_acyclic_dag()
    cyclic = build_sample_cyclic_dag()

    while True:
        print("\n--- SCHEDULING AND CRITICAL PATH ---")
        print("1. Topological sort (Kahn) — acyclic example")
        print("2. Topological sort (DFS) — acyclic example")
        print("3. Detect cycle — cyclic example")
        print("4. Earliest start times — acyclic example")
        print("5. Critical path — acyclic example")
        print("6. Attempt topological sort on cyclic graph")
        print("7. Show task dependencies")
        print("0. Return to main menu")
        choice = input("Choose an option: ").strip()

        try:
            if choice == "1":
                order, is_dag = topological_sort_kahn(acyclic)
                print("Kahn's topological order:")
                print("  " + " -> ".join(order))
                print(f"  DAG: {'Yes' if is_dag else 'No (cycle)'}")
            elif choice == "2":
                order, is_dag, cycle = topological_sort_dfs(acyclic)
                print("DFS topological order:")
                print("  " + " -> ".join(order))
            elif choice == "3":
                has_cycle, cycle = detect_cycle(cyclic)
                if has_cycle:
                    print("Cycle detected!")
                    print("  Cycle: " + " -> ".join(cycle))
                else:
                    print("No cycle found.")
            elif choice == "4":
                est, order = earliest_start_times(acyclic)
                print("Earliest start times:")
                for t in order:
                    print(f"  {t}: start={est[t]}, "
                          f"duration={acyclic.duration[t]}, "
                          f"finish={est[t] + acyclic.duration[t]}")
            elif choice == "5":
                path, total, est = critical_path(acyclic)
                print(f"Critical path (total duration = {total}):")
                print("  " + " -> ".join(path))
                print("\nAll task timings:")
                for t in acyclic.tasks:
                    print(f"  {t}: start={est[t]}, "
                          f"dur={acyclic.duration[t]}, "
                          f"end={est[t] + acyclic.duration[t]}")
            elif choice == "6":
                order, is_dag = topological_sort_kahn(cyclic)
                if is_dag:
                    print("Topological order:", " -> ".join(order))
                else:
                    print("Cannot produce a topological sort — cycle exists!")
                    _, _, cycle = topological_sort_dfs(cyclic)
                    if cycle:
                        print("Cycle found: " + " -> ".join(cycle))
            elif choice == "7":
                for dag, name in [(acyclic, "Acyclic"), (cyclic, "Cyclic")]:
                    print(f"\n{name} task graph:")
                    for t in dag.tasks:
                        deps = dag.adj[t]
                        dur = dag.duration[t]
                        if deps:
                            print(f"  {t} (dur={dur}) -> "
                                  f"{', '.join(deps)}")
                        else:
                            print(f"  {t} (dur={dur}) -> (none)")
            elif choice == "0":
                break
            else:
                print("Invalid option.")
        except ValueError as exc:
            print("Error:", exc)
