# Claims

## Main claim

Robot hierarchies become more robust when failure handling is treated as a containment problem, not just a recovery problem.

## Supporting claims

1. Failure propagation across levels is a measurable quantity and should be minimized.
2. Local retries alone can reduce upward propagation, but uncontrolled retries are not the key idea.
3. Explicit escalation budgets provide a better design handle than ad hoc recovery branching.
4. The correct unit of design is the hierarchy boundary, not only the controller or the classifier.
5. In a hierarchical execution stack, containing a failure early is different from eventually repairing it.

## What we can support now

- A toy simulator shows that increasing local retry budget reduces average propagation.
- The literature sweep shows many papers on diagnosis, recovery, containment control, and runtime assurance, but no clear robotics paper centered on containment budgets across hierarchy levels.

## What remains unproven

- that the exact containment policy here is optimal
- that the toy simulator predicts real robot performance quantitatively
- that every robot stack should use the same containment policy

## Honest framing

This should be framed as a systems/architecture paper with a concrete mechanism and adversarially checked empirical evidence, not as a universal theorem about all robot hierarchies.
