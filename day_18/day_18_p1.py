with open("./day_18.in") as fin:
    raw_data = fin.read().strip().split("\n")
data = [eval(line) for line in raw_data]


# We're representing data as a tree


class Node:
    def __init__(self, val=None):
        self.val = val
        self.left = None
        self.right = None
        self.par = None

    def __str__(self):
        if isinstance(self.val, int):
            return str(self.val)
        return f"[{str(self.left)},{str(self.right)}]"


def parse(fish_num):
    """
    Parse a big list into a tree
    """
    root = Node()
    if isinstance(fish_num, int):
        root.val = fish_num
        return root

    root.left = parse(fish_num[0])
    root.right = parse(fish_num[1])
    root.left.par = root
    root.right.par = root

    reduce(root)

    return root


def add(a, b):
    """
    Add two trees together
    """
    root = Node()
    root.left = a
    root.right = b
    root.left.par = root
    root.right.par = root
    reduce(root)
    return root


def magnitude(root):
    if isinstance(root.val, int):
        return root.val

    return 3 * magnitude(root.left) + 2 * magnitude(root.right)


def reduce(root):
    """
    Reduce a tree
    """
    done = True

    # Do a DFS through the tree
    stack = [(root, 0)]

    while len(stack) > 0:
        # A preorder traversal will have the right order
        node, depth = stack.pop()

        if node == None:
            continue

        condition = (node.left == None and node.right == None) or (
            node.left.val != None and node.right.val != None)

        if depth >= 4 and node.val == None and condition:
            # Go up the stack to find left node
            prev_node = node.left
            cur_node = node
            while cur_node != None and (cur_node.left == prev_node or cur_node.left == None):
                prev_node = cur_node
                cur_node = cur_node.par

            # Left node must exist
            if cur_node != None:

                # Now cur_idx has a left child; we go all the way down
                cur_node = cur_node.left
                while cur_node.val == None:
                    if cur_node.right != None:
                        cur_node = cur_node.right
                    else:
                        cur_node = cur_node.left

                # Update some values!
                cur_node.val += node.left.val

            # Go up the stack to find right node
            prev_node = node.right
            cur_node = node
            while cur_node != None and (cur_node.right == prev_node or cur_node.right == None):
                prev_node = cur_node
                cur_node = cur_node.par

            # Right node must exist
            if cur_node != None:

                # Now cur_idx has a left child; we go all the way down
                cur_node = cur_node.right
                while cur_node.val == None:
                    if cur_node.left != None:
                        cur_node = cur_node.left
                    else:
                        cur_node = cur_node.right

                # Update some values!
                cur_node.val += node.right.val

            # Final explode updates
            node.val = 0
            node.left = None
            node.right = None

            # Stop the DFS
            done = False
            break

        # DFS through the children
        stack.append((node.right, depth + 1))
        stack.append((node.left, depth + 1))

    # Look for splits later
    if not done:
        reduce(root)
        return

    stack = [root]
    while len(stack) > 0:
        node = stack.pop()
        if node == None:
            continue

        if node.val != None:
            # Split!
            assert node.left == None and node.right == None
            if node.val >= 10:
                node.left = Node(node.val//2)
                node.right = Node(node.val - (node.val//2))
                node.left.par = node
                node.right.par = node
                node.val = None

                done = False
                break

        stack.append(node.right)
        stack.append(node.left)

    # If not done, keep going
    if not done:
        reduce(root)


# Alright great
root = parse(data[0])

i = 1
while i < len(data):
    root = add(root, parse(data[i]))
    i += 1

ans = magnitude(root)
print(ans)
