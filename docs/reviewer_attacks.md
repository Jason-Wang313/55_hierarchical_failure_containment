# Reviewer Attacks

## Attack 1: This is just fault tolerance under a new name

Response:

- The paper is not about a better detector or compensator.
- The contribution is the containment policy across hierarchy levels.
- The evaluation should measure propagation, not just task success.

## Attack 2: Classical fault-containment theory already solved this

Response:

- Classical theory gives vocabulary and some formal locality results.
- The paper is robotics-specific: physical execution stacks, escalation budgets, and hierarchical control/runtime boundaries.
- The novelty is in instantiating containment as a design mechanism for robot hierarchies.

## Attack 3: This is just behavior trees with retries

Response:

- Behavior trees are an implementation substrate, not the thesis.
- The thesis is that retries must be budgeted and contained, not merely added.

## Attack 4: The toy simulation is too simple

Response:

- Agreed.
- It is only evidence of directional effect, not a full benchmark replacement.
- A more complete revision would need robot-stack or system-level validation.

## Attack 5: The failure propagation metric is invented

Response:

- Yes, and that is intentional.
- The paper should define and justify it carefully as the central outcome variable.

## Attack 6: The hierarchy itself may create brittleness

Response:

- That is a real limitation.
- The paper should admit that containment budgets help only when the hierarchy is already meaningful and the boundary design is good.

## Attack 7: The work is not enough for a strong conference submission

Response:

- That is plausible.
- The likely target is workshop or revise unless the final implementation and evaluation become much stronger than the toy result currently is.
