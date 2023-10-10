"""Assignment 2 functions."""

from copy import deepcopy

# Examples to use in doctests:
THREE_BY_THREE = [[1, 2, 1],
                  [4, 6, 5],
                  [7, 8, 9]]

FOUR_BY_FOUR = [[1, 2, 6, 5],
                [4, 5, 3, 2],
                [7, 9, 8, 1],
                [1, 2, 1, 4]]

UNIQUE_3X3 = [[1, 2, 3],
              [9, 8, 7],
              [4, 5, 6]]

UNIQUE_4X4 = [[10, 2, 3, 30],
              [9, 8, 7, 11],
              [4, 5, 6, 12],
              [13, 14, 15, 16]]

EPSILON = 0.005


def compare_elevations_within_row(elevation_map: list[list[int]], map_row: int,
                                  level: int) -> list[int]:
    """Return a new list containing three counts: the number of elevations are
    less than, equal to, and greater than elevation at row number map_row on
    elevation map elevation_map.

    Precondition: elevation_map is a valid elevation map.
                  0 <= map_row < len(elevation_map).

    >>> compare_elevations_within_row(THREE_BY_THREE, 1, 5)
    [1, 1, 1]
    >>> compare_elevations_within_row(FOUR_BY_FOUR, 1, 2)
    [0, 1, 3]
    >>> compare_elevations_within_row(UNIQUE_3X3, 1, 2)
    [0, 0, 3]
    >>> compare_elevations_within_row(UNIQUE_4X4, 3, 16)
    [3, 1, 0]
    >>> compare_elevations_within_row(UNIQUE_4X4, 0, 2)
    [0, 1, 3]

    """
    new_list = [0, 0, 0]
    for elevation in elevation_map[map_row]:
        if elevation < level:
            new_list[0] += 1
        elif elevation == level:
            new_list[1] += 1
        else:
            new_list[2] += 1
    return new_list


def update_elevation(elevation_map: list[list[int]], start: list[int],
                     stop: list[int], delta: int) -> None:
    """Update elevation map elevation_map that contains the new elevations
    between the start cell start and the end cell stop, inclusive, with the
    change of the given amount delta.

    Precondition: elevation_map is a valid elevation map.
                  start[0] == stop [0] or start[1] == stop [1]
                  if start[0] == stop [0], then stop[1] >= start[1]
                  if start[1] == stop [1], then stop[0] >= start[0]
                  delta will never cause an elevation to go below 1 on a map.

    >>> THREE_BY_THREE_COPY = deepcopy(THREE_BY_THREE)
    >>> update_elevation(THREE_BY_THREE_COPY, [1, 0], [1, 1], -2)
    >>> THREE_BY_THREE_COPY
    [[1, 2, 1], [2, 4, 5], [7, 8, 9]]
    >>> FOUR_BY_FOUR_COPY = deepcopy(FOUR_BY_FOUR)
    >>> update_elevation(FOUR_BY_FOUR_COPY, [1, 2], [3, 2], 1)
    >>> FOUR_BY_FOUR_COPY
    [[1, 2, 6, 5], [4, 5, 4, 2], [7, 9, 9, 1], [1, 2, 2, 4]]
    >>> UNIQUE_4X4_COPY = deepcopy(UNIQUE_4X4)
    >>> update_elevation(UNIQUE_4X4_COPY, [3, 3], [3, 3], -2)
    >>> UNIQUE_4X4_COPY
    [[10, 2, 3, 30], [9, 8, 7, 11], [4, 5, 6, 12], [13, 14, 15, 14]]

    """
    if start[0] == stop[0]:
        for difference in range(stop[1] - start[1] + 1):
            elevation_map[start[0]][start[1] + difference] += delta
    elif start[1] == stop[1]:
        for difference in range(stop[0] - start[0] + 1):
            elevation_map[start[0] + difference][start[1]] += delta


def get_average_elevation(elevation_map: list[list[int]]) -> float:
    """Return the average of all elevations on evaluation map evaluation_map.

    Precondition: elevation_map is a valid elevation map.

    >>> abs(get_average_elevation(UNIQUE_3X3) - 5.0) < EPSILON
    True
    >>> abs(get_average_elevation(FOUR_BY_FOUR) - 3.8125) < EPSILON
    True

    """
    count = 0
    length = len(elevation_map)
    for row_num in range(length):
        for column in range(length):
            count += elevation_map[row_num][column]
    return count / length ** 2


