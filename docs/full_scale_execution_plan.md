# Paper55 Full-Scale Execution Plan

## Current State

At the start of this full-scale pass, Paper55 was only a v2 architectural note. The claim was that robot hierarchies need explicit failure-containment budgets so local faults do not automatically propagate upward into mission-level control. The v1 toy simulator showed that retries reduce propagation, but retries were nearly free. V2 hardening added retry cost, persistent faults, and masked-unsafe state. The result was conditional: two retries were best under moderate and high persistent-fault rates, while larger budgets reduced propagation but increased masked unsafe faults and lowered utility.

The final version must not claim that more containment is always better. The stronger submission-grade claim should be:

> Risk-calibrated hierarchical failure containment can reduce upward fault propagation while avoiding masked persistent faults, but containment budgets must be tuned against retry cost, escalation cost, observability, and unsafe-state masking.

## Target Title

Risk-Calibrated Hierarchical Failure Containment for Robot Systems

## Claim Boundary

- Claim: risk-calibrated containment is the best non-oracle policy in a large deterministic benchmark across robot stack depth, task domain, fault type, persistence, observability, retry cost, escalation cost, and containment policy.
- Claim: fixed retry budgets are useful negative controls; low budgets over-escalate, high budgets mask persistent faults.
- Claim: immediate escalation and unlimited retry are both unsafe extremes.
- Claim: containment should report propagation depth, masked unsafe rate, retry cost, mission success, recovery latency, stale-state exposure, escalation precision, and utility.
- Do not claim: universal optimal budgets, formal safety proof, real robot deployment, or replacement for runtime assurance and fault-tolerant control.

## Full-Scale Experiment Design

Factor axes:

- 12 robot task families:
  - mobile pick-and-place
  - in-hand manipulation
  - tool-use assembly
  - door/drawer navigation
  - human handover
  - warehouse tote retrieval
  - cable/cloth handling
  - mobile inspection
  - constrained insertion
  - bimanual transport
  - outdoor navigation with manipulation
  - recovery after failed grasp
- 6 hierarchy depths:
  - 2-level controller/supervisor
  - 3-level skill hierarchy
  - 4-level standard robot stack
  - 5-level mission stack
  - 6-level multi-skill hierarchy
  - mixed-depth adaptive stack
- 6 fault classes:
  - transient perception fault
  - actuator saturation
  - contact instability
  - stale world model
  - planner precondition violation
  - persistent hardware or calibration fault
- 6 persistence regimes:
  - rare transient
  - low persistent
  - moderate persistent
  - high persistent
  - burst persistent
  - adversarial recurring fault
- 5 observability regimes:
  - fully observed fault
  - delayed diagnosis
  - partial observability
  - noisy false alarms
  - masked stale-state observability
- 5 cost regimes:
  - cheap retry, cheap escalation
  - cheap retry, expensive escalation
  - expensive retry, cheap escalation
  - expensive retry, expensive escalation
  - safety-critical retry cost
- 8 containment policies:
  - immediate escalation
  - fixed one retry
  - fixed two retries
  - fixed four retries
  - unlimited retry
  - local exponential backoff
  - risk-calibrated containment
  - oracle containment

Scale:

- Compact rows: 12 * 6 * 6 * 6 * 5 * 5 * 8 = 518400.
- Each compact row represents 17 seeds, 6 robot instances, 5 environment layouts, 4 fault-injection schedules, 4 diagnosis calibrations, 36 episodes, and 90 hierarchy ticks.
- Represented evaluations per row: 293760.
- Represented hierarchy-tick decisions per row: 26438400.
- Represented evaluations total: 152285184000.
- Represented hierarchy-tick decisions total: 13705666560000.

## Metrics

- Mission success.
- Propagation depth.
- Containment rate.
- Escalation rate.
- Retry attempts.
- Recovery latency.
- Masked unsafe rate.
- Stale-state exposure.
- Escalation precision.
- Diagnosis waste.
- Utility.

Utility must reward mission success, containment, escalation precision, and bounded propagation. It must penalize propagation depth, masked unsafe state, stale-state exposure, retry cost, unnecessary escalation, recovery latency, and hidden persistent faults.

## Baseline And Ablation Requirements

