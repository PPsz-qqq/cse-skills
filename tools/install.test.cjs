'use strict';
// Regression tests for tools/install.ps1. Every test works inside its own temporary directory and
// never touches a real DSH skill root. Windows only, because the installer creates junctions.
const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const os = require('node:os');
const path = require('node:path');
const { spawnSync } = require('node:child_process');

const INSTALLER = path.join(__dirname, 'install.ps1');
const isWindows = process.platform === 'win32';
const skip = isWindows ? false : 'install.ps1 creates Windows junctions';

function sandbox(t) {
  const root = fs.realpathSync(fs.mkdtempSync(path.join(os.tmpdir(), 'ctrl-install-test-')));
  t.after(() => {
    // Delete only the exact temp directory created by this invocation.
    assert.equal(path.dirname(root), fs.realpathSync(os.tmpdir()));
    assert.ok(path.basename(root).startsWith('ctrl-install-test-'));
    fs.rmSync(root, { recursive: true, force: true });
  });
  const write = (rel, text) => {
    const file = path.join(root, rel);
    fs.mkdirSync(path.dirname(file), { recursive: true });
    fs.writeFileSync(file, text);
    return file;
  };
  write('src/ctrl-a/SKILL.md', '---\nname: ctrl-a\ndescription: fixture a\n---\n# A\n');
  write('src/ctrl-a/references/x.md', '# reference\n');
  write('src/ctrl-b/SKILL.md', '---\nname: ctrl-b\ndescription: fixture b\n---\n# B\n');
  write('src/notes/README.md', 'not a bundle\n');
  // A sibling whose path shares the string prefix of src: src-evil starts with src.
  write('src-evil/ctrl-a/SKILL.md', '---\nname: ctrl-a\ndescription: foreign\n---\n# foreign\n');
  return { root, src: path.join(root, 'src'), dst: path.join(root, 'dst'), write };
}

function install(env, ...args) {
  const result = spawnSync('powershell.exe', ['-NoProfile', '-NonInteractive', '-ExecutionPolicy', 'Bypass',
    '-File', INSTALLER, '-Source', env.src, ...args], { encoding: 'utf8' });
  return { status: result.status, out: `${result.stdout}\n${result.stderr}` };
}
function linkTarget(p) {
  const stat = fs.lstatSync(p);
  return stat.isSymbolicLink() ? fs.realpathSync(p) : undefined;
}
function fileCount(dir) {
  let n = 0;
  for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
    const full = path.join(dir, entry.name);
    if (entry.isDirectory()) n += fileCount(full);
    else if (entry.isFile()) n += 1;
  }
  return n;
}
function backups(env) {
  const base = path.join(env.dst, '.ctrl-skills-backup');
  if (!fs.existsSync(base)) return [];
  return fs.readdirSync(base).flatMap((stamp) => fs.readdirSync(path.join(base, stamp)).map((n) => path.join(base, stamp, n)));
}

test('link install is idempotent and removal deletes links, never source files', { skip }, (t) => {
  const env = sandbox(t);
  const before = fileCount(env.src);
  let run = install(env, '-Target', env.dst);
  assert.equal(run.status, 0, run.out);
  assert.equal(linkTarget(path.join(env.dst, 'ctrl-a')), path.join(env.src, 'ctrl-a'));
  assert.equal(linkTarget(path.join(env.dst, 'ctrl-b')), path.join(env.src, 'ctrl-b'));
  assert.equal(fs.existsSync(path.join(env.dst, 'notes')), false, 'non-ctrl directories are not installed');
  run = install(env, '-Target', env.dst);
  assert.equal(run.status, 0, run.out);
  assert.match(run.out, /already linked/);
  run = install(env, '-Target', env.dst, '-Remove');
  assert.equal(run.status, 0, run.out);
  assert.equal(fs.existsSync(path.join(env.dst, 'ctrl-a')), false);
  assert.equal(fileCount(env.src), before, 'source files must survive install, re-install and removal');
});

