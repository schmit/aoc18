import attr
import collections
import re

from utils import read_input, first

@attr.s
class Claim:
    """ 
    Data structure to hold claims
    """
    id = attr.ib()
    x = attr.ib()
    y = attr.ib()
    width = attr.ib()
    height = attr.ib()

claim_regex = re.compile("\#([0-9]+)\s@\s([0-9]+),([0-9]+)\:\s([0-9]+)x([0-9]+)")

def parse_line(line) -> Claim:
    """ convert a line to a claim """
    match = claim_regex.match(line)
    return Claim(*map(int, match.groups()))

claims = [parse_line(line) for line in read_input(3)]

def patch(claim):
    """ returns all patches claimed in claim """
    return [(claim.x + dx, claim.y + dy)
            for dx in range(claim.width)
            for dy in range(claim.height)]

def patch_claim_count(claims):
    patch_counts = collections.Counter()
    for claim in claims:
        patch_counts.update(patch(claim))
    return patch_counts

def n_patches_with_multiple_claims(claims):
    """ part 1 """
    patch_counts = patch_claim_count(claims)
    return sum(1 for n in patch_counts.values() if n > 1)

def find_non_overlapping_claims(claims):
    """ part 2 """ 
    patch_counts = patch_claim_count(claims)
    for claim in claims:
        is_unique = all(patch_counts[elem] == 1 for elem in patch(claim))
        if is_unique:
            yield claim

solution_1 = n_patches_with_multiple_claims(claims)
solution_2 = first(find_non_overlapping_claims(claims))
