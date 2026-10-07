# Snapshot comparison and design history

Prepared: 2026-10-07. Status: source-informed documentation draft, not a complete version genealogy or evaluation report.

## Evidence categories

**Inspected text** means the configuration's readable body was retrieved or supplied. **Historical lead** means a conversation-memory retrieval describes a change; it is not a recovered source file or a verbatim conversation export. **Interpretation** means the current author's analysis of design implications.

Only the maintainer-supplied v2.9 snapshot is included in this package. The other inspected artifacts remain private, so a public reader cannot independently reproduce their full comparison from this repository yet. Nothing below should be read as a verified byte-level diff of the entire historical collection.

## Inspected artifacts

| Artifact | Source and status | What the inspected text supports |
| --- | --- | --- |
| TJ Configuration v2.4 — Consolidated Edition | Readable private Drive artifact; source metadata records a 2026-09-21 upload | Independent judgment, premise verification, evidence distinctions, non-artificial alternatives, and a larger set of academic/learning task modules are present |
| TJ Configuration v2.9 — Calibrated Retrieval Edition | Complete maintainer-supplied text; preserved in [the versioned file](../prompt/v2.9.md) | Explicit existing-capability checks, current-state inspection, external-memory retrieval ordering, and non-mechanical alternatives are present |
| TJ Configuration v3.0 — Lean Evidence-Gated Edition | Readable private Drive document; source metadata records a 2026-09-23 save | Completeness before brevity, state precedence, selective retrieval/verification, minimal intervention, and memory-capture scope are present |

Storage dates are not original authorship dates, approval dates, deployment dates, or release dates. For the inspected v3.0 document, its immediately previous Drive revision contained only a byte-order mark; the revision history captures document creation and insertion, not the full prompt's intellectual development.

## Design differences that can be described now

### 1. Independence is not reflexive opposition

The inspected texts frame the goal as accurate judgment rather than agreement. v2.9 also explicitly rules out generating alternatives just to satisfy a format. A useful interpretation is that disagreement is conditional on evidence, not a performance of independence. The documents specify this target; they do not measure whether it is achieved.

### 2. The task includes knowing the system's actual state

v2.9 explicitly adds current-system inspection and a sequence from existing capabilities to a remaining gap and only then to custom design. It distinguishes prompt guidance from retrieval, validation, provenance, permissions, and source-of-truth controls. This is a design boundary, not evidence that those controls are deployed.

### 3. More checking is not automatically more useful

The inspected v3.0 text gates verification and retrieval on material need, prevents stale records from overriding newer direct evidence, and discourages new checkpoints or components that do not close a relevant uncertainty. It also requires decisive evidence and meaningful uncertainty to survive attempts at concision.

**Interpretation:** the design tension is between epistemic discipline and useful completion—not simply between a shorter and a longer prompt. This interpretation can guide a future case study but does not establish a causal improvement.

### 4. Missing sections do not establish deletion

The inspected v2.4 file contains teaching and academic task modules absent from the v2.9 text supplied here. Their absence from this artifact does not show that the maintainer abandoned them. They could have moved into other configuration layers; the full configuration inventory has not been reconciled.

## Unresolved historical questions

Conversation-memory retrieval returned leads for earlier consolidation, evidence-gated alternatives, existing-solutions-first revisions, and retrieval-policy separation. Those leads are kept in a separate private review memo rather than promoted to a public release chronology.

Two ambiguities need original-file confirmation: a different earlier proposal also used the label “v3.0,” and a memory-capture addition was discussed under “v2.9” although it is absent from the supplied snapshot. Identify historical artifacts by full title, source, observed timestamp, and hash—not a bare version number. Do not silently renumber, merge, or backfill them.

## How later evidence should be added

Keep an original snapshot separate from commentary. For each proposed addition, record the source artifact, the observed change, the reported reason, and any known limitation. Distinguish a maintainer request, an assistant proposal, approval, actual deployment, and an observed result. Only label a behavior as tested when a corresponding input, output, context, and evaluation record exist.

No baseline comparison, effect size, cross-model advantage, novelty claim, or researcher-ability judgment follows from this history alone.
