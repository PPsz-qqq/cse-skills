#!/usr/bin/env node
// Replicates DSH's own skill discovery path against a real skill root, using the same
// `yaml` parser version that @deepseek-ai/dsh-skill-filesystem depends on (^2.4.2, resolved
// to 2.9.1 here). This is the acceptance test that matters: our own validator can be wrong,
// but this reproduces what the Harness actually does.
//
// Mirrors dsh-skill-filesystem/lib/index.js:
//   parseFrontmatter -> stringField(name) -> stringField(description) -> isSkillName ->
//   parseInvocationPolicy
'use strict';
const fs = require('node:fs');
const path = require('node:path');

// Locate the extracted DSH runtime reference, which carries the same `yaml` version that
// @deepseek-ai/dsh-skill-filesystem depends on. Search upward from this script, then allow
// an explicit override so the check still runs from a packaged copy of the pack.
function findYamlDir() {
  const candidates = [];
  if (process.env.DSH_RUNTIME_REFERENCE) candidates.push(process.env.DSH_RUNTIME_REFERENCE);
  let dir = __dirname;
  for (let i = 0; i < 6; i += 1) {
    candidates.push(path.join(dir, '.runtime-reference', 'dsh', 'node_modules'));
    const parent = path.dirname(dir);
    if (parent === dir) break;
    dir = parent;
  }
  for (const base of candidates) {
    const yamlDir = path.join(base, 'yaml');
    if (fs.existsSync(path.join(yamlDir, 'package.json'))) return yamlDir;
  }
  return undefined;
}

const yamlDir = findYamlDir();
let YAML;
try {
  YAML = yamlDir ? require(yamlDir) : require('yaml');
} catch (error) {
  console.error('Cannot load the yaml parser used by DSH.');
  console.error('Set DSH_RUNTIME_REFERENCE to the directory containing .runtime-reference,');
  console.error('or install the yaml package next to this script.');
  console.error(`Cause: ${error.message}`);
  process.exit(2);
}
const yamlVersion = (() => {
  try {
    return yamlDir ? require(path.join(yamlDir, 'package.json')).version : 'unknown';
  } catch {
    return 'unknown';
  }
})();
const root = path.resolve(process.argv[2] || path.join(process.env.USERPROFILE || '', '.dsh', 'skills'));

// --- functions lifted in behaviour from the provider ---
function parseFrontmatter(raw) {
  const firstLineEnd = raw.indexOf('\n');
  if (firstLineEnd < 0) return undefined;
  if (raw.slice(0, firstLineEnd).replace(/\r$/, '') !== '---') return undefined;
  const start = firstLineEnd + 1;
  const closing = findClosingFrontmatter(raw, start);
  if (closing === undefined) return undefined;
  const parsed = YAML.parse(raw.slice(start, closing.start));
  if (typeof parsed !== 'object' || parsed === null || Array.isArray(parsed)) return undefined;
  return { data: parsed, body: raw.slice(closing.bodyStart) };
}
function findClosingFrontmatter(raw, start) {
  let lineStart = start;
  while (lineStart <= raw.length) {
    const nextNewline = raw.indexOf('\n', lineStart);
    const lineEnd = nextNewline < 0 ? raw.length : nextNewline;
    if (raw.slice(lineStart, lineEnd).replace(/\r$/, '') === '---') {
      return { start: lineStart, bodyStart: nextNewline < 0 ? raw.length : nextNewline + 1 };
    }
    if (nextNewline < 0) return undefined;
    lineStart = nextNewline + 1;
  }
  return undefined;
}
function stringField(data, key) {
  const value = data[key];
  return typeof value === 'string' && value.length > 0 ? value : undefined;
}
function isSkillName(name) {
  return /^[a-z0-9]+(?:-[a-z0-9]+)*$/.test(name);
}
const BOOLEAN_TRUE = new Set(['true', 'yes', 'on', '1']);
const BOOLEAN_FALSE = new Set(['false', 'no', 'off', '0']);
function frontmatterBoolean(data, key) {
  if (!Object.hasOwn(data, key)) return undefined;
  const value = data[key];
  if (typeof value === 'boolean') return value;
  if (typeof value !== 'string') throw new TypeError(`frontmatter field "${key}" must be a boolean`);
  const normalized = value.trim().toLowerCase();
  if (BOOLEAN_TRUE.has(normalized)) return true;
  if (BOOLEAN_FALSE.has(normalized)) return false;
  throw new TypeError(`frontmatter field "${key}" must be a boolean`);
}
function parseInvocationPolicy(data) {
  return {
    disableModelInvocation: frontmatterBoolean(data, 'disable-model-invocation'),
    userInvocable: frontmatterBoolean(data, 'user-invocable'),
  };
}
function parseSkillFile(filePath) {
  let raw;
  try {
    raw = fs.readFileSync(filePath, 'utf8');
  } catch (error) {
    return { ok: false, reason: `unreadable: ${error.message}` };
  }
  let parsed;
  try {
    parsed = parseFrontmatter(raw);
  } catch (error) {
    return { ok: false, reason: `invalid YAML frontmatter: ${error.message}` };
  }
  if (!parsed) return { ok: false, reason: 'missing YAML frontmatter' };
  const name = stringField(parsed.data, 'name');
  const description = stringField(parsed.data, 'description');
  if (name === undefined || description === undefined) {
    return { ok: false, reason: 'frontmatter requires name and description' };
  }
  if (!isSkillName(name)) return { ok: false, reason: `invalid skill name "${name}"` };
  try {
    parseInvocationPolicy(parsed.data);
  } catch (error) {
    return { ok: false, reason: `invalid invocation frontmatter: ${error.message}` };
  }
  return { ok: true, name, description, body: parsed.body };
}

