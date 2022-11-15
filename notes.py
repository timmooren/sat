        # # store literals to check for pure literal later
        # literals_positive = set()
        # literals_negative = set()


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