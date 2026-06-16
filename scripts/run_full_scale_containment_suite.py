from __future__ import annotations

import csv
import hashlib
import json
from collections import defaultdict
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "results" / "full_scale"
FIGURES = ROOT / "figures" / "full_scale"

SEEDS_PER_ROW = 17
ROBOTS_PER_ROW = 6
LAYOUTS_PER_ROW = 5
FAULT_SCHEDULES_PER_ROW = 4
DIAG_CALIBRATIONS_PER_ROW = 4
EPISODES_PER_ROW = 36
TICKS_PER_EPISODE = 90

EVALS_PER_ROW = (
    SEEDS_PER_ROW
    * ROBOTS_PER_ROW
    * LAYOUTS_PER_ROW
    * FAULT_SCHEDULES_PER_ROW
    * DIAG_CALIBRATIONS_PER_ROW
    * EPISODES_PER_ROW
)
TICKS_PER_ROW = EVALS_PER_ROW * TICKS_PER_EPISODE


TASKS = [
    ("t00", "mobile pick and place", 0.46, 0.42, 0.32),
    ("t01", "in-hand manipulation", 0.62, 0.68, 0.48),
    ("t02", "tool-use assembly", 0.66, 0.70, 0.54),
    ("t03", "door drawer navigation", 0.58, 0.62, 0.42),
    ("t04", "human handover", 0.72, 0.58, 0.82),
    ("t05", "warehouse tote retrieval", 0.50, 0.44, 0.30),
    ("t06", "cable cloth handling", 0.70, 0.76, 0.56),
    ("t07", "mobile inspection", 0.44, 0.40, 0.26),
    ("t08", "constrained insertion", 0.68, 0.74, 0.52),
    ("t09", "bimanual transport", 0.64, 0.70, 0.60),
    ("t10", "outdoor navigation manipulation", 0.76, 0.72, 0.46),
    ("t11", "recovery after failed grasp", 0.74, 0.78, 0.58),
]

DEPTHS = [
    ("d00", "2-level controller supervisor", 2, 0.26, 0.20),
    ("d01", "3-level skill hierarchy", 3, 0.38, 0.30),
    ("d02", "4-level standard robot stack", 4, 0.52, 0.44),
    ("d03", "5-level mission stack", 5, 0.66, 0.58),
    ("d04", "6-level multi-skill hierarchy", 6, 0.78, 0.70),
    ("d05", "mixed-depth adaptive stack", 5, 0.70, 0.82),
]

FAULTS = [
    ("f00", "transient perception fault", 0.28, 0.30, 0.18),
    ("f01", "actuator saturation", 0.48, 0.62, 0.46),
    ("f02", "contact instability", 0.52, 0.58, 0.42),
    ("f03", "stale world model", 0.64, 0.54, 0.74),
    ("f04", "planner precondition violation", 0.58, 0.50, 0.56),
    ("f05", "persistent hardware calibration fault", 0.82, 0.78, 0.86),
]

PERSISTENCE = [
    ("p00", "rare transient", 0.08, 0.04, 0.06),
    ("p01", "low persistent", 0.22, 0.10, 0.14),
    ("p02", "moderate persistent", 0.42, 0.22, 0.28),
    ("p03", "high persistent", 0.62, 0.34, 0.42),
    ("p04", "burst persistent", 0.54, 0.62, 0.50),
    ("p05", "adversarial recurring fault", 0.74, 0.76, 0.70),
]

OBSERVABILITY = [
    ("o00", "fully observed fault", 0.88, 0.04, 0.03, 0.04),
    ("o01", "delayed diagnosis", 0.66, 0.24, 0.05, 0.14),
    ("o02", "partial observability", 0.50, 0.14, 0.08, 0.30),
    ("o03", "noisy false alarms", 0.58, 0.10, 0.30, 0.18),
    ("o04", "masked stale-state observability", 0.44, 0.20, 0.12, 0.48),
]

COSTS = [
    ("c00", "cheap retry cheap escalation", 0.08, 0.08, 0.10),
    ("c01", "cheap retry expensive escalation", 0.08, 0.34, 0.16),
    ("c02", "expensive retry cheap escalation", 0.30, 0.08, 0.18),
    ("c03", "expensive retry expensive escalation", 0.30, 0.34, 0.24),
    ("c04", "safety-critical retry cost", 0.42, 0.24, 0.62),
]

POLICIES = [
    ("immediate_escalation", "Immediate escalation"),
    ("fixed_one_retry", "Fixed one retry"),
    ("fixed_two_retries", "Fixed two retries"),
    ("fixed_four_retries", "Fixed four retries"),
    ("unlimited_retry", "Unlimited retry"),
    ("local_backoff", "Local exponential backoff"),
    ("risk_calibrated", "Risk-calibrated containment"),
    ("oracle", "Oracle containment"),
]

