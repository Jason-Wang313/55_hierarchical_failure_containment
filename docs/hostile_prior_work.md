# Hostile Prior Work Set

This set is deliberately adversarial: if any of these papers already solves the core problem, the thesis becomes weaker.

## Core hostile set

1. `Fault Tolerance and Failure Containment`
   - Classic containment language and formal locality.
   - Hostile because it may already cover the abstract notion if mapped carefully.

2. `Probabilistic Fault-Containment`
   - Adds probabilistic containment guarantees.
   - Hostile because it could subsume a stochastic version of the thesis.

3. `Fault containment in weakly stabilizing systems`
   - Directly on containment under faults.
   - Hostile because it may provide the right formal lens.

4. `Guaranteed fault containment and local stabilization in routing`
   - Strong locality guarantee in a distributed setting.
   - Hostile because it suggests the core mechanism may already exist for generic systems.

5. `Preserving the Fault-Containment of Ring Protocols Executed on Trees`
   - Explicitly about preserving containment under hierarchy-like structure.
   - Hostile because it threatens the “hierarchy is new” angle.

6. `An exercise in fault-containment: Self-stabilizing leader election`
   - Localizing faults in a canonical distributed protocol.
   - Hostile because the containment concept is already formalized there.

7. `Fault-Tolerant Containment Control of Multiple Unmanned Aerial Vehicles Based on Distributed Sliding-Mode Observer`
   - Contains multi-robot control with containment.
   - Hostile because “containment control” in robotics is already a term of art.

8. `Fault-Tolerant Containment Control for Multi-UAV Systems Based on ADP`
   - Another direct robotics containment prior.
   - Hostile because it may already show a multi-level recovery flavor.

9. `Distributed fault-tolerant containment control for multi-UAVs with actuator and sensor faults`
   - Directly combines containment and faults.
   - Hostile because it could already address failure containment at the control layer.

10. `Automated behavior tree error recovery framework for robotic systems`
    - Behavior-tree recovery is the closest execution-level analogue.
    - Hostile because it may already implement hierarchical failure handling.

11. `A Behavior Trees and Motion Generators (BTMG) Approach`
    - Recovery skills embedded in hierarchical structure.
    - Hostile because it may already be the same pattern with different vocabulary.

12. `Runtime Verification and Field Testing for ROS-Based Robotic Systems`
    - Runtime monitoring and robotics QA.
    - Hostile because it may imply containment via monitoring plus intervention.

13. `Flexible Fault Tolerance for the Robot Operating System`
    - System-level robustness in ROS.
    - Hostile because ROS is a realistic candidate stack for the paper.

14. `AEROS: A Single-Agent Operating Architecture with Embodied ...`
    - Strong architecture for embodied modularity.
    - Hostile because it may already define the right boundaries.

15. `Federated Single-Agent Robotics: Multi-Robot Coordination Without ...`
    - Explicit layered recovery and authority delegation.
    - Hostile because it is the closest architecture-level analogue.

16. `Safe Trusted Autonomy for Responsible Space Program`
    - Runtime assurance framework in safety-critical embodied autonomy.
    - Hostile because it may already contain the boundary logic.

17. `The Semantic Hierarchy in Robot Learning`
    - Hierarchical learning as a decomposition principle.
    - Hostile because the thesis might collapse to hierarchical abstraction.

18. `Hierarchical Hybrid Learning for Long-Horizon Contact-Rich Robotic ...`
    - Hierarchical recovery in practice.
    - Hostile because it could already demonstrate the desired robustness effect.

19. `Fault identification for robot manipulators`
    - If identification is already enough in some settings, containment may be weaker as a contribution.

20. `Fault-tolerant control of a service robot`
    - Generic FTC in a realistic robot.
    - Hostile because the paper may need a stronger architectural claim than control alone.

## What would falsify novelty

The thesis would be much weaker if any hostile paper already does all three:

- defines a hierarchy with explicit escalation levels
- quantifies failure propagation across levels
- shows that level-local containment improves mission robustness without collapsing task performance

## What still seems open

- a formal notion of failure blast radius in robot hierarchies
- escalation budgets that cap upward propagation
- architectural rules that keep failures local even when tasks are hierarchical
- empirical evidence that containment boundaries matter beyond generic recovery
