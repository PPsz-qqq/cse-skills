#!/usr/bin/env node
// Validator for the ctrl-* skill pack.
// Checks frontmatter, naming, BOM, invocation keys, and that every relative path resolves.
// Usage: node tools/validate-skills.cjs [skillsRoot] [--fix-bom]
// With no skillsRoot, the sibling `skills/` directory is used, falling back to the package root.
'use strict';
const fs = require('fs');
const path = require('path');

const stripBom = process.argv.includes('--fix-bom');

// The bundles live in a dedicated skill root, normally the `skills/` subdirectory of this
// package. Fall back to the package root so the check still works when the bundles are stored
// inline. Never return a root with no bundles: scanning nothing must not look like success.
function resolveDefaultRoot() {
  const pkgRoot = path.join(__dirname, '..');
  const candidates = [
    path.join(pkgRoot, 'skills'),      // this package's skill root
    path.join(pkgRoot, '..', 'skills'), // sibling layout
    pkgRoot,                            // bundles stored inline
  ];
  for (const candidate of candidates) {
    if (!fs.existsSync(candidate)) continue;
    const hasBundle = fs.readdirSync(candidate, { withFileTypes: true })
      .some((d) => d.isDirectory() && d.name.startsWith('ctrl-')
        && fs.existsSync(path.join(candidate, d.name, 'SKILL.md')));
    if (hasBundle) return candidate;
  }
  return path.join(pkgRoot, 'skills');
}

const rootArg = process.argv.slice(2).find((a) => !a.startsWith('--'));
const root = path.resolve(rootArg || resolveDefaultRoot());
const NAME_RE = /^[a-z0-9]+(-[a-z0-9]+)*$/;
const VALID_KEYS = new Set([
  'name', 'description', 'whenToUse', 'metadata', 'license',
  'disable-model-invocation', 'user-invocable', 'allowed-tools',
]);
const BOOL_TRUE = new Set(['true', 'yes', 'on', '1']);
const BOOL_FALSE = new Set(['false', 'no', 'off', '0']);
// Directories that legitimately live beside the skill bundles in this pack.
const NON_SKILL_DIRS = new Set(['tools', 'docs', 'scripts', 'evals', '_research', 'node_modules', '.git']);

const problems = [];
const warnings = [];
const report = [];

function fail(file, msg) { problems.push(`${file}: ${msg}`); }
function warn(file, msg) { warnings.push(`${file}: ${msg}`); }

function stripQuotes(s) {
  const t = s.trim();
  if ((t.startsWith('"') && t.endsWith('"')) || (t.startsWith("'") && t.endsWith("'"))) {
    return t.slice(1, -1);
  }
  return t;
}

// Minimal YAML frontmatter reader: top-level scalar keys plus block scalars.
function parseFrontmatter(text) {
  const m = /^---\r?\n([\s\S]*?)\r?\n---(\r?\n|$)/.exec(text);
  if (!m) return null;
  const lines = m[1].split(/\r?\n/);
  const data = {};
  for (let i = 0; i < lines.length; i += 1) {
    const line = lines[i];
    if (!line.trim() || line.trim().startsWith('#')) continue;
    const kv = /^([A-Za-z][A-Za-z0-9_-]*):(.*)$/.exec(line);
    if (!kv) {
      if (!/^\s/.test(line)) return { data, malformed: line };
      continue;
    }
    const key = kv[1];
    let rest = kv[2];
    if (/^\s*[>|][-+]?\s*$/.test(rest)) {
      const block = [];
      let indent = null;
      while (i + 1 < lines.length) {
        const next = lines[i + 1];
        if (!next.trim()) { block.push(''); i += 1; continue; }
        const lead = next.match(/^\s*/)[0].length;
        if (indent === null) {
          if (lead === 0) break;
          indent = lead;
        } else if (lead < indent) break;
        block.push(next.slice(indent));
        i += 1;
      }
      data[key] = block.join(' ').replace(/\s+/g, ' ').trim();
    } else if (/^\s*$/.test(rest)) {
      const items = [];
      let j = i + 1;
      while (j < lines.length && /^\s*[-*]\s+/.test(lines[j])) {
        items.push(lines[j].replace(/^\s*[-*]\s+/, '').trim());
        j += 1;
      }
      if (items.length) { data[key] = items.join(' '); i = j - 1; } else { data[key] = ''; }
    } else {
      data[key] = stripQuotes(rest);
    }
  }
  return { data };
}

