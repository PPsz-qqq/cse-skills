# Install the cse-* skill pack

The installable root is this package's `skills/` directory: nine bundles at
`<root>/<name>/SKILL.md`. Installing files and enabling a provider are separate operations.

`cse-figure-studio` also runs Python scripts. Data plots need Python 3 with matplotlib and numpy;
turning diagram SVGs into PDF or PNG needs a Chrome, Edge or Chromium (or `CSE_FIGURE_BROWSER`);
previews need Pillow. Check a machine with `python skills/cse-figure-studio/scripts/render.py --doctor`.

## DSH roots and prerequisites

Enable/configure `@deepseek-ai/dsh-skill-filesystem` in the intended DSH profile before expecting
live discovery. With default roots enabled, lower ranks take priority:

| Rank | Source | Path |
|---|---|---|
| 100 | project-dsh | `<projectRoot>/.dsh/skills` |
| 200 | project-agents | `<projectRoot>/.agents/skills` |
| 300 | custom | configured `customSkillDirs` |
| 400 | user-dsh | `<DSH_HOME>/skills`, default `~/.dsh/skills` |
| 500 | user-agents | `<DSH_AGENTS_HOME>/skills`, default `~/.agents/skills` |
| 600 | bundled | configured bundled root |

The local runtime reference finds the nearest ancestor containing `.git`; when none exists it
uses the session cwd as project root. Project rows do **not** disappear merely because `.git` is
absent. Check current provider settings and name collisions before selecting a destination.

Simplest maintenance setup: add the absolute path of this package's `skills/` to
`customSkillDirs`. No copying or junction is then required. This document does not change profile
configuration automatically.

## Installer

From the package root, with PowerShell 5.1 or PowerShell 7:

```powershell
powershell -File tools/install.ps1 -WhatIf      # preview, changes nothing
powershell -File tools/install.ps1
powershell -File tools/install.ps1 -Source .\skills -Target D:\skills -Mode copy
powershell -File tools/install.ps1 -Remove
```

The default source is in-package `skills/`, then the legacy sibling layout, then inline bundles.
The target honors `DSH_HOME`, falling back to the user home. Default mode creates Windows
junctions; copy mode creates snapshots that need re-running after source edits.

Ownership rules, enforced by [install.test.cjs](tools/install.test.cjs) on temporary roots:

| Destination found | Without `-Force` | With `-Force` |
|---|---|---|
| junction to this source's bundle | kept (link mode) or replaced | same |
| copy whose `.ctrl-skills-install.json` matches its files | replaced or removed | same |
| dangling link | replaced or removed; it holds no data | same |
| link to another location, including a path that merely shares the source's prefix | skipped | unlinked; its target is untouched |
| modified copy, or a directory or file the installer did not create | skipped | moved to `<Target>\.ctrl-skills-backup\<timestamp>\` |

Links are removed with a non-recursive call that deletes only the link. Nothing outside the
installer's own staging folder is ever deleted recursively, and a target inside the source tree is
refused. DSH scans only the top level of a root, so the backup folder is not discovered as a skill.

## Offline checks versus live availability

```powershell
node tools/validate-skills.cjs
node tools/check-dsh-discovery.cjs .\skills
node --test tools/skill-tools.test.cjs
node --test tools/install.test.cjs
```

Every description must stay within 500 characters after whitespace normalization: DSH's skill
catalog cuts longer descriptions at its default `catalogDescriptionMaxLength`, and the trigger
phrases at the end would never reach the model. Both checks fail on an over-long description.

The shared parser needs the local `yaml` package. Existing runtime-reference lookup works here;
on another machine set `DSH_RUNTIME_REFERENCE` to the runtime's **node_modules directory containing
`yaml`**, or `DSH_YAML_MODULE` to the yaml module path. Do not point it to the extracted-runtime
parent. No network installation or simplified YAML fallback is performed by the checks.

These commands check local files, parser compatibility and regression fixtures. They do not
prove a live provider is enabled, roots are configured, or the session catalog contains this pack.

To confirm live availability:

1. Inspect the intended profile's skill provider activation and configured roots.
2. Confirm a direct child bundle exists under a scanned root and its name is not shadowed.
3. Ask the skill tool to load `cse-shared` explicitly to inspect the contract, or a user-facing
   skill matching your task. A successful load, not an offline parse, is the live probe.
4. Check provider logs for skipped frontmatter, filesystem/watch failures and duplicate names.

When the provider is active and its watcher enabled/healthy, file changes invalidate the catalog
without a restart. Do not promise immediate visibility if the provider is inactive or watch is off.

## Manual junctions

From the package root; inspect the resolved source/target before running:

```powershell
$src = (Resolve-Path -LiteralPath '.\skills').Path
$dshBase = if ($env:DSH_HOME) { $env:DSH_HOME } else { Join-Path $HOME '.dsh' }
$dst = Join-Path $dshBase 'skills'
New-Item -ItemType Directory -Path $dst -Force | Out-Null
Get-ChildItem -LiteralPath $src -Directory |
  Where-Object { $_.Name -like 'cse-*' -and (Test-Path -LiteralPath (Join-Path $_.FullName 'SKILL.md')) } |
  ForEach-Object { New-Item -ItemType Junction -Path (Join-Path $dst $_.Name) -Target $_.FullName }
```

This does not replace existing destinations. A direct custom root is preferable when possible.

## Using the pack

See [QUICKSTART.zh-CN.md](docs/QUICKSTART.zh-CN.md) for Chinese examples and the distinction between
local editing, diagnosis, planning and finalization. Other packs may coexist; this one specializes
in the five control/vision axes and does not authorize training or submission by itself.
