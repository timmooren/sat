# read dimacs file
def read_dimacs(filename):
    with open(filename) as f:
        lines = f.readlines()

    clauses = []
    for line in lines:
        if line[0] == 'c':
            continue
        elif line[0] == 'p':
            n_vars = int(line.split()[2])
        else:
            clause = [int(literal) for literal in line.split()[:-1]]
            clauses.append(clause)

    return clauses, n_vars


clauses, vars =read_dimacs(filename='sudoku1.cnf')
print(clauses, vars)
