import attr
import collections
from utils import read_input

# Node = collections.namedtuple('Node', ['children', 'metadata'])

@attr.s
class Node:
    n_children = attr.ib()
    n_meta = attr.ib()
    children = attr.ib(factory=list)
    meta = attr.ib(factory=list)

def parse_input(inp):
    return list(map(int, inp.split()))

test_input = '2 3 0 3 10 11 12 1 1 0 1 99 2 1 1 2'


def create_tree(seq):
    """ creates tree of nodes of input sequence """
    def resolve(seq):
        """ returns list of nodes and remainder """
        # todo: pop(0) is slow so refactor
        # might want to work with reversed sequence
        n_children = seq.pop(0)
        n_meta = seq.pop(0)

        # adds each child
        children = []
        for i in range(n_children):
            child, seq = resolve(seq)
            children.append(child)

        # after finishing the children
        # grab the metadata
        meta = seq[:n_meta]

        # the remainder is pushed up the recursion tree
        remainder = seq[n_meta:]
        return Node(n_children, n_meta, children, meta), remainder

    tree, remainder = resolve(seq)
    assert not remainder
    return tree

def sum_metadata(node):
    """ sums metadata of node and all childrens metadata """
    return sum(node.meta) + sum(sum_metadata(child) for child in node.children)

def solve_part_1():
    inp = parse_input(next(read_input(8)))
    tree = create_tree(inp)
    return sum_metadata(tree)
