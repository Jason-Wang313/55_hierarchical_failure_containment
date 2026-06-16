# Submission Attack Log

## Attack: retries are free in the original simulator

Result: Sustained. V2 adds retry attempts to utility and includes persistent faults.

Decision impact: narrow to calibrated containment budgets.

## Attack: local containment can mask persistent faults

Result: Sustained. V2 and v3 both show that high retry can hide unsafe persistent state.

Decision impact: make masked unsafe state and stale exposure primary metrics.

## Attack: toy simulation is not a robot evaluation

Result: Partly sustained. V3 broadens to a full-scale deterministic mechanism benchmark but still does not claim real-robot deployment safety.

Decision impact: final manuscript is submission-ready as a benchmark/reporting paper, with real robot validation listed as future work.
