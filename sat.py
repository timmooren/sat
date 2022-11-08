class SAT():
    def __init__(self, cnf, assignments=[]) -> None:
        self.cnf = cnf
        self.assignments = assignments

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

    def dpll(self) -> bool:
        """Returns True if the CNF is satisfiable, False otherwise

        Args:
            cnf (list): Clauses in CNF

        Returns:
            bool: True if satisfiable, False otherwise
        """
        # store literals to check for pure literal later
        literals_positive = set()
        literals_negative = set()

        # if it contains an empty set of clauses
        if len(self.cnf) == 0:
            return True

        for clause in self.cnf:
            # if it contains an empty clause
            if len(clause) == 0:
                return False

            # if it contains tautology (p v ~p), remove it and restart
            if len(clause) == 2:
                literal1, literal2 = clause
                if literal1 == -literal2:
                    self.cnf.remove(clause)
                    self.dpll()
            # if it contains a unit clause, add it to assignments and restart
            if len(clause) == 1:
                self.assignments.extend(clause)
                self.cnf.remove(clause)
                self.dpll()

            # add all literals to set
            for literal in clause:
                literals_positive.add(
                    literal) if literal > 0 else literals_negative.add(abs(literal))

        # if it contains a pure literal, add it to assignments, remove it and restart
        set_difference = literals_negative - literals_positive
        if set_difference:
            pure_literal = set_difference.pop()
            self.assignments.extend(pure_literal)
            self.cnf.remove(pure_literal)
            self.dpll()

        # check whether dpll is satisfiable
        return self.dpll()

    # TODO
    def dpll2(self) -> bool:
        pass


if __name__ == '__main__':
    solver = SAT(cnf=[[1, 2], [-1, 2], [-2, 3], [-3, 1]])
    satisfaction = solver.dpll()
    print(satisfaction)
    print(solver.assignments)
