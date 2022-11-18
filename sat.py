# %%
import networkx as nx
from collections import Counter


class SAT():
    def __init__(self, cnf: list, assignments=set()) -> None:
        self.cnf = cnf
        self.KNOWLEDGE = cnf
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

    def clean_cnf(self, literals):
        for literal in literals:
            for clause in self.cnf.copy():
                # remove clauses containing literal
                if literal in clause:
                    self.cnf.remove(clause)

                # shorten clauses containing ~literal
                if -literal in clause:
                    clause.remove(-literal)

    def first_literal(self) -> int:
        """selects the first literal in the first clause

        Returns:
            int: first literal
        """
        return self.cnf[0][0]

    def get_literals(self):
        return set([literal for clause in self.cnf for literal in clause])

    def jeroslow_wang(self) -> int:
        """selects the literal with the highest Jeroslow Wang value

        Returns:
            int: best literal
        """
        best_literal = None
        best_jw = 0
        literals = self.get_literals()

        # compute jw for every literal
        for literal in literals:
            cost = 0

            for clause in self.cnf:
                if literal in clause:
                    cost += 2 ** -len(clause)

            if cost > best_jw:
                best_jw = cost
                best_literal = literal
        return best_literal


    def MOM(self, k: float) -> int:
        """Maximum Occurrences in Clauses of Minimum Size

        Args:
            k (float): tuning parameter

        Returns:
            int: best literal
        """
        best_literal = None
        best_score = 0
        min_clause_len = min(self.cnf, key=len)
        all_min_clauses = [clause for clause in self.cnf if len(
            clause) == min_clause_len]
        flat_list = [item for sublist in all_min_clauses for item in sublist]
        literal2occurence = Counter(flat_list)

        for literal in self.get_literals():
            f_x = literal2occurence[literal]
            f_neg_x = literal2occurence[-literal]
            score = f_x + f_neg_x * 2 ** k + f_x * f_neg_x

            if score > best_score:
                best_score = score
                best_literal = literal
        return best_literal


class DPLL(SAT):
    def solve(self, literals: set = set()) -> bool:
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
        if set() in self.cnf:
            return False

        for clause in self.cnf:
            # if it contains a unit clause, add it to assignments and restart
            if len(clause) == 1:
                self.assignments.update(clause)
                self.step2assignments[self.step] = self.assignments.copy()
                return self.solve(literals=[clause[0]])
        print(self.cnf[0])
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
