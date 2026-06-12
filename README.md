# Hierarchical Failure Containment for Robot Systems

Paper 55 in the robotics 60-paper batch.

This paper argues that robot hierarchies need explicit failure-containment budgets so local faults do not automatically propagate upward into mission-level control. The recovered build preserves the autonomous runner's literature sweep, novelty boundary notes, simulation, and ICLR-style manuscript.

Key artifacts:

- `docs/related_work_matrix.csv`: 1,102 literature-sweep rows.
- `docs/containment_sim_results.csv`: toy containment-budget simulator results.
- `scripts/sim_containment.py`: reproducible simulation script.
- `main.tex` and `main.pdf`: final manuscript.
- `docs/final_audit.md`: recovery and artifact audit.

Recovery note: the runner built a PDF but failed at BibTeX because no citations were requested from `references.bib`. The source now includes `\nocite{*}` and rebuilds cleanly.
