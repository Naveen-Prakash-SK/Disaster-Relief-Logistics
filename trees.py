"""General Tree and Binary Search Tree for Disaster Relief Logistics.

General tree hierarchy:
    Region -> District -> Shelter

BST:
    Supply records indexed by a unique supply ID.

No built-in tree libraries are used.
"""

# ---------------------------------------------------------------------------
# GENERAL TREE: Region -> District -> Shelter
# ---------------------------------------------------------------------------

class GeneralTreeNode:
    def __init__(self, name, location_type="Region"):
        self.name = name
        self.location_type = location_type
        self.children = []

    def __repr__(self):
        return f"{self.location_type}({self.name})"


class GeneralTree:
    def __init__(self, root_name="Disaster Relief Network"):
        self.root = GeneralTreeNode(root_name, "Network")

    def find(self, name, node=None):
        """Return the first node with the given name, or None."""
        if node is None:
            node = self.root
        if node.name == name:
            return node
        for child in node.children:
            found = self.find(name, child)
            if found is not None:
                return found
        return None

    def add_location(self, parent_name, name, location_type):
        """Add a Region, District, or Shelter under an existing parent."""
        if not name.strip():
            raise ValueError("Location name cannot be empty.")
        parent = self.find(parent_name)
        if parent is None:
            return False, f"Parent location '{parent_name}' was not found."
        if self.find(name) is not None:
            return False, f"A location named '{name}' already exists."
        allowed = {
            "Network": {"Region"},
            "Region": {"District"},
            "District": {"Shelter"},
            "Shelter": set(),
        }
        if location_type not in allowed.get(parent.location_type, set()):
            return False, (
                f"A {parent.location_type} cannot contain a "
                f"{location_type}. Follow Region -> District -> Shelter."
            )
        parent.children.append(GeneralTreeNode(name, location_type))
        return True, f"{location_type} '{name}' added under '{parent_name}'."

    def delete_subtree(self, name):
        """Delete a location and all descendants; the root cannot be deleted."""
        if self.root.name == name:
            return False, "The root network cannot be deleted."
        parent = self._find_parent(name, self.root)
        if parent is None:
            return False, f"Location '{name}' was not found."
        for child in parent.children:
            if child.name == name:
                parent.children.remove(child)
                return True, f"Deleted '{name}' and its entire subtree."
        return False, f"Location '{name}' was not found."

    def _find_parent(self, target_name, node):
        for child in node.children:
            if child.name == target_name:
                return node
            found = self._find_parent(target_name, child)
            if found is not None:
                return found
        return None

    def display(self, node=None, depth=0):
        """Print the hierarchy with indentation."""
        if node is None:
            node = self.root
        print("  " * depth + f"- {node.location_type}: {node.name}")
        for child in node.children:
            self.display(child, depth + 1)

    def preorder(self, node=None, result=None):
        if node is None:
            node = self.root
        if result is None:
            result = []
        result.append(node.name)
        for child in node.children:
            self.preorder(child, result)
        return result

    def postorder(self, node=None, result=None):
        if node is None:
            node = self.root
        if result is None:
            result = []
        for child in node.children:
            self.postorder(child, result)
        result.append(node.name)
        return result

    def level_order(self):
        """Iterative level-order traversal using a regular list as a queue."""
        result = []
        queue = [self.root]
        front = 0
        while front < len(queue):
            current = queue[front]
            front += 1
            result.append(current.name)
            queue.extend(current.children)
        return result


# ---------------------------------------------------------------------------
# BINARY SEARCH TREE: relief supply stock
# ---------------------------------------------------------------------------

class BSTNode:
    def __init__(self, key, item_name, quantity):
        self.key = key
        self.item_name = item_name
        self.quantity = quantity
        self.left = None
        self.right = None


