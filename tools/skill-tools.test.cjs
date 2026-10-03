'use strict';
const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const os = require('node:os');
const path = require('node:path');
const { EXPECTED_SKILLS, DSH_CATALOG_DESCRIPTION_MAX_LENGTH, catalogDescription, catalogProblem, parseSkillText,
  frontmatterBoolean, parseInvocationPolicy, discover, packProblems } = require('./skill-contract.cjs');
const { resolveDefaultRoot, markdownTargets, validateRoot } = require('./validate-skills.cjs');
const description = 'An offline test skill with a sufficiently descriptive trigger and a bounded workflow for regression testing.';
function text(name = 'ctrl-fixture', extra = '', body = '# Fixture\n\nA useful instruction.\n') {
  return `---\nname: ${name}\ndescription: ${description}\n${extra}---\n${body}`;
}
function fixture(t) {
  const root = fs.mkdtempSync(path.join(os.tmpdir(), 'ctrl-skill-tools-'));
  const verifiedRoot = fs.realpathSync(root);
  t.after(() => {
    // Delete only the exact temp fixture created by this invocation, never a glob/computed parent.
    assert.equal(fs.realpathSync(root), verifiedRoot);
    assert.equal(path.dirname(verifiedRoot), fs.realpathSync(os.tmpdir()));
    assert.ok(path.basename(verifiedRoot).startsWith('ctrl-skill-tools-'));
    fs.rmSync(verifiedRoot, { recursive: true, force: true });
  });
  return root;
}
function put(root, name, content = text(name)) {
  const dir = path.join(root, name);
  fs.mkdirSync(dir, { recursive: true });
  fs.writeFileSync(path.join(dir, 'SKILL.md'), content);
  return dir;
}

