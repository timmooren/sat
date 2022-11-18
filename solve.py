from dpll import DPLL
import pathlib
import time


def main():
    path = pathlib.Path('DIMACS_9x9')
    # read all 4x4 files in directory
    files = path.glob('*.cnf')
    repeats = 10
    times = []
    for file in files:
        solver = DPLL()
        solver.read_dimacs(file)
        for _ in range(repeats):
            start = time.perf_counter()
            satisfaction = solver.solve()
            end = time.perf_counter()
            times.append(end - start)
        assert satisfaction
    print(f'Average time: {sum(times) / len(times)}')




if __name__ == '__main__':
    main()