from utils import read_input
import collections


Coordinate = tuple

test_coords = [
    Coordinate([1, 1]),
    Coordinate([1, 6]),
    Coordinate([8, 3]),
    Coordinate([3, 4]),
    Coordinate([5, 5]),
    Coordinate([8, 9])]


def parse_coord(line):
    return Coordinate(map(int,line.split(', ')))


def parse_coords():
    return list(read_input(6, parse_coord))

def l1(a, b):
    """ returns manhattan distance between a and b """
    return sum(abs(x-y) for x, y in zip(a, b))

def closer_to(x, a, b):
    """
    returns True if x is closer to a than to b
    """
    return l1(x, a) < l1(x, b)


def compute_bounding_box(coords):
    """ returns corners of a box containing all coordinates """
    dimensions = len(coords[0])
    bounding_box = []
    for d in range(dimensions):
        m = min(coords, key=lambda t: t[d])[d]
        M = max(coords, key=lambda t: t[d])[d]
        bounding_box.append((m-1, M+1))
    return bounding_box


def border_elements(box):
    """ return all points on the border of a 2D box """
    xlims, ylims = box
    for y in ylims:
        xmin, xmax = xlims
        for x in range(xmin, xmax+1):
            yield Coordinate([x, y])

    for x in xlims:
        ymin, ymax = ylims
        for y in range(ymin, ymax+1):
            yield Coordinate([x, y])
            

def find_closest_coord(point, coords):
    """ returns coord closest to a given point """
    # if only 1 coordinate, then return it
    if len(coords) == 1:
        return coords[0]

    # sort all coords based on distance
    ordered_coords = sorted(coords, key=lambda c: l1(point, c))

    # check for ties
    if l1(point, ordered_coords[0]) < l1(point, ordered_coords[1]):
        return ordered_coords[0]

    # tie found, return None 
    return None


def infinite_areas(coords):
    """ returns coords with infinite areas """
    bounding_box = compute_bounding_box(coords)

    # an area corresponding to a coord has infinite
    # area if a point on the bounding box is closest to
    # the coord. So let's check all coordinates
    # on the bounding box
    infinite_set = set()
    for point in border_elements(bounding_box):
        # find closest coord
        closest = find_closest_coord(point, coords)
        if closest:
            infinite_set.add(closest)

    return infinite_set


def finite_areas(coords):
    """ return coords with finite areas """
    return set(coords) - infinite_areas(coords)


def neighbors(coord):
    x, y = coord
    return [Coordinate((x+1, y)),
            Coordinate((x-1, y)),
            Coordinate((x, y+1)),
            Coordinate((x, y-1))]
    


def find_closest_points(coord, coords, max_frontier=10e5):
    """ returns all points closest to coord """
    # search outward from coord
    frontier = [coord]
    added_to_frontier = set(frontier)
    closest = set()

    while frontier:
        # ensure we aren't looping forever for infinite area
        if len(frontier) > max_frontier:
            raise ValueError("Seems like there are an infinite number of closest points")
        current = frontier.pop()
        if coord == find_closest_coord(current, coords):
            closest.add(current)

            # add neighbors to frontier if not added before
            for n in neighbors(current):
                if n not in added_to_frontier:
                    frontier.append(n)
                    added_to_frontier.add(n)

    return closest


def compute_area(coord, coords):
    """ 
    Computes the area corresponding to coord
    Note: assumes area is finite
    """
    return len(find_closest_points(coord, coords))


def find_max_finite_area(coords):
    """ find the coordinate with max finite area """
    coord = max(finite_areas(coords),
               key=lambda c: compute_area(c, coords))
    # return coordinate and area
    return coord, compute_area(coord, coords)
    

def solve_part_1():
    coords = parse_coords()
    return find_max_finite_area(coords)

    
