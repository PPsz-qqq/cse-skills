# Validate and maintain the skill pack

Run from the package root:

```powershell
node tools/validate-skills.cjs
node tools/check-dsh-discovery.cjs skills
node --test tools/skill-tools.test.cjs
```

## What each check proves

| Tool | Checks | Does not prove |
|---|---|---|
| [validate-skills.cjs](validate-skills.cjs) | real YAML frontmatter, names/types/keys, duplicate names, empty bodies, BOM, resolvable relative links and explicit relative inline paths | scientific correctness, full CommonMark semantics, heading-anchor existence or live activation |
| [check-dsh-discovery.cjs](check-dsh-discovery.cjs) | bundles/flat Markdown/junction discovery, invocation compatibility and all eight distinct expected names | a live provider enabled/configured or visibility in this session |
| [skill-tools.test.cjs](skill-tools.test.cjs) | deterministic parser/discovery/validator fixtures, real-pack structure and behavioral-case schema | that every behavioral case was executed by a model |
| [evals.json](../evals/evals.json) | 26 behavior specifications with assertions | an automatic pass report or a complete evaluation runner |

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
inline paths beginning `./` or `../` are checked outside fenced examples. Example blocks do not
have to exist as source files. Anchor fragments are not validated. Resource references should
use real clickable links in each SKILL.md so they are discoverable and checkable.

Tests create uniquely named temporary fixtures, including local junctions, verify their exact
absolute root and remove only those fixtures. They do not install the pack or alter profile config.
For actual installation, inspect [INSTALL.md](../INSTALL.md); prefer a direct custom skill root.
Do not run the legacy installer's destructive `-Force` option on an unreviewed target.
