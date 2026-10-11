import random

class Futoshiki:
    def __init__(self, n, givens, ineqs):
        self.n = n
        self.givens = givens
        self.ineqs = ineqs
        self.fixed = [[givens[r][c] != 0 for c in range(n)] for r in range(n)]
        self.free_cells = [[c for c in range(n) if not self.fixed[r][c]] for r in range(n)]
        self.ineqs_of = {(r, c): [] for r in range(n) for c in range(n)}
        for i, (a, b) in enumerate(ineqs):
            self.ineqs_of[a].append(i)
            self.ineqs_of[b].append(i)
        self.movable_rows = [r for r in range(n) if len(self.free_cells[r]) >= 2]


class Solution:
    def __init__(self, puzzle, grid):
        self.puzzle = puzzle
        self.grid = grid

    def copy(self):
        return Solution(self.puzzle, [row[:] for row in self.grid])

    def __str__(self):
        return "\n".join(" ".join(str(v) for v in row) for row in self.grid)


def load_instance(path):
    with open(path) as f:
        lines = [l.split("#")[0].strip() for l in f]
    lines = [l for l in lines if l]
    n = int(lines[0])
    givens = [list(map(int, lines[1 + r].split())) for r in range(n)]
    ineqs = []
    for l in lines[1 + n:]:
        r1, c1, r2, c2 = map(int, l.split())
        ineqs.append(((r1, c1), (r2, c2)))
    return Futoshiki(n, givens, ineqs)

def initial_solution(puzzle, rng=random):
    n = puzzle.n
    grid = [row[:] for row in puzzle.givens]
    for r in range(n):
        missing = [v for v in range(1, n + 1) if v not in puzzle.givens[r]]
        rng.shuffle(missing)
        for c, v in zip(puzzle.free_cells[r], missing):
            grid[r][c] = v
    return Solution(puzzle, grid)

def column_conflicts(sol):
    n = sol.puzzle.n
    return sum(n - len({sol.grid[r][c] for r in range(n)}) for c in range(n))


def inequality_violations(sol):
    g = sol.grid
    total = 0
    for (r1, c1), (r2, c2) in sol.puzzle.ineqs:
        a, b = g[r1][c1], g[r2][c2]
        if a >= b:
            total += a - b + 1
    return total


def cost(sol):
    return column_conflicts(sol) + inequality_violations(sol)

def random_move(puzzle, rng=random):
    r = rng.choice(puzzle.movable_rows)
    c1, c2 = rng.sample(puzzle.free_cells[r], 2)
    return r, c1, c2


def apply_move(sol, move):
    r, c1, c2 = move
    g = sol.grid
    g[r][c1], g[r][c2] = g[r][c2], g[r][c1]


def _local_cost(sol, move):
    r, c1, c2 = move
    p, g, n = sol.puzzle, sol.grid, sol.puzzle.n
    cc = sum(n - len({g[i][c] for i in range(n)}) for c in (c1, c2))
    iv = 0
    for i in set(p.ineqs_of[(r, c1)] + p.ineqs_of[(r, c2)]):
        (ra, ca), (rb, cb) = p.ineqs[i]
        a, b = g[ra][ca], g[rb][cb]
        if a >= b:
            iv += a - b + 1
    return cc + iv


def delta_cost(sol, move):
    before = _local_cost(sol, move)
    apply_move(sol, move)
    after = _local_cost(sol, move)
    apply_move(sol, move)  # undo
    return after - before

def load_known_solution(path, puzzle):
    with open(path) as f:
        rows = [list(map(int, l.split())) for l in f if l.strip()]
    return Solution(puzzle, rows)

if __name__ == "__main__":
    p = load_instance("instances/4x4_test.txt")
    s = initial_solution(p)
    ok = True
    for _ in range(10000):
        m = random_move(p)
        before = cost(s)
        d = delta_cost(s, m)
        apply_move(s, m)
        if cost(s) - before != d:
            ok = False
            print("Mismatch!", m)
            break
        # givens must never change
        assert all(s.grid[r][c] == p.givens[r][c] for r in range(p.n) for c in range(p.n) if p.fixed[r][c])
    print("Delta cost check:", "OK" if ok else "FAILED")
    print(s)
    print("Cost:", cost(s))