# Artificial Intelligence Projects

## 8-Puzzle Solver

Implementation of A* and Branch & Bound to solve 8-puzzle.
The implementation of the B&B algorithm consist on Best-First
in order to improve run time.

### Project Structure

1. `Node.py` - Class for representing a node in the search tree.

1. `EightPuzzle.py` - Class for representing an 8-puzzle game. 
The class including the `solve()` method.

1. `heuristics.py` - Script which contains all the heuristics as functions
Each function in `heuristics.py` script most get the current state and the
goal state as numpy arrays, and return the heuristic value.

1. `main.py` - Script with an example of using the solver. Additionally, 
a comparison between the algorithms and heuristics and couple of 
plots for the comparison.