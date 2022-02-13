from asyncio.windows_events import INFINITE
from errno import ENFILE
import math
from sympy import root


class Node:
    def __init__(self, tag):
        self.left = None
        self.right = None
        self.tag = tag
        self.coordinate = 0
        self.Tag1 = 0
        self.Tag0 = 0
        self.vectors = []
        self.count = 0

    def Entropy(self):
        if self.count == 0:
            entropy = 1
        else:
            if self.Tag0 == 0 or self.Tag1 == 0:
                entropy = 0
            else:
                p = float(self.Tag1 / self.count)
                entropy = (-(p) * (math.log2(p))) - ((1 - p) * (math.log2(1 - p)))

        return entropy

    def display(self):
        # this code taken from https://stackoverflow.com/questions/34012886/print-binary-tree-level-by-level-in-python
        lines, *_ = self._display_aux()
        for line in lines:
            print(line)

    def _display_aux(self):
        # No child.
        if self.right is None and self.left is None:
            line = '%s' % self.coordinate
            width = len(line)
            height = 1
            middle = width // 2
            return [line], width, height, middle

        # Only left child.
        if self.right is None:
            lines, n, p, x = self.left._display_aux()
            c = 'l'
            s = '%s' % self.coordinate
            u = len(s)
            first_line = self.genereate_first_line(c, x, n, s)
            second_line = self.genereate_second_line(c, x, n, u)
            # shifted_lines = self.shifted_lines(c,u,lines)
            shifted_lines = [line + u * ' ' for line in lines]
            return [first_line, second_line] + shifted_lines, n + u, p + 2, n + u // 2

        # Only right child.
        if self.left is None:
            lines, n, p, x = self.right._display_aux()
            c = 'r'
            s = '%s' % self.coordinate
            u = len(s)
            first_line = self.genereate_first_line(c, x, n, s)
            second_line = self.genereate_second_line(c, x, n, u)
            # shifted_lines = self.shifted_lines(c,u,lines)
            shifted_lines = [u * ' ' + line for line in lines]
            return [first_line, second_line] + shifted_lines, n + u, p + 2, u // 2

        # Two children.
        left, n, p, x = self.left._display_aux()
        right, m, q, y = self.right._display_aux()
        c = 'b'
        s = '%s' % self.coordinate
        u = len(s)
        first_line = self.genereate_first_line(c, x, n, s, y, m)
        second_line = self.genereate_second_line(c, x, n, u, y, m)

        if p < q:
            left += [n * ' '] * (q - p)
        elif q < p:
            right += [m * ' '] * (p - q)
        zipped_lines = zip(left, right)
        lines = [first_line, second_line] + [a + u * ' ' + b for a, b in zipped_lines]
        return lines, n + m + u, max(p, q) + 2, n + u // 2

    def genereate_first_line(self, c, x=0, n=0, s=0, y=0, m=0):
        # left child
        if (c == 'l'):
            return (x + 1) * ' ' + (n - x - 1) * '_' + s
        # right child
        elif (c == 'r'):
            return s + x * '_' + (n - x) * ' '
        # both childs
        else:
            return (x + 1) * ' ' + (n - x - 1) * '_' + s + y * '_' + (m - y) * ' '

    def genereate_second_line(self, c, x=0, n=0, u=0, y=0, m=0):
        if (c == 'l'):
            return x * ' ' + '/' + (n - x - 1 + u) * ' '
        elif (c == 'r'):
            return (u + x) * ' ' + '\\' + (n - x - 1) * ' '
        else:
            return x * ' ' + '/' + (n - x - 1 + u + y) * ' ' + '\\' + (m - y - 1) * ' '

    def shifted_lines(self, c, u, lines):
        if (c == 'l'):
            return [line + u * ' ' for line in lines]
        else:
            return [u * ' ' + line for line in lines]