// Collect relative markdown links [text](target) and check they resolve on disk.
function checkLinks(file, text) {
  const dir = path.dirname(file);
  const re = /\[[^\]]*\]\(([^)\s]+)(?:\s+"[^"]*")?\)/g;
  let m;
  let count = 0;
  while ((m = re.exec(text)) !== null) {
    let target = m[1];
    if (/^(https?:|mailto:|#)/i.test(target)) continue;
    target = target.replace(/^<|>$/g, '').split('#')[0];
    if (!target) continue;
    count += 1;
    const resolved = path.resolve(dir, decodeURIComponent(target));
    if (!fs.existsSync(resolved)) {
      fail(path.relative(root, file), `broken relative link -> ${target}`);
    }
  }
  return count;
}

// Inline-code citations such as `../ctrl-shared/core/gate-contract.md` are not markdown
// links, so checkLinks never sees them. They resolve relative to the containing file, which
// means the same string is correct in SKILL.md and wrong one level deeper in references/.
// That failure is invisible unless it is checked explicitly.
function checkInlinePaths(file, text) {
  const dir = path.dirname(file);
  const re = /`([^`\n]*?(?:\.\.\/|\.\/)[^`\n]*?\.(?:md|py|json|csv|tex|ya?ml|sh|cjs|mjs|ps1|txt))`/g;
  let m;
  let count = 0;
  while ((m = re.exec(text)) !== null) {
    let target = m[1].trim().replace(/^<|>$/g, '').split('#')[0];
    if (!target || /^(https?:|mailto:)/i.test(target)) continue;
    count += 1;
    const resolved = path.resolve(dir, decodeURIComponent(target));
    if (!fs.existsSync(resolved)) {
      fail(
        path.relative(root, file),
        `broken inline-code path -> ${target} (resolved against ${path.relative(root, dir) || '.'})`,
      );
    }
  }
  return count;
}

function walkSkill(file) {
  const bytes = fs.readFileSync(file);
  const rel = path.relative(root, file).replace(/\\/g, '/');
  // A UTF-8 BOM breaks DSH's frontmatter parser, which requires the file to start with
  // exactly "---", and Windows PowerShell's `Set-Content -Encoding UTF8` adds one silently.
  if (bytes.length >= 3 && bytes[0] === 0xef && bytes[1] === 0xbb && bytes[2] === 0xbf) {
    if (stripBom) {
      fs.writeFileSync(file, bytes.subarray(3));
      warnings.push(`${rel}: stripped a UTF-8 BOM that would break frontmatter parsing`);
    } else {
      fail(rel, 'file starts with a UTF-8 BOM; the frontmatter parser requires the file to start with "---"');
    }
  }
  const text = fs.readFileSync(file, 'utf8');
  const dirName = path.basename(path.dirname(file));
  const fm = parseFrontmatter(text);
  if (!fm) { fail(rel, 'missing or malformed YAML frontmatter'); return; }
  const { data, malformed } = fm;
  if (malformed) fail(rel, `unparsable frontmatter line: ${JSON.stringify(malformed)}`);

  if (!data.name) fail(rel, 'frontmatter is missing required key "name"');
  else {
    if (!NAME_RE.test(data.name)) fail(rel, `name "${data.name}" is not lower-kebab-case`);
    if (data.name !== dirName) fail(rel, `name "${data.name}" does not match directory "${dirName}"`);
  }
  if (!data.description || !data.description.trim()) fail(rel, 'frontmatter is missing required key "description"');
  else {
    const len = data.description.length;
    if (len < 80) warn(rel, `description is short (${len} chars); triggers may not fire`);
    if (len > 1400) warn(rel, `description is long (${len} chars); the catalog renders a capped excerpt`);
  }
  for (const key of Object.keys(data)) {
    if (!VALID_KEYS.has(key)) fail(rel, `unknown frontmatter key "${key}"`);
    if (key === 'disable-model-invocation' || key === 'user-invocable') {
      const v = String(data[key]).toLowerCase();
      if (!BOOL_TRUE.has(v) && !BOOL_FALSE.has(v)) {
        fail(rel, `"${key}" must be a boolean spelling, got "${data[key]}"`);
      }
    }
  }

  const links = checkLinks(file, text);
  const inlinePaths = checkInlinePaths(file, text);
  const lineArr = text.split(/\r?\n/);
  const lines = lineArr.length;
  const closeIdx = lineArr.findIndex((l, i) => i > 0 && l.trim() === '---');
  const fmLines = closeIdx > 0 ? closeIdx + 1 : 0;
  if (fmLines === 0) fail(rel, 'frontmatter is not closed by a --- line');

  // Resource files in the bundle must be reachable from SKILL.md by a relative link.
  const linked = new Set();
  const re = /\[[^\]]*\]\(([^)\s]+)\)/g;
  let mm;
  while ((mm = re.exec(text)) !== null) {
    const t = mm[1].replace(/^<|>$/g, '').split('#')[0];
    if (!/^(https?:|mailto:|#)/i.test(t) && t) linked.add(path.normalize(t).replace(/\\/g, '/'));
  }
  const base = path.dirname(file);
  const dirs = ['references', 'core', 'assets', 'scripts', 'templates'];
  for (const d of dirs) {
    const p = path.join(base, d);
    if (!fs.existsSync(p)) continue;
    for (const entry of fs.readdirSync(p)) {
      if (!entry.endsWith('.md')) continue;
      const want = `${d}/${entry}`;
      if (!linked.has(want)) warn(rel, `resource "${want}" is not linked from SKILL.md`);
    }
  }

  if (fmLines > 40) warn(rel, `frontmatter spans ${fmLines} lines`);
  report.push({ skill: data.name || dirName, lines, links, inlinePaths });
}

// Walk every other markdown file in the bundle so that links inside reference
// files are checked too, not just the links in SKILL.md.
function walkResources(baseDir, skillRel) {
  const stack = [baseDir];
  const skip = new Set(['node_modules', '.git']);
  let checked = 0;
  while (stack.length) {
    const dir = stack.pop();
    for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
      if (skip.has(entry.name)) continue;
      const full = path.join(dir, entry.name);
      if (entry.isDirectory()) { stack.push(full); continue; }
      if (!entry.name.endsWith('.md')) continue;
      if (entry.name === 'SKILL.md' && dir === baseDir) continue; // already handled
      const rel = path.relative(root, full).replace(/\\/g, '/');
      const resBytes = fs.readFileSync(full);
      if (resBytes.length >= 3 && resBytes[0] === 0xef && resBytes[1] === 0xbb && resBytes[2] === 0xbf) {
        if (stripBom) {
          fs.writeFileSync(full, resBytes.subarray(3));
          warnings.push(`${rel}: stripped a UTF-8 BOM`);
        } else {
          warn(rel, 'file starts with a UTF-8 BOM');
        }
      }
      const text = fs.readFileSync(full, 'utf8');
      checked += checkLinks(full, text);
      checked += checkInlinePaths(full, text);
      if (/(^|\s)(TODO|TBD|FIXME|XXX)[:!]/.test(text) || /\[(TODO|TBD|FIXME|XXX)\]/.test(text)) {
        warn(rel, 'contains an unresolved TODO/TBD/FIXME/XXX marker; resolve it or mark it [UNVERIFIED]');
      }
      if (text.trim().length === 0) fail(rel, 'file is empty');
    }
  }
  return checked;
}

