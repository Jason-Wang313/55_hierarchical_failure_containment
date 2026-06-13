# Claims

## Supported

- Failure propagation depth is a useful metric for hierarchical robot systems.
- Local retry budgets can reduce upward propagation in a toy hierarchy.
- Retry budgets must be calibrated against retry cost and masked persistent-fault risk.

## Not Supported

- Universal optimal containment budget.
- Deployment-ready runtime assurance.
- Monotonic claim that more local retry is always better.

## V2 Boundary

At moderate persistent-fault rate, 2 retries are best by utility. Eight retries reduce propagation but increase masked-unsafe rate to 0.074 and lower utility.