def find_peak(elevation_map: list[list[int]]) -> list[int]:
    """Return the cell that has the greatest elevation on elevation map
    elevation_map.

    Precondition: elevation_map is a valid elevation map.
                  all values in the given map elevation_map are unique.

    >>> find_peak(UNIQUE_3X3)
    [1, 0]
    >>> find_peak(UNIQUE_4X4)
    [0, 3]

    """
    maximum = elevation_map[0][0]
    location = [0, 0]
    for row in range(len(elevation_map)):
        for column in range(len(elevation_map)):
            if maximum < elevation_map[row][column]:
                maximum = elevation_map[row][column]
                location = [row, column]
    return location


def is_sink(elevation_map: list[list[int]], cell: list[int]) -> bool:
    """Return True if and only if cell cell is a sink on elevation map
    elevation_map, vice versa. Also return False when the cell cell is not
    valid on elevation map elevation_map.

    Precondition: elevation_map is a valid elevation map.

    >>> is_sink(THREE_BY_THREE, [1,2])
    False
    >>> is_sink(THREE_BY_THREE, [0,1])
    False
    >>> is_sink(FOUR_BY_FOUR, [3,0])
    True
    >>> is_sink(UNIQUE_4X4, [4,0])
    False
    >>> is_sink(UNIQUE_4X4, [0,2])
    False
    >>> is_sink(UNIQUE_3X3, [1,1])
    False

    """
    dimension = len(elevation_map)
    row = cell[0]
    column = cell[1]
    if row > dimension - 1 or cell[1] > dimension - 1:
        return False
    for adj in get_adjacent_cells(cell, dimension):
        if elevation_map[row][column] >= elevation_map[adj[0]][adj[1]]:
            return False
    return True


def find_local_sink(elevation_map: list[list[int]],
                    cell: list[int]) -> list[int]:
    """Return the adjacent cell to cell cell with the lowest elevation on
    elevation map elevation_map.

    Precondition: elevation_map is a valid elevation map.
                  is_valid_cell(cell,len(elevation_map)) == True
                  all values on elevation map elevation_map are unique.

    >>> find_local_sink(UNIQUE_3X3, [1,1])
    [0, 0]
    >>> find_local_sink(UNIQUE_3X3, [2,2])
    [2, 1]
    >>> find_local_sink(UNIQUE_3X3, [0,2])
    [0, 1]
    >>> find_local_sink(UNIQUE_4X4, [2,2])
    [2, 1]
    >>> find_local_sink(UNIQUE_3X3, [0,0])
    [0, 0]

    """
    dimension = len(elevation_map)
    minimum = elevation_map[cell[0]][cell[1]]
    min_cell = cell
    for adjacent in get_adjacent_cells(cell, dimension):
        if minimum > elevation_map[adjacent[0]][adjacent[1]]:
            min_cell = adjacent
            minimum = elevation_map[adjacent[0]][adjacent[1]]
    return min_cell


