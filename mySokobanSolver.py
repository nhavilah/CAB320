
'''

    2020 CAB320 Sokoban assignment


The functions and classes defined in this module will be called by a marker script.
You should complete the functions and classes according to their specified interfaces.
No partial marks will be awarded for functions that do not meet the specifications
of the interfaces.


You are NOT allowed to change the defined interfaces.
That is, changing the formal parameters of a function will break the
interface and results in a fail for the test of your code.
This is not negotiable!


'''

# You have to make sure that your code works with
# the files provided (search.py and sokoban.py) as your code will be tested
# with these files
import search
import sokoban


# Useful Variables
#define a list of moves that the player/box can undertake
moveset = {
    'Up': (0, -1),
    'Down': (0, 1),
    'Left': (-1, 0),
    'Right': (1, 0)
}
#define an empty array to store the costs of moving for the weighted solver
costs = []
#define an empty array to store the taboo cells identified, so the solvers can use them
taboo_cells_arr = []
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


def my_team():
    '''
    Return the list of the team members of this assignment submission as a list
    of triplet of the form (student_number, first_name, last_name)

    '''
    return [(9448977, 'Kevin', 'Duong'), (10469231, 'Nicholas', 'Havilah'), (10522662, 'Connor', 'McHugh')]

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


def taboo_cells(warehouse):
    '''
    Identify the taboo cells of a warehouse. A cell inside a warehouse is
    called 'taboo'  if whenever a box get pushed on such a cell then the puzzle
    becomes unsolvable. Cells outside the warehouse should not be tagged as taboo.
    When determining the taboo cells, you must ignore all the existing boxes,
    only consider the walls and the target  cells.
    Use only the following two rules to determine the taboo cells;
     Rule 1: if a cell is a corner and not a target, then it is a taboo cell.
     Rule 2: all the cells between two corners along a wall are taboo if none of
             these cells is a target.

    @param warehouse:
        a Warehouse object with a worker inside the warehouse

    @return
       A string representing the puzzle with only the wall cells marked with
       a '#' and the taboo cells marked with a 'X'.
       The returned string should NOT have marks for the worker, the targets,
       and the boxes.
    '''

    # Variables
    taboo_cells
    taboo_visual = ''
    #allows us to assign values globally so other solvers can use them
    global taboo_cells_arr
    taboo_cells_arr = []
    # Assign easier variable names to properties from the sokoban file
    warehouse_width = warehouse.ncols
    warehouse_height = warehouse.nrows
    walls = warehouse.walls
    targets = warehouse.targets
    boxes = warehouse.boxes
    player = warehouse.worker

    # Check for taboo cells using Rule 1
    for y in range(warehouse_height):
        # Initialy, the program assumes that it is not looking in the game area
        inside_walls = False

        for x in range(warehouse_width):
            # This only needs to be run until the program find the first wall for each row
            if not inside_walls:
                # Once we find the first wall in a row, we can assume that we have entered the game area
                if (x, y) in walls:
                    inside_walls = True

            else:
                # If the program finds lots of empty space after a wall, we can assume that we have left the game area
                # THIS MAY NEED TO BE REWRITTERN TO BE MORE DEFINITE (e.g. with a loop)
                if (x+1, y) not in walls and (x+2, y) not in walls and (x+3, y) not in walls and (x+4, y) not in walls and (x+5, y) not in walls:
                    inside_walls = False
                    break

                if (x, y) not in walls and (x, y) not in targets:
                    if (x, y-1) in walls and (x-1, y) in walls:
                        taboo_cells_arr.append((x, y))

                    if (x, y-1) in walls and (x+1, y) in walls:
                        taboo_cells_arr.append((x, y))

                    if (x-1, y) in walls and (x, y+1) in walls:
                        taboo_cells_arr.append((x, y))

                    if (x+1, y) in walls and (x, y+1) in walls:
                        taboo_cells_arr.append((x, y))

    # Check for taboo cells using Rule 2
    for y in range(warehouse_width):
        for x in range(warehouse_height):
            if (x, y) not in walls and (x, y) not in targets:
                if (x+1, y) in taboo_cells_arr and (x-1, y) in taboo_cells_arr and (x, y-1) in walls:
                    taboo_cells_arr.append((x, y))

                if (x, y+1) in taboo_cells_arr and (x, y-1) in taboo_cells_arr and (x-1, y) in walls:
                    taboo_cells_arr.append((x, y))

                if (x+1, y) in taboo_cells_arr and (x-1, y) in taboo_cells_arr and (x, y+1) in walls:
                    taboo_cells_arr.append((x, y))

                if (x, y+1) in taboo_cells_arr and (x, y-1) in taboo_cells_arr and (x+1, y) in walls:
                    taboo_cells_arr.append((x, y))

    # Generate a string of the warehouse with taboo cells marked
    for y in range(warehouse_height):
        # Add a new line character as long as it is after the first row but before the last row
        if x > 0 and y > 0 and x < warehouse_height:
            taboo_visual += '\n'

        for x in range(warehouse_width):
            # Add empty spaces
            if (x, y) not in walls and (x, y) not in taboo_cells_arr:
                taboo_visual += ' '

            # Add wall characters
            if (x, y) in walls and (x, y) not in (taboo_cells_arr):
                taboo_visual += '#'

            # Add taboo cell markers
            if (x, y) in taboo_cells_arr and (x, y) not in (walls):
                taboo_visual += 'X'
    return str(taboo_visual)

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


