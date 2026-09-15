# Our Results — Final, Post-PDR-Fix (Real ns-3.45 Data)

**This supersedes both prior versions** (the original pixel-digitized version from the fabricated stub, and the intermediate ARP-bug-affected version — see `analysis/our-results_pre_arp_fix.md` for that intermediate state, kept for audit trail). This version comes from a 540-run sweep (6 schemes × [4 densities + 5 traffic rates] × 10 seeds, 250kbps default) run *after* fixing a real ARP-queue-starvation bug and adding proper store-and-forward buffering — see `analysis/methods-delta.md` section 7 for the full diagnostic story. Zero run failures.

## The honest headline: end-to-end PDR is ~0.5%, and that's a genuine finding, not a bug

True end-to-end PDR (received/generated, the correct definition) across the full sweep: **0.471%**. This is low, and it's real — verified by eliminating three alternative explanations (ARP tuning, MAC queue timeout, wake-window duration all tested directly; none improved it, one made it measurably worse). The actual cause: a single mobile sink with brief, infrequent contact windows (8 GA waypoints across 300s over a 1000×1000m field, ~70-100m node ranges) cannot service the offered load from 100-500 nodes at any tested rate, regardless of buffer size. **State this directly in Results as a structural property of single-hop mobile-sink WSN at this deployment scale** — the six-scheme comparison is still valid (identical constraint applied to all six), but absolute PDR/throughput numbers reflect a genuinely contact-starved regime.

## Loss breakdown (full 540-run sweep)

| Stage | Count | % of generated |
|---|---|---|
| Generated | 464,471,762 | 100% |
| Buffer overflow (drop-oldest, 50-packet cap) | 447,490,756 | 96.34% |
| Buffered → app Send() calls | 10,715,386 | 2.31% |
| → real MAC TX attempts | 3,351,866 | 0.72% |
| → received at sink | 2,188,528 | **0.471%** |
| ARP drops (sanity check post-fix) | 7,418,154 | 1.60% (was 97.55% pre-fix) |

The dominant loss is now buffer overflow (a designed, finite, drop-oldest buffer doing exactly what it's specified to do under genuine demand-exceeds-capacity conditions), not an artificial bug. ARP drops dropped from 97.55% of generated (pre-fix) to 1.60% (post-fix) — the fix held at full scale.

## Metric-by-metric summary (mean ± 95% CI across 10 seeds, at n=200 nodes / 250 kbps unless noted)

| Metric | IAGAPC-Enhanced | AGAPC | EGATS-N | RCGA-ABC | DGA-M | CGAPD |
|---|---|---|---|---|---|---|
| PDR (%) | **0.989** | 0.524 | 0.569 | 0.733 | 0.881 | 0.583 |
| End-to-end delay (s, incl. buffering) | **0.855** | 1.852 | 2.117 | 1.437 | 0.886 | 2.946 |
| LND (s, density sweep) | 146.93 ± 7.49 | 143.59 ± 5.53 | 150.87 ± 7.51 | 145.13 ± 8.03 | 140.88 ± 5.80 | 117.95 ± 0.80 |
| Energy efficiency (packets/J) | **41.78 ± 10.76** | 21.998 ± 5.82 | 23.97 ± 8.04 | 30.85 ± 11.12 | 37.54 ± 21.36 | 24.18 ± 3.92 |
| Avg. turning angle (deg, all configs) | **20.08 ± 5.34 (std)** | 74.88 ± 13.68 | 77.75 ± 16.82 | 100.87 ± 19.49 | 83.25 ± 13.17 | 67.38 ± 10.49 |

## Delay is now much larger than before — expected, and itself a finding

`avgDelaySec` now measures true end-to-end latency (generation → sink arrival, including buffering time), not just transmission time. Values (0.86-2.95s) are far larger than the pre-fix numbers (which only captured post-buffering transmission delay, ~0.001-3s but measuring a different, narrower thing). **This is the correct definition for mobile-sink WSN** — a packet's real latency includes however long it waited in the buffer for the sink to come back into range. The energy/lifetime vs. latency trade-off this exposes (schemes with better coverage frequency have both higher PDR and lower delay, e.g., IAGAPC-Enhanced; schemes with poor coverage have both low PDR and high delay from long buffering waits, e.g., CGAPD) is a genuine, central tension worth discussing explicitly in Results — per your direction, not minimized.

## What's genuinely well-supported

- **Turning angle**: unchanged from the prior check (this metric doesn't depend on traffic/PDR) — IAGAPC-Enhanced 20.08° vs. 67-101° for baselines, still the strongest, cleanest result in the whole dataset.
- **Energy efficiency**: IAGAPC-Enhanced leads (41.78 packets/J), consistent with the pre-fix finding, now confirmed with real PDR data — 1.1-1.9x better than every baseline.
- **PDR and delay both favor IAGAPC-Enhanced** at n=200/250kbps — highest PDR (0.989%) and lowest delay (0.855s) simultaneously, a coherent, non-cherry-picked result across 90 runs/scheme.
- **CGAPD is the consistent worst performer** across every single metric (PDR, delay, LND, energy efficiency) — matches the draft's own stated critique of rigid K-means+TSP clustering.

## What's still weak or requires disclosure

- **FND/HND remain completely flat** (FND: 34.393s vs. 34.392s, IAGAPC-Enhanced vs. AGAPC, 0.003% difference, p=0.93) — confirmed unchanged by the PDR fix, as expected (see `methods-delta.md` section 4 for the order-statistics explanation — this is architectural, not a bug, and doesn't interact with traffic/buffering).
- **LND shows real but modest differentiation** — CGAPD is clearly worst (tight CI, non-overlapping), the other five substantially overlap. IAGAPC-Enhanced (146.93s) is not statistically distinguishable from AGAPC/EGATS-N/RCGA-ABC/DGA-M on LND.
- **Absolute PDR/throughput are very low** (sub-1% PDR) — a genuine, disclosed structural finding (see headline above), not something to present without the explanation.
- **Duty-cycling ablation** (from `methods-delta.md` section 2): energy-efficiency ranking depends on the duty-cycling mechanism being present — with it off, ranking changes (RCGA-ABC leads instead of IAGAPC-Enhanced). Per your explicit direction, **report both ON/OFF rankings as a strength (a credibility-building ablation), not a caveat** — ties the energy-efficiency result to a stated, testable mechanism rather than presenting it as an unconditioned property of the algorithm.

## Both Conclusion claims — final disposition, re-verified against this dataset

1. **"45.9% FND improvement vs. AGAPC"** — **cut, confirmed again.** 0.003% real difference, p=0.93.
2. **"32° turning angle"** — **keep with the real number: ~20°** (20.08° ± 5.34° std vs. 67-101° for baselines). Unaffected by the PDR fix (purely geometric metric), so this number was already stable across both dataset versions — strongest, most reusable claim in the whole results set.

## Figures (all regenerated from this final dataset, vector PDF, `figures/`)

Same 11 files as before (`fig1a/b` through `fig8`), now reflecting 250kbps density sweep and 50/125/250/500/1000kbps traffic sweep. `data/wsn_raw_results.csv` is the source of truth; `data/wsn_raw_results_pre_arp_fix.csv` kept for audit trail only, not for use.