def can_hike_to(elevation_map: list[list[int]], start: list[int],
                dest: list[int], supplies: int) -> bool:
    """Return True if and only if the hiker can reach the destination dest from
    start start with the given supplies supplies, using the strategy of
    travelling to the destination dest directly in the direction, either north
    or west, with the smallest change in elevation.

    Precondition: elevation_map is a valid elevation map.
                  is_cell_valid(start, len(elevation_map)) == True
                  is_cell_valid(dest, len(elevation_map)) == True
                  supplies >= 0
                  dest[0] <= start[0]
                  dest[1] <= start[1]

    >>> can_hike_to(THREE_BY_THREE, [2,2], [1,1], 3)
    True
    >>> can_hike_to(THREE_BY_THREE, [2,2], [1,1], 2)
    False
    >>> can_hike_to(FOUR_BY_FOUR, [3,3], [2,2], 10)
    True
    >>> can_hike_to(UNIQUE_4X4, [1,1], [0,0], 1)
    False
    >>> can_hike_to(FOUR_BY_FOUR,[2,2], [0,0], 11)
    True
    >>> can_hike_to(FOUR_BY_FOUR,[2,3], [2,0], 1)
    False
    >>> can_hike_to(UNIQUE_4X4,[3,0], [1,0], 50)
    True

    """
    n_cell = [start[0], start[1]]
    n_value = elevation_map[n_cell[0]][n_cell[1]]
    required_supplies = 0
    while n_cell[0] > dest[0] and n_cell[1] > dest[1]:
        if abs(n_value - elevation_map[n_cell[0] - 1][n_cell[1]]) > abs(
                n_value - elevation_map[n_cell[0]][n_cell[1] - 1]):
            required_supplies += abs(n_value - elevation_map[n_cell[0]][n_cell[
                1] - 1])
            n_cell = [n_cell[0], n_cell[1] - 1]
            n_value = elevation_map[n_cell[0]][n_cell[1]]
        else:
            required_supplies += abs(elevation_map[n_cell[0] - 1][n_cell[1]] -
                                     n_value)
            n_cell = [n_cell[0] - 1, n_cell[1]]
            n_value = elevation_map[n_cell[0]][n_cell[1]]
    while n_cell[0] == dest[0] and n_cell[1] > dest[1]:
        required_supplies += abs(elevation_map[n_cell[0]][n_cell[1] - 1] -
                                 n_value)
        n_cell = [n_cell[0], n_cell[1] - 1]
        n_value = elevation_map[n_cell[0]][n_cell[1]]
    while n_cell[0] > dest[0] and n_cell[1] == dest[1]:
        required_supplies += abs(elevation_map[n_cell[0] - 1][n_cell[1]] -
                                 n_value)
        n_cell = [n_cell[0] - 1, n_cell[1]]
        n_value = elevation_map[n_cell[0]][n_cell[1]]
    return required_supplies <= supplies


def get_lower_resolution(elevation_map: list[list[int]]) -> list[list[int]]:
    """Return a new elevation map that contains the average of the original
    elevation on the new entries on map elevation_map. If the sidelength of
    elevation map elevation_map is even, the elevation map elevation_map is
    divided into 2x2 entries evenly. If the sidelength is odd, the part of
    the elevation map elevation_map excluding the last row and last column
    is divided equally into 2x2 entries, while the last elevation of the map
    is an individual entry and the rest are divided into 1x2 entries. Averages
    on the new elevations are in order. Entries on the same row cause their
    averages to be on the same row on the new elevation map.

    Precondition: elevation_map is a valid elevation map.

    >>> get_lower_resolution(THREE_BY_THREE)
    [[3, 3], [7, 9]]
    >>> get_lower_resolution(FOUR_BY_FOUR)
    [[3, 4], [4, 3]]
    >>> get_lower_resolution(UNIQUE_3X3)
    [[5, 5], [4, 6]]
    >>> get_lower_resolution(UNIQUE_4X4)
    [[7, 12], [9, 12]]

    """
    last_valid = len(elevation_map) - 1
    average_list = []
    new_list = []
    if len(elevation_map) % 2 == 0:
        for row in range(0, last_valid, 2):
            for column in range(0, last_valid, 2):
                average = get_2x2_adjacent_average([row, column],
                                                   elevation_map)
                average_list.append(average)
                if len(average_list) == len(elevation_map)/2:
                    new_list.append(average_list)
                    average_list = []
    elif len(elevation_map) % 2 != 0:
        new_list = get_odd_up_average(elevation_map)
        odd_bottom = get_odd_bottom_average(elevation_map)
        new_list.append(odd_bottom)
    return new_list


def is_valid_cell(cell: list[int], dimension: int) -> bool:
    """Return True if and only if cell is a valid cell in an elevation map of
    dimensions dimension x dimension.

    Precondition: cell is a list of length 2.

    >>> is_valid_cell([1, 1], 2)
    True
    >>> is_valid_cell([0, 2], 2)
    False

    """
    return 0 <= cell[0] <= dimension - 1 and 0 <= cell[1] <= dimension - 1


