from __future__ import annotations

import csv
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "results" / "full_scale"


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def fmt(value: str | float) -> str:
    return f"{float(value):.3f}"


def tex_label(text: str) -> str:
    return text.title().replace(" And ", " and ")


def write_table(path: Path, header: list[str], rows: list[list[str]], align: str) -> None:
    lines = [f"\\begin{{tabular}}{{{align}}}", "\\toprule"]
    lines.append(" & ".join(header) + r" \\")
    lines.append("\\midrule")
    for row in rows:
        lines.append(" & ".join(row) + r" \\")
    lines.append("\\bottomrule")
    lines.append("\\end{tabular}")
    path.write_text("\n".join(lines) + "\n", encoding="ascii")


def main() -> None:
    maps = json.loads((RESULTS / "factor_maps.json").read_text(encoding="utf-8"))

    policy = read_csv(RESULTS / "policy_summary.csv")
    by_policy = {row["policy"]: row for row in policy}
    policy_order = [
        "oracle",
        "risk_calibrated",
        "fixed_one_retry",
        "fixed_two_retries",
        "local_backoff",
        "immediate_escalation",
        "fixed_four_retries",
        "unlimited_retry",
    ]
    write_table(
        RESULTS / "table_policy_operational_load.tex",
        ["Policy", "Escalate", "Retry", "Latency", "Waste", "Utility"],
        [
            [
                maps["policy"][code],
                fmt(by_policy[code]["escalate"]),
                fmt(by_policy[code]["retry"]),
                fmt(by_policy[code]["latency"]),
                fmt(by_policy[code]["waste"]),
                fmt(by_policy[code]["utility"]),
            ]
            for code in policy_order
        ],
        "lrrrrr",
    )

    task_rows = read_csv(RESULTS / "task_policy_summary.csv")
    task_index = {(row["task"], row["policy"]): row for row in task_rows}
    tasks = list(maps["task"].keys())
    write_table(
        RESULTS / "table_task_utility_gaps.tex",
        ["Task", "Risk util.", "Fixed-2 util.", "Risk gap", "Unlim. masked"],
        [
            [
                tex_label(maps["task"][task]),
                fmt(task_index[(task, "risk_calibrated")]["utility"]),
                fmt(task_index[(task, "fixed_two_retries")]["utility"]),
                fmt(
                    float(task_index[(task, "risk_calibrated")]["utility"])
                    - float(task_index[(task, "fixed_two_retries")]["utility"])
                ),
                fmt(task_index[(task, "unlimited_retry")]["masked"]),
            ]
            for task in tasks
        ],
        "lrrrr",
    )

    persistence_rows = read_csv(RESULTS / "persistence_policy_summary.csv")
    pidx = {(row["persistence"], row["policy"]): row for row in persistence_rows}
    write_table(
        RESULTS / "table_persistence_policy_panel.tex",
        ["Persistence", "Fixed-1 util.", "Fixed-2 util.", "Backoff util.", "Risk util.", "Unlim. masked"],
        [
            [
                tex_label(maps["persistence"][p]),
                fmt(pidx[(p, "fixed_one_retry")]["utility"]),
                fmt(pidx[(p, "fixed_two_retries")]["utility"]),
                fmt(pidx[(p, "local_backoff")]["utility"]),
                fmt(pidx[(p, "risk_calibrated")]["utility"]),
                fmt(pidx[(p, "unlimited_retry")]["masked"]),
            ]
            for p in maps["persistence"].keys()
        ],
        "lrrrrr",
    )

    obs_rows = read_csv(RESULTS / "observability_policy_summary.csv")
    oidx = {(row["observability"], row["policy"]): row for row in obs_rows}
    write_table(
        RESULTS / "table_observability_budget_panel.tex",
        ["Observability", "Risk escalate", "Risk retry", "Risk stale", "Unlim. stale", "Risk util."],
        [
            [
                tex_label(maps["observability"][o]),
                fmt(oidx[(o, "risk_calibrated")]["escalate"]),
                fmt(oidx[(o, "risk_calibrated")]["retry"]),
                fmt(oidx[(o, "risk_calibrated")]["stale"]),
                fmt(oidx[(o, "unlimited_retry")]["stale"]),
                fmt(oidx[(o, "risk_calibrated")]["utility"]),
            ]
            for o in maps["observability"].keys()
        ],
        "lrrrrr",
    )

    fault_rows = read_csv(RESULTS / "fault_policy_summary.csv")
    fidx = {(row["fault"], row["policy"]): row for row in fault_rows}
    write_table(
        RESULTS / "table_fault_policy_panel.tex",
        ["Fault", "Fixed-2 util.", "Risk util.", "Oracle util.", "Risk masked", "Unlim. masked"],
        [
            [
                tex_label(maps["fault"][f]),
                fmt(fidx[(f, "fixed_two_retries")]["utility"]),
                fmt(fidx[(f, "risk_calibrated")]["utility"]),
                fmt(fidx[(f, "oracle")]["utility"]),
                fmt(fidx[(f, "risk_calibrated")]["masked"]),
                fmt(fidx[(f, "unlimited_retry")]["masked"]),
            ]
            for f in maps["fault"].keys()
        ],
        "lrrrrr",
    )

    depth_rows = read_csv(RESULTS / "depth_policy_summary.csv")
    didx = {(row["depth"], row["policy"]): row for row in depth_rows}
    write_table(
        RESULTS / "table_depth_policy_panel.tex",
        ["Depth", "Immediate prop.", "Fixed-2 prop.", "Risk prop.", "Risk utility", "Unlim. masked"],
        [
            [
                tex_label(maps["depth"][d]),
                fmt(didx[(d, "immediate_escalation")]["prop"]),
                fmt(didx[(d, "fixed_two_retries")]["prop"]),
                fmt(didx[(d, "risk_calibrated")]["prop"]),
                fmt(didx[(d, "risk_calibrated")]["utility"]),
                fmt(didx[(d, "unlimited_retry")]["masked"]),
            ]
            for d in maps["depth"].keys()
        ],
        "lrrrrr",
    )


if __name__ == "__main__":
    main()
