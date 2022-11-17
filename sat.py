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

    def jeroslow_wang(self, two_sided=False) -> int:
        """selects the literal with the highest Jeroslow Wang value

        Args:
            two_sided (bool, optional): two_sided JW. Defaults to False.

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
                if two_sided and -literal in clause:
                    cost += 2 ** -len(clause)

            if cost > best_jw:
                best_jw = cost
                best_literal = literal
        return best_literal

    def MOM(self, k:float) -> int:
        """Maximum Occurrences in Clauses of Minimum Size

        Args:
            k (float): tuning parameter

        Returns:
            int: best literal
        """
        best_literal = None
        best_score = 0
        min_clause_size = min(self.cnf, key=len)
        all_min_clauses = [clause for clause in self.cnf if len(clause) == min_clause_size]
        flat_list = [item for sublist in all_min_clauses for item in sublist]
        literal2occurence = Counter(flat_list)

        for literal in self.get_literals():
            score = literal2occurence[literal] + literal2occurence[-literal] * 2 ** k + literal2occurence[literal] * literal2occurence[-literal]
            if score > best_score:
                best_score = score
                best_literal = literal
        return best_literal


class DPLL(SAT):
    def dpll(self, literals: set = set()) -> bool:
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
                self.assignments.extend(clause)
                self.step2assignments[self.step] = self.assignments.copy()
                return self.dpll(literals=[clause[0]])

        # pick a literal and restart
        literal = self.first_literal()

        if self.dpll([literal]):
            self.assignments.append(literal)
            return True
        # backtrack if neccessary
        else:
            self.assignments.remove(literal)
            return self.dpll(-literal)


class CDCL(SAT):
    def __init__(self, cnf, assignments=set()) -> None:
        super().__init__(cnf, assignments)
        self.graph = nx.DiGraph(name="causal graph").add_node(0, label="root")
        self.last_node = 0

    def cdcl(self, literals: list = []) -> bool:
        """Conflict-driven clause learning

        Returns:
            bool: True if satisfiable, false otherwise
        """
        self.clean_cnf(literals)

        # if it contains no clauses
        if not self.cnf:
            return True
        # if it contains an empty clause
        if set() in self.cnf:
            return False

        # check for unit clause, add it to assignments and restart
        for clause in self.cnf:
            if len(clause) == 1:
                # add clause to causal graph
                self.graph.add_node(clause[0], label=clause[0])

                for clause in self.KNOWLEDGE:
                    difference = clause - self.assignments
                    if len(difference) == clause:
                        self.graph.add_edge(difference, clause[0])

                self.graph.add_edge(self.last_node, clause[0])
                self.last_node = clause[0]

                self.assignments.extend(clause)
                self.step2assignments[self.step] = self.assignments.copy()

                return self.cdcl(literals=[clause[0]])

        # pick a literal and restart
        literal = self.cnf[0][0]
        if self.cdcl([literal]):
            self.graph.add_node(literal, label=literal)
            self.assignments.append(literal)
            return True
        # backtrack if neccessary
        else:
            # add conflicts to knowledge base
            conflicts = set(self.graph.predecessors(literal)) + \
                set(self.graph.predecessors(-literal))
            self.cnf.add(conflicts)
            # remove wrong assumptions
            self.graph.remove_node(literal)
            self.assignments.remove(literal)

            self.dpll(-literal)


if __name__ == '__main__':
    solver = SAT(cnf=[[1, 2], [-1, 2], [-2, 3], [-3, 1]])
    satisfaction = solver.dpll()
    print(satisfaction)
    print(solver.assignments)