def get_adjacent_cells(cell: list[int], dimension: int) -> list[list[int]]:
    """Return a list of cells adjacent to cell cell on an elevation map with
    dimensions dimension x dimension.

    Precondition: cell is a valid cell for an elevation map with
                  dimensions dimension x dimension.

    >>> adjacent_cells = get_adjacent_cells([1, 1], 3)
    >>> adjacent_cells.sort()
    >>> adjacent_cells
    [[0, 0], [0, 1], [0, 2], [1, 0], [1, 2], [2, 0], [2, 1], [2, 2]]
    >>> adjacent_cells = get_adjacent_cells([1, 0], 3)
    >>> adjacent_cells.sort()
    >>> adjacent_cells
    [[0, 0], [0, 1], [1, 1], [2, 0], [2, 1]]
    >>> adjacent_cells = get_adjacent_cells([3, 0], 4)
    >>> adjacent_cells.sort()
    >>> adjacent_cells
    [[2, 0], [2, 1], [3, 1]]
    >>> adjacent_cells = get_adjacent_cells([0, 0], 4)
    >>> adjacent_cells.sort()
    >>> adjacent_cells
    [[0, 1], [1, 0], [1, 1]]
    >>> adjacent_cells = get_adjacent_cells([2, 3], 4)
    >>> adjacent_cells.sort()
    >>> adjacent_cells
    [[1, 2], [1, 3], [2, 2], [3, 2], [3, 3]]

    """
    last_valid = dimension - 1
    if cell[0] in range(1, last_valid) and cell[1] in range(1, last_valid):
        adjacent_list = adjacent_middle_cells(cell, dimension)
    elif cell[1] in range(1, last_valid):
        adjacent_list = adjacent_top_bottom_cells(cell, dimension)
    elif cell[0] in range(1, last_valid):
        adjacent_list = adjacent_left_right_cells(cell, dimension)
    else:
        adjacent_list = get_adjacent_corner_cells(cell, dimension)
    return adjacent_list


def adjacent_middle_cells(cell: list[int], dimension: int) -> list[list[int]]:
    """Return a list of cells adjacent to cell cell in the middle of an
    elevation map with dimensions dimension x dimension.

    Precondition: cell is a valid cell for an elevation map with
                  dimensions dimension x dimension.
                  cell[0] != 0 and cell[0] != dimension - 1
                  cell[1] != 0 and cell[1] != dimension - 1

    >>> adjacent_cells = adjacent_middle_cells([1, 1], 3)
    >>> adjacent_cells.sort()
    >>> adjacent_cells
    [[0, 0], [0, 1], [0, 2], [1, 0], [1, 2], [2, 0], [2, 1], [2, 2]]
    >>> adjacent_cells = adjacent_middle_cells([1, 2], 4)
    >>> adjacent_cells.sort()
    >>> adjacent_cells
    [[0, 1], [0, 2], [0, 3], [1, 1], [1, 3], [2, 1], [2, 2], [2, 3]]
    >>> adjacent_cells = adjacent_middle_cells([2, 2], 4)
    >>> adjacent_cells.sort()
    >>> adjacent_cells
    [[1, 1], [1, 2], [1, 3], [2, 1], [2, 3], [3, 1], [3, 2], [3, 3]]

    """
    middle = []
    last_valid = dimension - 1
    if cell[0] in range(1, last_valid) and cell[1] in range(1, last_valid):
        for i in range(-1, 2):
            for j in range(-1, 2):
                adjacent = [cell[0] + i, cell[1] + j]
                if adjacent != cell:
                    middle.append(adjacent)
    return middle


