# Base Paper — Structural Extraction

**Source:** Al-Mamari, G.T.; Bouabdallah, F.; Cherif, A. "Extending WSN Lifetime via Optimized Mobile Sink Trajectories: Linear Programming and Cuckoo Search Approaches with Overhearing-Aware Energy Models." *IoT* 2025, 6, 54. MDPI. https://doi.org/10.3390/iot6030054

**Purpose of this document:** capture ORGANIZATION and RIGOR ONLY — section order, how tables/figures are framed, how contributions are stated, how the conclusion is worded structurally. Zero phrasing from the base paper may be reused in our draft. This is not a source for our literature review or citation list (it is itself a WSN mobile-sink paper, closely adjacent to our topic — treat with extra care in the originality-auditor pass since it's the single highest-risk overlap source).

**Format note:** this base paper uses MDPI's `IoT` journal template (two-column, MDPI house style), NOT a Springer template. We borrow its organizational logic only; our actual output format is Springer LNCS/LNEE per Phase 2 target (see HUMAN_TODO.md for template confirmation ask).

---

## Section order

1. Title / Authors / Affiliations / Correspondence (MDPI metadata block: Academic Editor, Received/Revised/Accepted/Published dates, Citation, Copyright — none of this is imitable structure for a Springer submission, it's venue-specific boilerplate)
2. Abstract (single paragraph, ~180 words) + Keywords (4 keywords)
3. **1. Introduction**
   - Opens with domain framing (WSN ubiquity, IoT integration, application domains cited)
   - States the core problem (energy hole problem) with a figure illustrating it
   - Surveys FOUR classes of prior remedies in short paragraphs (relay node deployment, adaptive power control, non-uniform initial energy, unequal clustering) each with 1 concrete example + result
   - Identifies the specific gap (overhearing ignored in Sink mobility models)
   - States contributions as an explicit bulleted list (5 bullets)
   - Ends with a roadmap paragraph ("The remainder of this paper is structured as follows...")
4. **2. Related Work**
   - Organized thematically into three subsections by SOLUTION CATEGORY, not by paper: 2.1 LP-Based Sink Mobility Models, 2.2 AI-Based Sink Mobility Models, 2.3 Non-LP/AI Sink Mobility Models
   - Each subsection is a sequence of paragraphs, one per cited work, following a consistent internal pattern: [Author et al. proposed X] → [mechanism/approach description] → [what was evaluated/compared against] → [result] → (often) [limitation]
   - **2.4 Discussion** — a synthesis subsection with three sub-parts:
     - 2.4.1 Comparative Analysis — narrates three comparison tables (Table 1/2/3, one per category: LP-based / AI-based / Non-LP/AI), each table has columns: Reference | Approach | Key Features | Advantages | Limitations | Overhearing (Y/N) | Energy Balancing vs. Lifetime
     - 2.4.2 Critical Gaps in the Literature — explicit bulleted list of gaps (5 bullets), each gap named then explained in 1 sentence
     - 2.4.3 Research Contribution — explicit bulleted list mapping directly onto the gaps just stated (5 bullets), closing with a 1-sentence synthesis of the paper's positioning
5. **3. System Model**
   - 3.1 Main Constraints of Sink Mobility Approach — states 2-3 constraints in plain language before any math (energy constraint, flow conservation law, Sink traffic constraint)
   - 3.2 Assumptions and Network Topology — explicit bulleted list of modeling assumptions (8 bullets), each one atomic and testable; explicitly justifies WHY the simplification is acceptable (e.g., grid topology justified by real deployment precedent)
   - 3.3 Problem Description — introduces notation gradually alongside prose explanation, one equation at a time, each equation followed by a sentence unpacking what it means physically
6. **4. Mathematical Formulation**
   - 4.1 Parameters (bulleted list, symbol: description (unit))
   - 4.2 Decision Variables (bulleted list)
   - 4.3 Objective Function (equation + constraints, each constraint equation immediately followed by one sentence of plain-language interpretation)
7. **5. LP-Based Analytical Result** (first solution method's results)
   - Opens by restating simulation parameters in a table (Table 4: Parameter | Value — only 3 rows, very minimal)
   - 5.1 Achieved WSN Lifetime — result table (Table 5) + line-chart figure referencing the table; prose explains the table AND explains a secondary trend (why the effect shrinks as network grows) — always gives the mechanism, not just the number
   - 5.2 Sink's Sojourn and Sensors' Residual Energy Distribution — deeper-dive subsection analyzing 3 representative cases (L=6,9,14), each with a sub-figure grid (a)-(f) and 4 detail tables; explicitly narrates the qualitative pattern (Sink favors corners, avoids center under overhearing) with a physical explanation
8. **6. AI-Based Solution** (second solution method — Cuckoo Search) — same pattern: method description, then results subsections mirroring Section 5's structure (own lifetime table, own sojourn/residual-energy breakdown, execution-time comparison table since this is the "faster but approximate" alternative)
9. **7. Comparative analysis** (LP vs CS head-to-head — not fully captured in excerpt but implied by roadmap: "Section 7 offers an in-depth comparative analysis of these two methodological approaches")
10. **8. TSP application** — shortest-path table for Sink tour construction (Tables 16-17), one subsection, ties the two solution methods together via a shared downstream step
11. **9. Conclusions**
    - Paragraph 1: restate contribution (what was proposed, method names)
    - Paragraph 2: comparative takeaway between the two methods (which wins under which condition — LP for optimality, CS for scale) + the headline quantitative finding restated (48% figure) + how the TSP step fits in
    - Paragraph 3: explicit limitation statement (regular grid topology only) leading into future work, ending on an aspirational closing sentence
    - (MDPI-specific boilerplate follows: Author Contributions, Funding, Data Availability, Acknowledgments, Conflicts of Interest — Springer equivalent will differ, flagged in HUMAN_TODO.md)
12. **References** — 52 entries, numbered, IEEE-ish numeric citation style (MDPI's own reference style, not directly reusable — Springer LNCS uses splncs04 author-year or numeric depending on exact class)

## Figure/Table conventions observed

- Every results table pairs 1:1 with a figure that visualizes the same data — the paper never presents a table without also plotting it (or vice versa)
- Table captions are one-line, purely descriptive ("Table 5. Achieved WSN lifetime by LP with and without overhearing in different WSN sizes.") — no interpretive language in captions, interpretation lives in body prose
- Multi-part figures (a)-(f) are used heavily for parameter-sweep comparisons (same metric across L=6,9,14 × with/without a variant)
- Every table/figure is referenced by number in prose BEFORE its content is discussed ("Table 5 presents..." not discussion-then-citation)

## How contributions are framed

- Bulleted, not prose-embedded, in both the Introduction (research contributions) and Related Work §2.4.3 (contribution restated as direct answer to each named gap) — contribution list appears TWICE in the paper, once high-level (Intro) and once gap-mapped (end of Related Work), each phrased differently rather than copy-pasted between the two locations.

## How the simulation parameter table is presented

- Minimal: only 3 parameters in Table 4 (e0, e, r) because this paper's model is purely analytical/LP-derived, not a full network simulator run — very different from what our ns-3-based paper will need (our simulation parameter table must be much larger — see wsn-metrics skill and Section 7 requirements in the master plan).

## How each metric figure is captioned and discussed

Pattern per subsection: (1) one sentence restating what the table/figure shows, (2) the headline quantitative result stated as a percentage or magnitude, (3) at least one sentence giving the MECHANISM behind the trend (not just "X improved," but "X improved because Y"), (4) where relevant, a secondary/finer-grained trend noted afterward (e.g., "impact of overhearing decreases as network size increases, because...").

## How the conclusion is worded (structurally, not verbatim)

Three-paragraph shape: (1) what we did, (2) comparative headline finding + numeric takeaway, (3) named limitation → future work → closing aspirational sentence. We will follow this three-beat shape but construct entirely original sentences.
