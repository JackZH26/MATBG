# Literature Matrix

状态：checked and expanded through 2026-06-09; repeat before actual submission.

| Group | Reference | Model / System | Interband Pairing? | Stiffness Output? | Decomposition? | Observable Link | Use in This Project |
|---|---|---|---|---|---|---|---|
| Flat-band geometry | Peotta and Törmä, Nat. Commun. 2015 | Generic flat-band superconductivity | Not primary | Yes | Geometry bound | Indirect | Establish quantum metric lower-bound logic |
| Multiband geometry | Hu, Hyart, Pikulin, Rossi, PRL 2019 | Multiband superconductivity | Yes | Yes | Yes | Indirect | Support multiband/interband response formalism |
| Multiband geometry | Julku et al., PRB 2020 | Multiband flat-band superconductivity | Yes | Yes | Yes | Indirect | Cross-check decomposition language |
| MATBG topology | Xie, Song, Lian, Bernevig, PRL 2020 | MATBG fragile topology | Not central | Yes | Geometry bound | Indirect | Justify protected geometric contribution |
| Review | Törmä, Peotta, Bernevig, Nat. Rev. Phys. 2022 | Quantum geometry review | Discussed | Yes | Conceptual | Indirect | Literature framing |
| BM model | Bistritzer and MacDonald, PNAS 2011 | MATBG continuum model | No | No | No | No | Normal-state model foundation |
| Relaxation model | Nam and Koshino, PRB 2017 | Relaxed MATBG continuum/lattice | No | No | No | No | Parameter comparison |
| Tight-binding MATBG | Koshino et al., PRX 2018 | MATBG effective model | Pairing not primary | No | No | No | UV-complete future-work comparison |
| Experiment | Cao et al., Nature 2018 superconductivity | MATBG | No | Indirect | No | Yes | Superconducting dome context |
| Experiment | Cao et al., Nature 2018 insulator | MATBG | No | No | No | Yes | Correlated-state context |
| Experiment | Yankowitz et al., Science 2019 | MATBG | No | Indirect | No | Yes | Tuning and phase diagram context |
| Experiment | Oh et al., Nature 2021 | MATBG spectroscopy | No | Gap-related | No | Yes | Gap scale and doping context |
| Experiment | Tian et al., Nature 2023 | MATBG cQED stiffness | No | Yes | No | Yes | Direct stiffness comparison |
| Experiment | Tanaka et al., Nature 2025 | MATBG transport and microwave stiffness | No | Yes | No | Yes | Latest direct stiffness context and temperature-dependence constraint |
| Experiment | Portoles et al., Nat. Commun. 2025 | MATBG RF Josephson-junction dynamics | No | Yes | Phenomenological dynamics | Yes | Independent stiffness/condensate-dynamics context and anisotropic/nodal-gap motivation |
| Experiment | Banerjee et al., Nature 2025 | Twisted trilayer graphene stiffness | No | Yes | No | Yes | Broader magic-angle graphene nodal-gap stiffness context; not a MATBG input |
| Experiment | Park et al., Science 2025 | Magic-angle graphene tunneling plus transport | No | Gap spectroscopy | No | Yes | Nodal-gap and pseudogap motivation for tunneling/stiffness comparison; not used as direct MATBG stiffness calibration |
| Experiment | Kim et al., Nature 2026 | Magic-angle twisted trilayer STM/STS | No | Gap spectroscopy | No | Yes | Intervalley/coexisting-gap motivation for future valley-resolved extensions |
| Experiment / mechanism | Gao et al., Nat. Phys. 2026 | tBLG dielectric-environment tuning | Pairing mechanism constraint | Indirect | No | Yes | Supports conservative statement that microscopic pairing glue is unsettled |
| Interaction correction | Herzog-Arbeitman et al., PRL 2022 | Interaction-renormalized geometry | No | Related | Conceptual | Indirect | Explain remaining enhancement beyond mean field |
| Vertex/strong coupling | Verma, Hazra, Randeria, PNAS 2021 | Flat-band superfluid stiffness | Not central | Yes | Related | Indirect | Discussion of beyond-BCS effects |
| Pairing symmetry | Isobe, Yuan, Fu, PRX 2018 | MATBG pairing mechanisms | Candidate symmetries | No | No | Indirect | Candidate pairing comparison |
| Band-off-diagonal pairing | Christos, Sachdev, Scheurer, Nat. Commun. 2023 | Twisted graphene superlattices | Yes | Spectral consequences | Symmetry classification | Tunneling/gap structure | Direct predecessor; cite as microscopic motivation |
| Band-off-diagonal stiffness | Putzer and Scheurer, PRB 2025 | Twisted graphene | Yes | Yes | Eliashberg/multiband/geometry | Stiffness measurements | Direct predecessor; distinguish present orbital-projected response diagnostic |
| Finite-momentum pairing | Wang and Levin, arXiv 2026 | Kekule PDW superconductivity in magic-angle bilayer graphene | Yes, finite momentum | BKT/gap context | No | Tunneling/gap structure | Direct boundary of current uniform-pairing ansatz |
| Recent theory | Wang, Chen, Boyack, Levin, arXiv 2026 | Kekule / PDW superconductivity in twisted graphene | Yes, finite momentum | Yes | Geometric stiffness | Yes | Boundary of current uniform-pairing framework; future finite-momentum BdG extension |
| Prior internal baseline | Zhou, arXiv 2026 | MATBG band-basis superfluid-weight decomposition | No | Yes | Conventional/geometric/cross | Indirect | Source of prior benchmark table; cite only for provenance/self-audit |

Removed placeholder:
`Lamponen et al., PRB 2025` was searched but no matching primary source was
identified for the interband-pairing/stiffness context. It should not be cited
unless a concrete DOI or arXiv record is found later.

## Gap Statement Draft

Existing work establishes that quantum geometry contributes to superfluid stiffness in flat-band and MATBG settings. What remains underdeveloped is an observable-driven comparison of intra- and interband pairing signatures in a unified BM BdG response framework, with total stiffness and anisotropy treated as primary outputs and conventional/geometric/cross decomposition used as secondary explanation.

## Expansion Tasks

1. Bibliographic information for active manuscript rows was checked against
   primary arXiv, Nature, Science, APS, or journal pages on 2026-06-09.
2. 2024-2026 literature on stiffness, tunneling/nodal gaps, and
   band-off-diagonal/Kekule pairing was swept on 2026-06-09. Repeat immediately
   before actual PRB submission.
3. Add columns for equations used, numerical parameters, and limitations if the
   literature matrix is promoted into Supplemental Material.
4. Current placement: stiffness and nodal-gap experiments belong in the
   Introduction/Discussion; Christos-Putzer-Wang finite-momentum theory belongs
   in the limitation/future-extension discussion; the Zhou 2026 decomposition
   entry belongs only to benchmark provenance.
