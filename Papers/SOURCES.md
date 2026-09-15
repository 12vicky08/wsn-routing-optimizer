# SOURCES.md — Radhika Citations

Three papers by G. Radhika / N. Radhika (Amrita, Coimbatore), all now **read in full** from local PDF copies in the project folder (not abstracts, not search-engine paraphrase). A fourth (the 2026 LNNS mobile-sink paper) was removed entirely — see the historical note at the bottom.

## 1. `radhikag2025qlearning` — Energy-Efficient Clustering with Q-Learning + ACOA

- **Source:** `2025093034-2.pdf`, read in full (`pdftotext -layout`). International Journal of Intelligent Engineering and Systems, Vol. 18, No. 8, pp. 547–565, 2025. DOI `10.22266/ijies2025.0930.34` confirmed via the paper's own header. All bib fields verified against the PDF.
- **Content:** attribute-based cluster-head selection feeding a Q-learning routing algorithm (QLRA); an Adaptive Coati Optimization Algorithm (ACOA) tunes the Q-learning action sequences/forwarder choice specifically to prevent isolated nodes. Evaluated in MATLAB across three scenarios (round count, node count, %CH selection) against three named baselines (optimized QLRA without clustering, traditional QLRA with clustering, traditional QLRA without clustering). Reports an 11.82% throughput gain and a 25.19% energy-consumption reduction.
- **Placement:** two places. (a) End of Related Work §2.1 (GA-Based Clustering and Routing), as a non-GA alternative to LEACH-family election, following the Bala et al. paragraph's point that GA isn't automatically the best metaheuristic for this problem. (b) A clause in System Model §3 (Cluster-Head Election), contrasting our deliberately simple probabilistic LEACH rule against this attribute-based/Q-learning alternative — genuine fit since it's specifically about the CH-election design choice, not a generic citation dump.
- **Engagement:** full, unhedged — mechanism, baselines, and both headline numbers stated directly.

## 2. `radhikag2024cooperative` — Cooperative Self-Scheduling Routing (CS2RA/EOLSRA)

- **Source:** `Cooperative_Self-Scheduling_Routing_Approach_Based_on_Energy_Efficient_Optimal_Link_Stability_Routing_Allocation_for_Improving_QoS-WSN.pdf`, read in full. 2024 IEEE ASET conference. DOI `10.1109/ASET60340.2024.10708763` confirmed in the PDF's own IEEE Xplore header line. No traditional page range — ASET is DOI-identified per-article, consistent with the paper's own formatting; not omitted, just not applicable to this venue.
- **Content:** a per-link traffic-density probability estimate combined with residual energy feeds a Q-learning stage that clusters candidate next hops via an Adaptive Petal Spider Ant Colony step (link-stability route optimization); a second, duty-cycle-constrained stage (Lookup Energy Constraint Duty Cycle) re-routes around unstable links to extend network lifetime. Evaluated against PAR, PSO, and FAPRP baselines: 84%/83% routing/throughput performance at 25 nodes rising to 99%/99% at 100 nodes, 15% packet-drop ratio, latency falling from 24ms (25 nodes) to 8ms (100 nodes) — all read directly from the paper's Figs. 2–10 and accompanying text, not inferred.
- **Placement:** two places. (a) Related Work §2.3, in the "outside the GA family" paragraph alongside `radhikag2023smorl`. (b) A clause in System Model §3 (Relay Model), contrasting link-stability-aware relay (this paper's approach) against our relay model's pure greedy-geographic selection, which uses no link-stability metric — a genuine scope-clarifying citation, not padding.
- **Engagement:** full, unhedged — the earlier "access-restricted" framing is gone; IEEE Xplore blocked WebFetch specifically, but a local PDF copy made the actual text available.

## 3. `radhikag2023smorl` — ARL-SMO (Adaptive Reinforcement Learning + Spider Monkey Optimization)

- **Source:** `Radhika_2023_J._Phys.:_Conf._Ser._2571_012033.pdf`, read in full (cross-checked against an earlier web-fetched copy of the same article — identical core content, only the "related articles" sidebar differed). J. Phys. Conf. Ser. 2571, 012033 (2023), AICECS-2023 conference. DOI `10.1088/1742-6596/2571/1/012033`. URL field set to the IOPscience PDF link per instruction.
- **Content:** each sensor acts as a reinforcement-learning agent choosing its next hop by reward; a spider-monkey optimization step proposes candidate hops from residual energy and inter-node distance. Evaluated (NS-2) against two baselines, MOSMO and Flock-CC: quantified 35% lower end-to-end delay and 35% lower control overhead vs. MOSMO (Sections 4.2.1–4.2.2 of the source); gains on throughput, energy draw, network lifetime, and packet loss are shown only as plots in the source, not stated as numbers, so the paper does not claim exact margins for those four and neither do we.
- **Placement:** Related Work §2.3, same paragraph as `radhikag2024cooperative`. No natural fit found in System Model — its mechanism (per-hop RL route selection) doesn't map onto a specific subsection of our system model the way the other two do, so it's Related-Work-only.
- **Engagement:** full, unhedged, with the one honest scope limit preserved (plot-only metrics reported as such, not invented as numbers).

## Historical: `radhikan2026mobilesink` — removed

Previously cited (the 2026 LNNS mobile-sink paper, appearing twice in `Dr.md` as entries [20]/[62]). Could not be located anywhere online — no Springer Link page, no DOI, nothing indexed, most likely forthcoming/in-press. Per explicit instruction it was deleted from `refs.bib` and its `\cite`/prose mention removed from Related Work §2.4 (Positioning). Not restored here; this entry is kept only as an audit-trail note.

## Process note

Every number and mechanism description above traces to a specific page/figure/section in a locally-read PDF, not to search-engine summaries or abstracts alone. No field in `refs.bib` was filled with a guessed value; the two entries lacking a conventional page range (`radhikag2024cooperative`) reflect the source venue's own formatting, not an omission.
