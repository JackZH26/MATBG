# PRB Submission Package Build Note

Date: 2026-06-10

The local package builder is:

```bash
python3 scripts/build_prb_submission_package.py
```

Default package name:

```text
MATBG_PRB_submission_checkpoint_2026-06-10
```

The package is written under the ignored directory:

```text
submission/build/
```

The tracked build summary is:

```text
data/processed/prb_submission_package_build.csv
```

The package contains two top-level payload directories:

```text
journal_upload/
provenance/
```

The 2026-06-10 package includes the response-to-reviewers draft in
`journal_upload/` and places source data, audit outputs, scripts, source code,
YAML configs, and provenance notes in `provenance/`.
