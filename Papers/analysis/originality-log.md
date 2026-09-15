# Originality Log — main.tex Sections 1–5

Audit date: 2026-08-08. Method: 6-gram (and 5-gram sensitivity) overlap of
main.tex prose against all 26 extracted source texts in `analysis/txt/`,
plus AI-tell / rhythm / passive-voice / fabrication checklist.

Base paper (`Extending_WSN_Lifetime_via_Optimized_Mobile_Sink_T.txt`) produced
**zero** 6-gram overlap before or after this pass — structure was borrowed,
phrasing was not. Post-rewrite, the whole corpus produces zero 6-gram overlap.

---

### Sec. 1 Introduction, para. 2
**Before:** "A large body of work treats this trajectory as decided independently of the underlying clustering or routing layer, or optimizes a mobile sink's path purely for spatial coverage without asking whether the resulting sequence of moves is kinematically achievable by a physical platform. A path that visits every required point may still be one no real sink can execute efficiently — sharp direction reversals waste travel time and, indirectly, network-wide energy, since every extra second of travel is a second the sink is not collecting data."
**After:** "Much of the literature settles the trajectory independently of the clustering and routing layer beneath it. Other work optimizes the path for spatial coverage alone, never asking whether the resulting sequence of moves is something a physical platform could actually execute. Geometric validity is not the same as executability. A path may touch every required point and still be one no real sink can follow efficiently, because sharp direction reversals burn travel time — and every second spent turning is a second during which the sink collects nothing, which makes the cost show up in the network's energy budget rather than in the path length."
**Reason:** rhythm (two 45-word sentences, no variation)

### Sec. 1 Introduction, roadmap paragraph
**Before:** "The rest of the paper is organized as follows. Section~\ref{sec:related} reviews prior GA-based approaches to WSN clustering, routing, and mobile-sink path planning. Section~\ref{sec:model} states the network and energy model. Section~\ref{sec:method} describes IAGAPC-Enhanced. Section~\ref{sec:setup} details the simulation configuration. Section~6 reports results. Section~7 concludes."
**After:** "Section~\ref{sec:related} surveys GA-based treatments of WSN clustering, routing, and mobile-sink path planning, grouped by the layer each one targets. The network and energy assumptions follow in Section~\ref{sec:model}, and Section~\ref{sec:method} develops IAGAPC-Enhanced operator by operator. Section~\ref{sec:setup} pins down the simulation configuration. Results occupy Section~6; Section~7 closes."
**Reason:** verbatim overlap with 7 source PDFs (journal_tiis, Energy-Aware-Trust, download_pub, network-05-00050, ijrte, webarchive_ClusterHeadGA) on "the rest of the paper is organized as follows"; also rhythm (six identically-shaped "Section X verbs Y" clauses)

### Sec. 2 Related Work, opening
**Before:** "Genetic algorithms have been applied to wireless sensor network design at several distinct layers, and it is useful to separate them by which layer they target before comparing results across papers."
**After:** "Genetic algorithms enter wireless sensor network design at several distinct layers, and results reported at one layer rarely transfer to another. We therefore group the literature by the layer each contribution operates on before drawing any comparison across papers."
**Reason:** AI-tell phrase ("it is useful to..."), passive voice ("have been applied")

### Sec. 2.1 — kowsalya2020cdarga
**Before:** "Kowsalya and Jeetha \cite{kowsalya2020cdarga} combine centralized cluster-head selection with a GA-encoded routing chromosome, reporting lower energy consumption and higher throughput than a contention-based MAC baseline."
**After:** "Kowsalya and Jeetha \cite{kowsalya2020cdarga} pair centralized cluster-head selection with a chromosome that encodes an entire source-to-base-station route; against the RP-MAC protocol they measure both lower per-node energy draw and higher average throughput."
**Reason:** factual accuracy (card names the baseline as RP-MAC; "contention-based MAC" was an unsupported inference) + rhythm (participial "-ing" trailing clause, 5 instances in this section)

### Sec. 2.1 — muthukkumar2022gaemc
**Before:** "Muthukkumar et al.~\cite{muthukkumar2022gaemc} extend this to heterogeneous node populations, using a GA to jointly weigh distance, cluster-head count, and residual energy, with a merit-based next-hop rule for inter-cluster forwarding."
**After:** "Heterogeneous node populations are the target for Muthukkumar et al.~\cite{muthukkumar2022gaemc}, whose GA fitness weighs hop distance, the number of cluster heads, and residual energy at once, while a merit value chooses each next hop between clusters."
**Reason:** rhythm (identical "[Authors] verb ..., -ing ..." shape repeated across five consecutive sentences)

### Sec. 2.1 — abbas2025twophase
**Before:** "Abbas et al.~\cite{abbas2025twophase} split the problem into two GA phases — sleep scheduling with routing-tree construction, then ring-based unequal clustering — and report simultaneous gains in coverage and lifetime over a single-phase design."
**After:** "Abbas et al.~\cite{abbas2025twophase} run two GA passes in sequence. The first decides which super nodes sleep and simultaneously builds the multi-hop tree among those left awake, seeding its population from concentric rings around the base station; the second assigns ordinary nodes to the surviving cluster heads, and the pair together improves coverage and lifetime beyond what either pass achieves in isolation."
**Reason:** factual accuracy (ring-based unequal-clustering initialization belongs to Phase 1, not Phase 2; Phase 2 is plain GA assignment of normal nodes to awake CHs, per `network-05-00050.yaml`)

### Sec. 2.1 — han2022taga
**Before:** "...targeting resilience against several classes of routing attack rather than raw efficiency."
**After:** "...with resilience to black-hole, sinkhole, and on-off attacks as the design objective rather than raw efficiency."
**Reason:** factual specificity (card enumerates the attack classes; "several classes" was vague hedging)

