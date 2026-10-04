#!/usr/bin/env node
'use strict';
// Offline structural validator. Scientific/behavioral quality requires separate evaluation.
const fs = require('node:fs');
const path = require('node:path');
const { parseSkillText, catalogProblem } = require('./skill-contract.cjs');
const VALID_KEYS = new Set(['name', 'description', 'whenToUse', 'metadata', 'license',
  'disable-model-invocation', 'user-invocable', 'allowed-tools']);
const NON_SKILL_DIRS = new Set(['tools', 'docs', 'scripts', 'evals', '_research', 'node_modules', '.git']);

function resolveDefaultRoot(pkgRoot = path.join(__dirname, '..')) {
  for (const candidate of [path.join(pkgRoot, 'skills'), path.join(pkgRoot, '..', 'skills'), pkgRoot]) {
    if (!fs.existsSync(candidate) || !fs.statSync(candidate).isDirectory()) continue;
    if (fs.readdirSync(candidate).some((name) => name.startsWith('cse-')
      && fs.existsSync(path.join(candidate, name, 'SKILL.md')))) return candidate;
  }
  return path.join(pkgRoot, 'skills');
}
function withoutFences(text) {
  return text.replace(/^[ \t]*(`{3,}|~{3,})[^\n]*\n[\s\S]*?^[ \t]*\1[ \t]*\r?$/gm, '');
}
function markdownTargets(text) {
  const targets = [];
  const re = /!?\[[^\]\n]*\]\(\s*(<[^>\n]+>|[^\s)]+)(?:\s+["'][^\n]*?["'])?\s*\)/g;
  let match;
  while ((match = re.exec(withoutFences(text)))) targets.push(match[1].replace(/^<|>$/g, ''));
  return targets;
}
// Explicit parent tracking also supports Node versions without Dirent.parentPath.
function markdownFiles(base, skip = new Set(['node_modules', '.git'])) {
  const files = [];
  const stack = [base];
  while (stack.length) {
    const dir = stack.pop();
    for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
      if (skip.has(entry.name) || entry.isSymbolicLink()) continue;
      const full = path.join(dir, entry.name);
      if (entry.isDirectory()) stack.push(full);
      else if (entry.isFile() && entry.name.endsWith('.md')) files.push(full);
    }
  }
  return files;
}
function validateRoot(rootInput, options = {}) {
  const root = path.resolve(rootInput);
  const problems = [];
  const warnings = [];
  const skills = [];
  const seenNames = new Map();
  const checkedFiles = new Set();
  const fail = (file, msg) => problems.push(`${path.relative(root, file)}: ${msg}`);
  const warn = (file, msg) => warnings.push(`${path.relative(root, file)}: ${msg}`);
  function readText(file, isSkill) {
    let bytes = fs.readFileSync(file);
    if (bytes.length >= 3 && bytes[0] === 0xef && bytes[1] === 0xbb && bytes[2] === 0xbf) {
      if (options.fixBom) {
        bytes = bytes.subarray(3);
        fs.writeFileSync(file, bytes);
        warn(file, 'stripped UTF-8 BOM');
      } else (isSkill ? fail : warn)(file, 'UTF-8 BOM present; SKILL.md must begin exactly with ---');
    }
    return bytes.toString('utf8');
  }
  function resolveTarget(file, raw, type) {
    if (/^[a-z][a-z0-9+.-]*:/i.test(raw) || raw.startsWith('#') || raw.startsWith('//')) return undefined;
    const target = raw.split('#')[0];
    if (!target) return undefined;
    let decoded;
    try { decoded = decodeURIComponent(target); }
    catch { fail(file, `invalid URI escape in ${type}: ${raw}`); return undefined; }
    const full = path.resolve(path.dirname(file), decoded);
    if (!fs.existsSync(full)) fail(file, `broken ${type} -> ${target}`);
    return full;
  }
  // Inline paths such as `references/x.md` or `core/x.md` are bundle-root relative by convention.
  // Inside a resource file they resolve one level too deep, so they must be written as links
  // relative to that file. A preceding skill qualifier, as in `cse-shared` `core/x.md`, names
  // another bundle and is checked against that bundle instead.
  function checkBundlePaths(file, text, bundleDir) {
    const re = /(?:`(cse-[a-z0-9-]+)`\s+)?`((?:references|core|assets|scripts|templates)\/[^`\s]+?\.(?:md|json|cjs|py|ps1|txt))`/g;
    let match;
    const body = withoutFences(text);
    while ((match = re.exec(body))) {
      const [, qualifier, rel] = match;
      if (qualifier) {
        if (!fs.existsSync(path.join(root, qualifier, rel))) fail(file, `broken cross-skill path -> ${qualifier}/${rel}`);
        continue;
      }
      if (fs.existsSync(path.resolve(path.dirname(file), rel))) continue;
      if (fs.existsSync(path.join(bundleDir, rel))) fail(file, `bundle-root path \`${rel}\` inside a resource file; write a link relative to this file`);
      else fail(file, `broken inline path -> ${rel}`);
    }
  }
  function checkText(file, text, bundleDir) {
    if (checkedFiles.has(file)) return;
    checkedFiles.add(file);
    for (const target of markdownTargets(text)) resolveTarget(file, target, 'relative link');
    const re = /`([^`\n]*?(?:\.\.\/|\.\/)[^`\n]*?\.(?:md|py|json|csv|tex|ya?ml|sh|cjs|mjs|ps1|txt))`/g;
    let match;
    while ((match = re.exec(withoutFences(text)))) resolveTarget(file, match[1].trim(), 'inline-code path');
    if (bundleDir) checkBundlePaths(file, text, bundleDir);
    if (!text.trim()) fail(file, 'file is empty');
    if (/(^|\s)(TODO|TBD|FIXME|XXX)[:!]|\[(TODO|TBD|FIXME|XXX)\]/.test(text)) warn(file, 'unresolved TODO/TBD/FIXME/XXX marker');
  }
  if (!fs.existsSync(root) || !fs.statSync(root).isDirectory()) {
    problems.push(`skills root not found: ${root}`);
    return { root, skills, problems, warnings, checkedFiles: 0 };
  }
  for (const entry of fs.readdirSync(root, { withFileTypes: true })) {
    const full = path.join(root, entry.name);
    let info;
    try { info = fs.statSync(full); } catch (error) { fail(full, `unreadable entry: ${error.message}`); continue; }
    const file = info.isDirectory() ? path.join(full, 'SKILL.md')
      : info.isFile() && entry.name.endsWith('.md') ? full : undefined;
    if (!file) continue;
    if (!fs.existsSync(file)) {
      if (!NON_SKILL_DIRS.has(entry.name)) warn(full, 'directory has no SKILL.md');
      continue;
    }
    const text = readText(file, true);
    const result = parseSkillText(text);
    if (!result.ok) fail(file, result.reason);
    else {
      const { data, name, description, body } = result;
      const expectedName = info.isDirectory() ? entry.name : path.basename(entry.name, '.md');
      if (name !== expectedName) fail(file, `name "${name}" does not match entry "${expectedName}"`);
      if (seenNames.has(name)) fail(file, `duplicate skill name "${name}" also at ${seenNames.get(name)}`);
      seenNames.set(name, file);
      for (const key of Object.keys(data)) if (!VALID_KEYS.has(key)) fail(file, `unknown frontmatter key "${key}"`);
      if (!description.trim()) fail(file, 'description is blank');
      if (!body) fail(file, 'skill body is empty');
      const truncated = catalogProblem(description);
      if (truncated) fail(file, truncated);
      else if (description.trim().length < 80) warn(file, `description length ${description.trim().length} is below the advisory minimum of 80`);
      if (data.metadata !== undefined && (data.metadata === null || typeof data.metadata !== 'object' || Array.isArray(data.metadata))) fail(file, 'metadata must be a mapping');
      for (const key of ['license', 'whenToUse']) {
        if (data[key] !== undefined && typeof data[key] !== 'string') fail(file, `${key} must be a string`);
      }
      skills.push({ name, file, lines: text.split(/\r?\n/).length });
      const linked = new Set(markdownTargets(text).filter((t) => !/^[a-z][a-z0-9+.-]*:/i.test(t))
        .map((t) => { try { return path.resolve(path.dirname(file), decodeURIComponent(t.split('#')[0])); } catch { return ''; } }));
      if (info.isDirectory()) {
        for (const resourceDir of ['references', 'core', 'assets', 'scripts', 'templates']) {
          const dir = path.join(full, resourceDir);
          if (!fs.existsSync(dir) || !fs.statSync(dir).isDirectory()) continue;
          for (const resource of markdownFiles(dir)) if (!linked.has(resource)) warn(file, `resource not linked from SKILL.md: ${path.relative(full, resource)}`);
        }
      }
    }
    checkText(file, text, info.isDirectory() ? full : undefined);
    if (info.isDirectory()) for (const resource of markdownFiles(full)) {
      if (resource !== file) checkText(resource, readText(resource, false), full);
    }
  }
  if (!skills.length) problems.push('no valid skill bundles found; nothing can be declared validated');
  if (options.packageRoot) for (const doc of markdownFiles(options.packageRoot,
    new Set(['node_modules', '.git', '_research', 'skills']))) checkText(doc, readText(doc, false));
  return { root, skills, problems, warnings, checkedFiles: checkedFiles.size };
}
function main() {
  const args = process.argv.slice(2);
  for (const arg of args.filter((a) => a.startsWith('--'))) if (arg !== '--fix-bom') throw new Error(`unknown option: ${arg}`);
  const result = validateRoot(args.find((a) => !a.startsWith('--')) || resolveDefaultRoot(), {
    fixBom: args.includes('--fix-bom'), packageRoot: path.join(__dirname, '..'),
  });
  console.log(`scanned ${result.skills.length} valid skill(s) under ${result.root}, ${result.checkedFiles} Markdown files checked`);
  for (const skill of result.skills) console.log(`  ${skill.name.padEnd(30)} ${skill.lines} lines`);
  for (const warning of result.warnings) console.log(`  warn ${warning}`);
  for (const problem of result.problems) console.error(`  FAIL ${problem}`);
  if (result.problems.length) process.exitCode = 1;
  else console.log('no structural problems found');
}
if (require.main === module) {
  try { main(); } catch (error) { console.error(error.message); process.exitCode = 2; }
}
module.exports = { resolveDefaultRoot, markdownTargets, validateRoot };
