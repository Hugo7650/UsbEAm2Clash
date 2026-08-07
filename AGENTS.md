# Repository Guidelines

## Project Structure & Module Organization

- `src/UsbEAm2Clash.py` is the Python generator. It reads the two UsbEAm input snapshots and writes Clash domain rules.
- `src/Clash2Singbox.py` converts the generated Clash YAML rules into sing-box source JSON files.
- `UsbEAm.ini` and `UsbEAm_console.ini` are the upstream rule inputs.
- `Clash/` contains generated YAML rule sets, including platform files and `_Download` variants. `Clash/XBOX/` contains the nested Microsoft Store rules.
- `Sing-box/` contains generated sing-box JSON source rules with the same names and directory layout as `Clash/`.
- `mrs/` contains generated Mihomo MRS equivalents with the same names and directory layout as `Clash/`.
- `srs/` contains generated sing-box binary rules with the same names and directory layout as `Sing-box/`.
- `.github/workflows/update.yml` is the scheduled/manual update pipeline. There is no dedicated `tests/` directory; the rule files are the primary deliverables.

## Build, Test, and Development Commands

Run commands from the repository root:

```powershell
py -3.10 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python src\UsbEAm2Clash.py
python src\Clash2Singbox.py --source Clash --output Sing-box
python -m py_compile src\UsbEAm2Clash.py src\Clash2Singbox.py
```

The first script refreshes `Clash/**/*.yaml`; run the sing-box conversion script afterward to refresh `Sing-box/**/*.json`. MRS output requires Mihomo; use `mihomo convert-ruleset domain yaml` (for example, `Clash/Steam.yaml` to `mrs/Steam.mrs`). SRS output requires sing-box; use `sing-box rule-set compile --output srs/Steam.srs Sing-box/Steam.json`. The GitHub Actions workflow installs the latest Mihomo and sing-box releases and regenerates all output formats together.

## Coding Style & Naming Conventions

Use UTF-8 Python with four-space indentation and keep the existing small, procedural style. Preserve nearby naming conventions such as `saveRules` and `getGroup`, and avoid unrelated reformatting. Generated files use platform names with underscores, for example `Ubisoft_Connect(Uplay)_Download.yaml`; matching `.json`, `.mrs`, and `.srs` names and directory paths must be preserved. YAML uses two-space indentation and a `payload` list. Sing-box JSON uses two-space indentation, `version: 3`, and a `rules` list containing domain entries.

No formatter or linter is configured. Keep type hints and short comments where they clarify non-obvious parsing or grouping logic.

## Testing Guidelines

No automated test framework or coverage target is currently configured. For generator changes, run the compile check, regenerate all rule formats, verify that every Clash YAML has a matching JSON and SRS file, inspect representative YAML and JSON files, and confirm compiled SRS files are non-empty. Validate README links when rule names or directories change. If tests are added, place them under `tests/` and use `test_*.py` names.

## Generated Files and Updates

Treat `Clash/`, `Sing-box/`, `mrs/`, and `srs/` as generated artifacts. Change the generator or input data first, then regenerate all affected outputs together. `Sing-box/` mirrors `Clash/`, and `srs/` mirrors `Sing-box/`; preserve the `XBOX/` subdirectory to avoid collisions with top-level Microsoft Store rules. Review large upstream input diffs carefully, especially before committing scheduled-update results.

## Commit & Pull Request Guidelines

History uses short imperative subjects, such as `Add MRS conversion workflow` and the automated `Update UsbEAm rules`. Follow that pattern. Pull requests should explain the input or generator change, list regenerated `Clash/`, `Sing-box/`, `mrs/`, and `srs/` artifacts, describe README table changes when applicable, include validation commands/results, and link a related issue when one exists. Screenshots are unnecessary unless documentation presentation changes.
