# Child Status 55

Status: workshop_only
Attempt: 3
Stage: v2_submission_hardening

Current facts:
- Literature rows: 1,102.
- Original simulation rows: 4 aggregate retry-budget settings.
- Original best v1 setting: 3 retries, success 1.000, average propagation 0.0215.
- V2 moderate persistent-fault stress: 2 retries utility 0.893, propagation 0.147, masked unsafe 0.000.
- V2 moderate persistent-fault stress: 8 retries utility 0.841, propagation 0.038, masked unsafe 0.074.
- V2 high persistent-fault stress: 2 retries utility 0.862; higher budgets are worse.
- Canonical PDF target: `C:/Users/wangz/Downloads/55.pdf`.
- Canonical PDF size: 113383 bytes.
- Local generated `main.pdf` is removed after build.
- Desktop PDF copy is absent.

Decision:
- Workshop-only. The mechanism is useful as an architectural note, but v2 shows retry budgets must be calibrated against cost and masked persistent faults.

End time: 2026-06-13 13:07:30 +01:00