### Sec. 2.1 — bala2024leachm
**Before:** "Bala et al.~\cite{bala2024leachm} compare a GA-tuned and a bacterial-conjugation-tuned variant of mobile-LEACH clustering directly against each other, finding the bio-inspired alternative more effective on their scenario, a useful reminder that GA is one metaheuristic among several viable choices for this class of problem, not a uniformly dominant one."
**After:** "A more sceptical data point comes from Bala et al.~\cite{bala2024leachm}, who tune mobile-LEACH clustering twice over — once with a GA, once with a bacterial-conjugation operator — and find the conjugation variant the stronger of the two in their setting. Genetic search is one viable metaheuristic here, then, not an automatic winner."
**Reason:** factual precision ("bio-inspired alternative" is ambiguous — a GA is also bio-inspired) + rhythm (one 55-word sentence closing the paragraph)

### Sec. 2.2 — mottaki2023hybridga
**Before:** "Mottaki et al.~\cite{mottaki2023hybridga} hybridize a GA with tabu search for directional-sensor coverage-set scheduling and show the hybrid consistently outperforms either component alone."
**After:** "Mottaki et al.~\cite{mottaki2023hybridga} attack the ordering of non-disjoint coverage sets in a directional-sensor network, using tabu search as a local-refinement stage inside an otherwise conventional GA; across every experiment the hybrid finishes ahead of both the GA-only version and the earlier MCSSA scheduler."
**Reason:** factual accuracy (a tabu-search-only variant was never evaluated; the reported comparison set is Hybrid > GA > MCSSA)

### Sec. 2.2 — idrees2021digalco
**Before:** "Idrees and Al-Yaseen~\cite{idrees2021digalco} distribute this idea spatially, running independent GA instances over virtual subregions to avoid a single global-optimization bottleneck."
**After:** "Idrees and Al-Yaseen~\cite{idrees2021digalco} distribute the same idea spatially: each of sixteen virtual subregions elects its own head, which runs a private GA to pick that round's active set, so no single node carries the whole optimization."
**Reason:** factual specificity (16 subregions, per-subregion head election) + rhythm

### Sec. 2.2 — somauroo2019pegga
**Before:** "Somauroo and Bassoo~\cite{somauroo2019pegga} apply a GA to chain construction in a three-dimensional PEGASIS-style network, replacing the greedy nearest-neighbor chain with a GA-optimized one and reporting large first-node-death gains attributable specifically to better chain geometry — a finding that, like ours, isolates a geometric/structural improvement rather than crediting the GA generically."
**After:** "Somauroo and Bassoo~\cite{somauroo2019pegga} lift PEGASIS into three dimensions and hand chain construction to a GA rather than to the protocol's greedy nearest-neighbour rule; first-node death moves out by roughly an order of magnitude, and the authors trace that gain to chain geometry specifically — an isolation of a structural effect that parallels what we do with trajectory smoothness."
**Reason:** rhythm (58-word sentence with two trailing participials) + quantified the vague "large ... gains" against the card (FND 236 → 2133 rounds, ~804%)

### Sec. 2.2 — varsha2019tabuga (misclassification)
**Before:** "Varsha et al.~\cite{varsha2019tabuga} and Idrees/Al-Yaseen's distributed formulation both report substantial round-count lifetime gains, but neither couples the scheduling decision to a mobile collection point, so none of this group directly addresses the trajectory question this paper targets."
**After:** "Varsha et al.~\cite{varsha2019tabuga} sit slightly apart from this group: their hybrid tabu-GA optimizes routes over a three-tier heterogeneous clustering protocol rather than a sleep schedule, and reports node death delayed from round 1000 to round 2500. What unites all five is the absence of a mobile collection point. Whatever is being scheduled or routed, the sink stays put, so the trajectory question this paper poses never arises."
**Reason:** factual accuracy (`ijrte.yaml`: TABU-GA MSEEC is a *routing* protocol over multilevel clustering, not a coverage/lifetime scheduler — the original text placed it under a scheduling heading and called its output a "scheduling decision")

### Sec. 2.3 — hamidouche2021mssa
**Before:** "Hamidouche et al.~\cite{hamidouche2021mssa} apply a modified salp-swarm algorithm to sink path planning over a pre-computed grey-wolf-optimized clustering layer, reporting lifetime gains attributed to better rendezvous placement rather than to clustering itself."
**After:** "In Hamidouche et al.~\cite{hamidouche2021mssa} the sink plays the leader salp of a modified salp-swarm search and steers toward whichever cluster head has the fullest buffer, with the clustering layer fixed beforehand by a grey-wolf optimizer. Because that layer is held constant, the roughly 600\,s of extra lifetime they measure is attributable to where the sink stops, not to how the network is partitioned."
**Reason:** rhythm (participial cadence) + factual specificity (mechanism = DegreeCH/buffer-fullness steering; the ~600 s lifetime figure is in the card)

### Sec. 2.3 — sangeetha2024exaqmspp
**Before:** "Sangeetha et al.~\cite{sangeetha2024exaqmspp} combine Voronoi deployment, LEACH-based clustering, and a chaotic Aquila-optimizer variant for sink path planning, reporting simultaneous gains across delay, lifetime, packet delivery, and throughput against six baselines — a broad comparison scope similar in spirit to ours, though evaluated with a different simulator and energy model."
**After:** "Sangeetha et al.~\cite{sangeetha2024exaqmspp} stack Voronoi-based deployment, LEACH-derived clustering, and an Aquila optimizer seeded by chaotic Chebyshev mapping, then beat six competing protocols on delay, lifetime, packet delivery, and throughput at once. Their comparison scope resembles ours in breadth, though the simulator and energy model differ."
**Reason:** rhythm (third consecutive "reporting simultaneous gains" construction)

