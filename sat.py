# %%
class SAT():
    def __init__(self, cnf, assignments=[]) -> None:
        self.cnf = cnf
        self.assignments = assignments
        self.step = 0
        self.step2assignments = {}

    @property
    def cnf(self):
        return self._cnf

    @cnf.setter
    def cnf(self, value):
        self._cnf = value

    @property
    def assignments(self):
        return self._assignments

    @assignments.setter
    def assignments(self, value):
        self._assignments = value

    def dpll(self, literals:list=[]) -> bool:
        """Returns True if the CNF is satisfiable, False otherwise

        Args:
            cnf (list): Clauses in CNF

        Returns:
            bool: True if satisfiable, False otherwise
        """
        self.step += 1
        # store literals to check for pure literal later
        literals_positive = set()
        literals_negative = set()

        for literal in literals:
            for clause in self.cnf.copy():
                # remove clauses containing literal
                if literal in clause:
                    self.cnf.remove(clause)

                # shorten clauses containing ~literal
                if -literal in clause:
                    clause.remove(-literal)

        # if it contains no clauses
        if self.cnf == []:
            return True
        # if it contains an empty clause
        if any(clause == [] for clause in self.cnf):
            return False

        for clause in self.cnf:
            # if it contains a unit clause, add it to assignments and restart
            if len(clause) == 1:
                self.assignments.extend(clause)
                self.step2assignments[self.step] = self.assignments.copy()
                return self.dpll(literals=[clause[0]])

            # add all literals to set
            for literal in clause:
                literals_positive.add(
                    literal) if literal > 0 else literals_negative.add(abs(literal))

        # if it contains a pure literal, add it to assignments, remove it and restart
        pure_literals = literals_negative ^ literals_positive
        if pure_literals:
            pure_literal = pure_literals.pop()
            self.assignments.append(pure_literal)
            return self.dpll(literals=[pure_literal])

        # pick a literal and restart
        print(f' after = {self.cnf}')
        print()
        literal = self.cnf[0][0]

        if self.dpll([literal]):
            self.assignments.append(literal)
            return True
        # backtrack if neccessary
        else:
            self.assignments.remove(literal)
            self.dpll(-literal)

if __name__ == '__main__':
    solver = SAT(cnf=[[1, 2], [-1, 2], [-2, 3], [-3, 1]])
    satisfaction = solver.dpll()
    print(satisfaction)
    print(solver.assignments)

# %%
