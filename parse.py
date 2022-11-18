def read_dimacs(filename: str):
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
    return clauses, n_vars, n_clauses


clauses, n_vars, n_clauses = read_dimacs(filename='DIMACS_4x4/sudoku_4x4_nr_1.cnf')
print(clauses)
