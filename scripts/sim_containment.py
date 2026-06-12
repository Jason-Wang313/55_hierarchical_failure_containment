import csv
import os
import random
from statistics import mean


ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "docs", "containment_sim_results.csv")


def run_episode(depth=4, breadth=3, fault_p=0.15, retries=2, seed=0):
    rng = random.Random(seed)
    levels = [{"active": True, "faults": 0, "escalations": 0} for _ in range(depth)]
    propagation = 0
    contained = 0
    for level in range(depth):
        if not levels[level]["active"]:
            continue
        local_fault = rng.random() < fault_p
        if not local_fault:
            continue
        levels[level]["faults"] += 1
        handled = False
        for _ in range(retries):
            if rng.random() < (0.7 - 0.05 * level):
                handled = True
                contained += 1
                break
        if not handled and level + 1 < depth:
            levels[level + 1]["active"] = True
            levels[level + 1]["escalations"] += 1
            propagation += 1
    success = propagation < depth - 1
    return {"contained": contained, "propagation": propagation, "success": success}


def simulate(n=1000, retries=0):
    rows = []
    for i in range(n):
        rows.append(run_episode(retries=retries, seed=i))
    success_rate = mean(1.0 if r["success"] else 0.0 for r in rows)
    avg_prop = mean(r["propagation"] for r in rows)
    avg_cont = mean(r["contained"] for r in rows)
    return success_rate, avg_prop, avg_cont


def main():
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    configs = []
    for retries in [0, 1, 2, 3]:
        sr, ap, ac = simulate(n=2000, retries=retries)
        configs.append({"retries": retries, "success_rate": sr, "avg_propagation": ap, "avg_contained": ac})
    with open(OUT, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(configs[0].keys()))
        writer.writeheader()
        writer.writerows(configs)
    for row in configs:
        print(row)


if __name__ == "__main__":
    main()