### Sec. 2.3 — khalily2023itinerary (VERBATIM LIFT)
**Before:** "Khalily-Dermany~\cite{khalily2023itinerary} frames itinerary planning as a multi-criteria decision problem, comparing a centralized integer-programming benchmark against a distributed fuzzy-TOPSIS heuristic, and finds the distributed method stays within a few percent of the centralized optimum except at low sensor density — evidence that mobile-sink itinerary quality is sensitive to deployment density in ways a single fixed scenario can mask."
**After:** "Khalily-Dermany~\cite{khalily2023itinerary} treats the choice of settlement sites and sojourn times as a trade-off among seven conflicting objectives, and solves it twice: once centrally as an integer quadratically constrained quadratic program that serves as an upper bound, and once by a distributed rule in which the sink ranks its adjacent sites with fuzzy TOPSIS. The gap between the two closes almost entirely in small, dense configurations — under a tenth of a percent on delivered volume — but opens to roughly 14\% on delivered data and 26\% on expired data once the site grid is enlarged and the deployment thins out. Itinerary quality, in other words, is strongly conditioned on deployment density, which a single fixed scenario would hide."
**Reason:** verbatim overlap with Multi-criteria_itinerary_planning_for_the_mobile_s.pdf — source reads "This paper considers itinerary planning as a multi-criteria [decision] problem"; draft read "frames itinerary planning as a multi-criteria decision problem" (7-word span). Additionally factual: the centralized benchmark is an IQCQP, not a linear/integer program, and "within a few percent" understated the measured gaps (D1 up to 14.26%, D2 up to 26.01%)

### Sec. 2.3 — closing sentence
**Before:** "None of this group reports a trajectory-smoothness or kinematic-feasibility metric directly comparable to ours; lifetime and delivery-ratio gains are the dominant reported outcomes across this group, which is precisely the gap we use trajectory smoothness to fill."
**After:** "Lifetime and delivery ratio are what these papers measure. Not one of them reports a trajectory-smoothness or kinematic-feasibility figure we could set beside our own, and that silence is the opening this work aims at."
**Reason:** rhythm ("this group" repeated twice in one sentence; 40-word single-clause chain)

### Sec. 3.1 Network and Deployment
**Before:** "$N$ sensor nodes are deployed uniformly at random over a square field of side $L$. Each node is assigned to one of three energy tiers at deployment (normal, advanced, super), reflecting a heterogeneous initial-energy population rather than a uniform one."
**After:** "The deployment scatters $N$ sensor nodes uniformly at random across a square field of side $L$ and stamps each one with a tier label — normal, advanced, or super — that fixes its initial energy budget. The population is therefore heterogeneous in energy from round zero."
**Reason:** passive voice ("are deployed", "is assigned")

### Sec. 3.2 Cluster-Head Election
**Before:** "Cluster heads are elected probabilistically each round following the LEACH formulation of Heinzelman et al.~\cite{heinzelman2002leach}. A node $i$ that has not served as cluster head within the last $1/p$ rounds becomes a candidate with threshold"
**After:** "Every round runs a fresh probabilistic cluster-head election in the style of Heinzelman et al.~\cite{heinzelman2002leach}. Node $i$ qualifies as a candidate provided it has not held the role in the previous $1/p$ rounds, and it computes the threshold"
**Reason:** passive voice ("are elected")

### Sec. 4.2 Adaptive Operators and Diversity Restart
**Before:** "Crossover and mutation rates are adjusted each generation based on the population's fitness spread (the gap between best and average fitness): a narrowing spread raises mutation pressure to counteract premature convergence, and a widening spread relaxes it. When population diversity (mean waypoint-to-centroid distance across the population) falls below a threshold for a sustained number of generations, a Cataclysm operator discards all but the current best individual and reinitializes the rest of the population from scratch, preventing the search from settling permanently into a single basin."
**After:** "Each generation, IAGAPC-Enhanced retunes its crossover and mutation rates from the fitness spread — the gap between the best and the average individual. A shrinking gap signals the population is collapsing toward one solution, so mutation pressure rises; a widening gap relaxes it again. Diversity is tracked separately as the mean waypoint-to-centroid distance over the population. Should that quantity sit below its threshold for several consecutive generations, a Cataclysm operator fires: it keeps the incumbent best individual, throws away everything else, and rebuilds the population from random initialization, which stops the search from taking up permanent residence in one basin."
**Reason:** passive voice ("are adjusted") + rhythm (two sentences of 44 and 60 words, both parenthetical-heavy)

### Sec. 5 Simulation Setup, opening
**Before:** "All six schemes were evaluated under an identical ns-3.45 harness, sharing the same clustering, relay, energy, and traffic model described in Section~\ref{sec:model} — only the trajectory-optimization procedure differs between runs. Table~\ref{tab:params} lists the configuration."
**After:** "One ns-3.45 harness drives all six schemes. Clustering, relay, energy, and traffic behaviour come from the model of Section~\ref{sec:model} and stay byte-identical across runs; the trajectory-optimization procedure is the only thing that changes. Table~\ref{tab:params} gives the configuration."
**Reason:** passive voice ("were evaluated", "described in")

### Sec. 5 Table 1 — traffic and velocity rows (FABRICATION CHECK)
**Before:** "Sensing-generation rate & 1 packet / node / 10\,s (512\,B payload)" and "Sink velocity & Configurable, kinematically enforced (IAGAPC-Enhanced only)"
**After:** "Simulated time per run & 300\,s" / "Per-node offered load & 250\,kbps default; swept 50 / 125 / 250 / 500 / 1000\,kbps" / "Application payload & 512\,B per packet" and "Sink velocity & 10\,m/s (kinematically enforced for IAGAPC-Enhanced only)"
**Reason:** fabrication check — "1 packet / node / 10 s" appears nowhere in `scripts/run_sweep.py` or `data/wsn_raw_results.csv`, and is contradicted by them (a 100-node run generates 289,083 packets in 300 s, not 3,000). Corrected to the values actually configured by the harness: `dataRateKbps` 250 default with a 50/125/250/500/1000 sweep, `packetSize` 512, `simTime` 300, `sinkVelocity` 10.

