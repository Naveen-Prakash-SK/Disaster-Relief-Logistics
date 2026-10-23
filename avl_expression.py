"""AVL Tree (Relief-Camp Index) and Expression Tree (Relief Cost Calculator).

AVL tree: self-balancing BST with LL, RR, LR, RL rotations.
Expression tree: built from postfix expressions; evaluates and prints infix.

No built-in tree or eval() usage.
"""

import random
import re


# ============================================================================
# AVL TREE — Relief-Camp Index
# ============================================================================

class AVLNode:
    """A node in an AVL tree storing a camp key and optional value."""
    __slots__ = ("key", "value", "left", "right", "height")

    def __init__(self, key, value=None):
        self.key = key
        self.value = value
        self.left = None
        self.right = None
        self.height = 1

    def __repr__(self):
        return f"AVLNode(key={self.key}, h={self.height})"


class AVLTree:
    """AVL tree with insert, delete, search, all rotations and verification."""

    def __init__(self, trace_rotations=False):
        self.root = None
        self.size = 0
        self.trace_rotations = trace_rotations
        self.rotation_log = []          # list of rotation descriptions

    # --- Height and balance helpers ---

    @staticmethod
    def _h(node):
        return 0 if node is None else node.height

    def _update_height(self, node):
        node.height = 1 + max(self._h(node.left), self._h(node.right))

    def _bf(self, node):
        """Balance factor = height(left) - height(right)."""
        return self._h(node.left) - self._h(node.right)

    # --- Rotations ---

    def _rotate_right(self, z):
        """LL rotation (single right rotation)."""
        y = z.left
        t3 = y.right
        y.right = z
        z.left = t3
        self._update_height(z)
        self._update_height(y)
        if self.trace_rotations:
            self.rotation_log.append(f"LL (right rotation) at node {z.key}")
        return y

    def _rotate_left(self, z):
        """RR rotation (single left rotation)."""
        y = z.right
        t2 = y.left
        y.left = z
        z.right = t2
        self._update_height(z)
        self._update_height(y)
        if self.trace_rotations:
            self.rotation_log.append(f"RR (left rotation) at node {z.key}")
        return y

    def _rebalance(self, node):
        """Check balance factor and apply rotations if needed."""
        self._update_height(node)
        bf = self._bf(node)

        if bf > 1:
            if self._bf(node.left) < 0:
                # LR case
                if self.trace_rotations:
                    self.rotation_log.append(
                        f"LR case detected at node {node.key}")
                node.left = self._rotate_left(node.left)
                return self._rotate_right(node)
            else:
                # LL case
                return self._rotate_right(node)

        if bf < -1:
            if self._bf(node.right) > 0:
                # RL case
                if self.trace_rotations:
                    self.rotation_log.append(
                        f"RL case detected at node {node.key}")
                node.right = self._rotate_right(node.right)
                return self._rotate_left(node)
            else:
                # RR case
                return self._rotate_left(node)

        return node

    # --- Insert ---

    def insert(self, key, value=None):
        """Insert *key* (with optional value) into the AVL tree."""
        self.root = self._insert(self.root, key, value)

    def _insert(self, node, key, value):
        if node is None:
            self.size += 1
            return AVLNode(key, value)
        if key < node.key:
            node.left = self._insert(node.left, key, value)
        elif key > node.key:
            node.right = self._insert(node.right, key, value)
        else:
            node.value = value        # update existing
            return node
        return self._rebalance(node)

    # --- Delete ---

    def delete(self, key):
        """Delete *key* from the AVL tree. Returns True if found."""
        self.root, deleted = self._delete(self.root, key)
        if deleted:
            self.size -= 1
        return deleted

    def _delete(self, node, key):
        if node is None:
            return None, False
        deleted = False
        if key < node.key:
            node.left, deleted = self._delete(node.left, key)
        elif key > node.key:
            node.right, deleted = self._delete(node.right, key)
        else:
            deleted = True
            if node.left is None:
                return node.right, True
            if node.right is None:
                return node.left, True
            # Two children: replace with inorder successor.
            succ = node.right
            while succ.left is not None:
                succ = succ.left
            node.key = succ.key
            node.value = succ.value
            node.right, _ = self._delete(node.right, succ.key)
        return self._rebalance(node), deleted

    # --- Search ---

    def search(self, key):
        """Return the AVLNode with the given key, or None."""
        current = self.root
        while current is not None:
            if key == current.key:
                return current
            current = current.left if key < current.key else current.right
        return None

    # --- Traversals ---

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

    def height(self):
        return self._h(self.root)

    # --- Verification ---

    def verify(self):
        """Check BST ordering, stored heights and balance factors.
        Returns (ok, message).
        """
        try:
            self._verify_node(self.root, float('-inf'), float('inf'))
            return True, "AVL invariants verified."
        except AssertionError as e:
            return False, f"AVL invariant violation: {e}"

    def _verify_node(self, node, lo, hi):
        if node is None:
            return 0
        assert lo < node.key < hi, (
            f"BST order violation: key {node.key} not in ({lo}, {hi})")
        lh = self._verify_node(node.left, lo, node.key)
        rh = self._verify_node(node.right, node.key, hi)
        expected_h = 1 + max(lh, rh)
        assert node.height == expected_h, (
            f"Stored height {node.height} != computed {expected_h} "
            f"at key {node.key}")
        bf = lh - rh
        assert -1 <= bf <= 1, (
            f"Balance factor {bf} at key {node.key}")
        return expected_h

    # --- Bulk random operations with verification ---

    @staticmethod
    def random_stress_test(n_ops=10000, seed=42):
        """Insert and delete n_ops random keys; verify after each operation.
        Returns (tree, passed_count, total_ops).
        """
        rng = random.Random(seed)
        tree = AVLTree(trace_rotations=False)
        keys_present = set()
        passed = 0
        for i in range(n_ops):
            op = rng.choice(["insert", "delete"])
            key = rng.randint(1, n_ops // 2)
            if op == "insert":
                tree.insert(key, f"camp-{key}")
                keys_present.add(key)
            else:
                tree.delete(key)
                keys_present.discard(key)
            ok, msg = tree.verify()
            if ok:
                passed += 1
            else:
                print(f"  Verification FAILED at op {i+1}: {msg}")
                return tree, passed, i + 1
        return tree, passed, n_ops

    def display(self, node=None, prefix="", is_left=True, first_call=True):
        """Pretty-print the AVL tree."""
        if first_call:
            node = self.root
        if node is None:
            return
        connector = "├── " if is_left else "└── "
        if first_call:
            print(f"AVL root: {node.key} (h={node.height})")
        else:
            print(f"{prefix}{connector}{node.key} (h={node.height})")
        new_prefix = prefix + ("│   " if is_left else "    ")
        if node.left or node.right:
            if node.left:
                self.display(node.left, new_prefix, True, False)
            else:
                print(f"{new_prefix}├── (empty)")
            if node.right:
                self.display(node.right, new_prefix, False, False)
            else:
                print(f"{new_prefix}└── (empty)")


# ============================================================================
# EXPRESSION TREE — Relief Cost Calculator
# ============================================================================

class ExpressionNode:
    """A node in an expression tree. Stores either an operator or an operand."""
    __slots__ = ("value", "left", "right")

    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None


OPERATORS = {'+', '-', '*', '/', 'neg'}


def infix_to_postfix(expression):
    """Convert arithmetic infix text to postfix without evaluating it."""
    token_pattern = re.compile(
        r"\d+(?:\.\d*)?(?:[eE][+-]?\d+)?|\.\d+(?:[eE][+-]?\d+)?|"
        r"[A-Za-z_]\w*|[()+\-*/]")
    tokens = token_pattern.findall(expression)
    if not tokens or "".join(tokens) != re.sub(r"\s+", "", expression):
        raise ValueError("Use numbers, variable names, + - * /, and parentheses.")

    precedence = {'+': 1, '-': 1, '*': 2, '/': 2, 'neg': 3}
    output = []
    operators = []
    expects_operand = True
    for token in tokens:
        if token == "(":
            operators.append(token)
            expects_operand = True
        elif token == ")":
            if expects_operand:
                raise ValueError("Missing operand before ')'.")
            while operators and operators[-1] != "(":
                output.append(operators.pop())
            if not operators:
                raise ValueError("Unmatched closing parenthesis.")
            operators.pop()
            expects_operand = False
        elif token in "+-*/":
            if expects_operand:
                if token != "-":
                    raise ValueError(f"Operator '{token}' needs a left operand.")
                operator = "neg"
            else:
                operator = token
            while (operators and operators[-1] != "("
                   and (precedence[operators[-1]] > precedence[operator]
                        or (precedence[operators[-1]] == precedence[operator]
                            and operator != "neg"))):
                output.append(operators.pop())
            operators.append(operator)
            expects_operand = True
        else:
            if not expects_operand:
                raise ValueError("Insert an operator between operands.")
            output.append(token)
            expects_operand = False
    if expects_operand:
        raise ValueError("Expression ends where an operand is required.")
    while operators:
        operator = operators.pop()
        if operator == "(":
            raise ValueError("Unmatched opening parenthesis.")
        output.append(operator)
    return output


def build_expression_tree(postfix_tokens):
    """Build an expression tree from a list of postfix tokens.

    Tokens can be:
    - Numeric literals (int or float strings)
    - Named variables (alphabetic strings)
    - Operators: +, -, *, /

    Returns the root ExpressionNode.
    Raises ValueError on invalid input.
    """
    if not postfix_tokens:
        raise ValueError("Empty expression.")
    stack = []
    for token in postfix_tokens:
        if token == "neg":
            if not stack:
                raise ValueError("Unary minus requires one operand.")
            node = ExpressionNode(token)
            node.right = stack.pop()
            stack.append(node)
        elif token in OPERATORS:
            if len(stack) < 2:
                raise ValueError(
                    f"Operator '{token}' requires two operands, "
                    f"but only {len(stack)} available on stack.")
            node = ExpressionNode(token)
            node.right = stack.pop()
            node.left = stack.pop()
            stack.append(node)
        else:
            stack.append(ExpressionNode(token))
    if len(stack) != 1:
        raise ValueError(
            f"Invalid postfix expression: {len(stack)} items remain "
            f"on stack (expected exactly 1).")
    return stack[0]


def evaluate_expression(root, variables=None):
    """Evaluate an expression tree.

    *variables* is a dict mapping variable names to numeric values.
    Raises ValueError for undefined variables or division by zero.
    Does NOT use eval().
    """
    if variables is None:
        variables = {}

    def _eval(node):
        if node.value == "neg":
            return -_eval(node.right)
        if node.left is None and node.right is None:
            # Leaf: try numeric literal, then variable lookup.
            try:
                return float(node.value)
            except ValueError:
                if node.value in variables:
                    return float(variables[node.value])
                raise ValueError(
                    f"Undefined variable '{node.value}'. "
                    f"Provide its value in the variables dict.")
        left_val = _eval(node.left)
        right_val = _eval(node.right)
        if node.value == '+':
            return left_val + right_val
        if node.value == '-':
            return left_val - right_val
        if node.value == '*':
            return left_val * right_val
        if node.value == '/':
            if right_val == 0:
                raise ValueError("Division by zero.")
            return left_val / right_val
        raise ValueError(f"Unknown operator '{node.value}'.")

    return _eval(root)


def infix_string(root):
    """Return an infix string with minimal parentheses."""
    _PREC = {'+': 1, '-': 1, '*': 2, '/': 2, 'neg': 3}

    def _to_str(node, parent_op=None, is_right_child=False):
        if node.value == "neg":
            expression = f"-{_to_str(node.right, 'neg', True)}"
            if node.right.value in _PREC:
                expression = f"-({_to_str(node.right)})"
            return expression
        if node.left is None and node.right is None:
            return str(node.value)
        left_s = _to_str(node.left, node.value, False)
        right_s = _to_str(node.right, node.value, True)
        expr = f"{left_s} {node.value} {right_s}"
        if parent_op is not None:
            p_prec = _PREC.get(parent_op, 0)
            c_prec = _PREC.get(node.value, 0)
            # Parenthesise lower-precedence children and right children whose
            # grouping would change the represented operation sequence.
            if c_prec < p_prec:
                expr = f"({expr})"
            elif c_prec == p_prec and is_right_child:
                if parent_op in ('-', '/') or node.value != parent_op:
                    expr = f"({expr})"
        return expr

    return _to_str(root)


# ============================================================================
# Console menu
# ============================================================================

def avl_expression_menu():
    """Interactive menu for AVL tree and expression tree operations."""
    avl = AVLTree(trace_rotations=True)

    while True:
        print("\n--- AVL RELIEF-CAMP INDEX & EXPRESSION CALCULATOR ---")
        print("1.  Insert camp into AVL")
        print("2.  Delete camp from AVL")
        print("3.  Search camp in AVL")
        print("4.  Display AVL tree")
        print("5.  AVL inorder traversal")
        print("6.  Verify AVL invariants")
        print("7.  Show rotation log")
        print("8.  Run AVL stress test (10,000 ops)")
        print("9.  Expression tree: evaluate postfix")
        print("10. AVL vs BST height comparison (1,000 sorted keys)")
        print("0.  Return to main menu")
        choice = input("Choose an option: ").strip()

        try:
            if choice == "1":
                key = int(input("Camp ID (integer): "))
                name = input("Camp name: ").strip()
                avl.insert(key, name)
                print(f"Camp {key} inserted.")
                ok, msg = avl.verify()
                if not ok:
                    print("WARNING:", msg)
            elif choice == "2":
                key = int(input("Camp ID to delete: "))
                if avl.delete(key):
                    print(f"Camp {key} deleted.")
                else:
                    print(f"Camp {key} not found.")
                ok, msg = avl.verify()
                if not ok:
                    print("WARNING:", msg)
            elif choice == "3":
                key = int(input("Camp ID to search: "))
                node = avl.search(key)
                if node:
                    print(f"Found: key={node.key}, value={node.value}, "
                          f"height={node.height}")
                else:
                    print("Camp not found.")
            elif choice == "4":
                if avl.root is None:
                    print("AVL tree is empty.")
                else:
                    avl.display()
            elif choice == "5":
                nodes = avl.inorder()
                if not nodes:
                    print("AVL tree is empty.")
                else:
                    for n in nodes:
                        print(f"  key={n.key}, value={n.value}")
            elif choice == "6":
                ok, msg = avl.verify()
                print(msg)
            elif choice == "7":
                if not avl.rotation_log:
                    print("No rotations recorded yet.")
                else:
                    for entry in avl.rotation_log:
                        print(" ", entry)
            elif choice == "8":
                print("Running 10,000 random insert/delete operations "
                      "(seed=42) …")
                tree, passed, total = AVLTree.random_stress_test(10000, 42)
                print(f"Completed {total} operations. "
                      f"Verification passed: {passed}/{total}")
                print(f"Final tree height: {tree.height()}, "
                      f"size: {tree.size}")
                ok, msg = tree.verify()
                print(msg)
            elif choice == "9":
                _expression_submenu()
            elif choice == "10":
                _avl_vs_bst_height()
            elif choice == "0":
                break
            else:
                print("Invalid option.")
        except ValueError as exc:
            print("Input error:", exc)


def _expression_submenu():
    """Interactive postfix expression evaluation."""
    print("\nEnter a postfix expression (tokens separated by spaces).")
    print("Example: distance rate * toll +")
    print("Operators: + - * /")
    print("Operands: integers, decimals, or variable names.")
    raw = input("Postfix: ").strip()
    if not raw:
        print("No expression entered.")
        return
    tokens = raw.split()
    try:
        root = build_expression_tree(tokens)
    except ValueError as e:
        print("Error building expression tree:", e)
        return

    print(f"Infix expression: {infix_string(root)}")

    # Collect variable values.
    variables = {}
    # Identify variables (non-operator, non-numeric tokens).
    var_names = set()
    for t in tokens:
        if t not in OPERATORS:
            try:
                float(t)
            except ValueError:
                var_names.add(t)
    if var_names:
        print(f"Variables detected: {', '.join(sorted(var_names))}")
        for v in sorted(var_names):
            val = input(f"  Value for '{v}': ").strip()
            try:
                variables[v] = float(val)
            except ValueError:
                print(f"  Invalid number for '{v}'. Aborting evaluation.")
                return
    try:
        result = evaluate_expression(root, variables)
        print(f"Result: {result}")
    except ValueError as e:
        print("Evaluation error:", e)


def _avl_vs_bst_height():
    """Compare BST vs AVL heights for 1,000 sorted keys."""
    from trees import SupplyBST
    bst = SupplyBST()
    avl = AVLTree()
    for k in range(1, 1001):
        bst.insert(k, f"item-{k}", k)
        avl.insert(k, f"camp-{k}")
    print(f"Inserted 1,000 sorted keys (1 to 1000).")
    print(f"BST height : {bst.height()} nodes")
    print(f"AVL height : {avl.height()} nodes")
    print()
    print("Explanation:")
    print("  Inserting sorted keys into a plain BST creates a degenerate")
    print("  (linear) tree with height = n = 1000. Every node has only")
    print("  a right child, behaving like a linked list.")
    print("  The AVL tree maintains O(log n) height by performing")
    print("  rotations after each insertion, keeping balance factors")
    print("  within {-1, 0, +1}. For n=1000, AVL height ≈ 11–14.")
