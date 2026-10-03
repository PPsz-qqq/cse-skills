# LaTeX skeleton

A starting structure for the five axes. It carries the sections, the claim-bearing slots, and the
reviewer-facing infrastructure that this field expects. Replace the venue's document class and
style files with the current official ones, and verify the page limit and the anonymity rules
against the current call for papers before formatting (`../../ctrl-shared/core/venue-matrix.md`).

Adapt, do not fill blindly. A section that has nothing to say is removed rather than padded.

## Main file

```latex
% !TEX program = pdflatex
% Venue: <exact name, track, year>. Class and style from the official author kit, checked <date>.
% Page limit: <n> pages excluding references. Anonymity: <double-blind | single-blind | none>.
\documentclass[10pt,twocolumn]{<venue-class>}
\usepackage{<venue-style>}
\usepackage{amsmath,amssymb,amsfonts,bm}
\usepackage{graphicx,booktabs,multirow,siunitx}
\usepackage{algorithm,algpseudocode}
\usepackage{url}
\usepackage[pagebackref=false,breaklinks=true]{hyperref}

% Axis block. Fill the fields for the primary axis; delete the others.
% det:   resolution, TTA, NMS policy, AP convention
% track: detector provenance, public/private, online/offline, GPU
% reid:  resolution and crop policy, re-ranking on/off, query mode
% cnav:  architecture, exchange, delay, loss
% filt:  Monte Carlo count N, NEES/ANEES, chi-square bounds
\newcommand{\protocolblock}{<axis-critical protocol fields, one line>}

\title{<Contribution-bearing title, no marketing adjective>}
\author{<authors or Anonymous submission>}

\begin{document}
\maketitle

\begin{abstract}
% Numbers here must match the body exactly and have comparable ledger rows.
<problem sentence. gap sentence. method sentence. evidence sentence with value, units, run count,
dispersion, and protocol. boundary sentence.>
\end{abstract}

\section{Introduction}
% Para 1: task and why it matters, cited.
% Para 2: the specific limitation of current best, nearest competitor named.
% Para 3: the idea, in one sentence.
% Contribution list: three to four items, each naming its experiment or table.
\begin{itemize}
  \item \textbf{<contribution 1>} <one sentence, with the supporting experiment named>.
  \item \textbf{<contribution 2>} <...>.
  \item \textbf{<contribution 3>} <...>.
\end{itemize}

\section{Related Work}
% Subsections named after the distinction the paper turns on, not after method families.
\subsection{<Distinction A>}
\subsection{<Distinction B>}
% Close with the gap, derived from the differences above.

\section{Method}
\subsection{Problem formulation}
% Symbols defined at first use, consistent with ctrl-shared terminology-and-notation.
\subsection{<Component 1, the mechanism>}
\subsection{<Component 2>}
\subsection{<Component 3>}
\subsection{Implementation details}
% The details that change results: sampling, initialization, schedules, and their selection rule.

\section{Experiments}
\subsection{Datasets and evaluation protocol}
% One protocol block per comparison, or a pointer to the appendix block.
\subsection{Comparison with the state of the art}
\subsection{Ablation study}
\subsection{<Robustness, scaling, or failure analysis>}
\subsection{Limitations}
% Findings, tied to measured results. Simulation/field labels present.

\section{Discussion}
% Interpretations tied to measured results; mechanism claims separated from empirical findings.

\section{Conclusion}
% No new claim, no new number, no new citation.

\bibliographystyle{<venue-style>}
\bibliography{<bibfile>}

\appendix
\section{Protocol blocks}
% The full per-axis blocks, so that the numbers in the tables are auditable.
\section{Proofs}
% The closing arguments for every stated property, including the hard case.
\section{Additional results}
% Negative results, per-node or per-class breakdowns, and the losing cases.
\end{document}
```

## Table skeleton

```latex
\begin{table}[t]
  \centering
  \caption{<Comparison> on <dataset, split>. <Metric conventions>. Values are the mean over
  $N$ seeds and $\pm$ is the sample standard deviation. \protocolblock. Rows marked
  \emph{not comparable} use <the difference>; see protocol <P-axis-n>.}
  \label{tab:main}
  \begin{tabular}{lcccc}
    \toprule
    Method & <Protocol labels> & <Metric A> & <Metric B> & <Cost> \\
    \midrule
    <Baseline, reported>   & <its protocol>  & <value> & <value> & <value> \\
    <Baseline, re-impl.>   & \protocolblock  & <mean> $\pm$ <sd> & <mean> $\pm$ <sd> & <value> \\
    <Ours>                 & \protocolblock  & <mean> $\pm$ <sd> & <mean> $\pm$ <sd> & <value> \\
    \bottomrule
  \end{tabular}
\end{table}
```

Bold only a value that is best under a matched protocol. A `not comparable` value is never bolded,
even when it is numerically the largest.

## Figure skeleton

```latex
\begin{figure}[t]
  \centering
  \includegraphics[width=\linewidth]{fig/fig<n>-<slug>.pdf}
  \caption{<what is plotted, under which protocol, with what the reader should conclude>.
  <Simulation | Field data>. Source: \texttt{fig/fig<n>-<slug>.py}.}
  \label{fig:<slug>}
\end{figure}
```

Every figure has its generating script beside it, per
`../../ctrl-shared/core/artifact-contract.md`. A figure whose script is missing is a `G2` failure.

## Algorithm skeleton

```latex
\begin{algorithm}[t]
  \caption{<Named algorithm, with the setting it assumes>}
  \label{alg:<slug>}
  \begin{algorithmic}[1]
    \State \textbf{Input:} <inputs, with the communication each agent needs>
    \State \textbf{Output:} <outputs>
    \For{<each agent or each time step>}
      \State <operation, with the node that performs it made explicit for cnav>
    \EndFor
  \end{algorithmic}
\end{algorithm}
```

For `cnav`, the algorithm must show which agent performs each operation. An algorithm whose steps
are written for a single implicit node while the paper claims a distributed implementation is the
centralization defect that reviewers in that class look for first.

## Bilingual abstract block for a Chinese-language venue

```latex
\begin{abstract}
% 中文摘要: a real summary, not a translation. Same claims and same numbers as the English one.
<目的、方法、结果、结论，含具体数值与实验条件。>
\keywords{<关键词，3 到 8 个>}
\end{abstract}

\begin{abstract}[english]
<English abstract with the same claims and the same numbers.>
\keywords{<keywords>}
\end{abstract}

% 中图分类号 and 文献标识码 where the venue requires them.
% 基金项目 acknowledgment in the venue's required format.
```

The two abstracts must agree on every number
(`references/reconciliation-and-notation.md`, bilingual pass).

## Structural checks

```text
[ ] Class and style files are the current official ones, with the version recorded
[ ] Page limit respected, with the reference section treatment per the venue
[ ] Anonymity: no author names, no acknowledgments, no self-identifying repository links
[ ] Every figure has its generating script, and every table has its source data
[ ] Protocol blocks present, in the text or in the appendix, and referenced from every table
[ ] Every number in the abstract appears identically in the body
[ ] Every claim's strength matches its promotion condition
[ ] Simulation and field results labeled in captions and in prose
[ ] References complete, checked against sources, and formatted per the venue
[ ] Section budget roughly within the shares in references/section-workflow.md
```
