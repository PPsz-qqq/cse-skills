'use strict';
// Offline parsing/discovery compatibility helpers. No live plugin is enabled by this module.
const fs = require('node:fs');
const path = require('node:path');

const EXPECTED_SKILLS = Object.freeze([
  'cse-shared', 'cse-lit-radar', 'cse-idea-forge', 'cse-experiment-suite',
  'cse-paper-craft', 'cse-pre-submission-review', 'cse-response-craft', 'cse-paper-to-slides',
  'cse-figure-studio',
]);

// DSH's model-facing catalog (@deepseek-ai/dsh-tool-skill) shows each skill as its
// whitespace-normalized description, cut to catalogDescriptionMaxLength characters (default 500)
// with "..." appended. Anything beyond the limit, typically the trigger phrases, never reaches
// the model, so descriptions must fit the default limit.
const DSH_CATALOG_DESCRIPTION_MAX_LENGTH = 500;
function catalogDescription(value, maxLength = DSH_CATALOG_DESCRIPTION_MAX_LENGTH) {
  const normalized = value.replace(/\s+/g, ' ').trim();
  return normalized.length <= maxLength ? normalized : `${normalized.slice(0, maxLength - 3)}...`;
}
function catalogProblem(description, maxLength = DSH_CATALOG_DESCRIPTION_MAX_LENGTH) {
  const normalized = description.replace(/\s+/g, ' ').trim();
  if (normalized.length <= maxLength) return undefined;
  return `description is ${normalized.length} characters after whitespace normalization; the DSH skill `
    + `catalog truncates it to ${maxLength} and drops: "${normalized.slice(maxLength - 3)}"`;
}

function loadYaml() {
  const candidates = [];
  // Both overrides point to a node_modules directory, NOT the extracted-runtime parent.
  if (process.env.DSH_YAML_MODULE) candidates.push(process.env.DSH_YAML_MODULE);
  if (process.env.DSH_RUNTIME_REFERENCE) candidates.push(path.join(process.env.DSH_RUNTIME_REFERENCE, 'yaml'));
  try { candidates.push(require.resolve('yaml')); } catch { /* use local runtime reference */ }
  let dir = __dirname;
  for (;;) {
    candidates.push(path.join(dir, '.runtime-reference', 'dsh', 'node_modules', 'yaml'));
    const parent = path.dirname(dir);
    if (parent === dir) break;
    dir = parent;
  }
  for (const candidate of candidates) {
    try {
      const resolved = require.resolve(candidate);
      const parser = require(resolved);
      if (typeof parser.parse !== 'function') continue;
      let packageDir = path.dirname(resolved);
      let version = 'unknown';
      while (path.dirname(packageDir) !== packageDir) {
        const manifest = path.join(packageDir, 'package.json');
        if (fs.existsSync(manifest)) {
          const pkg = JSON.parse(fs.readFileSync(manifest, 'utf8'));
          if (pkg.name === 'yaml') { version = pkg.version; break; }
        }
        packageDir = path.dirname(packageDir);
      }
      return { parser, version, resolved };
    } catch { /* try another existing local module */ }
  }
  throw new Error('Cannot load yaml. Set DSH_RUNTIME_REFERENCE to the runtime node_modules directory, or DSH_YAML_MODULE to the yaml module path. No simplified YAML fallback is used.');
}

