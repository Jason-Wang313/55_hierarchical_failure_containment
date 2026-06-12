# Final Audit

- Paper number: 55
- Slug: hierarchical_failure_containment
- Recovery reason: runner attempts produced a local manuscript/PDF, but BibTeX exited nonzero because the bibliography database was present without citation commands.
- Fix applied: added `\nocite{*}` to `main.tex` and rebuilt with `pdflatex`, `bibtex`, `pdflatex`, `pdflatex`.
- Literature rows: 1,102
- Simulation rows: 4 aggregate retry-budget settings
- Best containment setting in the toy simulation: 3 retries, success rate 1.000, average propagation 0.0215, average contained 0.5855
- Final PDF: `main.pdf`, 4 pages, 111545 bytes
- Output target: `C:/Users/wangz/Downloads/55.pdf`

The evidence is a mechanism-level toy simulation plus a literature/novelty map. It should be read as an architectural note, not a deployment evaluation.