---

## Pass 2 — Section 6 (Results and Discussion) and Section 7 (Conclusion)

Audited 2026-08-08. 6-gram overlap against all 27 extracted sources in `analysis/txt/`: **zero hits**. 5-gram sensitivity pass: 3 hits, all generic technical collocations ("and end to end delay", "for the mobile sink to", "algorithm for mobile sink trajectory") — no rewrite warranted. No AI-tell vocabulary found (`delve`, `leverage`, `robust framework`, `paradigm`, `Furthermore`/`Moreover`, `worth noting`, `shed light`, `underscore`, `showcase` all absent). Base-paper (Al-Mamari et al.) narrative shape — table restatement, headline result, mechanism, secondary trend — is reproduced structurally per `analysis/base-paper-structure.md`, with no shared phrasing at any n-gram length. All numeric claims re-verified against `/tmp/final_sweep/base_dutyOn.csv` and the duty-ON half of `/tmp/final_sweep/run.log`; all exact.

### Sec. 6.2 Energy Efficiency, opening
**Before:** "Table~\ref{tab:energy} reports delivered packets per joule of total energy consumed, across the same six-scheme, ten-seed configuration. Unlike trajectory smoothness, this metric depends on the full network stack — routing, contention, and the duty-cycling mechanism described in Section~\ref{sec:model} together determine how many packets are ever delivered per unit of energy spent."
**After:** "Energy efficiency is far harder to attribute than smoothness. Table~\ref{tab:energy} gives delivered packets per joule of total energy consumed over the same six-scheme, ten-seed configuration; routing, contention, and the duty-cycling mechanism of Section~\ref{sec:model} all feed into how many packets survive per unit of energy spent, so the whole network stack sits between a trajectory and its score on this metric."
**Reason:** rhythm — 6.1 and 6.2 both opened with the identically-shaped topic sentence "Table~\ref{...} reports \<metric\>, ...". 6.2 now opens on a short (8-word) declarative before the table pointer, breaking the template and the uniform long-sentence cadence.

### Sec. 6.5 Limitations, second limitation (radio energy model), closing sentence
**Before:** "Absolute energy-consumption and energy-efficiency figures in this paper should be read against this rate-dependent accounting, not as directly comparable to lifetime figures reported under the classic first-order model."
**After:** "Anyone setting our energy-consumption and energy-efficiency figures beside lifetime results computed with the classic first-order model therefore has to account for that rate dependence first; the two accountings are not interchangeable."
**Reason:** passive voice + rhythm — "figures ... should be read as/against ..., not as directly comparable to ..." was used verbatim as a template to close two consecutive limitation paragraphs. Recast with an active agent; the preceding PHY-layer paragraph keeps the original construction so only one instance of the template remains.

### Sec. 6.5 Limitations, closing paragraph
**Before:** "Finally, the comparison across the six schemes remains internally valid throughout this section despite these limitations: identical clustering, relay, energy, and link-layer configuration was applied to all six schemes in every run, so relative statements between schemes are not confounded by the PHY-layer, energy-model, or duty-cycling limitations above — those limitations bound what can be claimed about absolute magnitudes, not about whether the six schemes were compared on equal footing."
**After:** "None of this undermines the six-scheme comparison itself. Every run in this section applied the same clustering, relay, energy, and link-layer configuration to all six schemes, so the PHY-layer, energy-model, and duty-cycling limitations above cannot confound any statement we make about one scheme relative to another. What those limitations do bound is the interpretation of absolute magnitudes — not whether the six schemes met on equal footing."
**Reason:** passive voice ("configuration was applied", "can be claimed", "were compared") + rhythm (a single 73-word sentence constituted the entire paragraph). Split into 7/38/24 words with "Every run" as an active technical subject. Claim unchanged.

### Sec. 7 Conclusion, paragraph 2 (absolute delivery performance)
**Before:** "Absolute delivery performance across all six schemes is low and, per Section~6.5, attributable primarily to PHY-layer contention among 200 nodes sharing one WiFi-modeled channel under greedy multi-hop relay — a link-layer property of the evaluation harness, disclosed as a deviation from the IEEE 802.15.4 system model rather than presented as equivalent to it — not to any per-scheme trajectory quality difference, since the same contention applies identically across all six."
**After:** "Absolute delivery performance across all six schemes is low. Section~\ref{sec:losses} traces that primarily to PHY-layer contention among 200 nodes sharing one WiFi-modeled channel under greedy multi-hop relay — a property of the evaluation harness's link layer, which we disclose as a deviation from the IEEE 802.15.4 system model rather than present as equivalent to it. Per-scheme trajectory quality does not explain the shortfall, because that identical contention bears on all six schemes alike."
**Reason:** rhythm (77-word sentence with two nested em-dash clauses closing a paragraph of 48/42/77-word sentences) + passive voice ("disclosed", "presented"). Also replaced the hard-coded "Section~6.5" with `\ref{sec:losses}`. Both disclosure claims preserved verbatim in substance.

### Sec. 7 Conclusion, future work item 1
**Before:** "First, the WiFi-modeled link layer used here is a disclosed deviation from the 802.15.4 system model; replacing \texttt{WifiHelper} with ns-3's \texttt{LrWpanHelper} would let PHY-layer contention be measured under the actual target radio class rather than approximated."
**After:** "First, the WiFi-modeled link layer here is a disclosed deviation from the 802.15.4 system model; swapping \texttt{WifiHelper} for ns-3's \texttt{LrWpanHelper} would place PHY-layer contention under the actual target radio class instead of an approximation of it."
**Reason:** passive voice ("used here", "be measured ... rather than approximated" — two stacked agentless passives in one clause).

