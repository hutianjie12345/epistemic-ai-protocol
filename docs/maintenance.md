# Maintenance notes

The publication checks run locally without third-party Python packages. The optional hosted workflow reuses GitHub Actions rather than adding a scheduler, server, or model-based reviewer.

## Scope of the local checker

The checker validates the selected prompt against `snapshots.json`, checks that every Markdown prompt snapshot is registered, and resolves inline relative Markdown file links. It checks a limited set of recognizable credentials, private document links, email addresses, local user paths, and excluded binary/archive formats. The scanner reports a rule and location without printing the suspected secret. It does not inspect Git history, follow external links, resolve Markdown section anchors, recognize every Markdown extension, or provide a security guarantee.

The workflow check is deliberately bounded: it looks for read-only permissions, hosted-runner selection, a full-SHA checkout pin, no persisted checkout credentials, and absence of privileged triggers or secret expressions. This is not a full GitHub Actions schema validator.

## Running the checks

```sh
python3 tools/check_repository.py
python3 tools/check_repository.py --json
python3 -m unittest discover -s tools -p 'test_*.py' -v
```

A report can be saved outside the public tree using shell redirection. Do not copy the private source-review memo into this repository. Run the privacy check before a public push: a failing hosted job cannot undo information already published in a commit.

## Later snapshots

Add an actual source file under `prompt/` and review its source, title, and intended disclosure before registering its SHA-256 in `snapshots.json`. Do not generate missing prompt text from memory. Keep previous snapshots unchanged unless a separately documented correction is deliberately approved. A manifest can detect accidental changes; it cannot prove historical authenticity or authorize an update.

## Hosted workflow status

The workflow is a prepared configuration. Local execution tests the Python commands only. Installation, repository Actions settings, a real workflow run, and its final result must be checked before displaying a hosted passing-status badge. No badge or hosted-success claim is included in this draft.

The configuration uses `push`, `pull_request`, and `workflow_dispatch`, `contents: read`, a GitHub-hosted runner, and `persist-credentials: false`. The `actions/checkout` commit was resolved from its official v4 ref and its action definition inspected on 2026-10-07. Its use is pinned, not floating. No paid model API or local MSI runner is involved.

## References

GitHub documentation: [README purpose and relative links](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-readmes), [workflow syntax](https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax), and [secure use](https://docs.github.com/en/actions/reference/security/secure-use). These support platform behavior and security choices, not the effectiveness of the prompt.
