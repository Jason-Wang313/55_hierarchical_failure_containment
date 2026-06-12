# Literature Map

## Field box

The closest useful field box is not “fault tolerance” in the abstract. It is:

**robot systems whose execution stack is hierarchical, but whose failure handling is not explicitly bounded by level-specific containment rules.**

That includes:

- behavior trees and hierarchical task graphs
- runtime assurance and safety shields
- multi-robot containment / formation control
- fault diagnosis and fault-tolerant control for robots
- modular and reconfigurable robot architectures
- self-stabilizing / fault-containment theory that can transfer to robotics

The key gap is that most work makes one of two bets:

1. local recovery is enough if the lower layer is robust enough
2. the supervisory layer can observe and repair failures after they surface

Neither bet explicitly designs for **failure propagation across hierarchy levels**.

## Landscape clusters

### 1. Classical fault containment theory

Representative prior work:

- `Fault Tolerance and Failure Containment`
- `Probabilistic Fault-Containment`
- `Fault containment in weakly stabilizing systems`
- `An exercise in fault-containment: Self-stabilizing leader election`
- `Guaranteed fault containment and local stabilization in routing`
- `Preserving the Fault-Containment of Ring Protocols Executed on Trees`

What these papers contribute:

- formalize containment domains or containment time
- prove that faults remain localized under specific protocol assumptions
- show locality is achievable when state, topology, and update rules are tightly constrained

What they assume:

- faults are discrete and often message/state-local
- the protocol structure is fixed
- the environment is abstracted away
- the system boundary is cleanly defined

Why this matters for robotics:

- robot systems are physical, hybrid, and often partially observed
- failure can propagate through perception, planning, control, and coordination layers
- containment is not just a graph-theoretic property; it is a scheduling and authority property

### 2. Robot fault diagnosis and fault-tolerant control

Representative prior work:

- `Robust Fault Detection and Isolation in Mobile Robot`
- `Supervisory Fault Adaptive Control of a Mobile Robot and Its Application in Sensor-Fault Accommodation`
- `Fault diagnosis and fault tolerant control of mobile robot based on neural networks`
- `Active fault-tolerant control for two-wheeled differential drive mobile robot based on fault compensation method`
- `Fault identification for robot manipulators`
- `Fault-tolerant control of a service robot`
- `A Robot Fault-Tolerance Approach Based on Fault Type`

What these papers contribute:

- detect, estimate, or compensate specific faults
- adapt control laws after faults are inferred
- treat the robot as the main containment unit

What they usually assume:

- fault classes are known or enumerable
- the controller can compensate once the fault is identified
- the rest of the stack remains reliable enough to keep operating

What they leave open:

- how a fault in one layer should be prevented from corrupting higher-level decisions
- how one failed subsystem should avoid triggering brittle global fallback behavior

### 3. Multi-robot containment and formation control

Representative prior work:

- `APPLICATION OF DISTRIBUTED CONTAINMENT CONTROL TO MULTI-ROBOT SYSTEMS`
- `Multi-Robot Containment and Disablement`
- `Fault-Tolerant Containment Control of Multiple Unmanned Aerial Vehicles Based on Distributed Sliding-Mode Observer`
- `Fault-Tolerant Containment Control for Multi-UAV Systems Based on ADP`
- `Distributed fault-tolerant containment control for multi-UAVs with actuator and sensor faults`
- `Fault-tolerant Containment Control Under Denial-of-Service Attacks`

What these papers contribute:

- containment in the control-theoretic sense
- leader-follower or target-set convergence
- resilience to certain actuator/sensor failures

What they assume:

- containment targets are defined at one level
- failures affect dynamics, not the supervisory architecture itself
- the control law remains the main artifact

Why they are not enough:

- they do not address hierarchical recovery boundaries
- they rarely study failure propagation from sensing to planning to execution orchestration

### 4. Behavior trees, runtime assurance, and execution monitoring

Representative prior work:

- `Automated behavior tree error recovery framework for robotic systems`
- `Behavior Trees in Industrial Applications: A Case Study`
- `A Behavior Trees and Motion Generators (BTMG) Approach`
- `Runtime Verification and Field Testing for ROS-Based Robotic Systems`
- `Safe Trusted Autonomy for Responsible Space Program`
- `Safe, Task-Consistent Manipulation with Operational Space Control ...`
- `Flexible Fault Tolerance for the Robot Operating System`

What these papers contribute:

- hierarchical execution abstraction
- recovery branches and monitoring hooks
- runtime safety / constraint enforcement

What they assume:

- recovery can be decided at the level that notices the failure
- execution hierarchy and authority hierarchy are aligned
- the cost of escalation is not a first-class design objective

What is missing:

- explicit containment between levels, with rules about when failures may not propagate upward
- a model of escalation as a controlled resource rather than a generic fallback

### 5. Hierarchical robot learning and modular architectures

Representative prior work:

- `The Semantic Hierarchy in Robot Learning`
- `Hierarchical Hybrid Learning for Long-Horizon Contact-Rich Robotic ...`
- `AEROS: A Single-Agent Operating Architecture with Embodied ...`
- `Federated Single-Agent Robotics: Multi-Robot Coordination Without ...`
- `Discovering and exploiting the task hierarchy to learn sequences of motor policies ...`

What these papers contribute:

- layered skill decomposition
- modular embodied capability design
- separation between persistent agent and executable capabilities

What they assume:

- hierarchy primarily helps composition and generalization
- failure handling is secondary or local
- the stack is meaningful as a decomposition, not as a containment boundary

## Strongest directional takeaway

The strongest thesis space is:

**designing robot hierarchies so that failures are contained by construction, using explicit containment boundaries and escalation budgets between levels.**

This is different from:

- better diagnosis
- better recovery skills
- better safety filters
- better hierarchical planning

The new center is **containment policy across levels**.

## Candidate thesis options considered

1. Fault containment domains for robot hierarchies.
2. Containment-budgeted escalation in behavior trees and modular stacks.
3. Multi-robot failure isolation through layered authority boundaries.
4. Hierarchical runtime assurance with bounded blast radius.

The strongest option is #2, because it can:

- connect control, planning, and runtime monitoring
- be evaluated in a concrete robot execution stack
- make failure propagation a measurable variable

## Short list of important prior work to carry into the paper

- classical containment theory for the formal vocabulary
- robot fault diagnosis / FTC for the robotics baseline
- behavior trees and runtime assurance for the execution-stack baseline
- multi-robot containment control for the overload term “containment”
- AEROS / federated single-agent robotics for the architectural counterpoint
