# Novelty Boundary Map

## Things the literature already does

- hierarchical task decomposition
- robot fault detection and isolation
- fault-tolerant control
- runtime safety filtering
- behavior-tree recovery
- multi-robot containment control
- modular embodied capability design
- self-stabilizing locality guarantees in distributed systems

## Things the literature usually does not do together

1. Treat hierarchy as a **containment graph**, not just a decomposition graph.
2. Measure failure propagation across levels as a first-class metric.
3. Design escalation boundaries before choosing recovery skills.
4. Limit upward failure flow with explicit budgets.
5. Separate local faults from supervisory faults in a robot stack.
6. Show how containment affects mission-level blast radius.
7. Compare “recover locally” against “escalate early” as design choices.
8. Study containment in physically grounded execution stacks rather than only graph protocols.

## Hidden assumptions worth breaking

1. Hierarchy only helps organization, not robustness.
2. Higher layers can safely see every lower-level failure.
3. Local recovery is always cheaper than escalation.
4. Any failure should be bubbled up until something works.
5. Diagnosis and containment are interchangeable.
6. The robot stack is modular enough that boundaries are obvious.
7. Recovery policies do not interfere with nominal performance.
8. The environment does not react adversarially to repeated retries.
9. Sensor failures are independent of planning failures.
10. Actuator faults do not poison supervisory state.
11. One failed skill does not corrupt the task model.
12. One robot’s failure does not propagate to peers.
13. Monitoring overhead is negligible.
14. Escalation latency is unimportant.
15. Containment can be judged only after failure occurs.
16. A single safety filter can protect all levels.
17. Containment at the control level implies containment at the system level.
18. Hierarchies are static.
19. The best recovery path is the deepest path that eventually succeeds.
20. The cost of false escalation is smaller than the cost of missed containment.

## Proposed paper directions that break assumptions

### Direction A: Containment budgets for behavior trees

- Each subtree gets a bounded retry/escalation budget.
- The parent only sees summarized failure classes.
- The system measures blast radius and escalation cost.

### Direction B: Fault containment domains for embodied capability modules

- Capabilities are grouped into domains with explicit failure quarantine rules.
- Cross-domain calls are restricted after local anomaly detection.
- Evaluation focuses on limiting corruption spread.

### Direction C: Multi-robot containment with local quarantine

- A failing robot is quarantined at the coordination layer.
- Peer robots stop inheriting its uncertainty and stale state.
- Mission recovery is measured by containment time and mission degradation.

## Strongest direction

**Direction A** is strongest because it:

- can be tested in a robot execution stack
- makes the novel mechanism explicit
- maps naturally to BTs, runtime monitors, or modular planners
- is more than “add a monitor” because the central object is the containment budget

## Current novelty boundary

This paper is novel only if the central contribution is:

- a new containment policy that limits failure propagation across hierarchy levels
- plus evidence that the policy changes behavior in a measurable way

It is not novel enough if it only adds:

- another recovery branch
- a generic monitor
- a better classifier
- a larger model
- more data