function main() {
  if (!fs.existsSync(root)) { console.error(`skills root not found: ${root}`); process.exit(2); }
  const dirs = fs.readdirSync(root, { withFileTypes: true }).filter((d) => d.isDirectory());
  let found = 0;
  for (const d of dirs) {
    const skillFile = path.join(root, d.name, 'SKILL.md');
    if (fs.existsSync(skillFile)) {
      found += 1;
      walkSkill(skillFile);
      const resourceLinks = walkResources(path.dirname(skillFile), d.name);
      const last = report[report.length - 1];
      if (last) last.resourceLinks = resourceLinks;
    } else if (!NON_SKILL_DIRS.has(d.name)) {
      warn(`${d.name}/`, 'directory has no SKILL.md, so it is not discoverable as a skill');
    }
  }
  console.log(`scanned ${found} skill(s) under ${root}`);
  // Scanning nothing while reporting success is the most dangerous outcome this tool can
  // produce: a moved or mistyped root would look like a clean pack. Refuse to pass.
  if (found === 0) {
    console.error('');
    console.error('FAIL: no skill bundles found at that root, so nothing was validated.');
    console.error('Pass the skill root explicitly, for example:');
    console.error('  node tools/validate-skills.cjs ../skills');
    process.exit(1);
  }
  for (const r of report) {
    console.log(`  ok  ${r.skill.padEnd(28)} ${String(r.lines).padStart(4)} lines, ${r.links} links + ${r.inlinePaths} inline paths in SKILL.md, ${r.resourceLinks || 0} checked in resources`);
  }
  // Check the package's own markdown before reporting, so its findings are printed too.
  checkPackageDocs(path.join(__dirname, '..'));
  if (warnings.length) {
    console.log(`\n${warnings.length} warning(s):`);
    for (const w of warnings) console.log(`  warn  ${w}`);
  }
  if (problems.length) {
    console.log(`\n${problems.length} problem(s):`);
    for (const p of problems) console.log(`  FAIL  ${p}`);
    process.exit(1);
  }
  console.log('\nno problems found');
}

// The package's own markdown (README, INSTALL, INTEGRATION, tools/README) lives outside the
// skill root but links into it, so a layout change can silently break those paths.
function checkPackageDocs(pkgRoot) {
  const docs = [];
  const stack = [pkgRoot];
  const skip = new Set(['node_modules', '.git', '_research']);
  while (stack.length) {
    const dir = stack.pop();
    for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
      if (skip.has(entry.name)) continue;
      const full = path.join(dir, entry.name);
      if (entry.isDirectory()) { stack.push(full); continue; }
      if (entry.name.endsWith('.md')) docs.push(full);
    }
  }
  let checked = 0;
  for (const doc of docs) {
    const rel = path.relative(pkgRoot, doc).replace(/\\/g, '/');
    const text = fs.readFileSync(doc, 'utf8');
    checked += checkLinks(doc, text);
    checked += checkInlinePaths(doc, text);
    if (/(^|\s)(TODO|TBD|FIXME|XXX)[:!]/.test(text) || /\[(TODO|TBD|FIXME|XXX)\]/.test(text)) {
      warn(rel, 'contains an unresolved TODO/TBD/FIXME/XXX marker');
    }
  }
  if (docs.length) console.log(`\npackage docs: ${docs.length} file(s), ${checked} relative path(s) checked`);
}

main();