def manhattan_distance(coords_a, coords_b):
    '''
    Calculate and return the manhattan distance between two cells.

    @param coord_a:
        Tuple containing the first set of coordinates

    @param coord_b:
        Tuple containing the second set of coordinates

    @return:
        An integer that is the manhattan distance between the given sets of 
        coordinates

    '''
    manhattan = int(abs(coords_a[0] - coords_b[0]) +
                    abs(coords_a[1] - coords_b[1]))
    return manhattan

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


def tuple_addition(a, b):
    '''
    Add values in tuples

    @param a:
        First tuple

    @param b:
        Second tuple

    @return:
        A new tuple that is the values of the param tuples added toether

    '''
    added = (a[0] + b[0], a[1] + b[1])
    return added

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


def tuple_subtraction(a, b):
    '''
    Subtract values in tuples

    @param a:
        First tuple

    @param b:
        Second tuple

    @return:
        A new tuple that is the values of the param tuples minused

    '''
    subtracted = (a[0] - b[0], a[1] - b[1])
    return subtracted

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


def warehouse_update(warehouse, state):
    '''
    Update the state of the website

    @param warehouse:
        The initial warehouse

    @param b:
        The current state of the warehouse

    @return:
        The updated state of the warehouse

    '''
    warehouse.boxes = state[1]
    warehouse.worker=state[0]
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


