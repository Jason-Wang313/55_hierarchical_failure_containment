# Hierarchical Failure Containment for Robot Systems

Paper 55 in the robotics 60-paper batch.

Decision: workshop-only.

The paper argues that robot hierarchies need explicit failure-containment budgets so local faults do not automatically propagate upward into mission-level control. The v1 toy simulator showed that local retry budgets reduce upward propagation, but it made retries nearly free.

V2 hardening adds a persistent-fault and retry-cost stress:

- At persistent-fault probability 0.25, two retries have the best utility: 0.893.
- Four retries reduce propagation to 0.076 but raise masked-unsafe rate to 0.044 and utility falls to 0.870.
- Eight retries reduce propagation to 0.038 but raise masked-unsafe rate to 0.074 and utility falls to 0.841.
- At persistent-fault probability 0.45, two retries again have the best utility: 0.862.

The supported claim is conditional: containment budgets are useful, but they must be calibrated against retry cost and masked persistent-fault risk.

## Reproduction

```powershell
python scripts/sim_containment.py
python scripts/v2_persistent_fault_stress.py
powershell -ExecutionPolicy Bypass -File scripts/build_pdf.ps1
```

The canonical built PDF is `C:/Users/wangz/Downloads/55.pdf`.

Local generated PDFs are not tracked. The build script copies the generated PDF to the canonical Downloads path and removes `main.pdf`.
