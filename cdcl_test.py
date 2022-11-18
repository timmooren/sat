# %%
from copy import deepcopy



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

    # numbers each cnf so it can be used for updating trails -> returns list 
    def number_cnf_list(self, cnf):
        numbered_cnf = []
        for i, clause in enumerate(cnf):
            temp = [clause, f'c{i+1}']
            numbered_cnf.append(temp)
        return numbered_cnf

    # numbers each cnf so it can be used for updating trails -> returs dict 
    def number_cnf_dict(self, cnf):
        numbered_cnf = {}
        for i, clause in enumerate(cnf):
            numbered_cnf[f'c{i+1}'] = clause
        return numbered_cnf

    def clean_cnf(self, literals):
        for literal in literals:
            for clause in self.cnf.copy():
                # remove clauses containing literal
                if literal in clause:
                    #HERE: UPDATE TRAILS l^clause
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

    def jeroslow_wang(self, two_sided=False, k=2) -> int:
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
                    cost += k ** -len(clause)
                elif -literal in clause:
                    cost += k ** -len(clause)

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

        # remove clauses in cnf
        self.clean_cnf(literals)

        # if it contains no clauses
        if not self.cnf:
            return True
        # if it contains an empty clause HERE: PERFORM CUT 
        if set() in self.cnf:
            return False

        for clause in self.cnf:
            # if it contains a unit clause, add it to assignments and restart
            if len(clause) == 1:
                # HERE: UPDATE TRAILS??  NOO
                self.assignments.add(clause[0]) # changed -> add for sets 
                self.step2assignments[self.step] = self.assignments.copy()
                return self.dpll(literals=[clause[0]])

        # pick a literal and restart
        literal = self.first_literal()
        # HERE: UPDATE TRAILS?? l^dec

        if self.dpll([literal]):
            self.assignments.add(literal) # changed -> add for sets 
            return True
        # backtrack if neccessary
        else:
            self.assignments.remove(literal)
            self.dpll(-literal)


class CDCL(SAT):

    def __init__(self, cnf: list, assignments=set()) -> None:
        super().__init__(cnf, assignments)
        # original copy of cnf used for updating trails - immutable 
        self.original_cnf = self.number_cnf_dict(deepcopy(self.cnf))
        # new cnf datasructure to tag clause for CDCL - mutable 
        self.cnf = self.number_cnf_list(self.cnf)
        # proxy datastructure for implication graph - muatable
        self.trails = []

    def first_literal_cdcl(self) -> int:
        return self.cnf[0][0][0]

    def clean_cnf_cdcl(self, literals):
        print(f'literals = {literals}')
        for literal in literals:
            for clause in self.cnf.copy():
                # remove clauses containing literal 
                # clause[0] contains literal, clause[1] contains clause tag (eg. 'c1')
                if literal in clause[0]:
                    # updates trails with {unit literal : original clause tag}
                    trail_literal = {literal : self.original_cnf[clause[1]]}
                    self.trails.append(trail_literal)
                    # removes clause containing literal
                    self.cnf.remove(clause)
                # shorten clauses containing ~literal
                if -literal in clause[0]: 
                    clause[0].remove(-literal)
        print(self.cnf)
        

    def cdcl(self, literals=set()) -> bool:
        # print(self.cnf)
        print(self.trails)
        self.step += 1

        # remove clauses in cnf & updates trails 
        self.clean_cnf_cdcl(literals) 

        # if it contains no clauses
        if not self.cnf:
            return True
        # if it contains an empty clause HERE: PERFORM CUT & also change check for empty set 
        if set() in self.cnf:
            return False

        for clause in self.cnf:
            # if it contains a unit clause, add it to assignments and restart
            if len(clause[0]) == 1:
                trail_literal = {literal : self.original_cnf[clause[1]]}
                self.trails.append(trail_literal)

                self.assignments.add(clause[0][0]) # changed -> add for sets 
                self.step2assignments[self.step] = self.assignments.copy()
                return self.cdcl(literals=[clause[0][0]])

        # pick a literal and restart
        literal = self.first_literal_cdcl()
        # print(literal)
        # updates trails with {decision literal : decision tag}
        self.trails.append({literal:'dec'})

        if self.cdcl([literal]):
            self.assignments.add(literal) # changed -> add for sets 
            return True
        # backtrack if neccessary HERE: MODIFICATION NEEDED (non-chronological backtracking)
        else:
            self.assignments.remove(literal)
            self.cdcl(-literal)



# if __name__ == '__main__':
#     solver = DPLL(cnf=[[1, 2], [-1, 2], [-2, 3], [-3, 1]])
#     print(solver.dpll())
#     print(solver.assignments)

if __name__ == '__main__':
    # use CNF from the lecture to test 
    solver = CDCL(cnf=[[-1,-2],[-1,3],[-3,-4],[2,4,5],[-5,6,-7],[2,7,8],[-8,-9],[-8,10],[9,10,11],[-10,-12],[-11,12]])
    solver.cdcl()
    # print(solver.assignments)

# if __name__ == '__main__':
#     solver = SAT(cnf=[[1, 2], [-1, 2], [-2, 3], [-3, 1]])
#     satisfaction = solver.dpll()
#     print(satisfaction)
#     print(solver.assignments)