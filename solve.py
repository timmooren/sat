from dpll import DPLL
import pathlib
import time
import csv


def main():
    # tweak these!
    repeats = 1
    sizes = ['9x9']
    heuristic = 'first'
    heuristics = ['first', 'jw', 'mom']

    for size in sizes:
        data = [
            ['path', 'size', 'time', 'steps', 'splits', 'backtracks']
        ]
        path = pathlib.Path(f'DIMACS_{size}')
        print(path)
        files = path.glob('*.cnf')

        for i, file in enumerate(files):
            if i == 500: 
                break

            print(file)
            solver = DPLL()

            solver.heuristic = heuristic
            solver.read_dimacs(file)

            for _ in range(repeats):
                start = time.perf_counter()
                satisfaction = solver.solve()
                end = time.perf_counter()
                seconds = end - start
                # solver.write_dimacs(f'solutions/{file}_{heuristic}.out')
                data.append([
                    file, size, seconds, solver.step, solver.splits, solver.backtracks])
                assert satisfaction


        with open(f'data/data{size}{heuristic}.csv', 'w') as f:
            writer = csv.writer(f)
            writer.writerows(data)


if __name__ == '__main__':
    main()