class SokobanPuzzle(search.Problem):
    '''
    An instance of the class 'SokobanPuzzle' represents a Sokoban puzzle.
    An instance contains information about the walls, the targets, the boxes
    and the worker.

    Your implementation should be fully compatible with the search functions of 
    the provided module 'search.py'. 

    Each SokobanPuzzle instance should have at least the following attributes
    - self.allow_taboo_push
    - self.macro

    When self.allow_taboo_push is set to True, the 'actions' function should 
    return all possible legal moves including those that move a box on a taboo 
    cell. If self.allow_taboo_push is set to False, those moves should not be
    included in the returned list of actions.

    If self.macro is set True, the 'actions' function should return 
    macro actions. If self.macro is set False, the 'actions' function should 
    return elementary actions.        
    '''
    #call for the global values of taboo cells in order to use them for the actions
    global taboo_cells_arr
    #allow player/boxes to move onto the taboo cells or not
    allow_taboo_push = False
    #call for the macro solver's actions and results, else will call for the elementary solver's moves and actions
    macro = False
    #allows the weighted elementary solver to define weightings for each movement
    weighted = False
    #initialise variables for the rest of the class to use
    def __init__(self, warehouse):
        self.puzzle = warehouse

        self.boxes = self.puzzle.boxes
        self.walls = self.puzzle.walls

        self.goal = self.puzzle.targets
        self.initial = (warehouse.worker, tuple(self.puzzle.boxes))
        self.taboo = taboo_cells(self.puzzle)

    def actions(self, state):
        """
        Return the list of actions that can be executed in the given state.

        As specified in the header comment of this class, the attributes
        'self.allow_taboo_push' and 'self.macro' should be tested to determine
        what type of list of actions is to be returned.
        """
        # Variable definitions
        worker, box_pos = state
        allowable_actions = []

        # this part is used for macro actions
        if self.macro == True:
            #this prevents the boxes moving onto taboo cells
            if self.allow_taboo_push == False:
                #ensure the warehouse is updated
                warehouse_update(self.puzzle, state)
                for box in box_pos:
                    for direction, move in moveset.items():
                        next_state = tuple_addition(box, move)
                        pushers_position = tuple_subtraction(box, move)
                        #rearrange the position array so the can_go_there function can read it
                        [a, b] = pushers_position
                        pushers_position = (b, a)
                        #check the move is legal and the player can get there
                        if next_state not in self.puzzle.walls and next_state not in box_pos and next_state not in taboo_cells_arr and can_go_there(self.puzzle, pushers_position):
                            allowable_actions.append((box, direction))
            #this allows boxes to(unwisely move onto taboo cells)
            else:
                #ensure the warehouse is updated
                warehouse_update(self.puzzle, state)
                for box in box_pos:
                    for direction, move in moveset.items():
                        next_state = tuple_addition(box, move)
                        pushers_position = tuple_subtraction(box, move)
                        #rearrange the position array so the can_go_there function can read it
                        [a, b] = pushers_position
                        pushers_position = (b, a)
                        #check the move is legal and the player can get there
                        if next_state not in self.puzzle.walls and next_state not in box_pos and can_go_there(self.puzzle, pushers_position):
                            allowable_actions.append((box, direction))
        # this part is used for elementary actions
        else:
            #prevents the box from being pushed into taboo cells
            if self.allow_taboo_push == False:
                for direction, move in moveset.items():
                    # move the player
                    worker_next_pos = tuple_addition(worker, move)
                    box_next_pos = tuple_addition(worker_next_pos, move)
                    # check player isn't pushing into a wall
                    if worker_next_pos not in self.walls:
                        #checks if the player is pushing a box
                        if worker_next_pos in box_pos:
                            #check the box move is legal
                            if box_next_pos not in self.walls and box_next_pos not in box_pos and box_next_pos not in taboo_cells_arr:
                                allowable_actions.append(direction)
                        #otherwise it's not pushing a box and the move is legal
                        else:
                            allowable_actions.append(direction)
            #this allows the player to(unwisely) move boxes into taboo cells
            else:
                for direction, move in moveset.items():
                    # move the player
                    worker_next_pos = tuple_addition(worker, move)
                    box_next_pos = tuple_addition(worker_next_pos, move)
                    # check player isn't pushing into a wall
                    if worker_next_pos not in self.walls:
                        #checks if the player is pushing a box
                        if worker_next_pos in box_pos:
                            #check the box move is legal
                            if box_next_pos not in self.walls and box_next_pos not in box_pos:
                                allowable_actions.append(direction)
                        #otherwise it's not pushing a box and the move is legal
                        else:
                            allowable_actions.append(direction)
        return allowable_actions

    def result(self, state, actions):
        """Return the state that results from executing the given
        action in the given state. The action must be one of
        self.actions(state).
        applying action a to state s results in
        s_next = s[:a]+s[-1:a-1:-1]
        """
        #this part is used by the macro solver
        if self.macro == True:
            #defines the current state
            worker = state[0]
            boxes = state[1]
            boxes = list(boxes)
            worker = actions[0]
            #updates the positions of the boxes and player as needed
            updated_box = tuple_addition(actions[0], moveset[actions[1]])
            boxes[boxes.index(actions[0])] = updated_box
            boxes = tuple(boxes)
        #this part is used by the elementary solvers(weighted and non weighted elementary solvers)
        else:
            #defines the current state
            worker = state[0]
            boxes = state[1]
            boxes = list(boxes)
            #updates the state as needed
            new_worker_pos = tuple_addition(worker, moveset[actions])
            #moves boxes if they're pushed
            if new_worker_pos in boxes:
                boxes[boxes.index(new_worker_pos)] = tuple_addition(
                    new_worker_pos, moveset[actions])
            worker = new_worker_pos
            boxes = tuple(boxes)
        return (worker, boxes)

    def goal_test(self, state):
        """Returns a boolean based on whether the
        current state matches the defined goal state
        """
        return set(state[1]) == set(self.goal)

    def h(self, n):
        """Call the heuristic function
        with the current node index
        and the current state of the puzzle """
        return heuristic(self, n)

    # define the path cost(used for the weighted solver(note this bit is lifted from search.py and then modified)
    def path_cost(self, c, state1, action, state2):
        """
        Defines the path cost for the solvers. If it is for the
        macro and elementary solvers, they return a move cost of 1.

        The weighted solver has different weightings for different moves.
        If the move doesn't push a box, it only costs 1.
        If the move pushes a box, it finds the cost relative to the index of the box
        (From the global array of move costs)
        """
        if self.weighted == False:
            return c+1
        else:
            #define the current state
            player_initial = state1[0]
            boxes = state1[1]
            #apply a move to the player
            player_final = tuple_addition(player_initial, moveset[action])
            #check whether boxes get moved and return a path cost as defined by the descriptor above
            if player_final in boxes:
                return c + costs[boxes.index(player_final)]
            else:
                return c+1

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