def adjacent_top_bottom_cells(cell: list[int],
                              dimension: int) -> list[list[int]]:
    """Return a list of cells adjacent to cell cell on the top or bottom row an
    elevation map with dimensions dimension x dimension.

    Precondition: cell is a valid cell for an elevation map with
                  dimensions dimension x dimension.
                  cell[0] == dimension - 1 or cell[0] == 0
                  cell[1] != 0 and cell[1] != dimension - 1

    >>> adjacent_cells = adjacent_top_bottom_cells([0, 1], 3)
    >>> adjacent_cells.sort()
    >>> adjacent_cells
    [[0, 0], [0, 2], [1, 0], [1, 1], [1, 2]]
    >>> adjacent_cells = adjacent_top_bottom_cells([2, 1], 3)
    >>> adjacent_cells.sort()
    >>> adjacent_cells
    [[1, 0], [1, 1], [1, 2], [2, 0], [2, 2]]
    >>> adjacent_cells = adjacent_top_bottom_cells([0, 2], 4)
    >>> adjacent_cells.sort()
    >>> adjacent_cells
    [[0, 1], [0, 3], [1, 1], [1, 2], [1, 3]]
    >>> adjacent_cells = adjacent_top_bottom_cells([3, 2], 4)
    >>> adjacent_cells.sort()
    >>> adjacent_cells
    [[2, 1], [2, 2], [2, 3], [3, 1], [3, 3]]

    """
    top_bottom = []
    last_valid = dimension - 1
    if cell[1] in range(1, last_valid):
        for i in range(2):
            for j in range(-1, 2):
                if cell[0] == 0 and [i, j] != [0, 0]:
                    adjacent = [i, cell[1] + j]
                    top_bottom.append(adjacent)
                elif cell[0] == last_valid and [i, j] != [0, 0]:
                    adjacent = [last_valid - i, cell[1] + j]
                    top_bottom.append(adjacent)
    return top_bottom


def adjacent_left_right_cells(cell: list[int],
                              dimension: int) -> list[list[int]]:
    """Return a list of cells adjacent to cell cell on the first or last column
    an elevation map with dimensions dimension x dimension.

    Precondition: cell is a valid cell for an elevation map with
                  dimensions dimension x dimension.
                  cell[1] == dimension - 1 or cell[1] == 0
                  cell[0] != 0 and cell[0] != dimension - 1

    >>> adjacent_cells = adjacent_left_right_cells([1, 0], 3)
    >>> adjacent_cells.sort()
    >>> adjacent_cells
    [[0, 0], [0, 1], [1, 1], [2, 0], [2, 1]]
    >>> adjacent_cells = adjacent_left_right_cells([1, 2], 3)
    >>> adjacent_cells.sort()
    >>> adjacent_cells
    [[0, 1], [0, 2], [1, 1], [2, 1], [2, 2]]
    >>> adjacent_cells = adjacent_left_right_cells([2, 0], 4)
    >>> adjacent_cells.sort()
    >>> adjacent_cells
    [[1, 0], [1, 1], [2, 1], [3, 0], [3, 1]]
    >>> adjacent_cells = adjacent_left_right_cells([2, 3], 4)
    >>> adjacent_cells.sort()
    >>> adjacent_cells
    [[1, 2], [1, 3], [2, 2], [3, 2], [3, 3]]

    """
    left_right = []
    last_valid = dimension - 1
    if cell[0] in range(1, last_valid):
        for i in range(-1, 2):
            for j in range(2):
                if cell[1] == 0 and [i, j] != [0, 0]:
                    adjacent = [cell[0] + i, cell[1] + j]
                    left_right.append(adjacent)
                elif cell[1] == last_valid and [i, j] != [0, 0]:
                    adjacent = [cell[0] + i, cell[1] - j]
                    left_right.append(adjacent)
    return left_right


def get_adjacent_corner_cells(cell: list[int],
                              dimension: int) -> list[list[int]]:
    """Return a list of cells adjacent to corner cell cell on an elevation map
    with dimensions dimension x dimension.

    Precondition: cell is a valid cell for an elevation map with
                  dimensions dimension x dimension.
                  cell[0] == dimension - 1 or cell[0] == 0
                  cell[1] == dimension - 1 or cell[1] == 0

    >>> adjacent_cells = get_adjacent_cells([0, 0], 3)
    >>> adjacent_cells.sort()
    >>> adjacent_cells
    [[0, 1], [1, 0], [1, 1]]
    >>> adjacent_cells = get_adjacent_cells([0, 2], 3)
    >>> adjacent_cells.sort()
    >>> adjacent_cells
    [[0, 1], [1, 1], [1, 2]]
    >>> adjacent_cells = get_adjacent_cells([3, 0], 4)
    >>> adjacent_cells.sort()
    >>> adjacent_cells
    [[2, 0], [2, 1], [3, 1]]
    >>> adjacent_cells = get_adjacent_cells([3, 3], 4)
    >>> adjacent_cells.sort()
    >>> adjacent_cells
    [[2, 2], [2, 3], [3, 2]]

    """
    last_valid = dimension - 1
    if cell in [[0, 0], [0, last_valid]]:
        adjacent_corner_list = get_adjacent_top_corner_cells(cell, dimension)
    else:
        adjacent_corner_list = get_adjacent_bottom_corner_cells(cell,
                                                                dimension)
    return adjacent_corner_list


