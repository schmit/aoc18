from utils import read_input


def part1():
    """
    Find the resulting frequency by parsing all deltas
    """
    return sum(x for x in read_input(1, int))

def part2():
    """
    Find the first frequency that occurs twice (might require looping)
    """
    visited = set()
    freq = 0
    while True:
        for delta in read_input(1, int):
            freq += delta
            if freq in visited:
                return freq

            visited.add(freq)