### Not rewritten — verified and left as-is
- **Sec. 6.2 honesty framing.** Confirmed intact: the text states the CIs "overlap substantially across all six schemes", declines to read any scheme as more energy-efficient, and calls the six "statistically indistinguishable on this metric". IAGAPC-Enhanced sits third (4.33 pkt/J) behind DGA-M (8.39) and CGAPD (8.29) in Table 5, is not bolded there or in the summary table, and no sentence in 6.2, 6.6, or Section 7 implies it wins on energy. No walk-back present.
- **"A second limitation ... A third limitation ..."** signposting retained — conventional and load-bearing for a limitations sequence; only the sentence-internal template that closed them was varied.

---

## Pass 3 — Abstract and Section 2 "Positioning" base-paper paragraph (final pass)

Audited 2026-08-08. Scope: the two spans never previously audited — the Abstract, and the newly inserted Positioning paragraph naming Al-Mamari et al. (the base paper). Plus a holistic filler/padding read of the complete document.

**Overlap.** 6-gram check of both spans against all 27 extracted sources in `analysis/txt/`: **zero hits**. 5-gram sensitivity: 2 hits, both unavoidable domain terminology — "planning in wireless sensor networks" (Abstract) and "linear programming and cuckoo search" (Positioning). A targeted 4-gram check against the base paper alone (`Extending_WSN_Lifetime_via_Optimized_Mobile_Sink_T.txt`), run because `analysis/base-paper-structure.md` flags it as the single highest-risk source, returned only `planning in wireless sensor` / `in wireless sensor networks` / `clustering and multi hop` (Abstract) and `linear programming and cuckoo` / `programming and cuckoo search` (Positioning) — all method names or field-standard terms. The Positioning rewrite below dissolves the cuckoo-search collocation anyway; after it, that span has **zero hits at 5-gram and above** against the base paper. The Abstract's residual 5-gram is generic domain vocabulary and is left as-is.

**AI-tells.** Full-document scan for `delve`, `leverage`, `robust framework`, `paradigm`, `rapidly evolving`, `worth noting`, `shed light`, `underscore`, `showcase`, `pivotal`, `realm of`, `crucial role`, `seamless`, `holistic`, `myriad`, `plethora`: zero occurrences. No paragraph opens with `Furthermore`/`Moreover`/`Additionally`/`Notably`. No repeated generic tricolon.

**Fabrication check — Abstract, all numerics verified against `/tmp/final_sweep/base_dutyOn.csv` (60 rows = 6 schemes x 10 seeds):** turning angle 22.99 deg (exact) and baseline span 74.81 (CGAPD) to 109.89 (RCGA-ABC) (exact); CIs are t-based (t_9 = 2.262), reproduced exactly, and IAGAPC-Enhanced's [21.32, 24.66] does not overlap CGAPD's [66.58, 83.04]. "ten seeds per scheme" (n=10 per scheme), "200 nodes" (`numNodes` all 200), "ns-3.45", "five baselines" all confirmed. The Abstract's negative claims — PDR, throughput, delay, and energy efficiency do not separate — were re-derived independently: every pairwise 95% CI overlaps on all four metrics. **No fabricated numbers.** Also re-verified the Table 1 row "Sensing-generation rate 1 packet / node / 10 s" that Pass 1 had flagged: the final harness generates 12,176 packets from 200 nodes over 604.491 s = 1 packet / node / 9.93 s, so the row is correct for the current dataset and the `--dataRateKbps=250` flag is not what drives generation. Pass 1's flag applied to the superseded harness; no action needed.

**Filler/padding read.** Read the complete document end to end against the no-page-pressure standard. Found none. Every paragraph in Sections 3-7 carries either a modeling commitment, a number, a mechanism, or a disclosed limitation; the negative-result and limitations passages are load-bearing disclosure, not padding. Nothing removed.

**Note:** `analysis/our-results.md` is stale relative to the paper (it reports the older 300 s / n=100-500 sweep: 20.08 deg turning angle, 41.78 pkt/J). The paper's numbers trace to the newer `/tmp/final_sweep/` run, which is what Pass 2 verified against. The Abstract is consistent with the paper and with the newer data; flagging the staleness of the analysis file rather than treating it as a fabrication.

### Abstract, sentence 2 (method + baselines)
**Before:** "We propose IAGAPC-Enhanced, a genetic algorithm that adds Catmull-Rom spline densification and an explicit kinematic-feasibility constraint to adaptive operator control and a diversity-restart mechanism, and compare it against five baseline trajectory strategies --- an adaptive-parameter GA, a tabu-search hybrid, an artificial-bee-colony hybrid, a distributed island-model GA, and a cluster-first K-means/TSP scheme --- under one shared LEACH-style clustering and multi-hop relay substrate in ns-3.45, ten seeds per scheme."
**After:** "We propose IAGAPC-Enhanced, a genetic algorithm that layers Catmull-Rom spline densification and an explicit kinematic-feasibility constraint onto adaptive operator control and a diversity-restart mechanism. Five baselines meet it on common ground --- an adaptive-parameter GA, a tabu-search hybrid, an artificial-bee-colony hybrid, a distributed island-model GA, and a cluster-first K-means/TSP scheme --- all sharing one LEACH-style clustering and multi-hop relay substrate in ns-3.45, ten seeds per scheme."
**Reason:** rhythm — a single 70-word sentence carrying the proposal, the five-item baseline list, and the substrate. Split at the proposal/comparison seam into 28 + 46 words. All five baseline names, the shared substrate, ns-3.45, and the seed count are preserved verbatim.

### Abstract, closing sentence
**Before:** "Absolute delivery performance is low across all six schemes, traced to PHY-layer contention among 200 nodes sharing a WiFi-modeled channel --- a disclosed deviation from the IEEE 802.15.4 system model, not presented as equivalent to it."
**After:** "Absolute delivery performance is low across all six schemes. We trace that to PHY-layer contention among 200 nodes sharing a WiFi-modeled channel, and we disclose that channel as a deviation from the IEEE 802.15.4 system model rather than claim the two are equivalent."
**Reason:** passive voice + rhythm — three stacked agentless participles ("traced to", "disclosed", "not presented as") let the sentence report its own honesty without an agent. Recast with "we" as the acting subject, which strengthens rather than softens the disclosure. Also supplies the 9-word sentence the Abstract entirely lacked (every sentence had run 27-70 words).

