# Validate and maintain the skill pack

Run from the package root:

```powershell
node tools/validate-skills.cjs
node tools/check-dsh-discovery.cjs skills
node --test tools/skill-tools.test.cjs
node --test tools/install.test.cjs      # Windows only; uses temporary directories
```

## What each check proves

| Tool | Checks | Does not prove |
|---|---|---|
| [validate-skills.cjs](validate-skills.cjs) | real YAML frontmatter, names/types/keys, duplicate names, empty bodies, BOM, descriptions that fit the DSH catalog limit, resolvable relative links, explicit relative inline paths, bundle-root paths misused inside resource files, and qualified cross-skill paths | scientific correctness, full CommonMark semantics, heading-anchor existence or live activation |
| [check-dsh-discovery.cjs](check-dsh-discovery.cjs) | bundles/flat Markdown/junction discovery, invocation compatibility, all nine distinct expected names, and the catalog text each description produces | a live provider enabled/configured or visibility in this session |
| [skill-tools.test.cjs](skill-tools.test.cjs) | deterministic parser/discovery/validator fixtures, real-pack structure and behavioral-case schema | that every behavioral case was executed by a model |
| [install.test.cjs](install.test.cjs) | installer ownership rules on temporary roots: idempotent links, link-only removal, prefix-sibling links, unowned and modified directories, backups, dangling links, refusal of a target inside the source, and `-WhatIf` | behaviour on a real profile root, network drives or non-Windows systems |
| [evals.json](../evals/evals.json) | 36 behavior specifications with assertions | an automatic pass report or a complete evaluation runner |
| [gallery.py](../skills/cse-figure-studio/scripts/gallery.py) | every figure template runs under a given theme and language with no error and no lint warning (text size, overlap, clipping, hairlines) | that a figure is correct for its data, or a visual judgement, which needs a person or a model to look at the output |

## The DSH catalog limit

DSH's `skill` tool lists each available skill to the model as one catalog line built from the
whitespace-normalized `description`, cut to `catalogDescriptionMaxLength` characters (default 500,
in `@deepseek-ai/dsh-tool-skill`) with `...` appended. Text beyond the limit never reaches the model,
and that is usually where trigger phrases sit. The validator and the discovery check therefore fail
any description longer than 500 characters after normalization. `whenToUse` is parsed by the
filesystem provider but is not shown in that catalog, so triggers belong in the description.

[skill-contract.cjs](skill-contract.cjs) is shared by both checks, replacing the earlier simplified
frontmatter reader and duplicated discovery parser. It uses the existing local `yaml` package;
no network download or new dependency installation occurs. On another machine:

- `DSH_RUNTIME_REFERENCE` is the **node_modules directory containing yaml**.
- `DSH_YAML_MODULE` is an explicit yaml module path.
- Otherwise a local yaml module or an ancestor's extracted runtime reference is used.

If none is available, fail with a dependency error rather than claim compatibility using an
approximate YAML reader. Invocation behavior matches the locally inspected DSH reference;
check it again after upgrading the runtime. Unknown frontmatter keys are a pack validation error,
even if a runtime version happens to ignore them.

## Safe file changes on Windows

Prefer version-guarded `read` / `edit` / `write`: read first, and re-read/rebase on a stale-version
error. Concurrent edits must not be overwritten. Normal checks are read-only; only the explicit
`--fix-bom` flag alters files to remove a BOM.

Windows PowerShell **5.1** `Set-Content -Encoding UTF8` and `Out-File -Encoding utf8` add a BOM.
PowerShell 7 defaults differ; inspect the actual version/encoding rather than treating every
PowerShell release identically. DSH's referenced skill parser requires the first line exactly
`---`; a BOM in SKILL.md breaks discovery. References are warned rather than treated as parser
failures. Do not use shell redirection to rewrite a skill entry casually.

```powershell
node tools/validate-skills.cjs --fix-bom
```

Relative Markdown links are checked, including angle-bracket paths containing spaces. Explicit
inline paths beginning `./` or `../` are checked outside fenced examples. Inline paths such as
`references/x.md` are bundle-root relative by convention: they are fine in SKILL.md, but inside a
resource file they must be links relative to that file, and a qualified form such as `cse-shared`
followed by `core/x.md` is checked against the named bundle. Example blocks do not have to exist as
source files. Anchor fragments are not validated. Resource references should use real clickable
links in each SKILL.md so they are discoverable and checkable.

Tests create uniquely named temporary fixtures, including local junctions, verify their exact
absolute root and remove only those fixtures. They do not install the pack into a real root or alter
profile config. For actual installation, inspect [INSTALL.md](../INSTALL.md); prefer a direct custom
skill root, and preview the installer with `-WhatIf`.
