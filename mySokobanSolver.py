
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


# DEFINE SOME GLOBAL VARIABLES
UP=(0,-1)
DOWN=(0,1)
LEFT=(-1,0)
RIGHT=(1,0)
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


def my_team():
    '''
    Return the list of the team members of this assignment submission as a list
    of triplet of the form (student_number, first_name, last_name)

    '''
    return [(12345678, 'Kevin', 'Duong'), (10469231, 'Nicholas', 'Havilah'), (10522662, 'Connor', 'McHugh')]

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
    global taboo_cells
    taboo_cells_arr = []
    taboo_visual = ''

    # Assign easier variable names to properties from the sokoban file
    warehouse_width = warehouse.ncols
    warehouse_height = warehouse.nrows
    walls = warehouse.walls
    targets = warehouse.targets

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

        for x in range(warehouse_height):
            # Add empty spaces
            if (x, y) not in walls and (x, y) not in taboo_cells_arr:
                taboo_visual += ' '

            # Add wall characters
            if (x, y) in walls and (x, y) not in (taboo_cells_arr):
                taboo_visual += '#'

            # Add taboo cell markers
            if (x, y) in taboo_cells_arr and (x, y) not in (walls):
                taboo_visual += 'X'

    # print(taboo_visual)
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

    allow_taboo_push = False
    macro = False

    def __init__(self, warehouse, targets):
##        search.Problem.__init__(self, initial)
##        self.game = warehouse
##        self.targets = self.game.targets
##        self.macro = macro
##        self.walls = walls
##        self.boxes = boxes
##        self.worker = worker
##        self.taboo = taboo_cells(self.game)
        self.puzzle = warehouse
        self.goal = goal
        self.initial = initial
        self.walls = self.puzzle.walls
        self.boxes = self.puzzle.boxes
        walls = warehouse.walls
        targets = warehouse.targets
        boxes = warehouse.boxes
        worker=warehouse.worker
        
    def actions(self, state):
        """
        Return the list of actions that can be executed in the given state.

        As specified in the header comment of this class, the attributes
        'self.allow_taboo_push' and 'self.macro' should be tested to determine
        what type of list of actions is to be returned.
        """
        # define all available actions as a tuple(not permeable this way)
        allActions = ["L", "R", "U", "D"]
        # determine the list of legal actions to be returned, based on if its elementary or macro movements
        if self.macro == False:
            # retrieve the current players position
            current_position = self.worker
            if self.allow_taboo_push == True:
                if ((current_position.x+1), current_position.y) not in walls or ((current_position.x+1), current_position.y) not in taboo_cells_arr:
                    allActions.remove("R")
                if ((current_position.x-1), current_position.y) not in walls or ((current_position.x-1), current_position.y) not in taboo_cells_arr:
                    allActions.remove("L")
                if (current_position.x, (current_position.y+1)) not in walls or (current_position.x, (current_position.y+1)) not in taboo_cells_arr:
                    allActions.remove("D")
                if (current_position.x, (current_position.y-1)) not in walls or (current_position.x, (current_position.y-1)) not in taboo_cells_arr:
                    allActions.remove("U")
            if self.allow_taboo_push == False:
                # retrieve the current players position
                if ((current_position.x+1), current_position.y) not in walls:
                    allActions.remove("R")
                if ((current_position.x-1), current_position.y) not in walls:
                    allActions.remove("L")
                if (current_position.x, (current_position.y+1)) not in walls:
                    allActions.remove("D")
                if (current_position.x, (current_position.y-1)) not in walls:
                    allActions.remove("U")
        if self.macro == True:
            for box in self.boxes:
                current_position = box
                if self.allow_taboo_push == True:
                    if ((current_position.x+1), current_position.y) not in walls or ((current_position.x+1), current_position.y) not in taboo_cells_arr:
                        allActions.remove("R")
                    if ((current_position.x-1), current_position.y) not in walls or ((current_position.x-1), current_position.y) not in taboo_cells_arr:
                        allActions.remove("L")
                    if (current_position.x, (current_position.y+1)) not in walls or (current_position.x, (current_position.y+1)) not in taboo_cells_arr:
                        allActions.remove("D")
                    if (current_position.x, (current_position.y-1)) not in walls or (current_position.x, (current_position.y-1)) not in taboo_cells_arr:
                        allActions.remove("U")
                if self.allow_taboo_push == False:
                    # retrieve the current players position
                    if ((current_position.x+1), current_position.y) not in walls:
                        allActions.remove("R")
                    if ((current_position.x-1), current_position.y) not in walls:
                        allActions.remove("L")
                    if (current_position.x, (current_position.y+1)) not in walls:
                        allActions.remove("D")
                    if (current_position.x, (current_position.y-1)) not in walls:
                        allActions.remove("U")
        return allActions

    def result(self, state, action):
        """Return the state that results from executing the given
        action in the given state. The action must be one of
        self.actions(state).
        applying action a to state s results in
        s_next = s[:a]+s[-1:a-1:-1]
        """
        assert action in self.actions(state)
        if action in self.actions(state)=="L":
            worker=worker+LEFT
        if action in self.actions(state)=="R":
            worker=worker+RIGHT
        if action in self.actions(state)=="U":
            worker=worker+UP
        if action in self.actions(state)=="D":
            worker=worker+DOWN
        return tuple(list(state[:action])+list(reversed(state[action:])))
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


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

    # "INSERT YOUR CODE HERE"
    raise NotImplementedError()


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
    #empty list to store the boxes if they aren't in the goal state
    #boxes_out_of_goal_state=[]
    #This function defines the approximate cost of movement that will be required from manhattan distance
##    walls = warehouse.walls
##    targets = warehouse.targets
##    boxes = warehouse.boxes
##    worker=warehouse.worker
##    state=walls,targets,boxes,worker
    def hooristic():
        #check if the boxes are in the target areas or not, and if they aren't, append them to a list that we can work from
        # for target in self.targets:
        #     for box in self.boxes:
        #         if box not in target:
        #             boxes_out_of_goal_state.append("Goal Cell")
        #             boxes_out_of_goal_state.append(target)
        #             boxes_out_of_goal_state.append("Box To Push")
        #             boxes_out_of_goal_state.append(box)
        box1 = warehouse.boxes[0]    
        target1 = warehouse.targets[0]
        return manhattan_distance(box1,target1)
    
    #define the problem
    puzzle=search.Problem(warehouse,goal=warehouse.targets)
    #implement the algorithm we want to use
    search.astar_graph_search(puzzle, hooristic())
    #print the list of actions taken
    if search.Node.solution is None:
        return []
    else:
        print("LENGTH:",len(search.Node.solution))
        sols=list()
        for coord, box, in search.Node.solution:
              sols.append(((coord[1], coord[0]),box))
        print("SOLUTION",sols)
        return sols
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


def can_go_there(warehouse, dst):
    '''    
    Determine whether the worker can walk to the cell dst=(row,column) 
    without pushing any box.

    @param warehouse: a valid Warehouse object

    @return
      True if the worker can walk to cell dst=(row,column) without pushing any box
      False otherwise
    '''

    # "INSERT YOUR CODE HERE"
    raise NotImplementedError()


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

    # "INSERT YOUR CODE HERE"

    raise NotImplementedError()

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

    raise NotImplementedError()

def main():
    wh = sokoban.Warehouse()
    wh.load_warehouse("./warehouses/warehouse_01.txt")
    solve_sokoban_elem(wh)
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
if __name__=="__main__":
    main()