class SupplyBST:
    """BST keyed by unique integer supply ID."""

    def __init__(self):
        self.root = None

    def insert(self, key, item_name, quantity):
        if quantity < 0:
            raise ValueError("Quantity cannot be negative.")
        new_node = BSTNode(key, item_name, quantity)
        if self.root is None:
            self.root = new_node
            return
        current = self.root
        while True:
            if key < current.key:
                if current.left is None:
                    current.left = new_node
                    return
                current = current.left
            elif key > current.key:
                if current.right is None:
                    current.right = new_node
                    return
                current = current.right
            else:
                # Update existing record.
                current.item_name = item_name
                current.quantity = quantity
                return


    def search(self, key):
        current = self.root
        while current is not None:
            if key == current.key:
                return current
            current = current.left if key < current.key else current.right
        return None

    def delete(self, key):
        parent = None
        node = self.root
        while node is not None and node.key != key:
            parent = node
            node = node.left if key < node.key else node.right
        if node is None:
            return False

        if node.left is not None and node.right is not None:
            successor_parent = node
            successor = node.right
            while successor.left is not None:
                successor_parent = successor
                successor = successor.left
            node.key = successor.key
            node.item_name = successor.item_name
            node.quantity = successor.quantity
            parent, node = successor_parent, successor

        child = node.left if node.left is not None else node.right
        if parent is None:
            self.root = child
        elif parent.left is node:
            parent.left = child
        else:
            parent.right = child
        return True

    def _minimum_node(self, node):
        current = node
        while current.left is not None:
            current = current.left
        return current

    def minimum(self):
        return None if self.root is None else self._minimum_node(self.root)

    def maximum(self):
        current = self.root
        if current is None:
            return None
        while current.right is not None:
            current = current.right
        return current

    def successor(self, key):
        """Return the node with the smallest key greater than key."""
        current = self.root
        candidate = None
        while current is not None:
            if key < current.key:
                candidate = current
                current = current.left
            else:
                current = current.right
        return candidate

    def predecessor(self, key):
        """Return the node with the largest key smaller than key."""
        current = self.root
        candidate = None
        while current is not None:
            if key > current.key:
                candidate = current
                current = current.right
            else:
                current = current.left
        return candidate

    def range_query(self, low, high):
        """Return all supply records with IDs in inclusive range [low, high]."""
        if low > high:
            return []
        result = []
        stack = []
        node = self.root
        while node is not None or stack:
            while node is not None:
                if node.key >= low:
                    stack.append(node)
                    node = node.left
                else:
                    node = node.right
            if not stack:
                break
            node = stack.pop()
            if node.key > high:
                break
            result.append(node)
            node = node.right
        return result

    def inorder(self):
        result = []
        def visit(node):
            if node is not None:
                visit(node.left)
                result.append(node)
                visit(node.right)
        visit(self.root)
        return result

    def preorder(self):
        result = []
        def visit(node):
            if node is not None:
                result.append(node)
                visit(node.left)
                visit(node.right)
        visit(self.root)
        return result

    def postorder(self):
        result = []
        def visit(node):
            if node is not None:
                visit(node.left)
                visit(node.right)
                result.append(node)
        visit(self.root)
        return result

    def level_order(self):
        if self.root is None:
            return []
        result, queue, front = [], [self.root], 0
        while front < len(queue):
            node = queue[front]
            front += 1
            result.append(node)
            if node.left is not None:
                queue.append(node.left)
            if node.right is not None:
                queue.append(node.right)
        return result

    # --- Iterative binary-tree traversals (explicit stack/queue) ---

    def inorder_iterative(self):
        """Iterative inorder traversal using an explicit stack."""
        result = []
        stack = []
        current = self.root
        while current is not None or stack:
            while current is not None:
                stack.append(current)
                current = current.left
            current = stack.pop()
            result.append(current)
            current = current.right
        return result

    def preorder_iterative(self):
        """Iterative preorder traversal using an explicit stack."""
        if self.root is None:
            return []
        result = []
        stack = [self.root]
        while stack:
            node = stack.pop()
            result.append(node)
            # Push right first so left is processed first.
            if node.right is not None:
                stack.append(node.right)
            if node.left is not None:
                stack.append(node.left)
        return result

    def postorder_iterative(self):
        """Iterative postorder using two stacks."""
        if self.root is None:
            return []
        result = []
        stack1 = [self.root]
        stack2 = []
        while stack1:
            node = stack1.pop()
            stack2.append(node)
            if node.left is not None:
                stack1.append(node.left)
            if node.right is not None:
                stack1.append(node.right)
        while stack2:
            result.append(stack2.pop())
        return result

    def level_order_iterative(self):
        """Iterative level-order traversal (alias for level_order)."""
        return self.level_order()

    def height(self):
        """Height measured in nodes; empty tree has height 0.
        Uses iterative approach to avoid RecursionError on skewed trees."""
        if self.root is None:
            return 0
        max_height = 0
        # Stack stores (node, depth) pairs.
        stack = [(self.root, 1)]
        while stack:
            node, depth = stack.pop()
            if depth > max_height:
                max_height = depth
            if node.right is not None:
                stack.append((node.right, depth + 1))
            if node.left is not None:
                stack.append((node.left, depth + 1))
        return max_height