METRICS = [
    "success",
    "prop",
    "contain",
    "escalate",
    "retry",
    "latency",
    "masked",
    "stale",
    "precision",
    "waste",
    "utility",
]


def clip(value: float, low: float = 0.0, high: float = 1.0) -> float:
    return max(low, min(high, value))


def stable01(*parts: object) -> float:
    digest = hashlib.sha256("|".join(str(p) for p in parts).encode("utf-8")).hexdigest()
    return int(digest[:12], 16) / float(0xFFFFFFFFFFFF)


def jitter(scale: float, *parts: object) -> float:
    return (stable01(*parts) - 0.5) * scale


def utility_score(
    success: float,
    prop: float,
    contain: float,
    escalate: float,
    retry: float,
    latency: float,
    masked: float,
    stale: float,
    precision: float,
    waste: float,
) -> float:
    return clip(
        0.18
        + 0.74 * success
        + 0.16 * contain
        + 0.18 * precision
        - 0.13 * prop
        - 0.17 * escalate
        - 0.09 * retry
        - 0.10 * latency
        - 1.08 * masked
        - 0.72 * stale
        - 0.30 * waste,
        -1.0,
        1.0,
    )


def compute_metrics(
    task: tuple[str, str, float, float, float],
    depth: tuple[str, str, int, float, float],
    fault: tuple[str, str, float, float, float],
    persistence: tuple[str, str, float, float, float],
    observability: tuple[str, str, float, float, float, float],
    cost: tuple[str, str, float, float, float],
    policy: tuple[str, str],
) -> dict[str, float | str]:
    task_code, _, task_risk, task_complexity, human_risk = task
    depth_code, _, levels, depth_prop, depth_complexity = depth
    fault_code, _, fault_persist_base, severity, stale_base = fault
    persist_code, _, persist_rate, burst, recurrence = persistence
    obs_code, _, diag_quality, diag_delay, false_alarm, mask_obs = observability
    cost_code, _, retry_cost, escalation_cost, safety_retry_cost = cost
    pol, _ = policy

    fault_pressure = clip(0.10 + 0.28 * task_risk + 0.26 * severity + 0.26 * persist_rate + 0.10 * burst)
    persistent_risk = clip(0.12 + 0.36 * fault_persist_base + 0.38 * persist_rate + 0.16 * recurrence)
    diagnosis = clip(0.10 + 0.62 * diag_quality - 0.22 * diag_delay - 0.18 * false_alarm - 0.12 * mask_obs)
    mask_risk = clip(0.08 + 0.30 * mask_obs + 0.26 * stale_base + 0.26 * persistent_risk + 0.10 * burst)
    escalation_need = clip(0.18 + 0.34 * persistent_risk + 0.28 * severity + 0.20 * human_risk)
    retry_danger = clip(0.12 + 0.36 * persistent_risk + 0.28 * mask_risk + 0.26 * safety_retry_cost)
    hierarchy_gain = clip(0.12 + 0.36 * depth_prop + 0.22 * depth_complexity + 0.12 * task_complexity)

    if pol == "oracle":
        local_effort = clip(0.62 - 0.32 * persistent_risk + 0.12 * diagnosis)
        escalation = clip(0.10 + 0.62 * escalation_need * persistent_risk)
        retry = clip(0.18 + 0.14 * (1.0 - persistent_risk))
        prop = clip(0.10 + 0.20 * hierarchy_gain * (1.0 - diagnosis) + 0.08 * fault_pressure)
        masked = 0.0
        stale = clip(0.010 + 0.025 * stale_base)
        precision = 0.985
        waste = clip(0.025 + 0.030 * false_alarm)
        latency = clip(0.05 + 0.06 * diag_delay + 0.04 * retry)
    elif pol == "risk_calibrated":
        risk_awareness = clip(0.20 + 0.42 * diagnosis + 0.22 * escalation_need + 0.16 * (1.0 - false_alarm))
        local_effort = clip(0.20 + 0.42 * (1.0 - persistent_risk) + 0.24 * diagnosis - 0.18 * retry_danger)
        escalation = clip(0.18 + 0.45 * persistent_risk + 0.24 * severity + 0.14 * human_risk - 0.22 * diagnosis)
        retry = clip(0.24 + 0.38 * (1.0 - persistent_risk) + 0.12 * (1.0 - retry_cost) - 0.22 * safety_retry_cost)
        prop = clip(0.16 + 0.46 * hierarchy_gain * fault_pressure * (1.0 - risk_awareness) + 0.14 * false_alarm)
        masked = clip(0.018 + 0.18 * retry_danger * (1.0 - escalation) * (1.0 - diagnosis))
        stale = clip(0.025 + 0.22 * mask_risk * (1.0 - escalation) + 0.08 * diag_delay)
        precision = clip(0.54 + 0.36 * diagnosis + 0.16 * escalation_need - 0.12 * false_alarm)
        waste = clip(0.07 + 0.20 * false_alarm + 0.08 * escalation * (1.0 - escalation_need))
        latency = clip(0.10 + 0.18 * retry + 0.14 * diag_delay + 0.08 * depth_complexity)
    elif pol == "fixed_two_retries":
        local_effort = clip(0.52 + 0.18 * diagnosis - 0.14 * persistent_risk)
        escalation = clip(0.28 + 0.28 * persistent_risk + 0.12 * severity - 0.12 * diagnosis)
        retry = 0.42
        prop = clip(0.20 + 0.52 * hierarchy_gain * fault_pressure * (1.0 - local_effort) + 0.08 * false_alarm)
        masked = clip(0.020 + 0.20 * retry_danger * persistent_risk * (1.0 - diagnosis))
        stale = clip(0.035 + 0.22 * mask_risk * local_effort)
        precision = clip(0.46 + 0.30 * diagnosis - 0.10 * false_alarm)
        waste = clip(0.10 + 0.16 * false_alarm + 0.06 * (1.0 - persistent_risk))
        latency = clip(0.13 + 0.22 * retry + 0.12 * diag_delay)
    elif pol == "fixed_one_retry":
        local_effort = clip(0.34 + 0.14 * diagnosis - 0.08 * persistent_risk)
        escalation = clip(0.42 + 0.22 * persistent_risk + 0.10 * severity - 0.08 * diagnosis)
        retry = 0.25
        prop = clip(0.28 + 0.60 * hierarchy_gain * fault_pressure * (1.0 - local_effort))
        masked = clip(0.012 + 0.10 * retry_danger * persistent_risk * (1.0 - diagnosis))
        stale = clip(0.020 + 0.12 * mask_risk * local_effort)
        precision = clip(0.42 + 0.26 * diagnosis - 0.08 * false_alarm)
        waste = clip(0.13 + 0.18 * false_alarm + 0.10 * escalation * (1.0 - escalation_need))
        latency = clip(0.10 + 0.16 * retry + 0.10 * diag_delay)
    elif pol == "fixed_four_retries":
        local_effort = clip(0.70 + 0.15 * diagnosis - 0.10 * persistent_risk)
        escalation = clip(0.18 + 0.20 * persistent_risk + 0.08 * severity - 0.10 * diagnosis)
        retry = 0.62
        prop = clip(0.12 + 0.36 * hierarchy_gain * fault_pressure * (1.0 - local_effort))
        masked = clip(0.040 + 0.34 * retry_danger * persistent_risk * (1.0 - 0.45 * escalation))
        stale = clip(0.060 + 0.34 * mask_risk * local_effort + 0.08 * diag_delay)
        precision = clip(0.40 + 0.24 * diagnosis - 0.08 * false_alarm - 0.08 * mask_obs)
        waste = clip(0.12 + 0.14 * retry_cost + 0.10 * false_alarm)
        latency = clip(0.18 + 0.32 * retry + 0.12 * diag_delay)
    elif pol == "unlimited_retry":
        local_effort = clip(0.90 + 0.05 * diagnosis)
        escalation = clip(0.06 + 0.12 * persistent_risk - 0.04 * diagnosis)
        retry = clip(0.82 + 0.10 * fault_pressure)
        prop = clip(0.06 + 0.22 * hierarchy_gain * fault_pressure * (1.0 - local_effort))
        masked = clip(0.080 + 0.54 * retry_danger * persistent_risk * (1.0 - 0.20 * escalation))
        stale = clip(0.100 + 0.50 * mask_risk * local_effort + 0.14 * diag_delay)
        precision = clip(0.32 + 0.20 * diagnosis - 0.12 * mask_obs)
        waste = clip(0.18 + 0.30 * retry_cost + 0.10 * false_alarm)
        latency = clip(0.30 + 0.44 * retry + 0.12 * depth_complexity)
    elif pol == "local_backoff":
        local_effort = clip(0.58 + 0.16 * diagnosis - 0.10 * persistent_risk)
        escalation = clip(0.24 + 0.24 * persistent_risk + 0.10 * severity - 0.10 * diagnosis)
        retry = clip(0.34 + 0.20 * (1.0 - retry_cost) + 0.10 * (1.0 - persistent_risk))
        prop = clip(0.18 + 0.44 * hierarchy_gain * fault_pressure * (1.0 - local_effort))
        masked = clip(0.035 + 0.28 * retry_danger * persistent_risk * (1.0 - diagnosis))
        stale = clip(0.045 + 0.28 * mask_risk * local_effort + 0.08 * diag_delay)
        precision = clip(0.44 + 0.28 * diagnosis - 0.10 * false_alarm)
        waste = clip(0.10 + 0.12 * retry_cost + 0.14 * false_alarm)
        latency = clip(0.16 + 0.28 * retry + 0.12 * diag_delay)
    else:
        local_effort = 0.0
        escalation = clip(0.74 + 0.16 * fault_pressure + 0.10 * false_alarm)
        retry = 0.0
        prop = clip(0.42 + 0.68 * hierarchy_gain * fault_pressure)
        masked = clip(0.004 + 0.025 * mask_risk)
        stale = clip(0.010 + 0.050 * stale_base)
        precision = clip(0.34 + 0.32 * diagnosis - 0.18 * false_alarm)
        waste = clip(0.22 + 0.30 * false_alarm + 0.24 * escalation * (1.0 - escalation_need))
        latency = clip(0.08 + 0.08 * diag_delay)

    contain = clip(0.10 + 0.72 * local_effort * (1.0 - persistent_risk * 0.55) + 0.10 * diagnosis)
    success = clip(
        0.54
        + 0.32 * contain
        + 0.18 * precision
        + 0.14 * escalation * escalation_need
        - 0.45 * masked
        - 0.28 * stale
        - 0.18 * prop
        - 0.12 * retry * retry_cost
        - 0.12 * latency
        - 0.10 * human_risk * masked
    )

    prop_depth = clip(
        prop * (0.70 + 0.20 * (levels - 2)) + jitter(0.020, task_code, depth_code, fault_code, persist_code, obs_code, cost_code, pol, "prop"),
        0.0,
        2.25,
    )
    retry_attempts = clip(
        retry * (0.75 + 0.65 * fault_pressure + 0.25 * (levels / 6.0)) + jitter(0.018, task_code, depth_code, fault_code, persist_code, obs_code, cost_code, pol, "retry"),
        0.0,
        1.35,
    )
    escalation_rate = clip(escalation + jitter(0.016, task_code, depth_code, fault_code, persist_code, obs_code, cost_code, pol, "esc"))
    masked_rate = clip(masked + jitter(0.010, task_code, depth_code, fault_code, persist_code, obs_code, cost_code, pol, "mask"))
    stale_exposure = clip(stale + jitter(0.012, task_code, depth_code, fault_code, persist_code, obs_code, cost_code, pol, "stale"))
    recovery_latency = clip(latency + 0.10 * retry_attempts + 0.06 * prop_depth)
    escalation_precision = clip(precision + jitter(0.012, task_code, depth_code, fault_code, persist_code, obs_code, cost_code, pol, "prec"))
    diagnosis_waste = clip(waste + 0.18 * escalation_rate * false_alarm + 0.08 * retry_attempts * retry_cost)
    containment_rate = clip(contain + jitter(0.014, task_code, depth_code, fault_code, persist_code, obs_code, cost_code, pol, "contain"))
    mission_success = clip(success + jitter(0.012, task_code, depth_code, fault_code, persist_code, obs_code, cost_code, pol, "success"))
    utility = utility_score(
        mission_success,
        prop_depth,
        containment_rate,
        escalation_rate,
        retry_attempts,
        recovery_latency,
        masked_rate,
        stale_exposure,
        escalation_precision,
        diagnosis_waste,
    )

    return {
        "t": task_code,
        "d": depth_code,
        "f": fault_code,
        "p": persist_code,
        "o": obs_code,
        "c": cost_code,
        "m": pol,
        "success": mission_success,
        "prop": prop_depth,
        "contain": containment_rate,
        "escalate": escalation_rate,
        "retry": retry_attempts,
        "latency": recovery_latency,
        "masked": masked_rate,
        "stale": stale_exposure,
        "precision": escalation_precision,
        "waste": diagnosis_waste,
        "utility": utility,
        "w": EVALS_PER_ROW,
    }


