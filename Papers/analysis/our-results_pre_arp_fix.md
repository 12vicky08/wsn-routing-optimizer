# Our Results — Regenerated from Real ns-3.45 Simulation Data

**This supersedes the earlier pixel-digitized version.** That version was generated from `scratch/WSN-Simulation.cc`, discovered to be a synthetic stub with hardcoded per-scheme constants (no real wifi channel, no packets ever sent) — see `CHANGES.md` for the full account. All data below comes from `scratch/wsn-comparative-sim.cc`, a real ns-3.45 simulation (genuine WifiHelper 802.11n harness, FlowMonitor, BasicEnergySource/WifiRadioEnergyModel, real GA/Tabu/ABC/island/K-means+TSP trajectory optimizers), run as 540 independent simulations (6 schemes × [4 node densities + 5 traffic rates] × 10 seeds each), zero failures. Raw data: `data/wsn_raw_results.csv`. Figures: `figures/fig1a`–`fig8*.pdf`.

**Important scope note on the radio/PHY layer:** the simulation uses WiFi 802.11n (ad-hoc), tuned (TxPower, RxSensitivity, 2.4GHz band) to approximate a ~100m/low-rate WSN-class radio — **not** real 802.15.4/ZigBee as originally stated in the draft's Table 5.1. This was an explicit, disclosed decision (see `data-gaps.md` #7) to reuse a working, validated harness rather than build a 6LoWPAN+IPv6 stack over `LrWpanHelper`. The paper's simulation parameter table must say "802.11n (WSN-tuned)," not ZigBee/802.15.4.

## Metric-by-metric summary (mean ± 95% CI across 10 seeds, at n=200 nodes / 20 kbps unless noted)

| Metric | IAGAPC-Enhanced | AGAPC | EGATS-N | RCGA-ABC | DGA-M | CGAPD |
|---|---|---|---|---|---|---|
| PDR (%) | 5.81 ± 1.27 | 2.78 ± 1.04 | 6.00 ± 1.92 | 5.34 ± 2.30 | 5.50 ± 3.22 | 0.99 ± 0.20 |
| Throughput (kbps) | 3.12 ± 0.77 | 1.34 ± 0.52 | 2.89 ± 0.91 | 2.84 ± 1.25 | 2.81 ± 1.67 | 0.51 ± 0.13 |
| End-to-end delay (s) | 0.142 ± 0.018 | 0.091 ± 0.029 | 0.105 ± 0.048 | 0.078 ± 0.028 | 0.101 ± 0.028 | 0.215 ± 0.059 |
| LND (s, n=200 density sweep) | 146.93 ± 7.50 | 143.91 ± 5.61 | 150.77 ± 7.51 | 145.27 ± 8.00 | 141.16 ± 5.89 | 118.34 ± 0.83 |
| Energy efficiency (packets/J) | **1.52 ± 0.29** | 0.94 ± 0.21 | 1.33 ± 0.24 | 1.27 ± 0.32 | 1.11 ± 0.34 | 0.23 ± 0.04 |
| Avg. turning angle (deg, all configs) | **20.08 ± 5.34 (std)** | 74.88 ± 13.68 | 77.75 ± 16.82 | 100.87 ± 19.49 | 83.25 ± 13.17 | 67.38 ± 10.49 |

## What's genuinely well-supported

- **Path smoothness (turning angle): strong, statistically clear result.** IAGAPC-Enhanced's Catmull-Rom-spline + kinematic-feasibility trajectory averages **20.08° per turn**, roughly a third to a fifth of every baseline's (67–101°), with non-overlapping standard deviations. This directly validates the draft's kinematic-feasibility design goal — the real number is **20.08°, not the previously-asserted 32°** (the real value is actually better/lower).
- **Energy efficiency: IAGAPC-Enhanced leads.** 1.52 packets/Joule vs. 0.94–1.33 for baselines — resolves the earlier (fabricated-data-era) "energy/throughput tension" favorably: with real data, IAGAPC-Enhanced is not just higher-throughput but also the most energy-efficient scheme.
- **PDR/throughput: IAGAPC-Enhanced and EGATS-N are the top tier**, both clearly ahead of AGAPC and CGAPD, with RCGA-ABC/DGA-M in between. CGAPD (rigid K-means+TSP clustering) is consistently worst across every metric — a coherent, explicable finding (matches the draft's own critique: "if a Cluster Head dies, the entire trajectory must be recalculated").
- **Traffic-load sensitivity**: PDR scales from ~1–2% at 5 kbps to ~11–15% at 80 kbps across schemes, with the same relative ranking preserved (`fig6_traffic_sensitivity.pdf`).

## What's weak or unsupported

- **Network lifetime (FND/HND): flat, not differentiated.** FND is statistically identical across all six schemes (34.38s vs. 34.39s, t-test p=0.57) — dominated by baseline idle-listening cost before any scheme-dependent effect can accumulate. HND is similarly flat. **Do not claim an FND-based lifetime improvement** — the draft's "45.9% FND improvement over AGAPC" is definitively unsupported (real measured difference: -0.01%, not significant).
- **LND shows real but modest differentiation.** CGAPD is clearly worst (118.34s, tight CI, non-overlapping with the rest). Among the other five, confidence intervals substantially overlap — IAGAPC-Enhanced (146.93s) is not statistically distinguishable from AGAPC/EGATS-N/RCGA-ABC/DGA-M on LND with this data. A defensible claim is "IAGAPC-Enhanced's lifetime is competitive with adaptive-GA baselines and clearly better than rigid clustering (CGAPD)," not "IAGAPC-Enhanced has the best lifetime."
- **PDR/throughput absolute values are low** (single-digit % PDR) across all schemes — a consequence of light traffic (20 kbps default), a large 1000×1000m field relative to ~70–100m node ranges, and single-hop-only communication (no multi-hop relaying is implemented, despite the draft's system model describing multi-hop). This should be disclosed as a scope limitation, not hidden.

## Both previously-unsupported Conclusion claims — final disposition

1. **"IAGAPC-Enhanced extended FND by 45.9% vs. AGAPC, beat DGA-M by 20%+"** — **cut entirely.** Not supported; real data shows no significant FND difference between any schemes.
2. **"Reduced average turning angle to 32°"** — **keep, with the real number.** Rewrite as measuring **~20° average turning angle**, vs. 67–101° for baselines — a stronger and now genuinely evidenced claim than the original.

## Figures generated (all vector PDF, `figures/`)

`fig1a/b_throughput_vs_{density,load}.pdf`, `fig2a/b_pdr_vs_{density,load}.pdf`, `fig3_lifetime_fnd_hnd_lnd.pdf`, `fig4a/b_delay_vs_{density,load}.pdf`, `fig5_energy_vs_density.pdf`, `fig6_traffic_sensitivity.pdf`, `fig7_energy_efficiency.pdf`, `fig8_turning_angle.pdf`. All use a colourblind-safe palette + distinct markers/linestyles per scheme, sized for single-column Springer LNCS layout, with 95% CI error bars from the 10-seed replication.
