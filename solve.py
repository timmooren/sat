from dpll import DPLL
import pathlib
import time
import csv


def main():
    repeats = 10
    data = [
        ['path', 'size' 'time', 'steps', 'assignments']
    ]
    sizes = ['4x4']

    for size in sizes:
        path = pathlib.Path(f'DIMACS_{size}')
        print(path)
        files = path.glob('*.cnf')

        for file in files:
            print(file)
            solver = DPLL()
            solver.read_dimacs(file)

            for _ in range(repeats):
                start = time.perf_counter()
                satisfaction = solver.solve()
                end = time.perf_counter()
                seconds = end - start
                data.append([file, size, seconds, solver.step, solver.assignments])
                assert satisfaction


    with open('data.csv', 'w') as f:
        writer = csv.writer(f)
        writer.writerows(data)


if __name__ == '__main__':
    main()
