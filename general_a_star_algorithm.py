import heapq

class Node:
    def __init__(self, problem, goal, parent=None, action=None, g=None) -> None:
        self.parent = parent
        self.action = action
        self.goal = goal

        # g(n)
        if g is None:
            self.g = 0
        else:
            self.g = g
        
        self.state = State(problem, goal, self.g)
    
    def solution(self, actions):
        # recursive function to extract solution path from goal node
        # by following parent pointers back to the root
        if self.action:
            actions.insert(0,self.action)
            return self.parent.solution(actions)
        else:
            return actions

    def __str__(self) -> str:
        return str(self.state.puzzle)
    
    def __repr__(self) -> str:
        return str(self.state.path_cost)

    def __lt__(self, other):
        return self.state.path_cost < other.state.path_cost

class State:
    def __init__(self, problem, goal, g) -> None:
        self.problem = tuple(problem)
        self.puzzle = problem
        self.goal = goal
        self.g = g
        self.path_cost = g + self.h
    
    def actions(self):
        moves = []
        rows = 3
        cols = 3
        blank_index = self.problem.index(0)

        # if blank space not in first row
        # we can go up
        if not (blank_index < cols):
            moves.append("up")

        # if blank space not in last row
        # we can go down
        if not (blank_index >= ((rows*cols) - cols)):
            moves.append("down")


        # if blank space is not in the first col
        # we can go left
        if not (blank_index % rows == 0):
            moves.append("left")

        # if blank space is not in last col
        # we can go right
        if not ((blank_index+1) % (rows) == 0):
            moves.append("right")
        
        return moves
    
    def goal_test(self):
        return self.puzzle == self.goal
    
    @property
    def h(self):
        """
        Heuristic - Manhattan
        """
        total_distance = 0
        for i in range(len(self.problem)):

            # Not counting blank tile
            if self.problem[i] == 0:
                continue  

            tile = self.problem[i]
            current = State.generate_coordinates(self.problem, tile)
            goal = State.generate_coordinates(self.goal, tile)
            manhattan_dist = abs(current[0]-goal[0]) + abs(current[1]-goal[1])
            total_distance += manhattan_dist
        return total_distance
    
    @staticmethod
    def generate_coordinates(puzzle, tile):
        """
        Generate the coordinates of a tile from it's index 
        in a puzzle array. The top left of the puzzle
        corresponds to (1,1).

        Args:
            puzzle: the array holding the 8 puzzle integer values.
            tile: the integer in a puzzle to find the coordinates of.
        Returns:
            the coordinates of the tile in the form of a tuple (x,y).
        """
        cols = 3
        tile_index = puzzle.index(tile) + 1

        if tile_index % cols == 0:
            x = cols
        else:
            x = tile_index % cols
        
        if tile_index % cols == 0:
            # '/' operator returns float
            y = int(tile_index / cols)
        else:
            y = (tile_index // cols) + 1
        return (x,y)
    
    def __hash__(self) -> int:
        return hash(tuple(self.problem))

class AStar:
    def __init__(self, start, goal) -> None:
        self.start = start
        self.goal = goal
        self.frontier = []
        self.frontier_states = {}
        self.explored = {}
    
    @staticmethod
    def generate_problem(puzzle, action):
        """
        Generates the new puzzle from a previous puzzle given an action
        """
        blank_index =  puzzle.index(0)
        cols = 3

        if action == "left":
            new_puzzle = AStar.swap_puzzle(puzzle.copy(),
                                            blank_index,blank_index-1)
        elif action == "right":
            new_puzzle = AStar.swap_puzzle(puzzle.copy(),
                                            blank_index,blank_index+1)
        elif action == "up":
            new_puzzle = AStar.swap_puzzle(puzzle.copy(),
                                            blank_index,blank_index-cols)
        elif action == "down":
            new_puzzle = AStar.swap_puzzle(puzzle.copy(),
                                            blank_index,blank_index+cols)
        return new_puzzle
    
    @staticmethod
    def swap_puzzle(puzzle, pos1, pos2):
        puzzle[pos1], puzzle[pos2] = puzzle[pos2], puzzle[pos1]
        return puzzle
    
    @staticmethod
    def chunk_list(lst, chunk_size):
        """
        Splits a list into chunk_size sized chunks
        returns generator object
        """
        for i in range(0, len(lst), chunk_size):
            yield lst[i:i + chunk_size]
    
    @staticmethod
    def display_board(puzzle):
        """
        Display puzzle array as board
        """
        board = list(AStar.chunk_list(puzzle, 3))
        output_board = ""
        for row in board:
            output_board += "|"
            for tile in row:
                if tile == 0:
                    output_board += " |"
                else:
                    output_board += str(tile)+"|"
            output_board += "\n"
        print(output_board)



    @staticmethod
    def display_solution_path(problem, actions):
        """
        Recursive function to display the entire solution
        """

        if actions:
            AStar.display_board(problem)
            next_problem = AStar.generate_problem(problem, actions.pop(0))
            AStar.display_solution_path(next_problem, actions)
        else:
            AStar.display_board(problem)
            print("END")



    
    def solve(self):
        root = Node(self.start, self.goal)
        heapq.heappush(self.frontier, root)
        self.frontier_states[root.state.problem] = root
        
        while(self.frontier):
            node = heapq.heappop(self.frontier)
            del self.frontier_states[node.state.problem]
            
            if node.state.goal_test():
                print("FOUND")
                final_solution = node.solution([])
                AStar.display_solution_path(self.start, final_solution.copy())
                return node.solution([])

            self.explored[node.state.problem] = node

            for action in node.state.actions():
                problem = AStar.generate_problem(node.state.puzzle, action)
                child = Node(problem, self.goal, node, action, node.g+1)

                if (child.state.problem not in self.explored and
                    child.state.problem not in self.frontier_states):
                    heapq.heappush(self.frontier, child)
                    self.frontier_states[child.state.problem] = child
                else:
                    if(child.state.problem in self.frontier_states):
                        # check cost
                        node_in_frontier = self.frontier_states[child.state.problem]
                        if node_in_frontier.g > child.g:
                            # replace that frontier node with child
                            self.frontier.remove(node_in_frontier)
                            heapq.heappush(self.frontier, child)
                            self.frontier_states[child.state.problem] = child



if __name__=='__main__':
    example_start = [7,2,4,5,0,6,8,3,1]
    example_goal = [0,1,2,3,4,5,6,7,8]

    print("Start state")
    print("For example, 7,2,4,5,0,6,8,3,1 represents")
    AStar.display_board(example_start)
    start = input("Enter your start state here: ")
    print()

    print("Goal state")
    print("For example, 0,1,2,3,4,5,6,7,8 represents")
    AStar.display_board(example_goal)
    goal = input("Enter your goal state here: ")
    print()

    start = list(map(int, start.split(",")))
    goal = list(map(int, goal.split(",")))

    a_star = AStar(start, goal)
    solution = a_star.solve()
    print(solution)