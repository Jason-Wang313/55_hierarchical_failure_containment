# Experiment Rigor Checklist

- Original simulator settings: 4 retry budgets.
- V2 stress settings: 3 persistent-fault rates x 7 retry budgets x 5,000 episodes.
- V3 full-scale factor grid: 12 tasks x 6 depths x 6 fault classes x 6 persistence regimes x 5 observability regimes x 5 cost regimes x 8 policies.
- Compact condition rows: 518,400.
- Represented evaluations: 152,285,184,000.
- Represented hierarchy-tick decisions: 13,705,666,560,000.
- Strong baselines: immediate escalation, fixed one retry, fixed two retries, fixed four retries, unlimited retry, local exponential backoff, oracle containment.
- Full-scale metrics: success, propagation, containment, escalation, retry, latency, masked unsafe, stale exposure, precision, waste, utility.
- Real robot data: no; stated as a limitation.
- Uncertainty/error bars: no; deterministic mechanism benchmark with row-level audit artifacts.
- Decision: final v3 full-scale submission candidate.
