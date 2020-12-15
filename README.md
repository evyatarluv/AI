# Artificial Intelligence Projects

## 8-Puzzle Solver

Using A* and Branch & Bound to solve 8-puzzle.
The implementation to the B&B algorithm consist on Best-First
in order to improve run time.

### Project Structure

1. Node - Class for representing a node in the search tree.

1. EightPuzzle - Class for representing an 8-puzzle game. 
The class including the `solve()` method.

1. heuristic - Script which contains all the heuristics as functions
Each function in `heuristics.py` script most get the current state and the
goal state as numpy arrays, and return the heuristic value.

1. main - Script with an example of using the solver. Additionally, 
a comparison between the algorithms and heuristics and couple of 
plots for the comparison.