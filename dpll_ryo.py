from sat import SAT
from copy import deepcopy
import random

class DPLL(SAT):
    def __init__(self, cnf: list = ..., assignments=...) -> None:
        super().__init__(cnf, assignments)
        self.assignments = []

    def solve(self, partial_assignment=None) -> bool:
        """Returns True if the CNF is satisfiable, False otherwise
        Args:
            cnf (list): partial assi
        Returns:
            bool: True if satisfiable, False otherwise
        """
        # at each step print the CNF
        # print(self.cnf)

        cnf_copy = deepcopy(self.cnf)
        # cnf_copy = self.cnf.copy()

        # --- reducing CNF ---
        for clause in cnf_copy:
            # ignore 
            if partial_assignment == None: break
            # 1- removing clauses in which the literal is True
            if partial_assignment in clause:
                # self.assignments.append(clause)
                self.cnf.remove(clause)
            # 2- remove -literal from clause 
            if -partial_assignment in clause:
                clause.remove(-partial_assignment)


        # --- checking satisfiability --- 
        # if all clauses are true under current partial assignment ie. empty CNF, return sat
        if not self.cnf:
            return True
        # if a conflict clause is encountered ie. empty clause, return unsat
        if [] in self.cnf:
            return False
            
        # --- unit propagation --- 
        for clause in self.cnf:
            # if we have a unit clause, call DPLL with partial assignment = unit literal  
            if len(clause) == 1:
                return self.solve(partial_assignment=clause[0])

        # --- making partial assignemnts --- 
        # make True partial assignment on random literal 
        random_literal = random.choice(random.choice(self.cnf))
        # if partial assignment was a correct return sat
        if self.solve(partial_assignment=random_literal) == True:
            return True 
        # elif conflict clause is encountered, backtrack chronologically with -literal
        else: 
            return self.solve(partial_assignment=-random_literal)







if __name__ == '__main__':
    # cnf=[[-1,-2],[-1,3],[-3,-4],[2,4,5],[-5,6,-7],[2,7,8],[-8,-9],[-8,10],[9,10,11],[-10,-12],[-11,12]]
    solver = DPLL(cnf=[[1, 2], [-1, 2], [-2, 3], [-3, 1]])
    # satisfaction = solver.solve()
    # print(satisfaction)
    # print(solver.assignments)

    # test_file = f'DIMACS_9x9/sudoku_9x9_nr_1.cnf'
    # print(test_file)
    # solver = DPLL()
    # solver.read_dimacs(test_file)
    # print(solver.cnf)
    # satisfaction = solver.solve()
    # print(satisfaction)

    for i in range(1,50):
        test_file = f'DIMACS_9x9/sudoku_9x9_nr_{i}.cnf'
        print(test_file)
        solver = DPLL()
        solver.read_dimacs(test_file)
        satisfaction = solver.solve()
        print(satisfaction)
    