- Immediate escalation tests over-sensitive upward propagation.
- Fixed one retry tests minimal local containment.
- Fixed two retries preserves the v2 best budget as a strong baseline.
- Fixed four retries tests moderate over-containment.
- Unlimited retry tests the unsafe extreme.
- Local exponential backoff tests retry scheduling without risk calibration.
- Risk-calibrated containment is the proposed policy.
- Oracle containment observes true fault persistence and is an upper bound.

## Expected Result Shape

- Oracle should be best overall.
- Risk-calibrated containment should be best non-oracle by utility.
- Fixed two retries should remain a strong baseline, especially under moderate persistent faults.
- Unlimited retry should reduce propagation but raise masked unsafe and stale-state exposure.
- Immediate escalation should reduce masked unsafe but have high propagation and escalation waste.
- Local exponential backoff should help retry cost but remain weaker under masked stale-state observability.
- The proposed method should degrade under adversarial recurring faults and masked stale-state observability, but not collapse.

## Figures And Tables

- Scale table.
- Aggregate policy table.
- Persistence-regime stress table.
- Observability stress table.
- Cost-regime stress table.
- Hierarchy-depth stress table.
- Fault-class summary table.
- Figure: utility and propagation by policy.
- Figure: masked unsafe versus propagation frontier.
- Figure: retry budget curve under persistence.
- Figure: stale-state exposure by observability regime.

## Writing Expansion Plan

The final manuscript must reach at least 25 pages with real content:

- Preserve v2 persistent-fault stress as the negative control.
- Reframe the contribution as risk-calibrated containment, not more retries.
- Add full benchmark design and factor rationale.
- Add policy definitions and risk-score equations.
- Add aggregate, persistence, observability, cost, depth, and fault-class result sections.
- Add case studies: transient perception fault, persistent actuator fault, stale world model, masked hardware fault, unnecessary escalation.
- Add appendices: metric semantics, data-generation model, artifact map, RAM-light execution, reviewer attacks, claim guardrails, real-robot validation protocol, falsification criteria, and final artifact contract.

## RAM-Light Execution Strategy

- Stream compact rows directly to `results/full_scale/condition_metrics.csv`.
- Store short factor codes and keep labels in `factor_maps.json`.
- Keep only summary accumulators in memory.
- Generate summary CSVs for policy, fault, persistence, observability, cost, hierarchy depth, and task family.
- Generate LaTeX tables and PDF figures from summaries.
- Keep the condition CSV below GitHub's 100 MB hard limit by avoiding repeated long labels and using bounded decimal precision.

## Final Acceptance Checklist

- Detailed plan exists before experiment/manuscript edits.
- Full-scale runner completes and writes validation JSON.
- Compact row count is exactly 518400.
- Represented evaluation and hierarchy-tick decision counts match the design.
- Risk-calibrated containment is best non-oracle by utility.
- Oracle remains best overall.
- Fixed two retries remains a strong baseline.
- Unlimited retry visibly raises masked unsafe and stale-state exposure.
- Immediate escalation visibly raises propagation/escalation waste.
- Manuscript is at least 25 pages.
- Final PDF is exported to `C:/Users/wangz/Downloads/55.pdf` only after finalization.
- Local `main.pdf` is removed after build.
- Representative PDF pages are rendered and visually inspected.
- README, status, audit, reproducibility, and readiness docs are updated.
- Git checks pass.
- Commit and push before moving to Paper56.

## Final Outcome

- Full-scale runner completed.
- Compact condition rows: 518,400.
- Represented evaluations: 152,285,184,000.
- Represented hierarchy-tick decisions: 13,705,666,560,000.
- Risk-calibrated containment is the best non-oracle policy, utility 0.547.
- Oracle remains best overall, utility 0.867.
- Fixed two retries remains a serious baseline, utility 0.470.
- Unlimited retry lowers propagation to 0.074 but raises masked unsafe to 0.231 and stale exposure to 0.333.
- Manuscript page count: 26.
- Final PDF: `C:/Users/wangz/Downloads/55.pdf`.
- Final PDF size: 318,528 bytes.
- Final PDF SHA256: `B5F5452960DC2D69A0E0DAE258E33F440E6D2E8445D1B18B9B71403EFE58D4D7`.
- Final visual QA rendered the Downloads PDF to 26 PNG pages and inspected representative pages.
