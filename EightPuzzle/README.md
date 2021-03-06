## 8-Puzzle Solver

Implementation of A* and Branch & Bound algorithms to solve 8-puzzle.
The implementation of the B&B algorithm can also get an search type. Currently, 
we implemented Depth-First search and Breadth-First search.

### Project Structure

1. `Node.py` - Class for representing a node in the search tree.

1. `EightPuzzle.py` - Class for representing an 8-puzzle game. 
The class including the `solve()` method.

1. `heuristics.py` - Script which contains all the heuristics as functions
Each function in `heuristics.py` script most get the current state and the
goal state as numpy arrays, and return the heuristic value. Currently, the script
contains the following heuristics:
    1. Number of misplaced tiles
    1. Euclidean distance
    1. Manhattan distance

1. `main.py` - Script with an example of using the solver. Additionally, 
a comparison between the algorithms and heuristics and couple of 
plots for the comparison.
The `solve_puzzle` function in the main is an interactive solver which get from the user
his preferred algorithm, search approach and heuristic function and solve a random puzzle.
 