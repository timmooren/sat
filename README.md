# SAT solver

This SAT solver is based on the Davis–Putnam–Logemann–Loveland algorithm, and includes 2 heuristics. On a split, literals can be picked based on:
- First literal in CNF
- Jeroslow-Wang heuristic
- Maximum Occurrences in clauses of Minimum Length heuristic



## Reproducability
To make reproducing our results simple, the repository contains a file called solve.py. If you run this file, it will solve the specified Sudoku's using a specified heuristic. Note that larger Sudoku's can take a very long time to solve!