def heuristic(problem, node):
    """
    This heuristic returns the average of:
    1) The distance between the player and the closest box
    2) The average distance between boxes and their closest targets
    """
    # step 1 is to define the variables
    worker = node.state[0]
    boxes = list(node.state[1])
    targets = list(problem.goal)
    # step 2 is to calculate the distance between  player and the closest box
    # create an array to store the distances between the player and each box
    distances = []
    # add each distance to the array
    for box in boxes:
        distances.append(manhattan_distance(worker, box))
    # find out the closest distance
    closest_distance = min(distances)
    # step 3 is to find the distance between each box and its closest target
    # create an array to store the distance between each box and its closest target
    box_distances = []
    # find out the distance between each box its closest target
    for box in boxes:
        # store the distance between the box and each target
        box_to_targets_distance = []
        for target in targets:
            box_to_targets_distance.append(manhattan_distance(box, target))
        closest_target_to_box_distance = min(box_to_targets_distance)
        box_distances.append(closest_target_to_box_distance)
    # find the average distance between boxes and their closest targets
    average_distance_boxes_to_targets = sum(box_distances)/len(box_distances)
    # step 4 is to find the average of the previous 2 steps
    heuristic_distance = (closest_distance+average_distance_boxes_to_targets)/2
    return heuristic_distance


# ---------------------------------------------------------------------------------------------------------------------------


class player_path(search.Problem):
    '''
    This class is used to determine a path from the player to a given location. This location will, in most
    cases, be the location next to the box that the player needs to move
    '''
    #initialise the current state of the mini puzzle
    def __init__(self, warehouse, goal, initial):
        self.puzzle = warehouse
        self.goal = goal
        self.initial = initial
        self.walls = self.puzzle.walls
        self.boxes = self.puzzle.boxes
    #define the actions that the player can undertake
    def actions(self, state):
        allowable_actions = []
        for direction, move in moveset.items():
            next_state = tuple_addition(state, move)
            #check the move is legal
            if next_state not in self.walls and next_state not in self.boxes:
                allowable_actions.append(direction)
        return allowable_actions
    #return the result of the applied action to the current state
    def result(self, state, actions):
        state = tuple_addition(state, moveset[actions])
        return state
    #check if the player has reached the goal
    def goal_test(self, state):
        return state == self.goal

