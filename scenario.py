"""Shared in-memory disaster-relief scenario and JSON persistence."""

import json
import math
import os

from avl_expression import AVLTree
from graph import Graph, build_sample_graph
from scheduling import TaskDAG
from trees import GeneralTree, SupplyBST


DATA_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                         "data", "scenario.json")


class Scenario:
    """All editable data used by the application's menu actions."""

    def __init__(self, network_name="Disaster Relief Network"):
        self.network_name = network_name
        self.locations = GeneralTree(network_name)
        self.supplies = SupplyBST()
        self.camps = AVLTree(trace_rotations=True)
        self.graph = Graph(directed=False)
        self.depots = []
        self.tasks = TaskDAG()

    def to_dict(self):
        """Convert structures to plain JSON-compatible records."""
        locations = []

        def collect(node):
            for child in node.children:
                locations.append({
                    "name": child.name,
                    "type": child.location_type,
                    "parent": node.name,
                })
                collect(child)

        collect(self.locations.root)
        return {
            "version": 1,
            "network_name": self.network_name,
            "locations": locations,
            "supplies": [
                {"id": node.key, "name": node.item_name,
                 "quantity": node.quantity}
                for node in self.supplies.inorder_iterative()
            ],
            "camps": [
                {"id": node.key, "name": node.value}
                for node in self.camps.inorder()
            ],
            "graph": {
                "directed": self.graph.directed,
                "vertices": list(self.graph.vertices),
                "edges": [
                    {"from": u, "to": v, "weight": w}
                    for u, v, w in self.graph.all_edges()
                ],
            },
            "depots": list(self.depots),
            "tasks": [
                {"name": task, "duration": self.tasks.duration[task],
                 "successors": list(self.tasks.adj[task])}
                for task in self.tasks.tasks
            ],
        }

    @classmethod
    def from_dict(cls, data):
        """Validate saved records and reconstruct the manual data structures."""
        if not isinstance(data, dict):
            raise ValueError("Scenario file must contain a JSON object.")
        if data.get("version") != 1:
            raise ValueError("Unsupported or missing scenario version.")
        name = data.get("network_name")
        if not isinstance(name, str) or not name.strip():
            raise ValueError("network_name must be a non-empty string.")
        scenario = cls(name.strip())

        locations = _require_list(data, "locations")
        remaining = list(locations)
        while remaining:
            progressed = False
            for record in remaining[:]:
                record = _require_record(record, "location")
                parent = record.get("parent")
                location_name = record.get("name")
                location_type = record.get("type")
                if not all(isinstance(item, str) and item.strip()
                           for item in (parent, location_name, location_type)):
                    raise ValueError(
                        "Each location needs non-empty parent, name, and type strings.")
                parent, location_name, location_type = (
                    parent.strip(), location_name.strip(), location_type.strip())
                if scenario.locations.find(parent) is None:
                    continue
                ok, message = scenario.locations.add_location(
                    parent, location_name, location_type)
                if not ok:
                    raise ValueError(message)
                remaining.remove(record)
                progressed = True
            if not progressed:
                raise ValueError(
                    "Locations contain a missing parent, invalid hierarchy, or cycle.")

        for record in _require_list(data, "supplies"):
            record = _require_record(record, "supply")
            key = _require_int(record.get("id"), "supply id")
            item_name = _require_text(record.get("name"), "supply name")
            quantity = _require_int(record.get("quantity"), "supply quantity")
            if quantity < 0:
                raise ValueError("Supply quantity cannot be negative.")
            if scenario.supplies.search(key) is not None:
                raise ValueError(f"Duplicate supply ID {key}.")
            scenario.supplies.insert(key, item_name, quantity)

        for record in _require_list(data, "camps"):
            record = _require_record(record, "camp")
            key = _require_int(record.get("id"), "camp id")
            value = _require_text(record.get("name"), "camp name")
            if scenario.camps.search(key) is not None:
                raise ValueError(f"Duplicate camp ID {key}.")
            scenario.camps.insert(key, value)

        graph_data = data.get("graph")
        if not isinstance(graph_data, dict):
            raise ValueError("graph must be a JSON object.")
        directed = graph_data.get("directed")
        if not isinstance(directed, bool):
            raise ValueError("graph.directed must be a boolean.")
        scenario.graph = Graph(directed=directed)
        vertices = _require_list(graph_data, "vertices")
        if len(vertices) > 1000:
            raise ValueError("Saved graphs may contain at most 1,000 vertices.")
        for vertex in vertices:
            vertex = _require_text(vertex, "vertex")
            if vertex in scenario.graph.adj_list:
                raise ValueError(f"Duplicate graph vertex '{vertex}'.")
            scenario.graph.add_vertex(vertex)
        edges = _require_list(graph_data, "edges")
        if len(edges) > 500000:
            raise ValueError("Saved graphs may contain at most 500,000 edge records.")
        seen_edges = set()
        for record in edges:
            record = _require_record(record, "edge")
            source = _require_text(record.get("from"), "edge source")
            target = _require_text(record.get("to"), "edge target")
            weight = record.get("weight")
            if (isinstance(weight, bool) or not isinstance(weight, (int, float))
                    or not math.isfinite(weight)):
                raise ValueError("Edge weight must be a finite number.")
            if source not in scenario.graph.adj_list or target not in scenario.graph.adj_list:
                raise ValueError("Every edge endpoint must be a listed graph vertex.")
            edge_key = (source, target) if directed else frozenset((source, target))
            if edge_key in seen_edges:
                raise ValueError(f"Duplicate edge '{source}' -> '{target}'.")
            seen_edges.add(edge_key)
            scenario.graph.add_edge(source, target, weight)

        depots = _require_list(data, "depots")
        for depot in depots:
            depot = _require_text(depot, "depot")
            if depot not in scenario.graph.adj_list:
                raise ValueError(f"Depot '{depot}' is not a graph vertex.")
            if depot in scenario.depots:
                raise ValueError(f"Duplicate depot '{depot}'.")
            scenario.depots.append(depot)

        task_records = _require_list(data, "tasks")
        normalized_tasks = []
        for record in task_records:
            record = _require_record(record, "task")
            task_name = _require_text(record.get("name"), "task name")
            duration = record.get("duration")
            if (isinstance(duration, bool) or not isinstance(duration, (int, float))
                    or not math.isfinite(duration) or duration < 0):
                raise ValueError("Task duration must be a finite non-negative number.")
            if task_name in scenario.tasks._index:
                raise ValueError(f"Duplicate task '{task_name}'.")
            scenario.tasks.add_task(task_name, duration)
            normalized_tasks.append({
                "name": task_name,
                "successors": _require_list(record, "successors"),
            })
        for record in normalized_tasks:
            for successor in _require_list(record, "successors"):
                successor = _require_text(successor, "task successor")
                if successor not in scenario.tasks._index:
                    raise ValueError(f"Unknown successor task '{successor}'.")
                scenario.tasks.add_dependency(record["name"], successor)
        return scenario

    def save(self, path=DATA_PATH, overwrite=False):
        """Save scenario records; existing files require explicit confirmation."""
        if os.path.exists(path) and not overwrite:
            raise FileExistsError(
                f"{path} already exists; confirm overwrite before saving.")
        directory = os.path.dirname(os.path.abspath(path))
        os.makedirs(directory, exist_ok=True)
        temporary = path + ".tmp"
        try:
            with open(temporary, "w", encoding="utf-8") as file:
                json.dump(self.to_dict(), file, indent=2, ensure_ascii=False,
                          allow_nan=False)
                file.write("\n")
            os.replace(temporary, path)
        except (OSError, TypeError, ValueError):
            if os.path.exists(temporary):
                os.remove(temporary)
            raise

    @classmethod
    def load(cls, path=DATA_PATH):
        """Load and validate a scenario JSON file."""
        try:
            with open(path, encoding="utf-8") as file:
                data = json.load(file)
        except json.JSONDecodeError as exc:
            raise ValueError(f"Malformed JSON in '{path}': {exc}") from exc
        except OSError as exc:
            raise OSError(f"Could not read scenario file '{path}': {exc}") from exc
        return cls.from_dict(data)

    @classmethod
    def sample(cls):
        """Create the documented sample scenario as editable in-memory data."""
        scenario = cls("Sample Disaster Relief Network")
        locations = [
            (scenario.locations.root.name, "TamilNadu", "Region"),
            (scenario.locations.root.name, "Kerala", "Region"),
            ("TamilNadu", "Coimbatore", "District"),
            ("TamilNadu", "Chennai", "District"),
            ("Kerala", "Wayanad", "District"),
            ("Coimbatore", "ShelterA", "Shelter"),
            ("Coimbatore", "ShelterB", "Shelter"),
            ("Chennai", "ShelterC", "Shelter"),
            ("Wayanad", "ShelterD", "Shelter"),
        ]
        for parent, name, location_type in locations:
            scenario.locations.add_location(parent, name, location_type)
        for record in [
            (101, "Water Bottles", 500), (102, "Rice Bags", 200),
            (103, "Blankets", 150), (104, "Medicine Kits", 80),
            (105, "Tents", 60), (106, "Fuel Cans", 40),
            (107, "Batteries", 300),
        ]:
            scenario.supplies.insert(*record)
        for key, name in [(1, "Camp Alpha"), (2, "Camp Beta")]:
            scenario.camps.insert(key, name)
        scenario.graph, _, scenario.depots = build_sample_graph()
        scenario.tasks.add_task("AssessDamage", 3)
        scenario.tasks.add_task("SecureArea", 2)
        scenario.tasks.add_task("DeliverSupplies", 4)
        scenario.tasks.add_dependency("AssessDamage", "SecureArea")
        scenario.tasks.add_dependency("SecureArea", "DeliverSupplies")
        return scenario


def _require_list(record, key):
    if not isinstance(record, dict) or not isinstance(record.get(key), list):
        raise ValueError(f"'{key}' must be a JSON array.")
    return record[key]


def _require_record(value, description):
    if not isinstance(value, dict):
        raise ValueError(f"Each {description} must be a JSON object.")
    return value


def _require_text(value, description):
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{description} must be a non-empty string.")
    return value.strip()


def _require_int(value, description):
    if isinstance(value, bool) or not isinstance(value, int):
        raise ValueError(f"{description} must be an integer.")
    return value
