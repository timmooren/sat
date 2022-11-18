from parse import read_dimacs
from sat import SAT
import pathlib


def main():
    path = pathlib.Path('DIMACS_4x4')
    # read all 4x4 files in directory
    files = path.glob('*.cnf')
    for file in files:
        clauses, n_vars, n_clauses = read_dimacs(file)
        sat = SAT(clauses)

        print(file,  len(clauses), n_clauses)
        print(clauses)

if __name__ == '__main__':
    main()