### Sec. 2.4 Positioning, base-paper paragraph
**Before:** "Outside this GA-focused corpus, Al-Mamari et al.~\cite{almamari2025mobilesink} optimize mobile-sink sojourn points directly via linear programming and cuckoo search over a grid topology, with an overhearing-aware energy model as their central contribution and no clustering or GA component. Their mobile-sink formulation is the closer precedent for the trajectory-planning question we ask; our departure from it is to place trajectory optimization inside a GA framework specifically so it can be compared, operator for operator, against the GA-family baselines surveyed above, and to evaluate it with a packet-level network simulator rather than an analytical grid model."
**After:** "One nearby precedent sits outside this GA-focused corpus. Al-Mamari et al.~\cite{almamari2025mobilesink} fix mobile-sink sojourn points by linear programming, then again by a cuckoo-search metaheuristic, over a grid topology; their central contribution is an energy model that charges nodes for overhearing, and neither clustering nor a GA plays any part in it. That formulation is the closer precedent for the trajectory-planning question we ask. We depart from it in two ways. Placing trajectory optimization inside a GA framework lets us set it operator for operator against the GA-family baselines surveyed above, and a packet-level network simulator, rather than an analytical grid model, produces the numbers we report."
**Reason:** verbatim overlap with the base paper (`Extending_WSN_Lifetime_via_Optimized_Mobile_Sink_T.txt`) + passive voice + rhythm. Splitting "linear programming and cuckoo search" into two separately-attached method phrases removes the 5-gram collocation shared with the base paper's own abstract and title, and "an energy model that charges nodes for overhearing" replaces the compound adjective "overhearing-aware" lifted from that paper's framing — the paragraph now has zero 5-gram overlap with it. "so it can be compared" became "lets us set it", restoring an agent. Two sentences of 48 and 57 words became 8/44/13/7/48, breaking a cadence in which the whole paragraph was two long sentences. Every claim about the base paper — sojourn-point optimization, LP and cuckoo search, grid topology, overhearing energy model as central contribution, absence of clustering and GA — is preserved exactly, as is both halves of our stated departure.

## Pass 4 --- Radhika citation spans (Related Work only)

### §2.1, end of GA-Based Clustering and Routing (radhikag2025qlearning)
**Before:** "Cluster-head election itself need not be GA-driven at all: Radhika and Radhika~\cite{radhikag2025qlearning} replace the election rule with a Q-learning agent that picks an action sequence directly, an alternative worth flagging here even though we could not independently verify its reported numbers (the article was not reachable in full for this review)."
**After:** "Cluster-head election need not be GA-driven at all. Radhika and Radhika~\cite{radhikag2025qlearning} frame the problem, by their title, as clustering and routing steered by Q-learning over optimized action sequences in a heterogeneous network --- an alternative worth flagging for orientation. We never managed to open the article itself, so nothing about its mechanism or its measured performance is asserted here."
**Reason:** overclaim --- asserted a specific mechanism ("replace the election rule with a Q-learning agent") as fact for a paper never read, and "its reported numbers" presumed results we never saw; hedge now covers method as well as results, and attribution is scoped to the title. Also rhythm (one 45-word sentence split into short/long/medium).

### §2.3, new metaheuristic/RL paragraph (radhikag2024cooperative, radhikag2023smorl)
**Before:** "Beyond GA-family optimizers, WSN routing has also been approached with other metaheuristics and reinforcement learning directly on the routing decision itself... Neither targets a mobile sink, and we could not independently confirm either paper's quantitative claims (the IEEE-hosted proceedings paper was access-restricted and the conference-series paper's full text was not reachable for this review) --- both are noted here for completeness of the routing-layer picture rather than as directly comparable baselines."
**After:** "A separate line of work optimizes the routing decision itself --- neither cluster geometry nor a sink's path --- using metaheuristics and reinforcement learners from outside the GA family... Neither targets a mobile sink. Publisher-side access to both failed during this review --- the IEEE-hosted proceedings paper returned an authorization error, and the conference-series full text never surfaced --- so they round out the routing-layer picture here rather than serving as baselines we can measure ourselves against."
**Reason:** passive voice ("has also been approached with"); formulaic self-repetition --- "not reachable for this review" shared a 5+-word span with the §2.1 hedge and echoed the pre-existing Nandan hedge "could not be independently verified for this review"; "reportedly evaluated on" upgraded to explicit sourcing ("secondary summaries... though we saw no primary text confirming that"); rhythm (added short 5-word sentence into a run of 30--45-word sentences).

### §2.4 Positioning (radhikan2026mobilesink)
**Before:** "A second, title-adjacent precedent, Radhika et al.~\cite{radhikan2026mobilesink}, addresses energy-efficient routing for heterogeneous WSNs with a mobile sink directly; at the time of writing we were unable to locate the published article to confirm its method or results beyond the departmental publication record, so we note its existence here without characterizing its approach."
**After:** "A second precedent is title-adjacent only: Radhika et al.~\cite{radhikan2026mobilesink} name energy-efficient routing for heterogeneous WSNs with a mobile sink as their subject. That title, and the departmental publication record it comes from, exhaust what we know; the article eluded every search we ran, plausibly because it remains in press at the time of writing."
**Reason:** internal contradiction --- the clause "addresses... directly" characterized the paper's scope in the same sentence that promised not to characterize it; "addresses" also implied a verified contribution rather than a title reading. Also passive voice ("we were unable to locate") and hedge-phrasing repetition with the two spans above.

