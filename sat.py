import networkx as nx
from collections import defaultdict
# %%

class SAT():
    def __init__(self, cnf: set(), assignments=set()) -> None:
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

    def jeroslow_wang(self, two_sided=False) -> int:
        """selects the literal with the highest Jeroslow Wang value

        Args:
            two_sided (bool, optional): two_sided JW. Defaults to False.

        Returns:
            int: best literal
        """
        best_literal = None
        best_jw = 0
        literals = set([literal for clause in self.cnf for literal in clause])

        # compute jw for every literal
        for literal in literals:
            if two_sided:
                literal = abs(literal)
            cost = 0

            for clause in self.cnf:
                if literal in clause:
                    cost += 2 ** -len(clause)
                elif -literal in clause:
                    cost += 2 ** -len(clause)

            if cost > best_jw:
                best_jw = cost
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
        # # store literals to check for pure literal later
        # literals_positive = set()
        # literals_negative = set()
        self.clean_cnf(literals)

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

            # # add all literals to set
            # for literal in clause:
            #     literals_positive.add(
            #         literal) if literal > 0 else literals_negative.add(abs(literal))

        # # if it contains a pure literal, add it to assignments, remove it and restart
        # pure_literals = literals_negative ^ literals_positive
        # if pure_literals:
        #     pure_literal = pure_literals.pop()
        #     self.assignments.append(pure_literal)
        #     return self.dpll(literals=[pure_literal])

        # pick a literal and restart
        literal = self.cnf[0][0]

        if self.dpll([literal]):
            self.assignments.append(literal)
            return True
        # backtrack if neccessary
        else:
            self.assignments.remove(literal)
            self.dpll(-literal)


class CDCL(SAT):
    def __init__(self, cnf, assignments=[]) -> None:
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
        if any(clause == set() for clause in self.cnf):
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