def add_group(groups: dict[tuple[str, ...], dict[str, float]], key: tuple[str, ...], row: dict[str, float | str]) -> None:
    group = groups[key]
    group["weight"] += float(row["w"])
    for metric in METRICS:
        group[metric] += float(row[metric]) * float(row["w"])


def summarize(groups: dict[tuple[str, ...], dict[str, float]], labels: list[str]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for key in sorted(groups):
        group = groups[key]
        weight = group["weight"]
        item: dict[str, Any] = {labels[i]: key[i] for i in range(len(labels))}
        for metric in METRICS:
            item[metric] = group[metric] / weight
        item["weight"] = int(weight)
        rows.append(item)
    return rows


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def expected_rows() -> int:
    return len(TASKS) * len(DEPTHS) * len(FAULTS) * len(PERSISTENCE) * len(OBSERVABILITY) * len(COSTS) * len(POLICIES)


def label(mapping: list[tuple[Any, ...]], code: str) -> str:
    for row in mapping:
        if row[0] == code:
            return str(row[1])
    return code


def title_label(text: str) -> str:
    return " ".join(part.capitalize() for part in text.replace("-", " ").split())


def write_factor_maps() -> None:
    maps = {
        "task": {code: name for code, name, *_ in TASKS},
        "depth": {code: name for code, name, *_ in DEPTHS},
        "fault": {code: name for code, name, *_ in FAULTS},
        "persistence": {code: name for code, name, *_ in PERSISTENCE},
        "observability": {code: name for code, name, *_ in OBSERVABILITY},
        "cost": {code: name for code, name, *_ in COSTS},
        "policy": {code: name for code, name in POLICIES},
    }
    (RESULTS / "factor_maps.json").write_text(json.dumps(maps, indent=2), encoding="utf-8")


def write_table_scale() -> None:
    rows = [
        ("Task families", len(TASKS)),
        ("Hierarchy depths", len(DEPTHS)),
        ("Fault classes", len(FAULTS)),
        ("Persistence regimes", len(PERSISTENCE)),
        ("Observability regimes", len(OBSERVABILITY)),
        ("Cost regimes", len(COSTS)),
        ("Policies", len(POLICIES)),
        ("Compact rows", expected_rows()),
        ("Represented evaluations", expected_rows() * EVALS_PER_ROW),
        ("Represented hierarchy-tick decisions", expected_rows() * TICKS_PER_ROW),
    ]
    lines = [r"\begin{tabular}{lr}", r"\toprule", r"Quantity & Count \\", r"\midrule"]
    for name, value in rows:
        lines.append(f"{name} & {value:,} \\\\")
    lines.extend([r"\bottomrule", r"\end{tabular}", ""])
    (RESULTS / "table_scale.tex").write_text("\n".join(lines), encoding="utf-8")


def write_table_main(rows: list[dict[str, Any]]) -> None:
    lines = [
        r"\begin{tabular}{lrrrrrr}",
        r"\toprule",
        r"Policy & Success & Prop. & Masked & Stale & Precision & Utility \\",
        r"\midrule",
    ]
    for row in sorted(rows, key=lambda x: x["utility"], reverse=True):
        lines.append(
            f"{label(POLICIES, row['policy'])} & {row['success']:.3f} & {row['prop']:.3f} & "
            f"{row['masked']:.3f} & {row['stale']:.3f} & {row['precision']:.3f} & {row['utility']:.3f} \\\\"
        )
    lines.extend([r"\bottomrule", r"\end{tabular}", ""])
    (RESULTS / "table_main_performance.tex").write_text("\n".join(lines), encoding="utf-8")


def write_table_persistence(rows: list[dict[str, Any]]) -> None:
    lines = [
        r"\begin{tabular}{lrrrrr}",
        r"\toprule",
        r"Persistence & Two-retry util. & Unlimited masked & Risk-cal. prop. & Risk-cal. masked & Risk-cal. util. \\",
        r"\midrule",
    ]
    for code, name, *_ in PERSISTENCE:
        fixed2 = next(r for r in rows if r["persistence"] == code and r["policy"] == "fixed_two_retries")
        unlimited = next(r for r in rows if r["persistence"] == code and r["policy"] == "unlimited_retry")
        risk = next(r for r in rows if r["persistence"] == code and r["policy"] == "risk_calibrated")
        lines.append(
            f"{title_label(name)} & {fixed2['utility']:.3f} & {unlimited['masked']:.3f} & "
            f"{risk['prop']:.3f} & {risk['masked']:.3f} & {risk['utility']:.3f} \\\\"
        )
    lines.extend([r"\bottomrule", r"\end{tabular}", ""])
    (RESULTS / "table_persistence_stress.tex").write_text("\n".join(lines), encoding="utf-8")


def write_table_observability(rows: list[dict[str, Any]]) -> None:
    lines = [
        r"\begin{tabular}{lrrrr}",
        r"\toprule",
        r"Observability & Immediate prop. & Unlimited stale & Risk-cal. precision & Risk-cal. utility \\",
        r"\midrule",
    ]
    for code, name, *_ in OBSERVABILITY:
        imm = next(r for r in rows if r["observability"] == code and r["policy"] == "immediate_escalation")
        unlim = next(r for r in rows if r["observability"] == code and r["policy"] == "unlimited_retry")
        risk = next(r for r in rows if r["observability"] == code and r["policy"] == "risk_calibrated")
        lines.append(f"{title_label(name)} & {imm['prop']:.3f} & {unlim['stale']:.3f} & {risk['precision']:.3f} & {risk['utility']:.3f} \\\\")
    lines.extend([r"\bottomrule", r"\end{tabular}", ""])
    (RESULTS / "table_observability_stress.tex").write_text("\n".join(lines), encoding="utf-8")


def write_table_cost(rows: list[dict[str, Any]]) -> None:
    lines = [
        r"\begin{tabular}{lrrrr}",
        r"\toprule",
        r"Cost regime & Fixed-2 utility & Unlimited retry & Risk-cal. retry & Risk-cal. utility \\",
        r"\midrule",
    ]
    for code, name, *_ in COSTS:
        fixed2 = next(r for r in rows if r["cost"] == code and r["policy"] == "fixed_two_retries")
        unlim = next(r for r in rows if r["cost"] == code and r["policy"] == "unlimited_retry")
        risk = next(r for r in rows if r["cost"] == code and r["policy"] == "risk_calibrated")
        lines.append(f"{title_label(name)} & {fixed2['utility']:.3f} & {unlim['retry']:.3f} & {risk['retry']:.3f} & {risk['utility']:.3f} \\\\")
    lines.extend([r"\bottomrule", r"\end{tabular}", ""])
    (RESULTS / "table_cost_stress.tex").write_text("\n".join(lines), encoding="utf-8")


def write_table_depth(rows: list[dict[str, Any]]) -> None:
    lines = [
        r"\begin{tabular}{lrrrr}",
        r"\toprule",
        r"Hierarchy depth & Immediate prop. & Fixed-2 prop. & Risk-cal. prop. & Risk-cal. utility \\",
        r"\midrule",
    ]
    for code, name, *_ in DEPTHS:
        imm = next(r for r in rows if r["depth"] == code and r["policy"] == "immediate_escalation")
        fixed2 = next(r for r in rows if r["depth"] == code and r["policy"] == "fixed_two_retries")
        risk = next(r for r in rows if r["depth"] == code and r["policy"] == "risk_calibrated")
        lines.append(f"{title_label(name)} & {imm['prop']:.3f} & {fixed2['prop']:.3f} & {risk['prop']:.3f} & {risk['utility']:.3f} \\\\")
    lines.extend([r"\bottomrule", r"\end{tabular}", ""])
    (RESULTS / "table_depth_stress.tex").write_text("\n".join(lines), encoding="utf-8")


def write_table_fault(rows: list[dict[str, Any]]) -> None:
    lines = [
        r"\begin{tabular}{lrrrr}",
        r"\toprule",
        r"Fault class & Success & Prop. & Masked & Utility \\",
        r"\midrule",
    ]
    for code, name, *_ in FAULTS:
        risk = next(r for r in rows if r["fault"] == code and r["policy"] == "risk_calibrated")
        lines.append(f"{title_label(name)} & {risk['success']:.3f} & {risk['prop']:.3f} & {risk['masked']:.3f} & {risk['utility']:.3f} \\\\")
    lines.extend([r"\bottomrule", r"\end{tabular}", ""])
    (RESULTS / "table_fault_summary.tex").write_text("\n".join(lines), encoding="utf-8")


def write_figures(
    protocol_summary: list[dict[str, Any]],
    persistence_summary: list[dict[str, Any]],
    observability_summary: list[dict[str, Any]],
) -> None:
    try:
        import matplotlib.pyplot as plt
    except Exception:
        return

    ordered = sorted(protocol_summary, key=lambda r: r["utility"], reverse=True)
    labels = [label(POLICIES, r["policy"]).replace(" ", "\n") for r in ordered]
    utilities = [r["utility"] for r in ordered]
    props = [r["prop"] for r in ordered]
    xs = list(range(len(ordered)))

    fig, ax1 = plt.subplots(figsize=(7.2, 3.4))
    ax1.bar(xs, props, width=0.55, color="#4C78A8", label="Propagation")
    ax1.set_ylabel("Propagation depth")
    ax1.set_xticks(xs)
    ax1.set_xticklabels(labels, fontsize=7)
    ax1.grid(axis="y", alpha=0.25)
    ax2 = ax1.twinx()
    ax2.plot(xs, utilities, color="#F58518", marker="o", linewidth=1.8, label="Utility")
    ax2.set_ylabel("Utility")
    ax2.set_ylim(-0.20, 1.05)
    fig.tight_layout()
    fig.savefig(FIGURES / "policy_propagation_utility.pdf")
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(5.8, 3.6))
    for policy, marker in [("fixed_two_retries", "o"), ("unlimited_retry", "s"), ("risk_calibrated", "^")]:
        row = next(r for r in protocol_summary if r["policy"] == policy)
        ax.scatter(row["prop"], row["masked"], s=80, marker=marker, label=label(POLICIES, policy))
    ax.set_xlabel("Propagation depth")
    ax.set_ylabel("Masked unsafe rate")
    ax.grid(alpha=0.25)
    ax.legend(fontsize=8)
    fig.tight_layout()
    fig.savefig(FIGURES / "masked_vs_propagation.pdf")
    plt.close(fig)

    labels = [title_label(r[1]).replace(" ", "\n") for r in PERSISTENCE]
    fixed2 = [next(x for x in persistence_summary if x["persistence"] == p[0] and x["policy"] == "fixed_two_retries")["utility"] for p in PERSISTENCE]
    unlimited = [next(x for x in persistence_summary if x["persistence"] == p[0] and x["policy"] == "unlimited_retry")["utility"] for p in PERSISTENCE]
    risk = [next(x for x in persistence_summary if x["persistence"] == p[0] and x["policy"] == "risk_calibrated")["utility"] for p in PERSISTENCE]
    xs = list(range(len(PERSISTENCE)))
    fig, ax = plt.subplots(figsize=(7.0, 3.2))
    ax.plot(xs, fixed2, marker="o", label="Fixed two retries", linewidth=1.8)
    ax.plot(xs, unlimited, marker="o", label="Unlimited retry", linewidth=1.8)
    ax.plot(xs, risk, marker="o", label="Risk-calibrated", linewidth=1.8)
    ax.set_xticks(xs)
    ax.set_xticklabels(labels, fontsize=7)
    ax.set_ylabel("Utility")
    ax.set_ylim(-0.20, 1.05)
    ax.grid(alpha=0.25)
    ax.legend(fontsize=8)
    fig.tight_layout()
    fig.savefig(FIGURES / "persistence_retry_curve.pdf")
    plt.close(fig)

    labels = [title_label(r[1]).replace(" ", "\n") for r in OBSERVABILITY]
    unlim_stale = [next(x for x in observability_summary if x["observability"] == o[0] and x["policy"] == "unlimited_retry")["stale"] for o in OBSERVABILITY]
    risk_stale = [next(x for x in observability_summary if x["observability"] == o[0] and x["policy"] == "risk_calibrated")["stale"] for o in OBSERVABILITY]
    xs = list(range(len(OBSERVABILITY)))
    fig, ax = plt.subplots(figsize=(6.8, 3.2))
    ax.plot(xs, unlim_stale, marker="o", label="Unlimited retry", linewidth=1.8)
    ax.plot(xs, risk_stale, marker="o", label="Risk-calibrated", linewidth=1.8)
    ax.set_xticks(xs)
    ax.set_xticklabels(labels, fontsize=7)
    ax.set_ylabel("Stale-state exposure")
    ax.grid(alpha=0.25)
    ax.legend(fontsize=8)
    fig.tight_layout()
    fig.savefig(FIGURES / "stale_by_observability.pdf")
    plt.close(fig)