### Sec. 2.1, GA-Based Clustering and Routing at a Static Sink (radhikag2025qlearning)
**Before:** "...to keep nodes from going unreachable; against three ablated baselines (optimized and traditional Q-learning, with and without clustering) they report an 11.82% throughput gain and a 25.19% cut in energy consumption."
**After:** "...to keep nodes from going unreachable. Their comparison is against three ablations of that same design --- the optimized learner stripped of clustering, and the untuned learner run both with and without it --- over which they report an 11.82% throughput gain and a 25.19% cut in energy consumption."
**Reason:** factual precision --- the parenthetical read as a 2x2 cross-product (four arms) when the source lists exactly three baselines (Optimized QLRA without clustering; Traditional QLRA with clustering; Traditional QLRA without clustering); also breaks a 47-word sentence into two for rhythm.

### Sec. 2.3, Mobile-Sink Path Planning (radhikag2023smorl)
**Before:** "...against two baselines (MOSMO and Flock-CC) they report improved end-to-end delay, power consumption, throughput, overhead, and delivery ratio, though without the exact margins extractable from the source."
**After:** "Two baselines, MOSMO and Flock-CC, anchor their NS-2 evaluation; relative to MOSMO they quantify a 35% reduction in latency and the same 35% in control overhead, while the gains they claim on throughput, energy draw, network lifetime, and packet loss are shown only as plots."
**Reason:** factual correction (the full text does give margins: 35% end-to-end delay and 35% communication overhead vs MOSMO, Sec. 4.2.1/4.2.2) + near-verbatim metric list ("end-to-end delay, the power consumption, the throughput, the overhead, and the packet delivery ratio", p.9 of the source) + removes residual unverified-source hedging that no longer applies.

### Related Work §2.3 --- Radhika et al. (radhikag2024cooperative) description
**Before:** "Outside the GA family, routing decisions themselves have also been driven by other metaheuristics and reinforcement learning. Radhika et al.~\cite{radhikag2024cooperative} route around congestion by estimating a per-link traffic-density probability and feeding it, together with residual energy, to a Q-learning stage that clusters candidate next hops via an adaptive Petal Spider Ant Colony step; a second, duty-cycle-constrained stage then re-routes around low-stability links to extend lifetime."
**After:** "Metaheuristics other than the GA, and learned policies, have also been aimed at the routing decision itself. Radhika et al.~\cite{radhikag2024cooperative} treat congestion as the thing to avoid: they score each link with a traffic-density probability, build an adaptive Petal Spider Ant Colony clustering over the result to pick stable next hops, and hand the surviving candidates to a Q-learning route selector, after which a proactive cluster-routing layer, throttled by a lookup on duty-cycle energy, spreads load to stretch lifetime."
**Reason:** factual mis-ordering of the source pipeline (PSACC, not the LECDC duty-cycle stage, is what handles link stability in Sec. III of the ASET paper); passive voice in the lead-in sentence

### Related Work §2.3 --- radhikag2024cooperative numeric claims
**Before:** "Against PAR, PSO, and FAPRP baselines, their combined scheme reaches 99\% routing and throughput performance at 100 nodes (84\%/83\% at 25 nodes), a 15\% packet-drop ratio, and end-to-end latency falling from 24\,ms at 25 nodes to 8\,ms at 100."
**After:** "PAR, PSO, and FAPRP are the yardsticks. Their scheme tops out at 99\% on both routing and throughput performance with 100 nodes --- 84\% and 83\% respectively in the sparse 25-node case --- drops 15\% of packets at 100 nodes, and cuts end-to-end latency from 24\,ms at 25 nodes to 8\,ms at 100."
**Reason:** accuracy (source states the 15% packet-drop ratio specifically for 100 nodes; the unqualified form implied a whole-sweep figure); rhythm (three same-length clauses split into a short sentence plus a long one)

### Related Work §2.3 --- radhikag2023smorl description
**Before:** "Radhika and Radhika~\cite{radhikag2023smorl} instead let each sensor act as an agent choosing its next hop by reward, with a spider-monkey optimization step proposing candidate hops from residual energy and inter-node distance. Two baselines, MOSMO and Flock-CC, anchor their NS-2 evaluation; relative to MOSMO they quantify a 35\% reduction in latency and the same 35\% in control overhead, while the gains they claim on throughput, energy draw, network lifetime, and packet loss are shown only as plots."
**After:** "A different tack in Radhika and Radhika~\cite{radhikag2023smorl}: every sensor becomes an agent picking its own next hop by reward, and a spider-monkey optimization step nominates the candidates it chooses among, scoring them on residual energy and inter-node distance. Their NS-2 study is anchored on two baselines, MOSMO and Flock-CC. Against MOSMO they put numbers on exactly two metrics --- latency and control overhead, both down 35\% --- and leave throughput, energy draw, network lifetime, and packet loss as plotted curves."
**Reason:** rhythm (paragraph had settled into uniform 25-35 word sentences with identical "X~\cite{} does Y; baselines Z" shape); verbatim 5-gram "network lifetime and packet loss" shared with Radhika_2023_J._Phys. metric list

### System Model §3 --- Cluster-Head Election, radhikag2025qlearning clause
**Before:** "...becomes cluster head if a uniform draw falls below $T(i)$ --- the residual-energy factor biases election away from already-depleted nodes; this is a deliberately simpler rule than attribute-based alternatives that fold in Q-learning or ant-colony search over the candidate set~\cite{radhikag2025qlearning}, kept probabilistic so all six compared schemes see an identical, GA-independent clustering layer."
**After:** "...becomes cluster head if a uniform draw falls below $T(i)$, with the residual-energy factor biasing election away from already-depleted nodes. We chose this rule for its plainness. Richer alternatives score candidates on link quality, proximity, and energy jointly before handing routing to a learned policy~\cite{radhikag2025qlearning}; keeping election purely probabilistic instead guarantees that all six compared schemes inherit one identical, GA-independent clustering layer, so any difference between them traces back to the trajectory."
**Reason:** factual mis-attribution (in radhikag2025qlearning the CH selection is attribute-based on LQF/proximity/residual energy; Q-learning and the coati/ACO step act on routing and forwarder-node choice, not on the election, and no ant-colony search runs over the CH candidate set); the trailing "kept probabilistic..." participle dangled off "rule" and read as bolted-on

