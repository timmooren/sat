from sat import SAT
from copy import deepcopy
import numpy as np
import json

class DPLL(SAT):
    def solve(self, literal=None) -> bool:
        """Returns True if the CNF is satisfiable, False otherwise

        Args:
            cnf (list): Clauses in CNF

        Returns:
            bool: True if satisfiable, False otherwise
        """
        self.step += 1

        # clean cnf
        if literal:
            self.assignments.append(literal)
            self.clean_cnf(literal)

        # if it contains no clauses
        if not self.cnf:
            return True
        # if it contains an empty clause
        if [] in self.cnf:
            return False

        # if it contains a unit clause, add it to assignments and restart
        for clause in self.cnf:
            if len(clause) == 1:
                # self.assignments.extend(clause)
                self.step2assignments[self.step] = self.assignments.copy()
                return self.solve(literal=clause[0])

        self.splits += 1
        # pick a literal
        if self.heuristic == 'first':
            literal = self.first_literal()
        elif self.heuristic == 'jw':
            literal = self.jeroslow_wang()
        elif self.heuristic == 'mom':
            literal = self.MOM(k=2)

        old_cnf = deepcopy(self.cnf)
        old_assignments = deepcopy(self.assignments)

        if self.solve(-literal):
            # self.assignments.append(-literal)
            return True
        # backtrack if neccessary
        else:
            self.backtracks += 1
            self.cnf = old_cnf
            self.assignments = old_assignments
            return self.solve(literal)


if __name__ == '__main__':

    solver = DPLL()
    # DIMACS_9x9/sudoku_9x9_nr_288.cnf
    solver.read_dimacs('DIMACS_9x9/sudoku_9x9_nr_278.cnf')
    satisfaction = solver.solve()
    print(satisfaction)
    assignments = solver.assignments
    print(f'length assignments: {len(set(assignments))}')
    # only ositive assignments
    assignments = sorted([assignment for assignment in assignments if assignment > 0])

    def assignments2sudoku(assignments):
        sudoku_shape = len(assignments) // 9
        for assingment in assignments:
            assignment = str(assingment)

        return sudoku
    print(sorted(set(assignments)))
    print(len(set(assignments)))

    d = solver.step2assignments
    # sort the lists inside the dict
    for key in d:
        d[key] = sorted(d[key])


    with open("steps.json", "w") as write_file:
        json.dump(d, write_file, indent=4)