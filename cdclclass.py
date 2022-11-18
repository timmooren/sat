
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

                self.assignments.add(clause)
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

