# Our Results — Final (Multi-Hop Clustering, Post-Instrumentation)

**This supersedes `our-results_pre_multihop.md`** (kept for audit trail — that version predates the traffic-generation-rate fix, the GA tour-time/compactness fix, multi-hop clustering, static ARP pre-population, and the 802.11b/RTS-CTS change; none of its numbers are current). Source of truth for everything below: `data/final_sweep/base_dutyOn.csv` and `data/final_sweep/ablation_dutyOff.csv` (60 runs each — 6 schemes × 10 seeds, $n{=}200$, 250kbps CSV label, current frozen code), plus the `[LOSSBREAKDOWN]` lines in `data/final_sweep/run.log`. These are the same files `paper/main.tex` Section 6 reports from — every number below and in the paper traces to this directory, not to any archived file.

## Headline: turning angle is the one clean, separating result

IAGAPC-Enhanced's trajectories turn **22.99° ± 1.67°** on average vs. **74.81–109.89°** for the five baselines (mean ± 95% CI, 10 seeds). No baseline's confidence interval overlaps IAGAPC-Enhanced's. This is the only metric in the evaluation that is purely a function of GA-output geometry (independent of MAC/PHY/traffic), and it is the paper's primary reported finding.

## Everything else: does not separate at n=10 seeds

| Metric | IAGAPC-Enhanced | AGAPC | EGATS-N | RCGA-ABC | DGA-M | CGAPD |
|---|---|---|---|---|---|---|
| Turning angle (°) | **22.99 ± 1.67** | 88.41 ± 13.62 | 83.97 ± 12.39 | 109.89 ± 15.23 | 90.66 ± 9.50 | 74.81 ± 8.23 |
| PDR (%) | 0.071 ± 0.032 | 0.051 ± 0.038 | 0.041 ± 0.018 | 0.084 ± 0.105 | 0.136 ± 0.127 | 0.135 ± 0.104 |
| Throughput (kbps) | 0.058 ± 0.026 | 0.042 ± 0.032 | 0.034 ± 0.015 | 0.069 ± 0.086 | 0.113 ± 0.105 | 0.111 ± 0.085 |
| Delay (s) | 11.86 ± 15.21 | 11.50 ± 14.90 | 6.16 ± 5.43 | 8.87 ± 16.98 | 19.77 ± 23.77 | 41.62 ± 35.41 |
| Energy eff. (pkt/J) | 4.33 ± 1.98 | 3.13 ± 2.33 | 2.52 ± 1.10 | 5.16 ± 6.41 | 8.39 ± 7.84 | 8.29 ± 6.38 |

PDR, throughput, delay, and energy efficiency all have confidence intervals that overlap between every pair of schemes — none of these four metrics support a ranking claim at this sample size, and the paper reports them as inconclusive rather than picking the numerically-highest mean as a headline.

## Network lifetime: not evaluated (all 60 runs)

`fndTimeSec`, `hndTimeSec`, `lndTimeSec` are all `-1` in every one of the 60 base-condition runs — no node death within the simulated horizon (a side effect of the energy recalibration needed for nodes to survive a full sink tour; see `methods-delta.md` §7). This is reported as an evaluation gap, not a finding.

## Loss breakdown (aggregate, 60 runs, base condition)

Of 610,094 relay-hop-level sends:

| Outcome | Count | % |
|---|---|---|
| Received at sink | 630 | 0.10% |
| Greedy dead-end | 129,053 | 21.15% |
| Leaf buffer overflow | 30,100 | 4.93% |
| Stranded, CH never visited | 4,667 | 0.76% |
| Stranded, CH visited but not yet flushed | 195 | 0.03% |
| PHY-layer reception failures (`phyRxDrops`, not directly comparable — see below) | 7,754,706 | 12.71× total sends |

`phyRxDrops` counts every WifiPhy reception failure across all 200 nodes' radios, not just packets addressed to a given node — it isn't summable against the 610,094 denominator the same way the application-layer rows are, but its scale (12.7× total sends) is the direct evidence for PHY-layer contention being the dominant loss mechanism. Full account in `methods-delta.md` §7–8.

## Duty-cycling ablation: dropped, not reported

`ablation_dutyOff.csv`: `packetsReceived=0` and `packetsBufferedSent=0` in **all 60 runs**. The OFF condition is degenerate under the current implementation (disabling duty-cycling also disables the only code path that transmits anything — see `methods-delta.md` §9), not a real comparison arm. No ablation table is presented in the paper; duty cycling remains a documented, unvalidated component of the energy model.

## What changed from the pre-multihop version

- Turning angle: 20.08° → 22.99° (both still cleanly separated from baselines; different codebase, same qualitative story — see `methods-delta.md` §7 for the compactness-term fitness change that explains the shift).
- Energy efficiency: previously reported as an IAGAPC-Enhanced win (41.78 pkt/J vs. 22–38 baseline) — **that framing does not hold under current data.** All six schemes' 95% CIs overlap; IAGAPC-Enhanced is not the numerical leader (4.33 vs. up to 8.39 for DGA-M/CGAPD) and no claim is made either way.
- PDR: previously ~0.5–1% (single-hop) → now ~0.04–0.14% (multi-hop, PHY-contention-dominated) — not comparable across versions, different architecture and bottleneck.
- FND/HND/LND: previously flat-but-reached (~34s); now unreached entirely. Different limitation, not the same finding restated.
