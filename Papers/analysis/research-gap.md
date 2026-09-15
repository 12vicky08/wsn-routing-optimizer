# Research Gaps — Contribution Statement Basis

Derived from `literature-matrix.md` (18 substantively-mined WSN papers + base paper) and cross-checked against what our own results (`our-results.md`) can currently support. Ranked by how well our available evidence backs each gap — **not** by how interesting the gap is in the abstract. Per instructions, this must not overclaim beyond what our figures show, so gap #4 and #5 are marked weakly-supported pending the answers requested in `data-gaps.md`.

## Gap 1 — Kinematic/physical feasibility of mobile-sink trajectories is almost universally ignored (STRONGLY addressed by our approach's design, not yet by our figures)

Across the 18 mined papers, every mobile-sink trajectory method (Hamidouche MSSA, Khalily-Dermany OP_Sink/MA_Sink, Mohan MFO-MS, Sangeetha ExAq-MSPP, base paper's LP/CS) treats the sink as a point that can move between sojourn/rendezvous points with no modeled turning radius, velocity limit, or path curvature constraint. None of the 18 papers' energy/path models account for kinematic feasibility. Our draft (`Paper.txt`, Section 3.3–4.1) explicitly models the sink as a non-holonomic vehicle with a turning-radius constraint and uses spline-based (Catmull-Rom/Bezier) smoothing over control points — this is a genuine, literature-supported gap. **However**, the only figure that would evidence this (turning-angle results) is currently missing from the folder (see data-gaps.md #2) — the claim exists in the draft's Conclusion but is unsupported by any plotted data right now. This gap is strong on the *methods* side but currently unsupported on the *results* side.

## Gap 2 — Adaptive/self-resetting diversity mechanisms in GA-based WSN optimization are rare (MODERATELY addressed, mechanism-level not figure-level)

Of the GA-based papers in the matrix, most use static or simply-adaptive crossover/mutation (Wireless.pdf, ijrte TABU-GA, CDARGA) or hybridize with a second metaheuristic for local refinement (Mottaki GA-TS, Sun GARWOA, Alnajjar). None implement an explicit "detect stagnation → cull → regenerate" restart mechanism analogous to the draft's "Cataclysm" operator (Section 4.4). This is a real methodological point of difference. No figure in the current image set directly evidences convergence/diversity behavior over generations (as opposed to over simulation rounds) — this gap is supportable in the Methodology section's algorithmic description but not currently demonstrable with a results figure.

## Gap 3 — ns-3 as the simulation platform is essentially unused in this literature corpus (methodologically supported, low narrative weight)

Simulators used across the 18 papers: NS2 (5), MATLAB (6), OMNeT++ (2), WSNSimPy (1), custom/unspecified (4). Zero use ns-3. Our use of ns-3 (version to be confirmed, see data-gaps.md #6) is a genuine methodological differentiator, but by itself this is a weak contribution claim — it should be mentioned as a strength (reproducibility, active maintenance, realistic MAC/PHY fidelity per IEEE 802.15.4) rather than headlined as a research gap.

## Gap 4 — Multi-objective fitness beyond energy+distance is uncommon (PARTIALLY addressed; depends on gap #3's resolution in data-gaps.md)

Most GA/metaheuristic WSN papers in the matrix optimize a fitness function combining at most 2-3 factors (typically distance + residual energy, e.g., GA-EMC, PEG-GA, ExAq-MSPP). Only Khalily-Dermany's OP_Sink/MA_Sink (7 criteria: data merit, latency, deadline, memory, travel time, density, fairness) rivals the draft's 4-objective fitness function (energy, smoothness, coverage, delay). This is a legitimate gap our methodology addresses on paper. Whether our *results* actually demonstrate the benefit of multi-objective optimization over single/dual-objective baselines depends on having a coverage/PDR figure that isolates this effect — currently our packet-delivery figure is a raw count, not the PDR ratio the fitness function itself uses internally (`f_coverage = Packets Received / Packets Generated`, per Section 4.2 of the draft). This is flagged in data-gaps.md #3.

## Gap 5 — Heterogeneous energy tiers combined with mobile-sink trajectory optimization is a narrow intersection (WEAKLY addressed pending gap resolution)

Static-network heterogeneity-aware GA clustering is common in the matrix (GA-EMC, TABU-GA MSEEC, Two-Phase GA, PEG-GA). Mobile-sink trajectory papers in the matrix (Hamidouche, Khalily-Dermany, Mohan, Sangeetha) are evaluated on **homogeneous** node energy. The combination — three-tier heterogeneous initial energy (Normal/Advanced/Super, per draft Section 5.2) *and* mobile-sink trajectory optimization *and* kinematic constraints together — does not appear as a combination in any of the 18 mined papers. This is the draft's most specific, defensible novelty claim structurally. **However**, this is currently the gap most exposed by the energy-efficiency tension in our own results (data-gaps.md #4): if IAGAPC-Enhanced consumes more energy than every baseline, the "heterogeneity-aware energy balancing" contribution needs the resolution in data-gaps.md #4 before this gap can be claimed as convincingly *addressed* rather than just *attempted*.

---

## How this maps to the paper's contribution statement (draft, pending data-gaps resolution)

Ranked by evidentiary strength as things stand today:
1. **Strongest, safe to claim now:** methodological novelty of combining kinematic constraints + multi-objective fitness + heterogeneous energy tiers + a diversity-restart GA mechanism — none of the 18 mined papers combine all of these.
2. **Claimable with caveats:** ns-3-based evaluation as a reproducibility/fidelity strength (not itself the core contribution).
3. **NOT yet claimable:** any specific magnitude of lifetime improvement, turning-angle reduction, or energy efficiency superiority — these require either new figures/data or a reframing of what "better" means for this scheme, per data-gaps.md #2 and #4.

This document should be revisited once data-gaps.md is resolved, since the final contribution bullets in the Introduction depend directly on which of the six required metrics end up with real supporting figures.