// --- discovery: <root>/<name>/SKILL.md and <root>/<name>.md, one level deep ---
if (!fs.existsSync(root)) {
  console.error(`skill root not found: ${root}`);
  process.exit(2);
}
const discovered = [];
const skipped = [];
for (const entry of fs.readdirSync(root, { withFileTypes: true })) {
  // Follow junctions: DSH's provider resolves symlinked directories as regular files.
  const full = path.join(root, entry.name);
  let isDir = entry.isDirectory();
  if (!isDir && (entry.isSymbolicLink() || entry.isDirectory)) isDir = true;
  if (!isDir && !entry.isFile()) {
    try { isDir = fs.statSync(full).isDirectory(); } catch { isDir = false; }
  }
  let skillFile;
  if (isDir) {
    try {
      if (!fs.statSync(full).isDirectory()) continue;
    } catch { continue; }
    skillFile = path.join(full, 'SKILL.md');
    if (!fs.existsSync(skillFile)) continue;
  } else if (entry.name.endsWith('.md')) {
    skillFile = full;
  } else {
    continue;
  }
  const result = parseSkillFile(skillFile);
  if (result.ok) discovered.push({ ...result, file: skillFile });
  else skipped.push({ file: skillFile, reason: result.reason });
}

console.log(`DSH parser (yaml ${yamlVersion}) over ${root}`);
console.log(`discovered ${discovered.length} skill(s), skipped ${skipped.length}`);
console.log('');
const wanted = discovered.filter((d) => d.name.startsWith('ctrl-'));
for (const d of discovered.sort((a, b) => a.name.localeCompare(b.name))) {
  const mark = d.name.startsWith('ctrl-') ? 'CTRL' : '    ';
  console.log(`  ${mark}  ${d.name.padEnd(30)} desc=${String(d.description.length).padStart(4)} body=${String(d.body.trim().length).padStart(6)} chars`);
}
for (const s of skipped) console.log(`  SKIP  ${s.file} :: ${s.reason}`);

console.log('');
if (wanted.length !== 8) {
  console.log(`FAIL: expected 8 ctrl-* skills discoverable, found ${wanted.length}`);
  process.exit(1);
}
console.log(`PASS: all ${wanted.length} ctrl-* skills are discoverable and parse under DSH's own frontmatter contract.`);
