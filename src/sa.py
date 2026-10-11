import math
import random
import time

from futoshiki import initial_solution, cost, random_move, apply_move, delta_cost


def simulated_annealing(puzzle, t0=2.0, alpha=0.99, t_min=0.05,
                        L_factor=10, time_limit=60.0, seed=None):
    """
    Simulated Annealing (lecture 3, slide 13).
    t0, alpha, t_min -> temperature list t[k] (geometric cooling)
    L_factor        -> L[k] = L_factor * n * n iterations per temperature
    Stops when cost == 0 (optimum) or time_limit is reached; reheats if schedule ends.
    """
    rng = random.Random(seed)
    n = puzzle.n
    L = L_factor * n * n

    current = initial_solution(puzzle, rng)
    cur_cost = cost(current)
    best, best_cost = current.copy(), cur_cost

    start = time.perf_counter()
    iterations, reheats = 0, 0
    history = [(0, best_cost)]

    while best_cost > 0 and time.perf_counter() - start < time_limit:
        t = t0
        while t > t_min and best_cost > 0:
            for _ in range(L):
                move = random_move(puzzle, rng)
                d = delta_cost(current, move)
                if d <= 0 or rng.random() < math.exp(-d / t):
                    apply_move(current, move)
                    cur_cost += d
                    if cur_cost < best_cost:
                        best, best_cost = current.copy(), cur_cost
                        history.append((iterations, best_cost))
                        if best_cost == 0:
                            break
                iterations += 1
            t *= alpha
            if time.perf_counter() - start >= time_limit:
                break
        if best_cost > 0:
            reheats += 1
            current, cur_cost = best.copy(), best_cost

    return {
        "best": best,
        "best_cost": best_cost,
        "iterations": iterations,
        "time": time.perf_counter() - start,
        "reheats": reheats,
        "history": history,
    }


if __name__ == "__main__":
    from futoshiki import load_instance
    p = load_instance("instances/4x4_test.txt")
    res = simulated_annealing(p, seed=1)
    print(res["best"])
    print("Cost:", res["best_cost"])
    print("Iterations:", res["iterations"], "| Time: %.3f s" % res["time"], "| Reheats:", res["reheats"])
    print("Verified cost:", cost(res["best"]))