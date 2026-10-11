import csv
import glob
import os
import statistics

from futoshiki import load_instance, load_known_solution, cost
from sa import simulated_annealing

RUNS = 10
TIME_LIMIT = 20.0
SA_PARAMS = dict(t0=2.0, alpha=0.99, t_min=0.05, L_factor=10)

def instance_key(path):
    name = os.path.basename(path)[:-4]
    size, k = name.split("_")
    return int(size.split("x")[0]), k

if __name__ == "__main__":
    files = sorted([f for f in glob.glob("instances/*.txt") if "test" not in f], key=instance_key)
    os.makedirs("results", exist_ok=True)
    rows, summary = [], []

    for path in files:
        name = os.path.basename(path)[:-4]
        p = load_instance(path)
        known = load_known_solution(path[:-4] + ".sol", p)
        givens = sum(p.fixed[r][c] for r in range(p.n) for c in range(p.n))
        runs = []
        for seed in range(RUNS):
            res = simulated_annealing(p, time_limit=TIME_LIMIT, seed=seed, **SA_PARAMS)
            assert cost(res["best"]) == res["best_cost"]   # sanity check
            run = {
                "instance": name, "n": p.n, "givens": givens, "inequalities": len(p.ineqs),
                "seed": seed, "initial_cost": res["history"][0][1],
                "final_cost": res["best_cost"], "optimal_cost": cost(known),
                "solved": res["best_cost"] == 0, "time_s": round(res["time"], 4),
                "iterations": res["iterations"], "reheats": res["reheats"],
            }
            runs.append(run)
            rows.append(run)
        times = [r["time_s"] for r in runs]
        s = {
            "instance": name, "n": p.n, "givens": givens, "inequalities": len(p.ineqs),
            "success_rate": f"{sum(r['solved'] for r in runs)}/{RUNS}",
            "mean_time_s": round(statistics.mean(times), 4),
            "median_time_s": round(statistics.median(times), 4),
            "mean_iterations": round(statistics.mean(r["iterations"] for r in runs)),
            "best_final_cost": min(r["final_cost"] for r in runs),
            "worst_final_cost": max(r["final_cost"] for r in runs),
        }
        summary.append(s)
        print(f"{name}: solved {s['success_rate']}, mean time {s['mean_time_s']} s, "
              f"mean iterations {s['mean_iterations']}, worst cost {s['worst_final_cost']}")

    for fname, data in (("results/results.csv", rows), ("results/summary.csv", summary)):
        with open(fname, "w", newline="") as f:
            w = csv.DictWriter(f, fieldnames=data[0].keys())
            w.writeheader()
            w.writerows(data)
    print("Saved results/results.csv and results/summary.csv")