def get_adjacent_top_corner_cells(cell: list[int],
                                  dimension: int) -> list[list[int]]:
    """Return a list of cells adjacent to top corner cells cell on an elevation
    map with dimensions dimension x dimension.

    Precondition: cell is a valid cell for an elevation map with
                  dimensions dimension x dimension.
                  cell[0] == 0
                  cell[1] == dimension - 1 or cell[1] == 0

    >>> adjacent_cells = get_adjacent_cells([0, 3], 4)
    >>> adjacent_cells.sort()
    >>> adjacent_cells
    [[0, 2], [1, 2], [1, 3]]
    >>> adjacent_cells = get_adjacent_cells([0, 2], 3)
    >>> adjacent_cells.sort()
    >>> adjacent_cells
    [[0, 1], [1, 1], [1, 2]]
    >>> adjacent_cells = get_adjacent_cells([0, 0], 3)
    >>> adjacent_cells.sort()
    >>> adjacent_cells
    [[0, 1], [1, 0], [1, 1]]

    """
    top_corner_list = []
    last_valid = dimension - 1
    for i in range(2):
        for j in range(2):
            if cell == [0, 0] and [i, j] != [0, 0]:
                adjacent = [cell[0] + i, cell[1] + j]
                top_corner_list.append(adjacent)
            elif cell == [0, last_valid] and [i, j] != [0, 0]:
                adjacent = [cell[0] + i, cell[1] - j]
                top_corner_list.append(adjacent)
    return top_corner_list


def get_adjacent_bottom_corner_cells(cell: list[int],
                                     dimension: int) -> list[list[int]]:
    """Return a list of cells adjacent to bottom corner cell cell on an
    elevation map with dimensions dimension x dimension.

    Precondition: cell is a valid cell for an elevation map with
                  dimensions dimension x dimension.
                  cell[0] == dimension - 1
                  cell[1] == dimension - 1 or cell[1] == 0

    >>> adjacent_cells = get_adjacent_cells([3, 3], 4)
    >>> adjacent_cells.sort()
    >>> adjacent_cells
    [[2, 2], [2, 3], [3, 2]]
    >>> adjacent_cells = get_adjacent_cells([2, 2], 3)
    >>> adjacent_cells.sort()
    >>> adjacent_cells
    [[1, 1], [1, 2], [2, 1]]
    >>> adjacent_cells = get_adjacent_cells([2, 0], 3)
    >>> adjacent_cells.sort()
    >>> adjacent_cells
    [[1, 0], [1, 1], [2, 1]]
    >>> adjacent_cells = get_adjacent_cells([3, 0], 4)
    >>> adjacent_cells.sort()
    >>> adjacent_cells
    [[2, 0], [2, 1], [3, 1]]

    """
    bottom_corner_list = []
    last_valid = dimension - 1
    for i in range(2):
        for j in range(2):
            if cell == [last_valid, 0] and [i, j] != [0, 0]:
                adjacent = [cell[0] - i, cell[1] + j]
                bottom_corner_list.append(adjacent)
            elif cell == [last_valid, last_valid] and [i, j] != [0, 0]:
                adjacent = [cell[0] - i, cell[1] - j]
                bottom_corner_list.append(adjacent)
    return bottom_corner_list


