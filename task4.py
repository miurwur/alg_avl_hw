import sys

class Node:
    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None
        self.parent = None
        self.height = 1 

class AVL:
    def __init__(self):
        self.root = None

    def get_height(self, node):
        return node.height if node else 0

    def get_balance(self, node):
        if node is None:
            return 0
        return self.get_height(node.right) - self.get_height(node.left)

    def update_height(self, node):
        node.height = 1 + max(
            self.get_height(node.left),
            self.get_height(node.right)
        )

    def rotate_left(self, x):
        if x is None or x.right is None:
            return

        y = x.right
        p = x.parent

        x.right = y.left
        if y.left:
            y.left.parent = x

        y.left = x
        x.parent = y
        y.parent = p

        if p is None:
            self.root = y
        elif p.left is x:
            p.left = y
        else:
            p.right = y

        self.update_height(x)
        self.update_height(y)

    def rotate_right(self, x):
        if x is None or x.left is None:
            return

        y = x.left
        p = x.parent

        x.left = y.right
        if y.right:
            y.right.parent = x

        y.right = x
        x.parent = y
        y.parent = p

        if p is None:
            self.root = y
        elif p.left is x:
            p.left = y
        else:
            p.right = y

        self.update_height(x)
        self.update_height(y)

    def rebalance(self, node):
        while node:
            self.update_height(node)
            balance = self.get_balance(node)

            if balance == 2:
                if self.get_balance(node.right) < 0:
                    self.rotate_right(node.right)
                self.rotate_left(node)

            elif balance == -2:
                if self.get_balance(node.left) > 0:
                    self.rotate_left(node.left)
                self.rotate_right(node)

            node = node.parent

    def add(self, key):
        if self.root is None:
            self.root = Node(key)
            return

        curr = self.root

        while True:
            if key == curr.key:
                return

            if key < curr.key:
                if curr.left:
                    curr = curr.left
                else:
                    new_node = Node(key)
                    curr.left = new_node
                    new_node.parent = curr
                    self.rebalance(curr)
                    return
            else:
                if curr.right:
                    curr = curr.right
                else:
                    new_node = Node(key)
                    curr.right = new_node
                    new_node.parent = curr
                    self.rebalance(curr)
                    return

    def find(self, key):
        curr = self.root

        while curr:
            if key == curr.key:
                return curr
            elif key < curr.key:
                curr = curr.left
            else:
                curr = curr.right

        return None

    def exists(self, key):
        return self.find(key) is not None

    def get_min(self, node):
        while node.left:
            node = node.left
        return node

    def delete(self, key):
        node = self.find(key)

        if node is None:
            return

        # если 2 ребенка, заменяем ключ на минимальный в правом поддереве
        if node.left and node.right:
            min_node = self.get_min(node.right)
            node.key = min_node.key
            node = min_node

        # удаляем узел с 0 или 1 ребенком
        child = node.left if node.left else node.right
        parent = node.parent

        if child:
            child.parent = parent

        if parent is None:
            self.root = child
        elif parent.left is node:
            parent.left = child
        else:
            parent.right = child

        # балансируем дерево до корня
        if parent:
            self.rebalance(parent)
        elif self.root:
            self.update_height(self.root)

    def next_key(self, key):
        curr = self.root
        result = None

        while curr:
            if curr.key >= key:
                result = curr.key
                curr = curr.left
            else:
                curr = curr.right

        return result

    def prev_key(self, key):
        curr = self.root
        result = None

        while curr:
            if curr.key <= key:
                result = curr.key
                curr = curr.right
            else:
                curr = curr.left

        return result

    def get_root(self):
        return self.root.key if self.root else "Empty"

    def height(self):
        return self.get_height(self.root)

    def preorder(self):
        if self.root is None:
            return "Empty"

        result = []
        stack = [self.root]

        while stack:
            node = stack.pop()
            result.append(str(node.key))

            if node.right:
                stack.append(node.right)
            if node.left:
                stack.append(node.left)

        return " ".join(result)


def main():
    input = sys.stdin.readline
    q = int(input())
    avl = AVL()
    output = []

    for _ in range(q):
        parts = input().split()
        cmd = parts[0]

        if cmd == "add":
            avl.add(int(parts[1]))

        elif cmd == "exists":
            output.append(
                "YES" if avl.exists(int(parts[1])) else "NO"
            )

        elif cmd == "next":
            result = avl.next_key(int(parts[1]))
            output.append(
                str(result) if result is not None else "None"
            )

        elif cmd == "prev":
            result = avl.prev_key(int(parts[1]))
            output.append(
                str(result) if result is not None else "None"
            )

        elif cmd == "root":
            output.append(str(avl.get_root()))

        elif cmd == "height":
            output.append(str(avl.height()))

        elif cmd == "print":
            output.append(avl.preorder())

        elif cmd == "del":
            avl.delete(int(parts[1]))

    print("\n".join(output))


if __name__ == "__main__":
    main()
