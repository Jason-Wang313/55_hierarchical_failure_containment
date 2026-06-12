# Novelty Decision

## Chosen thesis

**Robot hierarchies should be designed around explicit failure containment budgets so that faults are quarantined at the lowest viable level instead of propagating upward through the stack.**

## Why this thesis won

- It changes the central mechanism from “recover well” to “contain well.”
- It is robotic, not just abstract distributed systems theory.
- It creates a measurable variable: failure propagation across levels.
- It is compatible with behavior trees, modular robot runtimes, or multi-robot coordination stacks.

## What this is not

- not a bigger model
- not a better benchmark
- not generic uncertainty estimation
- not active learning
- not a verifier bolted on top
- not a planner-only paper
- not RL

## Strongest hostile challenge

The hostile challenge is that classical fault-containment theory already covers the abstract concept. The paper must therefore be about:

- the robotics-specific hierarchy
- physical execution stacks
- escalation budgets
- empirical containment effects

## Final mechanism claim

The mechanism is a **containment budget controller**:

- each level can retry locally a limited number of times
- only a bounded summary is allowed to escape upward
- after budget exhaustion, escalation occurs in a controlled way
- the design goal is not only success rate, but minimized propagation

## Why this is plausibly novel

The likely novelty is the combination of:

- explicit hierarchy-aware containment policy
- measurable propagation reduction
- robot execution stack instantiation

No single prior work in the sweep clearly owns that full triangle.
