import random
from futoshiki import load_instance, load_known_solution, cost

SIZES = [4, 5, 6, 7, 8, 9]
PER_SIZE = 3
GIVEN_RATIO = 0.10
INEQ_RATIO = 0.40


def random_latin_square(n, rng):
    base = [[(r + c) % n + 1 for c in range(n)] for r in range(n)]
    rows, cols = list(range(n)), list(range(n))
    rng.shuffle(rows)
    rng.shuffle(cols)
    symbols = list(range(1, n + 1))
    rng.shuffle(symbols)
    return [[symbols[base[r][c] - 1] for c in cols] for r in rows]


def make_instance(n, rng):
    sol = random_latin_square(n, rng)
    cells = [(r, c) for r in range(n) for c in range(n)]
    givens = [[0] * n for _ in range(n)]
    for r, c in rng.sample(cells, max(1, round(GIVEN_RATIO * n * n))):
        givens[r][c] = sol[r][c]
    pairs = [((r, c), (r, c + 1)) for r in range(n) for c in range(n - 1)] + \
            [((r, c), (r + 1, c)) for r in range(n - 1) for c in range(n)]
    ineqs = []
    for a, b in rng.sample(pairs, round(INEQ_RATIO * len(pairs))):
        if sol[a[0]][a[1]] < sol[b[0]][b[1]]:
            ineqs.append((a, b))
        else:
            ineqs.append((b, a))
    return sol, givens, ineqs


def write_files(name, n, sol, givens, ineqs):
    with open(f"instances/{name}.txt", "w") as f:
        f.write(f"# size\n{n}\n# grid (0 = empty)\n")
        for row in givens:
            f.write(" ".join(map(str, row)) + "\n")
        f.write("# inequalities: r1 c1 r2 c2  means cell(r1,c1) < cell(r2,c2)\n")
        for (r1, c1), (r2, c2) in ineqs:
            f.write(f"{r1} {c1} {r2} {c2}\n")
    with open(f"instances/{name}.sol", "w") as f:
        for row in sol:
            f.write(" ".join(map(str, row)) + "\n")


if __name__ == "__main__":
    rng = random.Random(2026)
    for n in SIZES:
        for k in range(1, PER_SIZE + 1):
            name = f"{n}x{n}_{k}"
            sol, givens, ineqs = make_instance(n, rng)
            write_files(name, n, sol, givens, ineqs)
            p = load_instance(f"instances/{name}.txt")
            known = load_known_solution(f"instances/{name}.sol", p)
            print(f"{name}: givens={sum(v != 0 for row in givens for v in row)}, "
                  f"inequalities={len(ineqs)}, known solution cost={cost(known)}")