test('LF and CRLF frontmatter, folded text and nested metadata parse', () => {
  const raw = '---\nname: ctrl-fixture\ndescription: >-\n  First line\n  and second line.\nmetadata:\n  category: research\nuser-invocable: false\n---\n# Body\n';
  const parsed = parseSkillText(raw);
  assert.equal(parsed.ok, true);
  assert.equal(parsed.description, 'First line and second line.');
  assert.equal(parsed.data.metadata.category, 'research');
  assert.equal(parsed.invocation.userInvocable, false);
  assert.equal(parseSkillText(raw.replace(/\n/g, '\r\n')).ok, true);
});
test('BOM, duplicate YAML keys, missing closure and wrong scalar types fail', () => {
  for (const raw of ['\ufeff' + text(), text('ctrl-fixture', 'name: duplicate\n'),
    '---\nname: ctrl-fixture\ndescription: hello\n', text().replace(`description: ${description}`, 'description: [one, two]'),
    text().replace('name: ctrl-fixture', 'name: 123')]) assert.equal(parseSkillText(raw).ok, false);
});
test('canonical invocation booleans match DSH contract including numeric 0/1', () => {
  for (const value of [true, 1, '1', 'TRUE', 'yes', 'on']) assert.equal(frontmatterBoolean({ flag: value }, 'flag'), true);
  for (const value of [false, 0, '0', 'FALSE', 'no', 'off']) assert.equal(frontmatterBoolean({ flag: value }, 'flag'), false);
  for (const value of [2, null, [], ' true ', 'maybe']) assert.throws(() => frontmatterBoolean({ flag: value }, 'flag'));
  assert.equal(frontmatterBoolean({}, 'flag'), undefined);
});
test('legacy invocation keys are rejected, not silently ignored', () => {
  for (const key of ['disableModelInvocation', 'modelInvocable', 'userInvocable']) {
    assert.throws(() => parseInvocationPolicy({ [key]: false }), /unsupported/);
  }
});
test('bundles, flat markdown and linked directories are discovered', (t) => {
  const root = fixture(t);
  put(root, 'ctrl-fixture');
  fs.writeFileSync(path.join(root, 'ctrl-flat.md'), text('ctrl-flat'));
  const target = path.join(root, 'resources');
  fs.mkdirSync(target);
  fs.writeFileSync(path.join(target, 'SKILL.md'), text('ctrl-linked'));
  fs.symlinkSync(target, path.join(root, 'ctrl-linked'), process.platform === 'win32' ? 'junction' : 'dir');
  const result = discover(root);
  assert.ok(result.discovered.some((s) => s.name === 'ctrl-fixture'));
  assert.ok(result.discovered.some((s) => s.name === 'ctrl-flat'));
  assert.ok(result.discovered.some((s) => s.name === 'ctrl-linked'));
});
test('eight records cannot conceal a missing name with a duplicate', () => {
  const discovered = EXPECTED_SKILLS.map((name, i) => ({ name, file: `bundle-${i}`, body: 'instruction' }));
  assert.deepEqual(packProblems({ discovered, skipped: [] }), []);
  discovered[7].name = discovered[0].name;
  const problems = packProblems({ discovered, skipped: [] });
  assert.ok(problems.some((p) => p.includes('duplicate')));
  assert.ok(problems.some((p) => p.includes('missing expected skill: ctrl-paper-to-slides')));
});
test('empty roots and blank bodies cannot pass validation', (t) => {
  const root = fixture(t);
  assert.ok(validateRoot(root).problems.some((p) => p.includes('no valid skill')));
  put(root, 'ctrl-fixture', text('ctrl-fixture', '', ''));
  assert.ok(validateRoot(root).problems.some((p) => p.includes('body is empty')));
});
test('default root prioritizes in-package skills over legacy sibling', (t) => {
  const root = fixture(t);
  const pkg = path.join(root, 'pack');
  put(path.join(pkg, 'skills'), 'ctrl-inner');
  put(path.join(root, 'skills'), 'ctrl-legacy');
  assert.equal(resolveDefaultRoot(pkg), path.join(pkg, 'skills'));
});
test('local links with spaces, encoded names and anchors resolve; bad escapes fail cleanly', (t) => {
  const root = fixture(t);
  const dir = put(root, 'ctrl-fixture', text('ctrl-fixture', '', '# Fixture\n[x](<references/space name.md>#part)\n[y](references/space%20name.md)\n[z](bad%Q1.md)\n'));
  fs.mkdirSync(path.join(dir, 'references'));
  fs.writeFileSync(path.join(dir, 'references', 'space name.md'), '# Resource\n');
  const result = validateRoot(root);
  assert.equal(result.problems.length, 1);
  assert.match(result.problems[0], /invalid URI escape/);
  assert.deepEqual(markdownTargets('[x](<a b.md>)\n[y](c.md "title")'), ['a b.md', 'c.md']);
});
test('broken reference and inline paths fail while code-fence examples are ignored', (t) => {
  const root = fixture(t);
  put(root, 'ctrl-fixture', text('ctrl-fixture', '', '# Fixture\n[x](missing.md)\n`../missing.json`\n```text\n[example](fictional.md)\n```\n'));
  const problems = validateRoot(root).problems;
  assert.equal(problems.length, 2);
  assert.ok(problems.some((p) => p.includes('relative link')));
  assert.ok(problems.some((p) => p.includes('inline-code path')));
});
test('frontmatter unknown keys, duplicate names and invalid metadata fail', (t) => {
  const root = fixture(t);
  put(root, 'ctrl-fixture', text('ctrl-fixture', 'unknown: true\nmetadata: []\n'));
  fs.writeFileSync(path.join(root, 'ctrl-flat.md'), text('ctrl-fixture'));
  const problems = validateRoot(root).problems;
  for (const needle of ['unknown frontmatter key', 'duplicate skill name', 'metadata must be a mapping']) {
    assert.ok(problems.some((p) => p.includes(needle)), needle);
  }
});
test('BOM repair is opt-in and normal checks are read-only', (t) => {
  const root = fixture(t);
  const dir = put(root, 'ctrl-fixture', '\ufeff' + text());
  const file = path.join(dir, 'SKILL.md');
  const before = fs.readFileSync(file);
  assert.ok(validateRoot(root).problems.length);
  assert.deepEqual(fs.readFileSync(file), before);
  assert.equal(validateRoot(root, { fixBom: true }).problems.length, 0);
  assert.equal(fs.readFileSync(file, 'utf8').startsWith('---'), true);
});
test('actual pack has exact skill names, scoped execution links and valid structure', () => {
  const root = resolveDefaultRoot();
  assert.deepEqual(packProblems(discover(root)), []);
  assert.deepEqual(validateRoot(root, { packageRoot: path.join(__dirname, '..') }).problems, []);
  for (const name of EXPECTED_SKILLS.filter((n) => n !== 'ctrl-shared')) {
    assert.match(fs.readFileSync(path.join(root, name, 'SKILL.md'), 'utf8'), /execution-contract\.md/);
  }
});
test('bundle-root inline paths fail inside resource files; qualified cross-skill paths are checked', (t) => {
  const root = fixture(t);
  const dir = put(root, 'ctrl-fixture', text('ctrl-fixture', '', '# Fixture\nSee `references/b.md`.\n[a](references/a.md) [b](references/b.md)\n'));
  fs.mkdirSync(path.join(dir, 'references'));
  fs.writeFileSync(path.join(dir, 'references', 'b.md'), '# B\n');
  fs.writeFileSync(path.join(dir, 'references', 'a.md'),
    '# A\nAmbiguous: `references/b.md`.\nQualified: `ctrl-other` `core/rules.md` and `ctrl-other`\n`core/missing.md`.\n```text\n`references/fenced.md`\n```\n');
  const other = put(root, 'ctrl-other');
  fs.mkdirSync(path.join(other, 'core'));
  fs.writeFileSync(path.join(other, 'core', 'rules.md'), '# Rules\n');
  const problems = validateRoot(root).problems;
  assert.ok(problems.some((p) => p.includes('bundle-root path `references/b.md`')), problems.join('\n'));
  assert.ok(problems.some((p) => p.includes('broken cross-skill path -> ctrl-other/core/missing.md')), problems.join('\n'));
  assert.equal(problems.filter((p) => p.includes('SKILL.md')).length, 0, 'bundle-root paths are valid in SKILL.md');
  assert.equal(problems.length, 2, problems.join('\n'));
});
test('catalog descriptions follow the DSH truncation rule and over-limit text fails', (t) => {
  assert.equal(DSH_CATALOG_DESCRIPTION_MAX_LENGTH, 500);
  assert.equal(catalogDescription('  folded\n  text\twith   gaps '), 'folded text with gaps');
  const exact = 'x'.repeat(500);
  assert.equal(catalogDescription(exact), exact);
  assert.equal(catalogProblem(exact), undefined);
  const long = `${'y'.repeat(497)}TAIL`;
  assert.equal(catalogDescription(long), `${'y'.repeat(497)}...`);
  assert.match(catalogProblem(long), /drops: "TAIL"/);
  const root = fixture(t);
  put(root, 'ctrl-fixture', `---\nname: ctrl-fixture\ndescription: >-\n  ${'z'.repeat(480)}\n  trigger words at the end\n---\n# Fixture\n`);
  assert.ok(validateRoot(root).problems.some((p) => p.includes('DSH skill catalog truncates')));
  const discovered = EXPECTED_SKILLS.map((name) => ({ name, file: name, body: 'x', description: 'short enough' }));
  discovered[2].description = long;
  assert.ok(packProblems({ discovered, skipped: [] }).some((p) => p.startsWith(`${EXPECTED_SKILLS[2]}: description is 501`)));
});
test('every shipped description reaches the model untruncated and names its Chinese triggers', () => {
  const result = discover(resolveDefaultRoot());
  for (const skill of result.discovered) {
    assert.equal(catalogProblem(skill.description), undefined, skill.name);
    assert.match(skill.description, /[\u4e00-\u9fff]/, `${skill.name} has no Chinese trigger text`);
  }
});
test('behavioral cases have unique IDs, valid skills and nonempty assertions', () => {
  const file = path.join(__dirname, '..', 'evals', 'evals.json');
  const suite = JSON.parse(fs.readFileSync(file, 'utf8'));
  assert.deepEqual(new Set(suite.skills), new Set(EXPECTED_SKILLS));
  assert.equal(new Set(suite.evals.map((e) => e.id)).size, suite.evals.length);
  for (const item of suite.evals) {
    assert.ok(EXPECTED_SKILLS.includes(item.skill), item.id);
    assert.ok(item.prompt && item.expected_output && item.assertions.length, item.id);
    for (const assertion of item.assertions) assert.ok(assertion.name && assertion.description, item.id);
  }
});
