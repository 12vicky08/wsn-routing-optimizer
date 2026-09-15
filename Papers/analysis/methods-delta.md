# Methods Delta — Every Functional Difference Between the Simulation Code and `Paper.pdf`

This documents every place `scratch/wsn-comparative-sim.cc` (the code that produced `data/wsn_raw_results.csv` and every figure in `figures/`) behaves differently from what the draft describes. Written for you to audit before Phase 4 — nothing here is hidden in the results write-up either, but it's collected in one place.

**UPDATE (post-PDR investigation):** sections 1-6 below describe the state as of the first 540-run sweep. A follow-up investigation (prompted by the ~1-8% PDR looking suspicious) found and fixed a real bug (ARP queue starvation) and added real store-and-forward buffering. See **section 7** for the full account — it supersedes the PDR-related parts of sections 3 and 5 below (radio-rate is now 250kbps, not 20kbps) but the duty-cycling mechanism (section 1), the ablation finding (section 2), and the FND/HND order-statistics explanation (section 4) all still apply to the new data, re-verified.

**FINAL CONFIRMATION (full 540-run sweep, post-fix):** the diagnostic conclusions in section 7 held at full scale, not just in smoke tests. Across all 540 runs: 96.34% of generated packets are lost to genuine buffer overflow (the finite 50-packet buffer doing what it's specified to do under real demand-exceeds-capacity conditions), ARP drops fell to 1.60% of generated (was 97.55% of generated pre-fix — confirms the fix held), and true end-to-end PDR averaged **0.471%**. FND remained exactly flat (34.393s vs. 34.392s, IAGAPC-Enhanced vs. AGAPC, p=0.93) and turning angle unchanged (20.08° vs. 67-101°), as expected since neither depends on the traffic/buffering model. Energy efficiency still favors IAGAPC-Enhanced (41.78 packets/J vs. 22-38 for baselines). Full final numbers in `our-results.md`.

## 7. PDR investigation: ARP queue starvation (real bug, fixed) + store-and-forward buffering (added) + persistent low PDR (genuine, not a bug)

**Symptom that triggered this:** reported PDR (1-8%) turned out to be computed as received/**sent**, not received/**generated** — a much more flattering ratio than true end-to-end delivery. Real end-to-end PDR was 0.116%.

**Root cause, found and verified, not guessed:** added a true "generated" counter (`OnOffApplication`'s `Tx` trace, which the old `pdrPercent` calculation didn't use) and instrumented `ArpL3Protocol`/`ArpCache` `Drop` traces. Result: **97.55% of generated packets never reached MAC TX**, and ARP drops accounted for essentially all of that gap. Specific mechanism: `ArpCache::PendingQueueSize` defaults to 3 packets; while an ARP entry is unresolved (the common case, since the sink is rarely in range), only 3 packets queue per destination before the rest are silently dropped. This is a real, fixable ns-3 configuration bug, not a fundamental limitation — fixed via `Config::SetDefault` (`PendingQueueSize`→500, `WaitReplyTimeout`→3s, `MaxRetries`→5, `DeadTimeout`→20s), set before `stack.Install()` so it actually takes effect (an earlier placement right before `stack.Install()` looked reasonable but was — for the ARP part — correct; a related `WifiMacQueue::MaxDelay` change initially placed in the same spot had **zero effect** because `wifi.Install()`, which constructs the MAC queue objects, runs much earlier in `main()` — `Config::SetDefault` only affects objects constructed after the call. Moved to before `wifi.Install()`; documented here because it's exactly the kind of silent-no-op bug that's easy to miss and worth flagging for anyone extending this code.)

**Store-and-forward buffering, added on top of the ARP fix (your direction, not a unilateral choice):** replaced `OnOffApplication`/`PacketSinkHelper` with custom code:
- `GeneratePacket(nodeId, intervalS)`: scheduled at a fixed interval derived from `dataRateKbps`/`packetSize`, pushes a generation timestamp into a per-node `std::deque`.
- **Finite capacity: 50 packets** (~25.6KB at 512B packets) — chosen as a plausible small-embedded-MCU buffer size, not fit to any target PDR. **Drop-oldest policy on overflow**: freshest sensor reading is kept, oldest stale backlog is evicted — justified as the standard assumption for real-time environmental monitoring (a 10-minute-old temperature reading is less useful than a fresh one), not chosen to maximize a metric.
- `FlushBuffer(nodeId)`: called from `ProximityDutyCycle`'s in-range branch — drains the whole buffer via real `Socket::Send()` calls only when the sink is confirmed in range.
- `SinkRxCallback`: raw socket receive handler on the sink, replacing `PacketSinkHelper`. Looks up each received packet's generation time via its ns-3 packet UID (`g_packetGenTime` map) to compute **true end-to-end delay** (generation → arrival, including buffering time) — this is a deliberate redefinition of `avgDelaySec` per your explicit direction ("data latency now includes buffering delay... that is the correct definition for mobile-sink WSN"). Expect this to be substantially larger than the old FlowMonitor-based transmission-only delay once the new sweep runs.
- `pdrPercent` is now genuinely `received/generated` (true end-to-end), not `received/sent`.
- New CSV columns: `packetsGenerated`, `packetsBufferedSent`, `packetsSent` (MacTx, kept as a diagnostic), `packetsReceived`, `bufferOverflowDrops`, plus `arpL3Drops`/`arpCacheDrops` (kept as an ongoing sanity check that the ARP fix is holding).

**After the fix: PDR improved (0.116%→0.79% at 250kbps, a ~7x gain) but remains low (~1%), and this is now a verified, genuine finding, not a remaining bug.** Three further hypotheses were tested and empirically ruled out before concluding this:

1. **Was ARP still gating throughput even after the fix?** Tested `PendingQueueSize` at 64 vs. 500 — `packetsSent` was bit-identical (5160) in both. No effect.
2. **Was `WifiMacQueue::MaxDelay` (500ms default) expiring packets queued behind ARP resolution?** Relaxed to 5s, correctly placed before device install this time (verified via the same test) — still bit-identical. No effect.
3. **Was the 0.3s post-contact wake window too short to drain a 50-packet burst?** Extended to 0.9s — **PDR got worse** (0.79%→0.32%), because more awake time costs more idle-current energy, which kills nodes faster (LND dropped 143.5s→104.95s), leaving fewer total contact opportunities over the run. Reverted to 0.3s.
4. **Is this rate-specific (250kbps overwhelming the buffer)?** Tested at 20kbps (12.5x less generation pressure) — PDR barely moved (0.79%→0.96%), and buffer overflow still consumed ~72% of generated packets.

**Conclusion, verified by elimination rather than assumed:** the persistent low PDR is not an artificial/fixable bottleneck. It's a genuine structural consequence of a single mobile sink with brief, infrequent contact windows (the trajectory has only 8 GA waypoints, further spline-densified for IAGAPC-Enhanced, spread across 300s over a 1000×1000m field, with ~70-100m node ranges) — demand structurally exceeds the sink's service capacity at this deployment scale, regardless of data rate or buffer tuning. **Per your direction, this is reported as a genuine finding in the results, not hidden or further chased down with more parameter tweaks.** The six-scheme comparison remains valid — the same constraint applies identically to all six schemes — but absolute PDR/throughput numbers should be presented and discussed as reflecting a contact-starved regime, which is itself informative about single-hop mobile-sink WSN limitations at this scale.

**Rate changed 20kbps→250kbps for the density sweep** (and the traffic-sensitivity sweep re-centered to 50/125/250/500/1000kbps) per your direction, to match the draft's stated Table 5.1 parameter and close the 10x radio-model mismatch documented in section 3 (original numbering) above.

## 1. Sink-proximity duty cycling — the energy/lifetime mechanism

### What it does, mechanically

Every sensor node's WiFi radio is normally kept in `SLEEP` state (ns-3 `WifiPhy::SetSleepMode()`, ~20 μA draw). A per-node function (`ProximityDutyCycle`, checked every 1.0s) computes the real Euclidean distance from that node's fixed position to the mobile sink's actual current position (read from the sink's live `WaypointMobilityModel`):

- **If within communication range:** wake for 0.3s (`ResumeFromSleep()`), then return to sleep. Represents a brief, sufficient duty cycle when a coordinator is nearby — standard low-power-listening (LPL) behavior.
- **If out of range:** stay fully awake (idle-current draw, 5 mA) continuously until the next check. Represents a node "searching"/unable to rendezvous, unable to drop to low-power sleep because it has undelivered data and no coordinator in range.

### Where the numbers came from

**Mechanism precedent:** low-power-listening / duty-cycled MAC protocols (B-MAC, X-MAC, and the general LPL family) are standard, well-published WSN energy-saving techniques — the general principle (sleep when no coordinator/traffic is expected, wake more when uncertain) is textbook, not invented. **I did not find or cite a specific paper's exact parameterization** — the 0.3s wake window, 1.0s check interval, and the binary in-range/out-of-range switch (rather than a graduated backoff schedule, which is what real LPL protocols like B-MAC actually use) are **mechanism design choices I made, not values taken from a cited source.** Say so plainly, as asked: these numbers are mine, chosen to be a plausible order-of-magnitude LPL model, not validated against or drawn from any specific published protocol's parameters. If this needs literature backing for the paper, that's still open — flag for `HUMAN_TODO.md`.

**Current magnitudes** (idle 5mA, TX 5mA, RX 4mA, sleep 20μA, all at 3V supply): tuned once, before any scheme-comparison results existed, purely to make a 0.5–1.5J WSN-scale energy budget deplete over tens-to-hundreds of seconds instead of instantly (see #2 below) or never (see the 5x-budget saturation test). Not re-tuned after seeing scheme rankings.

### Was this tuned before or after seeing results? (asked explicitly — answering precisely)

Timeline, in order:
1. Discovered energy/FND completely flat across all six schemes using a **fixed** 1s-on/1s-off duty cycle (same for every node regardless of scheme) — this was a diagnosis, not a ranking.
2. Diagnosed the cause: nothing tied radio activity to sink position, so idle+sleep draw (scheme-independent) swamped Tx/Rx draw (the only scheme-dependent term) by orders of magnitude. Confirmed this diagnosis by re-testing with energy budgets multiplied 5x — ranking was *still* flat (224.136J for all six, differing only in the 5th decimal) — ruling out a saturation/ceiling artifact and confirming an architectural cause.
3. Designed `ProximityDutyCycle` as a fix for that specific diagnosed cause (couple radio wake state to real sink distance) — designed once, generically, without looking at per-scheme output first.
4. Ran it once for a crash/sanity check on a single config (IAGAPC-Enhanced + 5 baselines, n=100, seed=1) — at that point I *did* see a ranking (LND ranged 110–147.85s, IAGAPC-Enhanced had the *shortest* LND, i.e., not favored). **I did not change any parameter after seeing this.** I moved directly to a 72-run crash-only validation matrix (which checks fail/pass, not rankings) and then the full 540-run sweep.
5. No duty-cycle parameter (0.3s wake, 1.0s interval, 5mA/20μA currents) was changed at any point after step 3.

So: the *mechanism's existence* was motivated by a diagnosed structural gap (flat energy), which is a legitimate reason to add it. The *specific numeric parameters* were not tuned against scheme outcomes at any point. I did not cherry-pick toward IAGAPC-Enhanced winning — see #2 below, which shows the mechanism does not structurally favor it.

## 2. Ablation test: does duty cycling structurally advantage IAGAPC-Enhanced?

**No — the mechanism does not structurally favor any scheme. But it does change which scheme wins**, which is a different and more important finding than "no effect."

Ran all 6 schemes × 3 seeds at n=200/20kbps with `--dutyCycle=false` (radio always idle, never sleeps — matches pre-duty-cycle behavior) and compared packets/Joule ranking against the same config from the real (duty-cycle-on) sweep:

| Rank | Duty cycle OFF (packets/J) | Duty cycle ON (packets/J, real sweep) |
|---|---|---|
| 1 | RCGA-ABC — 2.45 | **IAGAPC-Enhanced — 1.55** |
| 2 | EGATS-N — 1.81 | EGATS-N — 1.43 |
| 3 | IAGAPC-Enhanced — 1.62 | RCGA-ABC — 1.41 |
| 4 | DGA-M — 1.18 | DGA-M — 1.39 |
| 5 | AGAPC — 0.96 | AGAPC — 0.66 |
| 6 (worst, both) | CGAPD — 0.29 | CGAPD — 0.26 |

With duty cycling off, energy is exactly flat (140.0J for every scheme, confirming the original diagnosis), so packets/J ranking there is **purely a proxy for packets delivered** — RCGA-ABC happens to deliver the most packets in this 3-seed sample. With duty cycling on, IAGAPC-Enhanced moves from 3rd to 1st, and RCGA-ABC drops from 1st to 3rd.

**What this means, stated plainly:** IAGAPC-Enhanced's energy-efficiency lead in the real sweep is **not a property of its trajectory optimization alone** — it emerges from the *interaction* between its trajectory and the sink-proximity duty-cycle mechanism I added (plausibly because IAGAPC-Enhanced's fitness function includes an energy-balance term that biases its trajectory toward nodes needing coverage, which pairs well with a mechanism that specifically rewards proximity-time — but that's a hypothesis, not verified further here). **This is a real result of a real simulation, not fabricated — but it is contingent on a specific, self-designed energy-accounting mechanism, and the paper should say so rather than present it as an unconditional property of the algorithm.** Recommend citing this ablation directly in a Discussion/Limitations paragraph rather than omitting it.

CGAPD is the one ranking that's robust to this ablation (worst in both cases) — that finding can be stated with more confidence.

## 3. Radio model sanity check against the draft's own stated constants

Draft Section 3.2 states Eelec=50nJ/bit, εfs=10pJ/bit/m², εmp=0.0013pJ/bit/m⁴, giving a threshold distance d₀=√(εfs/εmp)≈87.7m — matches the draft's own claimed "typically 87m" (internal consistency check passes).

Computed analytic per-packet cost at 512 bytes (4096 bits) using this formula and compared against our sim's actual current×time model (5mA TX / 4mA RX at 3V, over the packet's airtime at our 20kbps default rate):

| | Analytic (draft's formula, d=50m) | Our sim (current × airtime, 20kbps) | Ratio |
|---|---|---|---|
| ETx | 307.2 μJ | 3072.0 μJ | **10.0x** |
| ERx | 204.8 μJ | 2457.6 μJ | 12.0x |

**Our simulation's per-packet energy cost is an order of magnitude (~10x) higher than the draft's own analytic first-order radio model predicts, at the same packet size.** Root cause, identified precisely: the classic Heinzelman-style formula (`k·Eelec + k·ε·d^n`) is rate-independent — it doesn't know or care how fast bits are clocked out. Our current-based model (current × time, where time = bits/rate) is rate-*dependent*: at a low 20kbps application data rate, the radio's TX current draws for a proportionally longer airtime than the higher chip rates (~250kbps–1Mbps class) the classic formula is typically calibrated against. Confirmed numerically: **the two models match almost exactly at ~200kbps** — very close to the draft's own stated 250kbps data rate parameter (Table 5.1), which our simulation's actual default (20kbps) does not currently match.

**Recommendation:** either (a) rerun the sweep at 250kbps to match the draft's stated parameter and bring the two energy-accounting approaches into close agreement, or (b) keep 20kbps (chosen for a plausible light WSN traffic load) and disclose in the paper that per-packet energy cost in this simulation reflects a current×airtime accounting model at 20kbps, not the classic bit-energy formula at typical higher chip rates — the two aren't literally the same thing and the paper's Section 3.2 equations, if kept, should not be presented as exactly what was simulated. I have not changed the data rate without your direction, since it would mean re-running the whole sweep.

## 4. Why FND and HND don't differentiate any scheme — verified, not just diagnosed

**This is a genuine architectural/statistical property, not a broken coupling.** Energy consumption *is* coupled to real per-node position and real-time sink distance (confirmed: `ProximityDutyCycle` reads each node's actual position and the sink's actual live location every check). The flatness has a precise, numerically-verified explanation:

**FND is the minimum of ~70-350 nearly-i.i.d. per-node depletion times**, and that minimum is set by whichever node is *worst-covered* — i.e., a node that is essentially never in range and stays continuously awake (idle current) for its whole life. For such a node: `time to deplete 0.5J tier budget = 0.5J / (5mA × 3V) = 33.33s`. **Observed FND across all 540 runs: 34.38s, every single scheme.** The 3% gap (33.33 predicted vs. 34.38 observed) is explained by occasional brief in-range sleep credit. With PDR only 1–8% across every scheme, *most* low-tier nodes in *every* scheme spend most of their time in this same "effectively never covered" regime — so the worst-case node's depletion time is nearly deterministic and scheme-independent, because it's set by the physics of continuous-idle drain, not by trajectory quality.

**HND** (needs 50% of the population dead) is reached almost immediately after FND (37s vs. 34s) because 70% of the population shares the same lowest tier and the same "mostly-uncovered, mostly-idle-draining" regime — the bulk of that group clusters through depletion in a narrow window for the same reason, and 70% > 50%, so HND doesn't need to reach into the higher-energy tiers at all.

**LND** *does* differentiate (CGAPD clearly worst, ~118s vs. ~141–151s for the rest) because it requires depleting the 10% super-tier (1.5J, 3x longer baseline) too — a much smaller group, where individual per-node coverage luck (and therefore real scheme-dependent trajectory quality) has enough weight to show up in the aggregate statistic, unlike the large low-tier group where it gets averaged away.

**Verdict: genuine architectural property of order statistics over a heterogeneous, low-average-coverage population — not a modeling gap in the coupling itself.** The coupling is real (LND proves it); FND/HND are just the wrong statistic to expect scheme sensitivity from, at this coverage probability and tier-size skew. Confirmed by direct calculation, not empirically re-verified with per-node instrumentation — I can add that (dump per-node death time + tier to CSV for one run) if you want direct empirical confirmation rather than the closed-form argument above; didn't do it unprompted since the arithmetic match (33.33 vs 34.38s) is already a tight, verifiable confirmation.

## 5. Single-hop vs. the draft's multi-hop claim

Draft Section 3.1: "Nodes use multi-hop communication to reach the MS or a designated Rendezvous Point." **Not implemented.** Every sensor sends directly to the sink (`OnOffHelper` → sink's `InetSocketAddress`, one hop, no routing protocol). This is why absolute PDR/throughput are low (single-digit % PDR) — with 70–100m node ranges over a 1000×1000m field and no relaying, most nodes are simply out of direct range most of the time. The six-way scheme comparison is still internally valid (identical single-hop limitation applied uniformly to all six), but absolute numbers shouldn't be presented as representative of a full multi-hop deployment. State as a scope limitation in the paper.

## 6. Everything else changed beyond pure instrumentation

- **WiFi 802.11n (2.4GHz, tuned TxPower/RxSensitivity), not 802.15.4/ZigBee** — explicit decision, documented in `data-gaps.md` #7.
- **IP subnet widened from /24 to /16** — pure bug fix (500-node runs overflowed 254 host addresses), no behavioral effect on results below 254 nodes.
- **Physical energy budget decoupled from the paper's declared 0.5/1.0/1.5J tiers** — `BasicEnergySource` is given a large physical budget (10,000J) that never triggers ns-3's own automatic depletion-triggered PHY shutdown (root cause of an earlier crash class); the paper's real tier budgets are tracked independently in application code (`g_initialEnergy`) and compared against *consumed* energy to determine logical death. This is accounting, not a behavior change — verified to reproduce exact expected totals (e.g., 70.0J for a 100-node population with 70/20/10% tier split, matching the analytic sum precisely) when nodes fully deplete.
- Everything else (all 6 trajectory optimizers' algorithmic logic, the GA operators, spline/kinematic model, fitness functions) is unchanged from what's described in `data-gaps.md` #5 — no further deltas there.

## 7. Multi-hop clustering added, then a chain of real bugs found and fixed (traffic rate, tour-time circularity, PDR loss breakdown)

Superseding note: section 5 above ("single-hop only") is now historical. Multi-hop relay to LEACH-elected cluster heads was implemented (greedy geographic forwarding, hop cap 3, `kSensorToCHRangeM=50m` NOT recovered from literature, `kCHToSinkRangeM=100m`) — see code comments in `wsn-comparative-sim.cc` around `ElectClusterHeads`/`GreedyNextHop`/`RelayRecvCallback`. Getting it to a defensible PDR took several rounds of real bugs, each found by direct instrumentation, not assumption:

**Bug A — per-node traffic generation rate was 400x too high.** `intervalS = (packetSize*8)/(dataRateKbps*1000.0)` treated the 250kbps *link* rate as the *per-node generation* rate, producing a packet every ~16ms/node (110M packets generated for 200 nodes over 12450s). Fixed: fixed 10s/packet periodic-sensing interval (`kSensingIntervalS`), independent of `dataRateKbps`, which now only describes the link/PHY parameter-table row. Generated packets dropped to a sane ~12,000/run at n=200.

**Bug B — GA tour time tracked simTime and could never converge.** `InitPopulation` sampled candidate waypoint times from `[0, simTime]`; measuring "true" tour time at increasing simTime values gave 4150s at simTime=5000, then 10334s at simTime=12450 — window-dependent, not a fixed physical quantity, so "set simTime=3x measured tour time" could never stabilize. Fixed: an a-priori tour-time target (`EstimateTourTimeTarget`, Beardwood-Halton-Hammersley open-tour-length estimate, `0.7124*sqrt(numWaypoints*areaW*areaH)/vMax`) computed independent of simTime, used as the GA's time-sampling window instead of simTime, plus a compactness term added to `CalculateFitnessProxy` (`0.6*coverage + 0.2*energyEff + 0.2*compactness`) so the GA is actually incentivized to keep the tour short — previously nothing in the fitness function depended on time at all. Confirmed converged: target 201.5s, measured actual tour times 55-287s across the six schemes (same order of magnitude, no runaway).

**Full loss breakdown, instrumented (not guessed).** At n=200/250kbps/seed 1, of 16,532 relay-hop-level sends, app-layer counters (greedy dead-end, ARP cache/L3 drop, hop-cap exceeded, stranded-in-CH-buffer) accounted for only ~55%; the rest was traced to `phyRxDrops` (ns-3's `WifiPhy::PhyRxDrop` trace), which alone was 12x the total app-level send count — confirming PHY-layer collision/reception failure among 200 nodes sharing one channel under greedy multi-hop relay, not an app-logic bug, as the dominant loss mechanism.

**Two follow-up config changes tested (no new mechanisms, no rewrite):**
1. Static ARP pre-population (`ArpCache::Add`+`SetMacAddress`+`MarkPermanent`, full mesh, at t=0) — modeling 802.15.4's beacon-based neighbor knowledge instead of WiFi ARP broadcast/reply. **Result: ARP drops went from 6,136 (37.1% of relay-hop sends) to 0, exactly as predicted.**
2. RTS/CTS enabled (`RtsCtsThreshold=0`) + switched from 802.11n/HtMcs0 to 802.11b/DsssRate1Mbps (lowest available rate in ns-3's wifi module) to cut PHY contention. **Result: `phyRxDrops` fell 199,026 → 134,774 (-32%) but remained dominant — collision/reception failure among 200 contending relayers on a shared channel is not primarily a rate-choice problem.**

**Combined result: PDR 0.0151% (single fix 1, tour-time-only) → 0.0904% (both tour-time+traffic-rate fixes) → 0.1150% (+ ARP pre-population + RTS/CTS + lowest rate).** Two full rounds of real, verified fixes, each confirmed by direct measurement against its predicted effect, moved PDR by roughly one order of magnitude total but it remains far under any defensible threshold (target was 85%+, floor was 10%). Per explicit instruction, no third fix attempted — this is the honest state of the multi-hop-clustering + WiFi-as-802.15.4-stand-in simulation as of this investigation.

## 8. Simulator/PHY-standard disclosure (explicit, plain statement)

**The simulation uses ns-3's `WifiHelper` (IEEE 802.11, currently 802.11b/DSSS at the lowest rate), not IEEE 802.15.4.** `Paper.pdf` Section 3/5 claims IEEE 802.15.4/ZigBee as the PHY. This was a disclosed, deliberate simplification from the start (see `data-gaps.md` #7 — real `LrWpanHelper`+6LoWPAN would need substantially more implementation than tuning WifiHelper's range/rate/power to approximate a WSN-radio class), not something discovered now. It is restated here plainly because it is directly relevant to the PDR investigation above: 200 nodes contending for one WiFi-modeled channel under greedy multi-hop relay produces WiFi-specific collision behavior (`phyRxDrops`) that a real, narrowband, CSMA-CA 802.15.4 PHY at a much lower node density per channel access would not necessarily reproduce at the same severity. **This must be stated as an explicit limitation in the paper's Methods/Limitations section, not left implicit in a parameter table row.**

## 9. Duty-cycling ablation dropped from the paper (decision, with reasoning)

Re-running the ablation (10 seeds, `--dutyCycle=false`) on the current multi-hop-clustering codebase produced `packetsBufferedSent=0` and `packetsReceived=0` in **all 60 runs**, with no exceptions. Root cause: `FlushBuffer` and `FlushBufferRelay` — the only two functions that ever move a packet out of a node's buffer — are called exclusively from inside `NodeDutyCycle`. Setting `dutyCycleEnabled=false` does not leave the radio always-on with unchanged transmission behavior (which is what a meaningful ON/OFF ablation requires); it disables the call path that transmits anything at all. The OFF arm is therefore not a degraded version of the ON arm — it is a different, degenerate condition (zero transmissions) that cannot be compared to it.

**Consequence for the earlier finding:** the pre-multi-hop ablation result documented in section 2 of this file (energy-efficiency ranking flips, RCGA-ABC leading when duty-cycling is off) was measured on the old single-hop codebase, where `FlushBuffer` was not gated behind `NodeDutyCycle` the same way. That old result is not reproducible on current code and should not be read as evidence of a real interaction effect — it was never re-verified against a working OFF arm on this architecture, and now cannot be, without decoupling the flush call path from the duty-cycle gate (an architectural change, out of scope for the "no third fix" constraint already in force this session).

**Decision:** the ablation is dropped from the paper entirely, not presented with a caveat and not silently reused from the stale pre-multi-hop numbers. Duty cycling remains documented as a real, implemented component of the energy model (System Model + parameter table), with its window durations and currents stated plainly as this study's own configuration choices, not values drawn from a cited source. The Results/Limitations discussion states plainly that this mechanism's isolated contribution to the reported energy numbers could not be validated, because the ablation configuration needed to isolate it is not functional under the current implementation. Section 6.2 (energy efficiency) reports the six-scheme packets/Joule comparison under the single ON condition only, with no ON/OFF claim.