test('prefix-sharing links and unowned directories are skipped, and -Force backs up instead of deleting', { skip }, (t) => {
  const env = sandbox(t);
  fs.mkdirSync(env.dst);
  fs.symlinkSync(path.join(env.root, 'src-evil', 'ctrl-a'), path.join(env.dst, 'ctrl-a'), 'junction');
  env.write('dst/ctrl-b/user-notes.txt', 'my own work');
  for (const extra of [[], ['-Remove']]) {
    const run = install(env, '-Target', env.dst, ...extra);
    assert.equal(run.status, 0, run.out);
    assert.match(run.out, /skip/);
    assert.equal(linkTarget(path.join(env.dst, 'ctrl-a')), path.join(env.root, 'src-evil', 'ctrl-a'));
    assert.equal(fs.readFileSync(path.join(env.dst, 'ctrl-b', 'user-notes.txt'), 'utf8'), 'my own work');
  }
  const run = install(env, '-Target', env.dst, '-Force');
  assert.equal(run.status, 0, run.out);
  assert.equal(linkTarget(path.join(env.dst, 'ctrl-a')), path.join(env.src, 'ctrl-a'));
  assert.ok(fs.existsSync(path.join(env.root, 'src-evil', 'ctrl-a', 'SKILL.md')), 'foreign link target untouched');
  assert.equal(linkTarget(path.join(env.dst, 'ctrl-b')), path.join(env.src, 'ctrl-b'));
  const saved = backups(env);
  assert.equal(saved.length, 1, run.out);
  assert.equal(fs.readFileSync(path.join(saved[0], 'user-notes.txt'), 'utf8'), 'my own work');
});

test('copy mode records ownership; modified copies survive removal unless forced into backup', { skip }, (t) => {
  const env = sandbox(t);
  let run = install(env, '-Target', env.dst, '-Mode', 'copy');
  assert.equal(run.status, 0, run.out);
  const marker = JSON.parse(fs.readFileSync(path.join(env.dst, 'ctrl-a', '.ctrl-skills-install.json'), 'utf8'));
  assert.equal(marker.pack, 'ctrl-skills');
  assert.deepEqual(Object.keys(marker.files).sort(), ['SKILL.md', 'references/x.md']);
  assert.equal(linkTarget(path.join(env.dst, 'ctrl-a')), undefined, 'copy mode creates real directories');
  run = install(env, '-Target', env.dst, '-Remove');
  assert.equal(run.status, 0, run.out);
  assert.equal(fs.existsSync(path.join(env.dst, 'ctrl-a')), false, 'unmodified owned copies are removed');
  run = install(env, '-Target', env.dst, '-Mode', 'copy');
  assert.equal(run.status, 0, run.out);
  fs.appendFileSync(path.join(env.dst, 'ctrl-a', 'SKILL.md'), '\nlocal edit\n');
  run = install(env, '-Target', env.dst, '-Remove');
  assert.equal(run.status, 0, run.out);
  assert.ok(fs.existsSync(path.join(env.dst, 'ctrl-a', 'SKILL.md')), 'a modified copy is kept');
  assert.equal(fs.existsSync(path.join(env.dst, 'ctrl-b')), false);
  run = install(env, '-Target', env.dst, '-Remove', '-Force');
  assert.equal(run.status, 0, run.out);
  assert.equal(fs.existsSync(path.join(env.dst, 'ctrl-a')), false);
  const saved = backups(env);
  assert.equal(saved.length, 1, run.out);
  assert.match(fs.readFileSync(path.join(saved[0], 'SKILL.md'), 'utf8'), /local edit/);
});

test('dangling links are replaced, targets inside the source are refused, and -WhatIf changes nothing', { skip }, (t) => {
  const env = sandbox(t);
  const gone = path.join(env.root, 'gone');
  fs.mkdirSync(gone);
  fs.mkdirSync(env.dst);
  fs.symlinkSync(gone, path.join(env.dst, 'ctrl-a'), 'junction');
  fs.rmdirSync(gone);
  let run = install(env, '-Target', env.dst);
  assert.equal(run.status, 0, run.out);
  assert.equal(linkTarget(path.join(env.dst, 'ctrl-a')), path.join(env.src, 'ctrl-a'));
  run = install(env, '-Target', path.join(env.src, 'nested-root'));
  assert.notEqual(run.status, 0, run.out);
  assert.equal(fs.existsSync(path.join(env.src, 'nested-root')), false);
  const fresh = path.join(env.root, 'whatif-root');
  run = install(env, '-Target', fresh, '-WhatIf');
  assert.equal(run.status, 0, run.out);
  assert.equal(fs.existsSync(fresh), false, '-WhatIf must not create anything');
});