def can_go_there(warehouse, dst):
    '''    
    Determine whether the worker can walk to the cell dst=(row,column) 
    without pushing any box.

    @param warehouse: a valid Warehouse object

    @return
      True if the worker can walk to cell dst=(row,column) without pushing any box
      False otherwise
    '''
    #flip the coordinates around so it works with can_go_there
    [a, b] = dst
    dst = (b, a)
    #define a heuristic that returns the manhattan distance between the player and the target
    def heuristic(n):
        state = n.state
        return manhattan_distance(state, dst)
    #define the puzzle, then apply the search algorithm to the puzzle
    puzzle = player_path(warehouse, dst, warehouse.worker)
    path = search.astar_graph_search(puzzle, heuristic)
    #return the results of the solver
    if path is None:
        return False
    else:
        return True
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


def check_elem_action_seq(warehouse, action_seq):
    '''

    Determine if the sequence of actions listed in 'action_seq' is legal or not.

    Important notes:
      - a legal sequence of actions does not necessarily solve the puzzle.
      - an action is legal even if it pushes a box onto a taboo cell.

    @param warehouse: a valid Warehouse object

    @param action_seq: a sequence of legal actions.
           For example, ['Left', 'Down', Down','Right', 'Up', 'Down']

    @return
        The string 'Impossible', if one of the action was not successul.
           For example, if the agent tries to push two boxes at the same time,
                        or push one box into a wall.
        Otherwise, if all actions were successful, return                 
               A string representing the state of the puzzle after applying
               the sequence of actions.  This must be the same string as the
               string returned by the method  Warehouse.__str__()
    '''
    #define the initial state
    worker = warehouse.worker
    walls = warehouse.walls
    boxes = warehouse.boxes

    (x, y) = worker

    # Run through each action in the sequence of actions
    for action in action_seq:
        if (action == 'Down'):
            # If the next position of the worker is a wall, it is an impossible move
            if ((x, y + 1) in walls):
                return 'Impossible'
                break

            # If the next position of the box is a wall or another box, it is an impossible move
            elif ((x, y + 1) in boxes and (x, y + 2) in (walls or boxes)):
                return 'Impossible'
                break

            # If the next position is safe to move into, do so
            else:
                (x, y) = (x, y + 1)
                worker = (x, y)

        elif (action == 'Up'):
            # If the next position of the worker is a wall, it is an impossible move
            if ((x, y - 1) in walls):
                return 'Impossible'
                break

            # If the next position of the box is a wall or another box, it is an impossible move
            elif ((x, y - 1) in boxes and (x, y - 2) in (walls or boxes)):
                return 'Impossible'
                break

            # If the next position is safe to move into, do so
            else:
                (x, y) = (x, y - 1)
                worker = (x, y)

        elif (action == 'Right'):
            # If the next position of the worker is a wall, it is an impossible move
            if ((x + 1, y) in walls):
                return 'Impossible'
                break

            # If the next position of the box is a wall or another box, it is an impossible move
            elif ((x + 1, y) in boxes and (x + 2, y) in (walls or boxes)):
                return 'Impossible'
                break

            # If the next position is safe to move into, do so
            else:
                (x, y) = (x + 1, y)
                worker = (x, y)

        elif (action == 'Left'):
            # If the next position of the worker is a wall, it is an impossible move
            if ((x - 1, y) in walls):
                return 'Impossible'
                break

            # If the next position of the box is a wall or another box, it is an impossible move
            elif ((x - 1, y) in boxes and (x - 2, y) in (walls or boxes)):
                return 'Impossible'
                break

            # If the next position is safe to move into, do so
            else:
                (x, y) = (x - 1, y)
                worker = (x, y)

        new_warehouse = warehouse
        new_warehouse.worker = worker

    return str(new_warehouse)


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


