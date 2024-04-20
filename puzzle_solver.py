#############################################################
# FILE : puzzle_solver.py
# WRITER : david hadad,david.hadad, 314618448
# EXERCISE : intro2cs2 ex2 2022
# DESCRIPTION: some functions to solve a puzzle with some constrains,
# and check how many solution we can get
# STUDENTS I DISCUSSED THE EXERCISE WITH: Gilad shinaar, eyal
# WEB PAGES THAT I USED: stackoverflow.com, programiz.com, youtube
#############################################################
from typing import *


def max_seen_cells(picture: List[List[int]], row: int, col: int) -> int:
    """A function that receives a partial image and a position on it,
     and returns the number of "visible" cells
     From the cell at this location if all the unknown cells are considered white."""
    if picture[row][col] == 0:
        return 0
    else:
        return 1 + one_direction(picture, row + 1, col, "u", 1) \
               + one_direction(picture, row - 1, col, "d", 1) + one_direction(picture, row, col + 1, "r", 1) \
               + one_direction(picture, row, col - 1, "l", 1)


def out_of_range(picture: List[List[int]], row: int, col: int) -> bool:
    """function that get a given index and chack if he is out of picture"""
    if row >= len(picture) or row < 0 or col >= len(picture[0]) or col < 0:
        return True
    return False


def one_direction(picture: List[List[int]], row: int, col: int, direction: str, is_max) -> int:
    """A function that receives a partial image and a position on it,
     and returns the number of "visible" cells
     From the cell at this location if all the unknown cells are considered white for single direction."""

    if out_of_range(picture, row, col):
        return 0
    if picture[row][col] == 0 and is_max:
        return 0
    if picture[row][col] != 1 and not is_max:
        return 0
    if direction == "u":
        return 1 + one_direction(picture, row + 1, col, direction, is_max)
    elif direction == "d":
        return 1 + one_direction(picture, row - 1, col, direction, is_max)
    elif direction == "r":
        return 1 + one_direction(picture, row, col + 1, direction, is_max)
    elif direction == "l":
        return 1 + one_direction(picture, row, col - 1, direction, is_max)


def min_seen_cells(picture: List[List[int]], row: int, col: int) -> int:
    """like the max, only all the unknown cells in black"""
    if picture[row][col] != 1:
        return 0
    else:
        return 1 + + one_direction(picture, row + 1, col, "u", 0) \
               + one_direction(picture, row - 1, col, "d", 0) + one_direction(picture, row, col + 1, "r", 0) \
               + one_direction(picture, row, col - 1, "l", 0)


def check_constraints(picture: List[List[int]],
                      constraints_set: Set[Tuple[int, int, int]]) -> int:
    """
    A function that receives a partial image and a set of constraints
    , and returns an integer between 0 and 2 that indicates success
    Satisfying the constraints in the partial picture.
    """
    temp_lst = []
    for tuple in constraints_set:
        if tuple[2] == max_seen_cells(picture, tuple[0], tuple[1]) == min_seen_cells(picture, tuple[0], tuple[1]):
            temp_lst.append(1)
        elif tuple[2] <= max_seen_cells(picture, tuple[0], tuple[1]) \
                and tuple[2] >= min_seen_cells(picture, tuple[0], tuple[1]):

            temp_lst.append(2)
        else:
            return 0
    if 2 in temp_lst:
        return 2
    return 1


def start_puzzle(rows, columns):
    """ create a start puzzle with all the cells unknown"""
    puzzle_lst = []
    for i in range(rows):
        puzzle_lst.append([-1 for j in range(columns)])
    return puzzle_lst


def solve_puzzle_helper(constraints_set: Set[Tuple[int, int, int]], picture: [List[List[int]]],
                        current_row, current_column) -> Optional[List[List[int]]]:
    """check if there is a solution for a given picture and list of constrain, rerurn cool accordingly"""
    found = False
    possible_colors = [0, 1]
    rows = len(picture)
    columns = len(picture[0])

    for color in possible_colors:
        if not found:
            picture[current_row][current_column] = color
            if check_constraints(picture, constraints_set):
                if current_row == rows - 1 and current_column == columns - 1:
                    if check_constraints(picture, constraints_set) == 1:
                        found = True
                    return found
                elif current_column == columns - 1 and current_row < rows - 1:
                    found = solve_puzzle_helper(constraints_set, picture, current_row + 1, 0)
                else:
                    found = solve_puzzle_helper(constraints_set, picture, current_row, current_column + 1)
            else:
                picture[current_row][current_column] = -1
    return found


def solve_puzzle(constraints_set: Set[Tuple[int, int, int]],
                 n: int, m: int) -> Optional[List[List[int]]]:
    """A function that accepts a set of constraints and a table size
    (number of rows and number of columns (representing a table)
    Plays, and returns an image depicting one solution of the board, if any."""
    picture = start_puzzle(n, m)
    if solve_puzzle_helper(constraints_set, picture, 0, 0):
        return picture


def how_many_solutions_helper(constraints_set: Set[Tuple[int, int, int]], picture: [List[List[int]]],
                              current_row: int, current_column: int) -> int:
    """return the number of solutions a given constrains and picture has"""
    count = 0
    possible_colors = [0, 1]
    rows = len(picture)
    columns = len(picture[0])

    for color in possible_colors:
        picture[current_row][current_column] = color
        if check_constraints(picture, constraints_set):
            if current_row == rows - 1 and current_column == columns - 1:
                if check_constraints(picture, constraints_set) == 1:
                    count += 1
            elif current_column == columns - 1:
                count += how_many_solutions_helper(constraints_set, picture, current_row + 1, 0)
            else:
                count += how_many_solutions_helper(constraints_set, picture, current_row, current_column + 1)

        picture[current_row][current_column] = -1
    return count


def how_many_solutions(constraints_set: Set[Tuple[int, int, int]],
                       n: int, m: int) -> int:
    """return the number of solutions a given constrains and picture has"""
    picture = start_puzzle(n, m)
    return how_many_solutions_helper(constraints_set, picture, 0, 0)


def generate_puzzle(picture: List[List[int]]) -> Set[Tuple[int, int, int]]:
    constrains_set = set()
    constrains_set_temp = set()
    for i in range(len(picture)):
        for j in range(len(picture[0])):
            constrains_set.add((i, j, max_seen_cells(picture, i, j)))
            constrains_set_temp.add((i, j, max_seen_cells(picture, i, j)))

    for s in constrains_set_temp:
        constrains_set.remove(s)
        if how_many_solutions(constrains_set, len(picture), len(picture[0])) != 1:
            constrains_set.add(s)

    return constrains_set
