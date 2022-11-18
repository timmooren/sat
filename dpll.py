from sat import SAT

class DPLL(SAT):
    def solve(self, literals:list=[]) -> bool:
        """Returns True if the CNF is satisfiable, False otherwise

        Args:
            cnf (list): Clauses in CNF

        Returns:
            bool: True if satisfiable, False otherwise
        """
        self.step += 1

        # remove clauses in cnf
        self.clean_cnf(literals)

        # if it contains no clauses
        if not self.cnf:
            return True
        # if it contains an empty clause
        if [] in self.cnf:
            return False

        for clause in self.cnf:
            # if it contains a unit clause, add it to assignments and restart
            if len(clause) == 1:
                self.assignments.extend(clause)
                self.step2assignments[self.step] = self.assignments.copy()
                return self.solve(literals=clause)
        # pick a literal and restart
        literal = self.first_literal()

        if self.solve([literal]):
            self.assignments.append(literal)
            return True
        # backtrack if neccessary
        else:
            self.assignments.remove(literal)
            return self.solve(-literal)


if __name__ == '__main__':
    solver = SAT(cnf=[[1, 2], [-1, 2], [-2, 3], [-3, 1]])
    satisfaction = solver.dpll()
    print(satisfaction)
    print(solver.assignments)
