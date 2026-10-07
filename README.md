# Epistemic AI Protocol

A personal, evolving research-assistant configuration: evidence before agreement, and checks that serve the task rather than replace it.

**Read the prompt:** [TJ Configuration v2.9 — Calibrated Retrieval Edition](prompt/v2.9.md)  
**Explore the design:** [Snapshot comparison and open questions](docs/evolution.md)

## What this demonstrates

This project documents a customized human–AI interaction workflow. Its design questions are practical: how should an assistant challenge an unsupported premise without inventing disagreement, use prior records without trusting stale summaries, and inspect existing capabilities before proposing new infrastructure?

The artifact is the prompt and its documented design choices—not a claim that instructions guarantee those behaviors. No comparative model evaluation is reported. The examples below are authored illustrations, not experimental results or captured model outputs.

| Failure mode addressed | Instruction in the v2.9 snapshot | Remaining limitation |
| --- | --- | --- |
| Agreement driven by user confidence | Keep evaluation standards fixed; revise conclusions for evidence or valid reasoning | The instruction does not establish that sycophancy has been eliminated |
| Reasoning from an unverified premise | Verify externally checkable premises that materially affect the conclusion | Source selection and interpretation can still fail |
| Building before inspecting | Existing capabilities → remaining gap → custom design | The assistant can still misunderstand the task or overbuild |
| Treating uncertain memory as current state | Retrieve relevant records and prefer newer direct evidence | Requires accessible records and correct state resolution |
| Producing objections to satisfy a format | Develop alternatives only when evidence makes them meaningful | Evidence strength remains a judgment, not a keyword check |

## An illustrative interaction

**Input:** “What fraction of errors in a dataset makes a study's conclusion invalid?”

**Failure pattern to avoid:** supplying a universal percentage without specifying the error process, analysis, or conclusion being tested.

**Intended response pattern:** identify the missing variables; distinguish random and systematic errors; define the conclusion or decision criterion; then recommend a sensitivity analysis for those assumptions. Do not invent a numerical threshold merely because the question asks for one.

This is a synthetic illustration written for this README. It is not a private correspondence extract, a baseline-versus-treatment comparison, or evidence that this prompt improves a model.

## Reuse and adaptation

Read [the complete snapshot](prompt/v2.9.md), then adapt a separate copy to your language, research domain, available tools, and workflow. Retain the versioned source when recording changes. The Chinese-response preference, research interests, Google Drive references, and `AI_Memory` dependency are deliberate parts of TJ's configuration; other users are not expected to reproduce that environment.

Copying the prompt does not install retrieval, grant permissions, create private records, or ensure identical behavior. Check what your environment actually supports. The surrounding memory and execution systems are not distributed here.

## Design history and provenance

The public-package snapshot is the complete v2.9 text supplied by the maintainer on 2026-10-07. It is preserved without edits. A private v2.4 artifact and a private **v3.0 — Lean Evidence-Gated Edition** were also inspected during preparation; [the comparison](docs/evolution.md) separates their observed text from incomplete historical recollections.

The selected snapshot is not asserted to be the latest private configuration. A version number alone is not enough to identify an artifact or establish a linear history. [The manifest](snapshots.json) records this file's title, source category, and SHA-256; [the changelog](CHANGELOG.md) records package preparation separately from prompt evolution.

The maintainer supplied the prompt and the publication requirements. These explanatory documents and the maintenance checks were prepared with AI assistance. This statement does not assign authorship of every historical wording choice or treat assistant suggestions as maintainer decisions.

## Maintenance checks

With Python 3.10 or later, run:

```sh
python3 tools/check_repository.py
python3 -m unittest discover -s tools -p 'test_*.py' -v
```

The checks cover snapshot integrity against a reviewed manifest, local Markdown file links, suspicious private-data patterns, and a small set of workflow restrictions. They do not assess reasoning quality, test model performance, verify external links, guarantee absence of secrets, or enforce publication authorization. Updating both a file and its manifest can defeat a checksum check; review is still required.

The included [GitHub Actions workflow](.github/workflows/validate.yml) is configured for pushes, pull requests, and manual dispatch after installation. It uses a GitHub-hosted runner, read-only repository permissions, a SHA-pinned checkout action, and no model API calls. A locally passing script is not evidence of a successful hosted workflow run. See [maintenance notes](docs/maintenance.md).

## License and maintainer

Maintained by **TJ / `hutianjie12345`**. Questions and proposed changes can be discussed through repository issues after publication; no support response time is promised.

The prompt and documentation are available under [CC BY 4.0](LICENSE), including commercial reuse and modification with attribution. The helper scripts and workflow configuration use [MIT](LICENSE-CODE). Both are provided as-is. Private source records and third-party rights are not licensed by this repository.
