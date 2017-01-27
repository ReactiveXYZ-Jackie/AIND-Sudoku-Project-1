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

def naked_twins(values):
    """Eliminate values using the naked twins strategy.
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}

    Returns:
        the values dictionary with the naked twins eliminated from peers.
    """

    # Find all instances of naked twins
    # Eliminate the naked twins as possibilities for their peers

def cross(A, B):
    return [letter + index for letter in a for index in b]

""" Prepare utilities """
# source of indices
rows = "ABCDEFGHI"
cols = "123456789"
# individual boxes like "A1", "B2"...
boxes = cross(rows, cols)
# unitlists like each row, col, subsquare and diagonal
row_units = [cross(row, cols) for row in rows]
col_units = [cross(rows, col) for col in cols]
subsquare_units = [cross(rs, clms) for rs in ('ABC','DEF','GHI') for clms in ('123','456','789')]
diagonal_units = [[rows[i] + cols[i] for i in range(9)] , [rows[i] + cols[9 - i] for i in range(9)]]
unitlists = row_units + col_units + subsquare_units + diagonal_units
# units matching each box to its respective unit lists
def units_dict():
    results = {}
    for box in boxes:
        box_result = [unitlist for unitlist in unitlists if box in unitlist]
        results[box] = box_result
    return results

units = units_dict()

def peers_dict():
    results = {}
    for box, box_unitlists in units:
        results[box] = set([]) - set(box)






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

    for index, box in boxes:
        if grid[index] == '.':
            values[box] = '123456789'
        else:
            values[box] = grid[index]
    return values


def display(values):
    """
    Display the values as a 2-D grid.
    Args:
        values(dict): The sudoku in dictionary form
    """
    pass

def eliminate(values):
    # for each
    pass

def only_choice(values):
    pass

def reduce_puzzle(values):
    pass

def search(values):
    pass

def solve(grid):
    """
    Find the solution to a Sudoku grid.
    Args:
        grid(string): a string representing a sudoku grid.
            Example: '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    Returns:
        The dictionary representation of the final sudoku grid. False if no solution exists.
    """



if __name__ == '__main__':
    diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    display(solve(diag_sudoku_grid))

    try:
        from visualize import visualize_assignments
        visualize_assignments(assignments)
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')
