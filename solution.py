assignments = []

def assign_value(values, box, value):
    """
    Please use this function to update your values dictionary!
    Assigns a value to a given box. If it updates the board record it.
    """
    values[box] = value
    if len(value) == 1:
        assignments.append(values.copy())
    return values

def cross(A, B):
    return [letter + index for letter in A for index in B]

""" Prepare utilities """
# source of indices
rows = "ABCDEFGHI"
cols = "123456789"
digits = cols
# individual boxes like "A1", "B2"...
boxes = cross(rows, cols)
# unitlists like each row, col, subsquare and diagonal
row_units = [cross(row, cols) for row in rows]
col_units = [cross(rows, col) for col in cols]
subsquare_units = [cross(rs, clms) for rs in ('ABC','DEF','GHI') for clms in ('123','456','789')]
diagonal_units = [[rows[i] + cols[i] for i in range(len(digits))] , [rows[i] + cols[len(digits) - i - 1] for i in range(len(digits))]]
unitlists = row_units + col_units + subsquare_units + diagonal_units
# units matching each box to its respective unit lists
def units_dict():
    results = {}
    for box in boxes:
        box_result = [unitlist for unitlist in unitlists if box in unitlist]
        results[box] = box_result
    return results
units = units_dict()
# peers matching each box to a list of its respective peers
def peers_dict():
    results = {}
    for box, box_unitlists in units.items():
        box_unitlists_flatterned = [item for sublist in box_unitlists for item in sublist]
        results[box] = set(box_unitlists_flatterned) - set([box])
    return results
peers = peers_dict()


def grid_values(grid):
    """
    Convert grid into a dict of {square: char} with '123456789' for empties.
    Args:
        grid(string) - A grid in string form.
    Returns:
        A grid in dictionary form
            Keys: The boxes, e.g., 'A1'
            Values: The value in each box, e.g., '8'. If the box has no value, then the value will be '123456789'.
    """
    values = {}
    assert len(grid) == 81
    for index, box in enumerate(boxes):
        if grid[index] == '.':
            values = assign_value(values, box, digits)
        else:
            values = assign_value(values, box, grid[index])
    return values


def display(values):
    """
    Display the values as a 2-D grid.
    Args:
        values(dict): The sudoku in dictionary form
    """
    width = 1+max(len(values[s]) for s in boxes)
    line = '+'.join(['-'*(width*3)]*3)
    for r in rows:
        print(''.join(values[r+c].center(width)+('|' if c in '36' else '')
                      for c in cols))
        if r in 'CF': print(line)
    print

def naked_twins(values):
    """Eliminate values using the naked twins strategy.
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}

    Returns:
        the values dictionary with the naked twins eliminated from peers.
    """

    # Find all instances of naked twins
    # Eliminate the naked twins as possibilities for their peers

    # loop through all unitlists
    for unitlist in unitlists:
        # init twin
        twin_value = '-1'
        
        # start searching for twin
        for index, box in enumerate(unitlist):
            # found a naked double
            if len(values[box]) == 2:
                # check if it has any twins
                for comparison in unitlist[(index + 1):]:
                    # found a naked twin and stop
                    if values[comparison] == values[box]:
                        twin_value = values[comparison]
                        break

        if int(twin_value) > 0:
            # eliminate twin values from other peers in the same unit
            non_twin_boxes = [box for box in unitlist if len(values[box]) > 2]
            for box in non_twin_boxes:
                for digit in twin_value:
                    values[box] = values[box].replace(digit, '')

        # reset twin value
        twin_value = -1

    return values
        

def eliminate(values):
    # for each box, if a box only has one value, eliminate it from all of its peers
    single_valued_boxes = [box for box in boxes if len(values[box]) == 1]
    for box in single_valued_boxes:
        box_peers = peers[box]
        for peer in box_peers:
            values = assign_value(values, peer, values[peer].replace(values[box],''))
    return values
    

def only_choice(values):

    # for each unitlist, if one value only exists in one certain box, 
    # then it should be the only choice for that box
    for unitlist in unitlists:
        for digit in digits:
            boxes_containing_digit = [box for box in unitlist if digit in values[box]]
            if len(boxes_containing_digit) == 1:
                values = assign_value(values, boxes_containing_digit[0], digit)
    return values

def reduce_puzzle(values):

    def solved_boxes():
        return [box for box in boxes if len(values[box]) == 1]

    # check how many are solved
    solved_boxes_current = solved_boxes()
    # check if both strategies cannot be used more, i.e. stalled
    stalled = False
    # apply eliminate and only_choice strategies
    while not stalled:
        # number of boxes solved before applying strategy
        num_solved_boxes_before = len(solved_boxes())
        # apply strategies
        values = only_choice(naked_twins(eliminate(values)))
        # number of boxes solved after
        num_solved_boxes_after = len(solved_boxes())
        # compare before and after to check if the Sodoku is stalled
        stalled = num_solved_boxes_before == num_solved_boxes_after
        # sanity check:
        # whether in one case we've eliminated all values in a box
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False
    
    return values  

def search(values):
    
    def box_with_min_num_values():
        return min((len(values[s]),s) for s in boxes if len(values[s]) > 1)

    def solved_boxes():
        return [s for s in boxes if len(values[s]) == 1]

    # reduze puzzle first
    values = reduce_puzzle(values)
    # validity check:
    # whether puzzle has already had boxes with zero available values
    if not values:
        return False
    # validity check:
    # whether puzzie has already been solved
    if len(solved_boxes()) == len(boxes):
        return values

    # otherwise, start searching
    # choose the box with minimum number of availbilities
    length, box = box_with_min_num_values()
    # start expanding the search tree by trying out 
    # the available digits in the box
    for digit in values[box]:
        # make a new copy of sudoku
        new_sudoku = values.copy()
        # set our proposed digit for the new sudoku
        new_sudoku = assign_value(new_sudoku, box, digit)
        # start DFS search
        new_sudoku_solution = search(new_sudoku)
        # check if we'got a new solution
        if new_sudoku_solution:
            return new_sudoku_solution


def solve(grid):
    """
    Find the solution to a Sudoku grid.
    Args:
        grid(string): a string representing a sudoku grid.
            Example: '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    Returns:
        The dictionary representation of the final sudoku grid. False if no solution exists.
    """
    return search(grid_values(grid))


if __name__ == '__main__':
    diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    display(solve(diag_sudoku_grid))

    try:
        from visualize import visualize_assignments
        visualize_assignments(assignments)
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')