const yaml = loadYaml();
function parseFrontmatter(raw) {
  const firstLineEnd = raw.indexOf('\n');
  if (firstLineEnd < 0 || raw.slice(0, firstLineEnd).replace(/\r$/, '') !== '---') return undefined;
  const start = firstLineEnd + 1;
  let lineStart = start;
  while (lineStart <= raw.length) {
    const newline = raw.indexOf('\n', lineStart);
    const lineEnd = newline < 0 ? raw.length : newline;
    if (raw.slice(lineStart, lineEnd).replace(/\r$/, '') === '---') {
      const data = yaml.parser.parse(raw.slice(start, lineStart));
      if (typeof data !== 'object' || data === null || Array.isArray(data)) return undefined;
      return { data, body: raw.slice(newline < 0 ? raw.length : newline + 1) };
    }
    if (newline < 0) break;
    lineStart = newline + 1;
  }
  return undefined;
}
function frontmatterBoolean(data, key) {
  if (!Object.hasOwn(data, key)) return undefined;
  const value = data[key];
  if (typeof value === 'boolean') return value;
  if (value === 1 || value === '1') return true;
  if (value === 0 || value === '0') return false;
  if (typeof value === 'string') {
    if (['true', 'yes', 'on'].includes(value.toLowerCase())) return true;
    if (['false', 'no', 'off'].includes(value.toLowerCase())) return false;
  }
  throw new TypeError(`frontmatter field "${key}" must be a boolean`);
}
function parseInvocationPolicy(data) {
  for (const [legacy, canonical] of [
    ['disableModelInvocation', 'disable-model-invocation'],
    ['modelInvocable', 'disable-model-invocation'], ['userInvocable', 'user-invocable'],
  ]) {
    if (Object.hasOwn(data, legacy)) throw new Error(`frontmatter field "${legacy}" is unsupported; use "${canonical}"`);
  }
  return {
    modelInvocable: frontmatterBoolean(data, 'disable-model-invocation') !== true,
    userInvocable: frontmatterBoolean(data, 'user-invocable') !== false,
  };
}
function parseSkillText(raw) {
  let parsed;
  try { parsed = parseFrontmatter(raw); }
  catch (error) { return { ok: false, reason: `invalid YAML frontmatter: ${error.message}` }; }
  if (!parsed) return { ok: false, reason: 'missing YAML frontmatter' };
  const { name, description } = parsed.data;
  if (typeof name !== 'string' || !name || typeof description !== 'string' || !description) {
    return { ok: false, reason: 'frontmatter requires name and description strings' };
  }
  if (!/^[a-z0-9]+(?:-[a-z0-9]+)*$/.test(name)) return { ok: false, reason: `invalid skill name "${name}"` };
  let invocation;
  try { invocation = parseInvocationPolicy(parsed.data); }
  catch (error) { return { ok: false, reason: `invalid invocation frontmatter: ${error.message}` }; }
  return { ok: true, name, description, body: parsed.body.trim(), data: parsed.data, invocation };
}
function parseSkillFile(file) {
  try { return parseSkillText(fs.readFileSync(file, 'utf8')); }
  catch (error) { return { ok: false, reason: `unreadable: ${error.message}` }; }
}
function discover(root) {
  const discovered = [];
  const skipped = [];
  for (const entry of fs.readdirSync(root, { withFileTypes: true })) {
    const full = path.join(root, entry.name);
    let kind;
    try { kind = fs.statSync(full); }
    catch (error) { skipped.push({ file: full, reason: `cannot follow entry: ${error.message}` }); continue; }
    let file;
    if (kind.isDirectory()) file = path.join(full, 'SKILL.md');
    else if (kind.isFile() && entry.name.endsWith('.md')) file = full;
    else continue;
    if (kind.isDirectory() && !fs.existsSync(file)) continue;
    const result = parseSkillFile(file);
    if (result.ok) discovered.push({ ...result, file });
    else skipped.push({ file, reason: result.reason });
  }
  return { discovered, skipped };
}
function packProblems(result) {
  const problems = [];
  const names = new Map();
  for (const skill of result.discovered.filter((s) => s.name.startsWith('cse-'))) {
    if (names.has(skill.name)) problems.push(`duplicate skill name ${skill.name}: ${names.get(skill.name)} and ${skill.file}`);
    names.set(skill.name, skill.file);
    if (!EXPECTED_SKILLS.includes(skill.name)) problems.push(`unexpected cse-* skill: ${skill.name}`);
    if (!skill.body) problems.push(`empty skill body: ${skill.name}`);
    const truncated = typeof skill.description === 'string' ? catalogProblem(skill.description) : undefined;
    if (truncated) problems.push(`${skill.name}: ${truncated}`);
  }
  for (const name of EXPECTED_SKILLS) if (!names.has(name)) problems.push(`missing expected skill: ${name}`);
  for (const skipped of result.skipped) {
    const candidate = path.basename(skipped.file) === 'SKILL.md'
      ? path.basename(path.dirname(skipped.file)) : path.basename(skipped.file, '.md');
    if (candidate.startsWith('cse-')) problems.push(`invalid cse-* candidate ${skipped.file}: ${skipped.reason}`);
  }
  return problems;
}
module.exports = { EXPECTED_SKILLS, DSH_CATALOG_DESCRIPTION_MAX_LENGTH, catalogDescription, catalogProblem,
  yaml, parseFrontmatter, frontmatterBoolean, parseInvocationPolicy, parseSkillText, parseSkillFile,
  discover, packProblems };
