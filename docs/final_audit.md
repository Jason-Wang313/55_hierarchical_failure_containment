# Final Audit

Paper-readiness judgment: workshop-only.

## Original Thesis

Robot hierarchies should treat failure propagation as a measurable design variable and use containment budgets to limit upward fault spread.

## V1 Evidence

- Literature rows: 1,102.
- Simulation rows: 4 aggregate retry-budget settings.
- Best v1 toy setting: 3 retries, success rate 1.000, average propagation 0.0215, average contained 0.5855.

## V2 Persistent-Fault Stress

- Persistent-fault probability 0.25: 2 retries utility 0.893, success 0.935, propagation 0.147, masked unsafe 0.000.
- Persistent-fault probability 0.25: 4 retries utility 0.870, propagation 0.076, masked unsafe 0.044.
- Persistent-fault probability 0.25: 8 retries utility 0.841, propagation 0.038, masked unsafe 0.074.
- Persistent-fault probability 0.45: 2 retries utility 0.862; 8 retries utility 0.733.

## Decision

Workshop-only. The mechanism is useful, but the evidence is a toy simulator and v2 shows more containment is not always better. The manuscript must frame containment budgets as calibrated policies with escalation costs and masked-fault audits.

## Artifact Policy

- Canonical PDF: `C:/Users/wangz/Downloads/55.pdf`
- Local tracked/generated PDF policy: `main.pdf` is ignored and removed after build.
- Desktop copy: absent.
