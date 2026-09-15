---
name: springer-lnee
description: Springer target format decision for this paper — class, packages, section order, figure/table conventions, and reference style. Every writing step (main.tex authoring, latex-builder, citation-checker) must load this before touching the document.
---

# Springer Target Format — Locked Decision

**No conference-supplied template was found in the working directory** (checked for `.cls`/`.zip`/`llncs`/`svmult`/`sn-*` files — none present). Defaulting per instructions to:

- **Class:** `llncs.cls` (Springer Lecture Notes in Computer Science / LNEE-compatible single-column conference style)
- **Bibliography style:** `splncs04.bst` (numeric, Springer LNCS standard)
- **Layout:** single-column, no `twocolumn` option
- **Action required:** HUMAN_TODO.md carries an item to confirm with the conference organizers whether this venue actually uses `llncs`-based LNCS style or a `svmult`-based LNEE chapter template — these differ (LNEE/svmult uses a different sectioning/appendix convention and sometimes different margins). Do NOT assume this is settled; it is a placeholder default until confirmed.

## Section order for main.tex (Springer LNCS convention, adapted to our content plan)

1. `\title` / `\author` / `\institute` — TODO placeholders only, never invented
2. `\begin{abstract}` (150-200 words) + `\keywords{}` (4-6 terms)
3. `\section{Introduction}`
4. `\section{Related Work}`
5. `\section{System Model and Problem Formulation}`
6. `\section{Proposed Methodology}` (architecture diagram, flow diagram, pseudocode, complexity)
7. `\section{Simulation Setup}` (booktabs parameter table)
8. `\section{Results and Discussion}` (one `\subsection` per metric + summary comparison table)
9. `\section{Conclusion and Future Work}`
10. `\bibliographystyle{splncs04}` + `\bibliography{refs}`

## Packages

- `\usepackage{graphicx}` — figures
- `\usepackage{booktabs}` — all tables (never plain `\hline` tables — Springer style expects booktabs rules: `\toprule`/`\midrule`/`\bottomrule`)
- `\usepackage{amsmath,amssymb}` — equations
- `\usepackage{algorithm2e}` or `\usepackage{algorithmic}` + `\usepackage{algorithm}` — pseudocode (pick one, do not mix)
- `\usepackage{tikz}` + relevant TikZ libraries (`positioning`, `arrows.meta`, `shapes.geometric`) — architecture + flow diagrams, hand-authored, vector
- `\usepackage{cite}` or rely on `splncs04` numeric citation behavior — citations as `[1]`, `[2,3]` style, not author-year
- `\usepackage[T1]{fontenc}` — standard LNCS encoding

## Figure/table conventions (borrowed structurally from base-paper-structure.md, applied to our format)

- Every results figure pairs with a source-of-truth table (either in the figure caption's referenced digitized data in analysis/, or an explicit table in the paper for the summary comparison).
- Captions: one descriptive line, no interpretation — interpretation lives in body prose immediately following the figure/table reference.
- Reference figures/tables in prose BEFORE discussing their content ("Figure 3 shows..." precedes analysis).
- All tables use `booktabs` (`\toprule`, `\midrule`, `\bottomrule`), never manual `\hline` grids.

## Page target

Minimum 8 full pages, aim 9-10, single-column LNCS layout. If short: deepen Related Work thematic analysis and Results discussion depth — never pad with filler sentences or restate content.

## Reference style

Numeric (`splncs04`), cited as `[N]` inline, ordered by first appearance (standard LNCS numeric behavior) or alphabetically depending on `.bst` resolution — citation-checker agent verifies resolution consistency at build time, does not need to be decided by hand.
