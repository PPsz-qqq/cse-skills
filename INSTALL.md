# Install the ctrl-* skill pack

The pack is a directory of skill bundles. Each bundle is `<name>/SKILL.md`, which is exactly
what DSH's filesystem skill provider discovers at the top level of a scanned root.

## Where DSH looks

Scanned roots, in priority order:

| Rank | Source | Path |
|---|---|---|
| 100 | `project-dsh` | `<projectRoot>/.dsh/skills` |
| 200 | `project-agents` | `<projectRoot>/.agents/skills` |
| 300 | `custom` | the provider's configured `customSkillDirs` |
| 400 | `user-dsh` | `<DSH_HOME>/skills`, default `~/.dsh/skills` |
| 500 | `user-agents` | `<DSH_AGENTS_HOME>/skills`, default `~/.agents/skills` |
| 600 | `bundled` | the configured bundled root |

`<projectRoot>` is the nearest ancestor containing `.git`. In this session the working
directory has no `.git` ancestor at `F:\dsh-test`, so the project rows do not apply and the user
root at `%USERPROFILE%\.dsh\skills` is the correct destination.

## Install

From the `ctrl-skills` package root:

```powershell
powershell -File tools/install.ps1
```

The scripts default to the sibling skill root `../skills/`, which is where the eight bundles
live, and fall back to the package root if the bundles are stored inline. The default mode
creates a directory junction per bundle under `~/.dsh/skills`. A junction needs no elevation on
Windows, and because it points at `skills/`, edits there are live and DSH's watcher picks them up.

Other forms:

```powershell
# install from an explicit skill root
powershell -File tools/install.ps1 -Source ..\skills

# install a copied snapshot into a different root
powershell -File tools/install.ps1 -Mode copy -Target D:\skills

# remove only the links this script created
powershell -File tools/install.ps1 -Remove

# replace an existing non-linked destination
powershell -File tools/install.ps1 -Force
```

Note that `pwsh` is not present on every Windows install. Use `powershell` when only Windows
PowerShell 5.1 is available; the script is written to work on both.

Safety properties, which the script enforces rather than documents:

- it refuses to operate when the skill root resolves to the repository itself;
- it never deletes a destination unless the destination is a link whose target resolves inside
  this repository, or unless `-Force` is passed explicitly;
- a failure on one bundle does not abort the rest, and the script exits non-zero if any failed.

## Verify discovery

The provider watches its roots, so no restart is needed. Confirm the pack is live:

1. Check the links exist:

   ```powershell
   Get-ChildItem $env:USERPROFILE\.dsh\skills -Directory | Where-Object Name -like 'ctrl-*'
   ```

2. In a DSH session, load one skill through the skill tool. `ctrl-shared` is a safe probe; it is
   the shared contract and is also a usable standalone entry point.

3. If a bundle is missing from the catalog, the cause is almost always frontmatter. DSH skips a
   file whose `name` is not kebab-case, whose `description` is empty, or whose invocation key has
   an invalid boolean spelling, and it reports no per-skill diagnostic to the model. Run the
   validator to find it:

   ```powershell
   node tools/validate-skills.cjs
   ```

   With no argument it checks the sibling `../skills/` root. It exits non-zero if it finds no
   bundles at all, so a mistyped root cannot look like a clean pack.

## Uninstall

```powershell
powershell -File tools/install.ps1 -Remove
```

For a copy-mode install, pass the same `-Target` and `-Mode copy`. Deleting the links leaves
`skills/` untouched.

## Manual install

If you would rather not run the script, create one junction or copy per bundle. Each command
below is equivalent to one line of the script's output:

```powershell
$src = Join-Path (Split-Path -Parent $PSScriptRoot) 'skills'
$dst = Join-Path $env:USERPROFILE '.dsh\skills'
Get-ChildItem $src -Directory |
  Where-Object { $_.Name -like 'ctrl-*' -and (Test-Path (Join-Path $_.FullName 'SKILL.md')) } |
  ForEach-Object { New-Item -ItemType Junction -Path (Join-Path $dst $_.Name) -Target $_.FullName }
```

## Coexistence with other installed packs

This pack does not modify, depend on, or shadow any other installed skill. It is designed to sit
alongside the existing `nature-*` and `academic-*` packs, which serve the natural sciences and
general academic writing. If both packs cover a request, prefer this one for the five control
axes and delegate general scientific-writing polish to the other pack, since its style rules are
tuned for the natural-science literature rather than for engineering venues.
