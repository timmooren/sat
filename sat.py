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

    def dpll(self, literal=None) -> bool:
        """Returns True if the CNF is satisfiable, False otherwise

        Args:
            cnf (list): Clauses in CNF

        Returns:
            bool: True if satisfiable, False otherwise
        """
        # store literals to check for pure literal later
        literals_positive = set()
        literals_negative = set()

        if literal:
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

        for clause in self.cnf.copy():
            # if it contains an empty clause
            if clause == []:
                return False

            # if it contains a unit clause, add it to assignments and restart
            if len(clause) == 1:
                self.assignments.extend(clause)
                self.dpll(literal=clause[0])

            # # if it contains tautology (p v ~p), remove it and restart
            # if len(clause) == 2:
            #     literal1, literal2 = clause
            #     if literal1 == -literal2:
            #         self.cnf.remove(clause)
            #         self.dpll()

            # add all literals to set
            for literal in clause:
                literals_positive.add(
                    literal) if literal > 0 else literals_negative.add(abs(literal))

        # if it contains a pure literal, add it to assignments, remove it and restart
        set_difference = literals_negative - literals_positive
        if set_difference:
            pure_literal = set_difference.pop()
            self.dpll(literal=pure_literal)

        # pick a literal and restart
        print(self.cnf)
        literal = self.cnf[0][0]

        return True if self.dpll(literal) else self.dpll(-literal)


    # TODO
    def dpll2(self) -> bool:
        pass


if __name__ == '__main__':
    solver = SAT(cnf=[[1, 2], [-1, 2], [-2, 3], [-3, 1]])
    satisfaction = solver.dpll()
    print(satisfaction)
    # print(solver.assignments)
