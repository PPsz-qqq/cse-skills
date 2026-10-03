# Writing files in this pack safely on Windows

Windows PowerShell's `Set-Content -Encoding UTF8` writes a **byte-order mark** at the start of
the file, and `Out-File -Encoding utf8` does the same. DSH's skill provider requires a skill
file to begin with exactly `---`, so a BOM makes the whole skill silently undiscoverable: the
provider logs a warning and the model catalog simply never shows it.

This is the single most damaging mechanical mistake available in this repository, because it is
invisible in most editors and produces no error at write time. Twelve files in this pack were
briefly corrupted this way during development.

## Rules

1. Prefer the `write` and `edit` tools for every file change. They write UTF-8 without a BOM and
   they preserve the rest of the file.
2. Do not use `Set-Content`, `Out-File`, or `>` redirection to rewrite a markdown file. If you
   must use PowerShell, write bytes explicitly:

   ```powershell
   [System.IO.File]::WriteAllText($path, $text, (New-Object System.Text.UTF8Encoding($false)))
   ```

   On PowerShell 5.1 in ConstrainedLanguage mode the static call fails; use a different tool
   instead of falling back to `Set-Content`.
3. Guard every pipeline that writes markdown with the validator, which detects a BOM:

   ```powershell
   node tools/validate-skills.cjs
   ```

   It fails on a BOM by default, and repairs it with `--fix-bom`:

   ```powershell
   node tools/validate-skills.cjs --fix-bom
   ```

4. Add no BOM to `SKILL.md` specifically. A BOM in a reference file is merely untidy; a BOM in
   `SKILL.md` breaks discovery of the entire bundle.

## Why the validator also checks inline paths

The same class of silent failure applies to relative paths. A path like `../ctrl-shared/core/`
plus a filename is correct in a `SKILL.md` and wrong inside `references/`, where it resolves one
level too high. Nothing warns you, because the file simply is not found at read time. The
validator therefore checks three things separately:

| Check | Catches |
|---|---|
| markdown links in every `.md` | a link target that does not resolve |
| inline-code paths in every `.md` | a backticked relative path that does not resolve |
| frontmatter and BOM in `SKILL.md` | a bundle that will not be discovered |

Write real examples only if the target is real, since the checker treats every backticked
relative path as a citation and will flag a fictional one.

A fourth check confirms the real contract: `node tools/check-dsh-discovery.cjs` runs DSH's own
frontmatter parser over the installed skill root and reports what the Harness will actually see.
Run it after any change to frontmatter or to the install layout.
