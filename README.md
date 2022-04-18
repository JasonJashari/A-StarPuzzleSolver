# a-star-puzzle-solver
A* search algorithm to solve an 8-puzzle problem

The 8-puzzle consists of a 3x3 board. Eight tiles in the board are numbered from 1 to 8, and one tile is blank. Any tile adjacent to the blank space can slide into that space. The goal of the game is to reach a given goal configuration from the given initial state. A typical instance of the 8-puzzle is shown below. The solution to this problem is 26 steps long.

![alt text](https://github.com/JasonJashari/a-star-puzzle-solver/blob/main/eight%20puzzle%20example.png?raw=true)

Here, I will phrase the 8-puzzle problem as a heuristic search and implement the A* algorithm to solve it.

# How can the 8-puzzle problem be seen as a search problem?
The problem can be represented as a graph with the states of the 8-puzzle. Solving the puzzle corresponds to searching the graph. The standard formulation which I use is as follows:
- States: A state description specifies the location of each of the eight tiles and the blank in one of the nine squares.
- Initial state: Any state can be designated as the initial state.
- Actions: Movements of the blank space left, right, up or down. Different subsets of these are possible depending on where the blank is.
- Transition model: Takes a state and an aciton, returns the resulting state.
- Goal test: Checks whether the state matches the goal configuration.
- Path cost: : Each step costs 1, so the path cost is the number of steps in the path. 

# Searching for a solution
A solution is an action sequence and the search algorithm will work by considering various possible action sequences. The possible action sequences starting at the initial state form a **search tree** with the initial state at the root. The branches are actions and the **nodes** correspond to states. If the node we are at is not the goal state, we consider taking various actions by **expanding** the current state, i.e., applying each legal action to the current state **generating** a new set of states. These new set of states become the **child nodes** to the **parent node** they came from. Now we must choose which of the new possiblities to to consider further. The essence of the search is following up one option now and putting the others aside for later, in case the first choice does not lead to a solution. Each of the nodes we can explore next is a **leaf node** and the set of all leaf nodes available for expansion at any given point is called the **frontier**. The process of expanding nodes on the frontier continues until either a solution is found or there are no more states to expand.
