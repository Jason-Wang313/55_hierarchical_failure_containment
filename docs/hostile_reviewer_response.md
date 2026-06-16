# Hostile Reviewer Response

The strongest criticism of the original draft was correct: the first simulator made local retry too cheap, so the result looked monotone. V2 hardening showed that high retry budgets can reduce propagation while hiding persistent unsafe faults.

The final v3 manuscript turns that failure into the central claim boundary. It evaluates risk-calibrated containment against immediate escalation, fixed retry budgets, unlimited retry, local backoff, and an oracle ceiling. Risk-calibrated containment is the best non-oracle policy in the deterministic full-scale benchmark, while unlimited retry exposes the masking failure.

The paper still does not claim deployment safety. It claims a benchmark, reporting discipline, and policy mechanism that must be validated on real robot hierarchy logs.
