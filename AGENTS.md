# Academic homepage maintenance

- Read README.md and site_config.json before editing. Preserve the selected academic-homepage layout2.
- User: 陈辰 / Chen Chen, Peking University 第一临床医学院 direct PhD student.
- Only public email: chenc2025@stu.pku.edu.cn. Do not add former homepages, former emails, student ID, course reports, or private research data.
- Edit build.py and sources/, then run python3 build.py. docs/ is generated and is the GitHub Pages publication root.
- No package installation is needed. Keep .nojekyll. Respect the project subpath from site_config.json, including 404 links.
- Preserve Paper, DOI, BibTeX and the local TeX SVG for L_{0/1}. Keep author order; use # only for sourced corresponding authors.
- Reviewer publishers: Nature Portfolio, Elsevier, Springer Nature, Frontiers; journals alphabetical within each group. Show journal/publisher/2025 JIF only.
- Undergraduate interests: Machine Learning, Pattern Recognition, Optimization; methods Multi-view Learning, Support Vector Machines. PhD focus Spatial Transcriptomics Algorithm Design; interests Computational Pathology, Bioinformatics.
- Pair each Chinese keyword with its own English parentheses. Keyword links use the concept resources in profile.json, including Multi-view Learning, Support Vector Machines and Safe Screening, not Scholar author-label searches. Advisor 薛瑞栋研究员 links to his official PKU profile; homepage bio ends with 欢迎交流！. News descriptions end with a Chinese full stop before the [Paper] link.
- Bold Chinese research keywords and journal names in the homepage bio; English explanations use regular weight and muted gray. Keep each Chinese/English pair in its own parentheses, use neutral gray links with subtle underlines in prose, and keep the three research stages visually separated with a readable text width. Home selected publications include the forest biomass paper (10.1016/j.compag.2025.110020), not the wind forecasting paper; retain all seven papers in Publications. The hybrid truncated loss SVM paper (10.1016/j.eswa.2026.134683) is first in the five homepage selections and October 2026 News; display its verified online date and omit an unavailable volume. Keep the Blue Envelope interview under Experience / Service; do not restore the removed paragraph beginning 希望将此前在多视图学习与最优化方面.
- Dates use English month abbreviations, italic, aligned right; known periods are in profile.json and awards.json.
- Do not invent projects, individual contributions, awards, impact factors, or publication status.
- Before publishing, check desktop/mobile layout, navigation, local assets and year filtering. Reuse the existing GitHub repository; do not create another hosting account or Site.
- Keep documentation consistent with actual publication status. No credentials or authentication tokens belong in the repository.

- Full-paragraph paper descriptions end with a Chinese full stop. Award titles omit the freshman scholarship academic-year prefix and the Beijing mathematics competition subnote; keep their right-aligned award dates.
