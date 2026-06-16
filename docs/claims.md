# Claims

## Supported

- Failure propagation depth is a useful metric for hierarchical robot systems.
- Local retry budgets can reduce upward propagation, but propagation alone is insufficient.
- Retry budgets must be calibrated against retry cost, escalation cost, diagnosis quality, stale-state exposure, human-proximity risk, and masked persistent-fault risk.
- In the full-scale deterministic benchmark, risk-calibrated containment is the best non-oracle policy with utility 0.547.
- The oracle remains best overall with utility 0.867, so the result is not presented as a solved safety problem.
- Unlimited retry exposes the over-containment failure: propagation 0.074, masked unsafe 0.231, stale exposure 0.333, utility -0.096.

## Not Supported

- Universal optimal containment budget.
- Deployment-ready runtime assurance.
- Real-robot safety proof.
- Monotonic claim that more local retry is always better.

## Boundary

The final contribution is a benchmark, reporting discipline, and concrete risk-calibrated containment policy for robot hierarchies. The v2 stress remains the negative control that forced this claim boundary.