class Tree:
    def __init__(self):
        self.root = Node(-1)

    def searchForLeaves(self, root):
        result = []
        if root.left:
            result.extend(self.searchForLeaves(root.left))
        if root.right:
            result.extend(self.searchForLeaves(root.right))
        if not result:
            if root.Tag0 < root.Tag1:
                root.tag = 1
                root.coordinate = "True"
            else:
                root.tag = 0
                root.coordinate = "False"
            result = [root]
        return result

    def insertionHelper(self, root, vectors, k):
        for v in vectors:
            self.insertA(root, v, k - 1)

        leaves = self.searchForLeaves(root)
        err = self.errorFun(leaves)
        return (err / 150)

    def errorFun(self, leaves):
        err = 0
        for i in leaves:
            if i.tag == 0:
                err += (i.Tag1)
            elif i.tag == 1:
                err += (i.Tag0)
        return err

    def insertA(self, root, vector, k):
        if k > 0:
            coordinate = root.coordinate
            if vector[coordinate] == 0:
                if root.left is None:
                    root.left = Node(0)
                    self.insertA(root.left, vector, k - 1)

                else:
                    self.insertA(root.left, vector, k - 1)
            elif vector[coordinate] == 1:
                if root.right is None:
                    root.right = Node(1)
                    self.insertA(root.right, vector, k - 1)

                else:
                    self.insertA(root.right, vector, k - 1)
        elif k == 0:
            root.count += 1
            if vector[8] == 1:
                root.Tag1 += 1
            elif vector[8] == 0:
                root.Tag0 += 1

    def split(self, root, vectors):
        n = len(vectors[0]) - 1
        best_i = 0
        left, right = Node(0), Node(1)
        LEntropy = INFINITE
        REntropy = INFINITE
        min_entropy = INFINITE
        for i in range(n):
            root.left = Node(0)
            root.right = Node(1)

            for v in vectors:
                if v[i] == 0:
                    if v[n] == 0:
                        root.left.count += 1
                        root.left.Tag0 += 1
                        root.left.vectors.append(v)
                    elif v[n] == 1:
                        root.left.count += 1
                        root.left.Tag1 += 1
                        root.left.vectors.append(v)
                elif v[i] == 1:
                    if v[n] == 0:
                        root.right.count += 1
                        root.right.Tag0 += 1
                        root.right.vectors.append(v)
                    elif v[n] == 1:
                        root.right.count += 1
                        root.right.Tag1 += 1
                        root.right.vectors.append(v)

            LEntropy = root.left.Entropy()
            REntropy = root.right.Entropy()
            if (LEntropy + REntropy) < min_entropy:
                min_entropy = LEntropy + REntropy
                best_i = i
                left = root.left
                right = root.right
        root.left = left
        root.right = right
        return [best_i, min_entropy]

    def insertB(self, root, k, vectors):

        Split = self.split(root, vectors)
        root.coordinate = Split[0]
        left = root.left
        right = root.right
        Lsplit = self.split(left, left.vectors)
        Rsplit = self.split(right, right.vectors)
        root.left.coordinate = Lsplit[0]
        root.right.coordinate = Rsplit[0]

        return [self, Split[0], Lsplit[0], Rsplit[0]]


def Q1A(vectors, k):
    min_error = INFINITE
    best_indexs = []
    for i in range(len(vectors[0]) - 1):
        for l in range(len(vectors[0]) - 1):
            for r in range(len(vectors[0]) - 1):
                tree = Tree()
                root = tree.root
                root.coordinate = i
                root.left = Node(0)
                root.left.coordinate = l
                root.right = Node(1)
                root.right.coordinate = r
                tree_error = tree.insertionHelper(root, vectors, k)
                if tree_error < min_error:
                    min_error = tree_error
                    best_indexs = [tree, min_error]

    return best_indexs


def Q1B(vectors, k):
    tree = Tree()
    root = tree.root
    root_split = tree.insertB(root, k, vectors)
    tree = root_split[0]
    leaves = tree.searchForLeaves(root)
    error_in_tree = tree.errorFun(leaves)
    return [root_split, (error_in_tree / 150)]


def main(vectors, k):
    best_tree = Q1A(vectors, k)
    print("Question 1 \nPart A:")
    print("The {} levels tree with the lowest error:".format(k))
    best_tree[0].root.display()
    print("The error is:", best_tree[1])
    print("\nQuestion 1 Part B:")
    print("The {} levels tree using binary entropy:".format(k))

    best_tree_entropy = Q1B(vectors, k)
    best_tree_entropy[0][0].root.display()
    print("The error is: {:.2f} ".format(best_tree_entropy[1]))


if __name__ == '__main__':

    f = open("vectors.txt", "r")
    lines = f.read().splitlines()
    f.close()
    vectors = []
    for v in lines:
        line = v.split()
        vector = [int(i) for i in line]
        vectors.append(vector)

    main(vectors, 3)