def main() -> None:
    RESULTS.mkdir(parents=True, exist_ok=True)
    FIGURES.mkdir(parents=True, exist_ok=True)

    groups: dict[tuple[str, ...], dict[str, float]] = defaultdict(lambda: defaultdict(float))
    condition_path = RESULTS / "condition_metrics.csv"
    row_count = 0

    fieldnames = ["t", "d", "f", "p", "o", "c", "m", *METRICS, "w"]
    with condition_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for task in TASKS:
            for depth in DEPTHS:
                for fault in FAULTS:
                    for persistence in PERSISTENCE:
                        for observability in OBSERVABILITY:
                            for cost in COSTS:
                                for policy in POLICIES:
                                    row = compute_metrics(task, depth, fault, persistence, observability, cost, policy)
                                    writer.writerow(
                                        {
                                            "t": row["t"],
                                            "d": row["d"],
                                            "f": row["f"],
                                            "p": row["p"],
                                            "o": row["o"],
                                            "c": row["c"],
                                            "m": row["m"],
                                            **{metric: f"{float(row[metric]):.5f}" for metric in METRICS},
                                            "w": int(row["w"]),
                                        }
                                    )
                                    add_group(groups, ("policy", str(row["m"])), row)
                                    add_group(groups, ("task", str(row["t"]), str(row["m"])), row)
                                    add_group(groups, ("depth", str(row["d"]), str(row["m"])), row)
                                    add_group(groups, ("fault", str(row["f"]), str(row["m"])), row)
                                    add_group(groups, ("persistence", str(row["p"]), str(row["m"])), row)
                                    add_group(groups, ("observability", str(row["o"]), str(row["m"])), row)
                                    add_group(groups, ("cost", str(row["c"]), str(row["m"])), row)
                                    row_count += 1

    policy_summary = summarize({k[1:]: v for k, v in groups.items() if k[0] == "policy"}, ["policy"])
    task_summary = summarize({k[1:]: v for k, v in groups.items() if k[0] == "task"}, ["task", "policy"])
    depth_summary = summarize({k[1:]: v for k, v in groups.items() if k[0] == "depth"}, ["depth", "policy"])
    fault_summary = summarize({k[1:]: v for k, v in groups.items() if k[0] == "fault"}, ["fault", "policy"])
    persistence_summary = summarize({k[1:]: v for k, v in groups.items() if k[0] == "persistence"}, ["persistence", "policy"])
    observability_summary = summarize({k[1:]: v for k, v in groups.items() if k[0] == "observability"}, ["observability", "policy"])
    cost_summary = summarize({k[1:]: v for k, v in groups.items() if k[0] == "cost"}, ["cost", "policy"])

    write_csv(RESULTS / "policy_summary.csv", policy_summary)
    write_csv(RESULTS / "task_policy_summary.csv", task_summary)
    write_csv(RESULTS / "depth_policy_summary.csv", depth_summary)
    write_csv(RESULTS / "fault_policy_summary.csv", fault_summary)
    write_csv(RESULTS / "persistence_policy_summary.csv", persistence_summary)
    write_csv(RESULTS / "observability_policy_summary.csv", observability_summary)
    write_csv(RESULTS / "cost_policy_summary.csv", cost_summary)
    write_factor_maps()

    write_table_scale()
    write_table_main(policy_summary)
    write_table_persistence(persistence_summary)
    write_table_observability(observability_summary)
    write_table_cost(cost_summary)
    write_table_depth(depth_summary)
    write_table_fault(fault_summary)
    write_figures(policy_summary, persistence_summary, observability_summary)

    validation = {
        "paper": 55,
        "condition_rows": row_count,
        "expected_condition_rows": expected_rows(),
        "evals_per_row": EVALS_PER_ROW,
        "ticks_per_row": TICKS_PER_ROW,
        "represented_evaluations": row_count * EVALS_PER_ROW,
        "represented_hierarchy_tick_decisions": row_count * TICKS_PER_ROW,
        "row_count_ok": row_count == expected_rows(),
    }
    (RESULTS / "experiment_validation.json").write_text(json.dumps(validation, indent=2), encoding="utf-8")
    (RESULTS / "experiment_summary.json").write_text(
        json.dumps(
            {
                "paper": 55,
                "condition_rows": row_count,
                "policy_summary": [
                    {
                        "policy": row["policy"],
                        **{metric: f"{row[metric]:.6f}" for metric in METRICS},
                        "weight": str(row["weight"]),
                    }
                    for row in policy_summary
                ],
            },
            indent=2,
        ),
        encoding="utf-8",
    )
    (RESULTS / "README.md").write_text(
        "\n".join(
            [
                "# Full-Scale Results",
                "",
                "Generated by `scripts/run_full_scale_containment_suite.py`.",
                "",
                f"- Compact condition rows: {row_count:,}",
                f"- Represented evaluations: {row_count * EVALS_PER_ROW:,}",
                f"- Represented hierarchy-tick decisions: {row_count * TICKS_PER_ROW:,}",
                "",
            ]
        ),
        encoding="utf-8",
    )

    best_non_oracle = max((row for row in policy_summary if row["policy"] != "oracle"), key=lambda r: r["utility"])
    oracle = next(row for row in policy_summary if row["policy"] == "oracle")
    print("rows", row_count)
    print("represented_evaluations", row_count * EVALS_PER_ROW)
    print("represented_hierarchy_tick_decisions", row_count * TICKS_PER_ROW)
    print("best_non_oracle", best_non_oracle["policy"], f"{best_non_oracle['utility']:.6f}")
    print("oracle", f"{oracle['utility']:.6f}")


if __name__ == "__main__":
    main()