# ---------------------------------------------------------------------------
# Console menu and display helpers
# ---------------------------------------------------------------------------

def _print_supply(node):
    if node is None:
        print("No matching supply record.")
    else:
        print(f"ID: {node.key} | Item: {node.item_name} | Quantity: {node.quantity}")


def trees_menu():
    location_tree = GeneralTree()
    supply_tree = SupplyBST()

    while True:
        print("--- LOCATION TREE AND SUPPLY BST ---")
        print("1. Add region")
        print("2. Add district")
        print("3. Add shelter")
        print("4. Display location hierarchy")
        print("5. Location traversals")
        print("6. Delete location subtree")
        print("7. Insert/update supply stock")
        print("8. Search supply")
        print("9. Delete supply")
        print("10. Display supplies (inorder)")
        print("11. Minimum and maximum supply ID")
        print("12. Successor and predecessor")
        print("13. Supply ID range query")
        print("14. Compare BST height with 1,000 sorted IDs")
        print("0. Return to main menu")
        choice = input("Choose an option: ").strip()

        try:
            if choice == "1":
                name = input("Region name: ").strip()
                ok, message = location_tree.add_location(
                    location_tree.root.name, name, "Region")
                print(message)
            elif choice == "2":
                parent = input("Parent region name: ").strip()
                name = input("District name: ").strip()
                ok, message = location_tree.add_location(parent, name, "District")
                print(message)
            elif choice == "3":
                parent = input("Parent district name: ").strip()
                name = input("Shelter name: ").strip()
                ok, message = location_tree.add_location(parent, name, "Shelter")
                print(message)
            elif choice == "4":
                location_tree.display()
            elif choice == "5":
                print("Preorder:", " -> ".join(location_tree.preorder()))
                print("Postorder:", " -> ".join(location_tree.postorder()))
                print("Level-order:", " -> ".join(location_tree.level_order()))
            elif choice == "6":
                name = input("Location name to delete: ").strip()
                ok, message = location_tree.delete_subtree(name)
                print(message)
            elif choice == "7":
                key = int(input("Supply ID (integer): "))
                item = input("Supply item name: ").strip()
                quantity = int(input("Quantity: "))
                supply_tree.insert(key, item, quantity)
                print("Supply record inserted/updated.")
            elif choice == "8":
                _print_supply(supply_tree.search(int(input("Supply ID: "))))
            elif choice == "9":
                key = int(input("Supply ID to delete: "))
                print("Deleted." if supply_tree.delete(key) else "Supply ID not found.")
            elif choice == "10":
                records = supply_tree.inorder_iterative()
                if not records:
                    print("No supply records.")
                for node in records:
                    _print_supply(node)
            elif choice == "11":
                print("Minimum:")
                _print_supply(supply_tree.minimum())
                print("Maximum:")
                _print_supply(supply_tree.maximum())
            elif choice == "12":
                key = int(input("Supply ID: "))
                print("Successor:")
                _print_supply(supply_tree.successor(key))
                print("Predecessor:")
                _print_supply(supply_tree.predecessor(key))
            elif choice == "13":
                low = int(input("Minimum supply ID: "))
                high = int(input("Maximum supply ID: "))
                records = supply_tree.range_query(low, high)
                if not records:
                    print("No supply records in that range.")
                for node in records:
                    _print_supply(node)
            elif choice == "14":
                # Deliberately unbalanced BST: insert sorted keys.
                benchmark = SupplyBST()
                for key in range(1, 1001):
                    benchmark.insert(key, f"Supply-{key}", key)
                print("Sorted IDs inserted:", 1000)
                print("BST height (measured in nodes):", benchmark.height())
                print("Compare this with the AVL height after implementing the AVL module.")
            elif choice == "0":
                break
            else:
                print("Invalid option.")
        except ValueError as exc:
            print("Input error:", exc)
        except RecursionError:
            print("This operation exceeded Python's recursion limit. Sorted BST inputs can become highly unbalanced.")
