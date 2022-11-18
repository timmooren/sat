# %%
import networkx as nx
from collections import Counter


class SAT():
    def __init__(self, cnf: list=[], assignments=[]) -> None:
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

    def read_dimacs(self, filename: str):
        """Read DIMACS file

        Args:
            filename (str): path to file

        Returns:
            tuple: clauses, number of variables, number of clauses
        """
        with open(filename) as f:
            lines = f.readlines()

        clauses = []
        for line in lines:
            # if comment, skip line
            if line[0] == 'c':
                continue
            # if the line starts with p, it is the header
            elif line[0] == 'p':
                n_vars = int(line.split()[2])
                n_clauses = int(line.split()[3])
            # otherwise, extract clauses
            else:
                # ignore the last number
                clause = [int(literal) for literal in line.split()[:-1]]
                clauses.append(clause)
        self.cnf = clauses

    def clean_cnf(self, literals:list):
        # copy cnf and remove all clauses containing the
        cnf = self.cnf.copy()
        self.cnf.clear()

        for literal in literals:
            for clause in cnf:
                # skip clauses containing literal
                if literal in clause:
                    continue
                # shorten clauses containing ~literal
                elif -literal in clause:
                    clause.remove(-literal)
                # add clause to cnf
                self.cnf.append(clause)

    def first_literal(self) -> int:
        """selects the first literal in the first clause

        Returns:
            int: first literal
        """
        return self.cnf[0][0]

    def get_literals(self):
        return [set([literal for clause in self.cnf for literal in clause])]

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