def get_2x2_adjacent_average(cell: list[int], elevation_map:
                             list[list[int]]) -> int:
    """Return the average of adjacent elevation of local elevation with cell
    cell on 2x2 entries on an elevation map elevation_map. Elevation at cell
    cell is included in the sum and cell cell is considered as the most
    northwest elevation of the entries.

    Precondition: cell[0] is even, in which 0 is included
                  cell[1] in even, in which 0 is included
                  is_valid_cell(cell,len(elevation_map)) == True
                  len(elevation_map) %2 == 0

    >>> get_2x2_adjacent_average([0,0], FOUR_BY_FOUR)
    3
    >>> get_2x2_adjacent_average([2,0], FOUR_BY_FOUR)
    4
    >>> get_2x2_adjacent_average([2,2], UNIQUE_4X4)
    12
    """
    adjacent_list = []
    row = cell[0]
    column = cell[1]
    total = 0
    for i in range(2):
        for j in range(2):
            adjacent_cell = [row + i, column + j]
            adjacent_list.append(adjacent_cell)
    for adjacent in adjacent_list:
        total += elevation_map[adjacent[0]][adjacent[1]]
    average = total // 4
    return average


def get_odd_up_average(elevation_map: list[list[int]]) -> list[list[int]]:
    """Return a new elevation map that contains the average of the original
    elevation on the new entries on an odd side-length map elevation_map. This
    new elevation only covers the 2x2 entries and 1x2 entries that aren't on
    the last row.

    Precondition: elevation_map is a valid elevation map.
                  len(elevation_map) % 2 != 0

    >>> get_odd_up_average(THREE_BY_THREE)
    [[3, 3]]
    >>> get_odd_up_average(UNIQUE_3X3)
    [[5, 5]]

    """
    odd_top_list = []
    last_valid = len(elevation_map) - 1
    average_list = []
    for row in range(0, last_valid, 2):
        for column in range(0, last_valid, 2):
            average = get_2x2_adjacent_average([row, column], elevation_map)
            average_list.append(average)
            if len(average_list) == (len(elevation_map) - 1) / 2:
                total = elevation_map[row][last_valid] + elevation_map[
                    row + 1][last_valid]
                average = total // 2
                average_list.append(average)
                odd_top_list.append(average_list)
                average_list = []
    return odd_top_list


def get_odd_bottom_average(elevation_map: list[list[int]]) -> list[int]:
    """Return a new elevation map that contains the average of the original
    elevation on the new entries on an odd side-length map elevation_map. This
    new elevation only covers the 1x2 entries and individual entry on the
    last row.

    Precondition: elevation_map is a valid elevation map.
                  len(elevation_map) % 2 != 0

    >>> get_odd_bottom_average(THREE_BY_THREE)
    [7, 9]
    >>> get_odd_bottom_average(UNIQUE_3X3)
    [4, 6]

    """
    last_valid = len(elevation_map)-1
    average_odd_bottom = []
    for column in range(0, last_valid, 2):
        total = get_last_row_sum([last_valid, column], elevation_map)
        average = total // 2
        average_odd_bottom.append(average)
        if len(average_odd_bottom) == (len(elevation_map) - 1) / 2:
            average_odd_bottom.append(elevation_map[last_valid][last_valid])
    return average_odd_bottom


def get_last_row_sum(cell: list[int], elevation_map: list[list[int]]) -> int:
    """Return the sum of local elevation at cell cell and the elevation from
    one column east from it. Cell cell is considered as the westest cell of
    the entries.

    Precondition: cell[0] == len(elevation_map) - 1
                  cell[1] in even, in which 0 is included
                  cell[1] < len(elevation_map) - 1
                  is_valid_cell(cell,len(elevation_map)) == True
                  len(elevation_map) %2 != 0

    >>> get_last_row_sum([2,0],THREE_BY_THREE)
    15
    >>> get_last_row_sum([2,0],UNIQUE_3X3)
    9
    >>> get_last_row_sum([2,0],THREE_BY_THREE)
    15
    """
    adjacent_list = []
    column = cell[1]
    row = cell[0]
    total = 0
    for j in range(2):
        adjacent_cell = [row, column + j]
        adjacent_list.append(adjacent_cell)
    for adjacent in adjacent_list:
        total += elevation_map[adjacent[0]][adjacent[1]]
    return total


if __name__ == '__main__':
    import doctest

    doctest.testmod()
