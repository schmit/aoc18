from utils import read_input


test_input = 'dabAcCaCBAcCcaDA'

    
def test_reacts():
    assert reacts('a', 'A')
    assert reacts('A', 'a')
    assert not reacts('a', 'a')
    assert not reacts('A', 'A')
    assert not reacts('a', 'b')
    print("tests pass")


def test_reduce_polymer():
    assert reduce_polymer('aA') == ''
    assert reduce_polymer('aABb') == ''
    assert reduce_polymer('aAa') == 'a'
    assert reduce_polymer('a') == 'a'
    assert reduce_polymer('aBbA') == ''
    assert reduce_polymer('aabAAB') == 'aabAAB'
    print("tests pass")


def reacts(x, y):
    """ 
    returns True if x and y react.
    That is, x=a, y=A or x=A and y=a
    """
    if x == x.upper() and y == y.lower():
        # reduce to case x is lowercase and y is uppercase
        return reacts(y, x)
    return y != x and y.lower() == x
       

def reduce_polymer(polymer):
    reduction = ''
    while polymer != '':
        if not reduction or not reacts(reduction[-1], polymer[0]):
            reduction += polymer[0]
        else:
            reduction = reduction[:-1]

        # remove first element
        polymer = polymer[1:]

    return reduction

def recursive_reduce_polymer(polymer, reduction=''):
    """
    Recursively reduces the polymer
    """
    # return current polymer if no more elements remain
    if not polymer:
        return reduction

    # unpack polymer
    first_polymer, *rest_polymer = polymer
    # check if first_polymer elem reacts with end of current
    # in which case both get destroyed
    if reduction and reacts(first_polymer, reduction[-1]):
        return reduce_polymer(rest_polymer, reduction[:-1])
    # otherwise, append element to current reduction
    return reduce_polymer(rest_polymer, reduction + first_polymer)
    

def solve_part_1():
    polymer = next(read_input(5)).strip()
    return len(reduce_polymer(polymer))
