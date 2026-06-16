# Final Audit

Paper-readiness judgment: final v3 full-scale submission candidate.

## Final Thesis

Robot hierarchies should treat failure propagation as a measurable design variable and use risk-calibrated containment budgets to limit upward fault spread without hiding persistent unsafe state.

## Evidence

- Literature rows: 1,102.
- V2 negative control: high retry budgets reduce propagation but can increase masked unsafe state and lower utility.
- Full-scale compact condition rows: 518,400.
- Represented evaluations: 152,285,184,000.
- Represented hierarchy-tick decisions: 13,705,666,560,000.
- Risk-calibrated containment: utility 0.547, success 0.710, propagation 0.255, masked unsafe 0.043, stale exposure 0.082.
- Oracle containment: utility 0.867.
- Fixed two retries: utility 0.470.
- Unlimited retry: propagation 0.074, masked unsafe 0.231, stale exposure 0.333, utility -0.096.

## Decision

Final v3 full-scale submission candidate. The paper does not claim real-robot deployment safety or universal optimality. It claims a deterministic benchmark and reporting discipline showing that containment budgets must be calibrated against persistence, stale state, diagnosis quality, and cost.

## Artifact Policy

- Canonical PDF: `C:/Users/wangz/Downloads/55.pdf`
- Pages: 26
- Size: 318,528 bytes
- SHA256: `B5F5452960DC2D69A0E0DAE258E33F440E6D2E8445D1B18B9B71403EFE58D4D7`
- Local tracked/generated PDF policy: `main.pdf` is ignored and removed after build.
- Desktop copy: absent.
- Visual QA: rendered the Downloads PDF to 26 PNG pages and inspected representative pages.