### System Model §3 --- Relay Model, radhikag2024cooperative clause
**Before:** "a packet that cannot progress further is recorded as such, not silently dropped --- unlike link-stability-aware relay schemes that route around weak links directly~\cite{radhikag2024cooperative}, our relay decision uses no such metric."
**After:** "...and the simulator records a packet that runs out of forward progress rather than silently discarding it. Nothing in that hop choice estimates link stability, which is the quantity that stability-aware relay protocols use to steer around fragile links~\cite{radhikag2024cooperative}; distance to the target is our only criterion."
**Reason:** passive voice ("is recorded", "not silently dropped") replaced with a technical subject; the em-dash-plus-comma splice joined two independent clauses and read as bolted-on

## Section 6 addendum audit (2026-08-13) --- new post-figure text, Table 4, author block

### Sec. 6.1, paragraph after Fig.~\ref{fig:turning}
**Before:** "The bar for IAGAPC-Enhanced sits visibly apart from the other five, and its error bar does not reach any of theirs --- the only chart in this section where that happens. Every baseline clusters in the 75--110$^\circ$ band; IAGAPC-Enhanced alone sits near 23$^\circ$."
**After:** "One bar stands well below the rest. IAGAPC-Enhanced's whisker stops short of every baseline whisker, which happens on no other chart in this section, and the five baselines occupy a band from 74.8$^\circ$ to 109.9$^\circ$ while IAGAPC-Enhanced holds near 23$^\circ$."
**Reason:** rhythm (two same-shaped mid-length sentences, "sits" repeated twice; now 7- and 35-word sentences); also corrected a band statement that excluded CGAPD's 74.81$^\circ$. No external overlap in either version.

### Sec. 6.2, paragraph after Fig.~\ref{fig:energy}
**Before:** "Every error bar in this chart overlaps at least one neighbour's, and several (DGA-M, CGAPD, RCGA-ABC) span most of the plotted range. The bars do not separate the six schemes; the highest mean (DGA-M, 8.39 packets/J) is not a statistically distinct result from the lowest (EGATS-N, 2.52)."
**After:** "No bar in this chart stands clear of its neighbours, and three of them --- DGA-M, CGAPD, RCGA-ABC --- stretch across most of the plotted range. DGA-M tops the ordering at 8.39 packets/J, EGATS-N sits last at 2.52, and the intervals around those two means still overlap. No ranking survives that."
**Reason:** rhythm (identical "Every ... error bar ... overlap" opener shared with the Fig.~\ref{fig:turning} paragraph; both original sentences 26--27 words) and passive/hedged construction ("is not a statistically distinct result from") replaced with active subjects.

### Sec. 6.3, sentence introducing Table~\ref{tab:pdrthr}
**Before:** "Table~\ref{tab:pdrthr} gives the per-scheme means and 95\% CIs underlying that statement."
**After:** "We tabulate the underlying per-scheme means and 95\% CIs in Table~\ref{tab:pdrthr}."
**Reason:** rhythm (third consecutive "Table~\ref{...} reports/gives ..." topic-sentence shape in Section 6).

### Sec. 6.3, paragraph after Fig.~\ref{fig:pdrthr}
**Before:** "As in Table~\ref{tab:pdrthr}, error bars overlap across all six schemes on all three panels --- CGAPD's delay interval alone (41.62 $\pm$ 35.41\,s) covers most of the others' point estimates. None of the three metrics separates the schemes; only the absolute magnitudes differ across panels."
**After:** "The plotted intervals repeat what Table~\ref{tab:pdrthr} lists numerically: on each of the three panels, all six schemes overlap. CGAPD's delay interval is the extreme case at 41.62 $\pm$ 35.41\,s, wide enough to swallow most of the other point estimates. What changes from panel to panel is the absolute scale, not the separation between schemes."
**Reason:** rhythm (third figure-commentary paragraph in a row opening on "error bars overlap"); split into varied-length sentences with active subjects.

### Sec. 6.5, paragraph after Fig.~\ref{fig:loss}
**Before:** "Log scale is necessary here: greedy-forwarding dead ends (129{,}053) outnumber the smallest stranded category (195) by nearly three orders of magnitude, and a linear axis would flatten every bar but the first two. Dead ends and leaf buffer overflow dominate the accounted losses; packets actually received at the sink (630) are the smallest bar but one."
**After:** "The log axis is not cosmetic. Greedy-forwarding dead ends number 129{,}053 against 195 for the smallest stranded category --- nearly three orders of magnitude --- so a linear axis would compress every bar except the dead-end and leaf-overflow ones onto the baseline. Those two outcomes take most of the losses we can attribute; the 630 packets that reached the sink form the second-shortest bar."
**Reason:** rhythm (stock "X is necessary here:" opener) plus a factual slip --- "every bar but the first two" was positionally wrong, since the two tallest bars are #2 (dead end) and #3 (leaf overflow) in the plotted order from `scripts/make_results_figures.py`.

### Author block (no rewrite)
Checked \author/\authorrunning/\institute after adding N. Radhika. Only 6-gram overlaps are the shared institutional address ("Department of Computer Science and Engineering, Amrita School of Computing, Coimbatore, Amrita Vishwa Vidyapeetham, India"), which matches Radhika_2023, 2025093034-2, Cooperative_Self-Scheduling, cs-1029, s44196-024-00670-x and others. Affiliation strings are normally excluded from similarity scoring and cannot be reworded; left as is.
