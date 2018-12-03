from utils import read_input
import collections


def has_n_occurance(seq, n):
    counts = collections.Counter(seq)
    return any(v == n for v in counts.values())


def part1():
    """
    Find checksum by multiplying the number of codes
    that have duplicate characters and the number of codes that have
    triplets of characters
    """
    duplicate_count = 0
    triplet_count = 0
    for s in read_input(2):
        if has_n_occurance(s, 2):
            duplicate_count += 1
        if has_n_occurance(s, 3):
            triplet_count += 1
    
    return duplicate_count * triplet_count


def n_in_common(a, b):
    return sum(x == y for x, y in zip(a, b))


def part2():
    """
    Return the common characters of 2 codes that differ by 1 character
    """
    visited = set()
    for s in read_input(2, lambda x: x.strip()):
        for v in visited:
            if n_in_common(s, v) == len(s) - 1:
                # return the characters they have in common
                return ''.join(x for x, y in zip(s, v) if x == y)

        visited.add(s)
