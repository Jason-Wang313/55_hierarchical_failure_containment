import csv
import json
import random
from pathlib import Path
from statistics import mean


ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
OUT_CSV = DOCS / "v2_persistent_fault_stress_summary.csv"
OUT_JSON = DOCS / "v2_persistent_fault_stress.json"
OUT_TEX = ROOT / "v2_persistent_fault_table.tex"


def run_episode(seed, retries, persistent_fault_p=0.25, depth=4, fault_p=0.18):
    rng = random.Random(seed)
    propagation = 0
    contained = 0
    attempts = 0
    unsafe_masked = False
    mission_success = True

    for level in range(depth):
        if rng.random() >= fault_p:
            continue
        persistent = rng.random() < persistent_fault_p
        handled = False
        for attempt in range(retries):
            attempts += 1
            if persistent:
                # Persistent faults are hard to clear locally; repeated retries can hide stale state.
                if rng.random() < max(0.05, 0.18 - 0.03 * level):
                    handled = True
                    contained += 1
                    break
                if attempt >= 2 and rng.random() < 0.18 + 0.04 * level:
                    unsafe_masked = True
            else:
                if rng.random() < max(0.2, 0.72 - 0.06 * level):
                    handled = True
                    contained += 1
                    break
        if not handled:
            if level + 1 < depth:
                propagation += 1
            else:
                mission_success = False

    mission_success = mission_success and not unsafe_masked
    utility = (
        (1.0 if mission_success else 0.0)
        - 0.10 * propagation
        - 0.025 * attempts
        - 0.45 * (1.0 if unsafe_masked else 0.0)
    )
    return {
        "success": mission_success,
        "propagation": propagation,
        "contained": contained,
        "attempts": attempts,
        "unsafe_masked": unsafe_masked,
        "utility": utility,
    }


def summarize(persistent_fault_p, retries, n=5000):
    rows = [run_episode(seed, retries, persistent_fault_p=persistent_fault_p) for seed in range(n)]
    return {
        "persistent_fault_p": persistent_fault_p,
        "retries": retries,
        "n": n,
        "success_rate": mean(1.0 if row["success"] else 0.0 for row in rows),
        "avg_propagation": mean(row["propagation"] for row in rows),
        "avg_contained": mean(row["contained"] for row in rows),
        "avg_retry_attempts": mean(row["attempts"] for row in rows),
        "unsafe_masked_rate": mean(1.0 if row["unsafe_masked"] else 0.0 for row in rows),
        "utility": mean(row["utility"] for row in rows),
    }


def main():
    DOCS.mkdir(exist_ok=True)
    persistent_levels = [0.05, 0.25, 0.45]
    retry_budgets = [0, 1, 2, 3, 4, 6, 8]
    summary = [summarize(p, r) for p in persistent_levels for r in retry_budgets]

    with OUT_CSV.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(summary[0].keys()))
        writer.writeheader()
        writer.writerows(summary)

    by_persistent = {}
    for p in persistent_levels:
        candidates = [row for row in summary if row["persistent_fault_p"] == p]
        by_persistent[str(p)] = max(candidates, key=lambda row: row["utility"])

    OUT_JSON.write_text(
        json.dumps(
            {
                "decision": "workshop-only",
                "reason": "Containment budgets need cost and masked-fault audits; unlimited local retry is not robust.",
                "best_by_persistent_fault_rate": by_persistent,
                "summary": summary,
            },
            indent=2,
        ),
        encoding="utf-8",
    )

    selected = [row for row in summary if row["persistent_fault_p"] == 0.25 and row["retries"] in {0, 2, 4, 8}]
    OUT_TEX.write_text(
        "\n".join(
            [
                r"\begin{tabular}{lrrrr}",
                r"\toprule",
                r"Retries & Success & Propagation & Masked unsafe & Utility \\",
                r"\midrule",
                *[
                    (
                        f"{row['retries']} & {row['success_rate']:.3f} & {row['avg_propagation']:.3f} & "
                        f"{row['unsafe_masked_rate']:.3f} & {row['utility']:.3f} \\\\"
                    )
                    for row in selected
                ],
                r"\bottomrule",
                r"\end{tabular}",
                "",
            ]
        ),
        encoding="utf-8",
    )

    for p in persistent_levels:
        best = by_persistent[str(p)]
        print(
            f"persistent={p}",
            f"best_retries={best['retries']}",
            f"utility={best['utility']:.3f}",
            f"unsafe={best['unsafe_masked_rate']:.3f}",
        )


if __name__ == "__main__":
    main()
