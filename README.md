# Risk-Calibrated Hierarchical Failure Containment for Robot Systems

Paper 55 in the robotics 60-paper batch.

Decision: final v3 full-scale submission candidate.

The paper argues that robot hierarchies need explicit failure-containment budgets, but those budgets must be calibrated against persistent-fault risk, stale-state exposure, retry cost, escalation cost, diagnosis quality, and human-proximity risk. The v2 persistent-fault stress is preserved as a negative control: more retry can reduce propagation while increasing masked unsafe state.

## Final Result

- Compact condition rows: 518,400.
- Represented evaluations: 152,285,184,000.
- Represented hierarchy-tick decisions: 13,705,666,560,000.
- Best non-oracle policy: risk-calibrated containment, utility 0.547.
- Oracle utility: 0.867.
- Fixed two retries utility: 0.470.
- Unlimited retry: propagation 0.074, masked unsafe 0.231, stale exposure 0.333, utility -0.096.

## Canonical PDF

- Path: `C:/Users/wangz/Downloads/55.pdf`
- Pages: 26
- Size: 318,528 bytes
- SHA256: `B5F5452960DC2D69A0E0DAE258E33F440E6D2E8445D1B18B9B71403EFE58D4D7`
- Local `main.pdf` is removed after build.
- Desktop PDF copy is absent.

## Reproduction

```powershell
python scripts/run_full_scale_containment_suite.py
python scripts/generate_appendix_tables.py
powershell -ExecutionPolicy Bypass -File scripts/build_pdf.ps1
```

The build script enforces at least 25 pages, records page count/hash metadata, copies the final PDF to Downloads, and removes local `main.pdf`.