def solve_sokoban_elem(warehouse):
    '''    
    This function should solve using A* algorithm and elementary actions
    the puzzle defined in the parameter 'warehouse'.

    In this scenario, the cost of all (elementary) actions is one unit.

    @param warehouse: a valid Warehouse object

    @return
        If puzzle cannot be solved return the string 'Impossible'
        If a solution was found, return a list of elementary actions that solves
            the given puzzle coded with 'Left', 'Right', 'Up', 'Down'
            For example, ['Left', 'Down', Down','Right', 'Up', 'Down']
            If the puzzle is already in a goal state, simply return []
    '''
    # define the problem
    puzzle = SokobanPuzzle(warehouse)
    # set the macro bool to True
    puzzle.macro = False
    puzzle.allow_taboo_push = False
    puzzle.weighted = False
    # implement the algorithm we want to use
    sol = search.astar_graph_search(puzzle, puzzle.h)
    #return the results of the solver
    if sol is None:
        return 'Impossible'
    else:
        return sol.solution()

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


def solve_sokoban_macro(warehouse):
    '''    
    Solve using using A* algorithm and macro actions the puzzle defined in 
    the parameter 'warehouse'. 

    A sequence of macro actions should be 
    represented by a list M of the form
            [ ((r1,c1), a1), ((r2,c2), a2), ..., ((rn,cn), an) ]
    For example M = [ ((3,4),'Left') , ((5,2),'Up'), ((12,4),'Down') ] 
    means that the worker first goes the box at row 3 and column 4 and pushes it left,
    then goes to the box at row 5 and column 2 and pushes it up, and finally
    goes the box at row 12 and column 4 and pushes it down.

    In this scenario, the cost of all (macro) actions is one unit. 

    @param warehouse: a valid Warehouse object

    @return
        If the puzzle cannot be solved return the string 'Impossible'
        Otherwise return M a sequence of macro actions that solves the puzzle.
        If the puzzle is already in a goal state, simply return []
    '''
    # define the problem
    puzzle = SokobanPuzzle(warehouse)
    # set the macro bool to True
    puzzle.macro = True
    puzzle.allow_taboo_push = False
    puzzle.weighted = False
    # implement the algorithm we want to use
    sol = search.astar_graph_search(puzzle, puzzle.h)
    #return the results of the solver
    if sol is None:
        return ['Impossible']
    else:
        solution_arr = []
        #return the solution formatted to work in sanity_check
        for coord, box in sol.solution():
            solution_arr.append(((coord[1], coord[0]), box))
        return solution_arr

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


def solve_weighted_sokoban_elem(warehouse, push_costs):
    '''
    In this scenario, we assign a pushing cost to each box, whereas for the
    functions 'solve_sokoban_elem' and 'solve_sokoban_macro', we were 
    simply counting the number of actions (either elementary or macro) executed.

    When the worker is moving without pushing a box, we incur a
    cost of one unit per step. Pushing the ith box to an adjacent cell 
    now costs 'push_costs[i]'.

    The ith box is initially at position 'warehouse.boxes[i]'.

    This function should solve using A* algorithm and elementary actions
    the puzzle 'warehouse' while minimizing the total cost described above.

    @param 
     warehouse: a valid Warehouse object
     push_costs: list of the weights of the boxes (pushing cost)

    @return
        If puzzle cannot be solved return 'Impossible'
        If a solution exists, return a list of elementary actions that solves
            the given puzzle coded with 'Left', 'Right', 'Up', 'Down'
            For example, ['Left', 'Down', Down','Right', 'Up', 'Down']
            If the puzzle is already in a goal state, simply return []
    '''
    # add the push costs to a global variable so the path costs can be used by the puzzle class
    for cost in push_costs:
        costs.append(cost)
    # define the problem
    puzzle = SokobanPuzzle(warehouse)
    # set the macro bool to True
    puzzle.macro = False
    puzzle.allow_taboo_push = False
    puzzle.weighted = True
    # implement the algorithm we want to use
    sol = search.astar_graph_search(puzzle, puzzle.h)
    #return the results of the solver
    if sol is None:
        return 'Impossible'
    else:
        return sol.solution()

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

