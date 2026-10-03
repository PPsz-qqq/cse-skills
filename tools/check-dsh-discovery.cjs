#!/usr/bin/env node
'use strict';
// Offline compatibility check, not a live DSH catalog/activation check.
const fs = require('node:fs');
const os = require('node:os');
const path = require('node:path');
function main() {
  const { yaml, discover, packProblems } = require('./skill-contract.cjs');
  const root = path.resolve(process.argv[2] || path.join(process.env.DSH_HOME || path.join(os.homedir(), '.dsh'), 'skills'));
  if (!fs.existsSync(root) || !fs.statSync(root).isDirectory()) throw new Error(`skill root not found: ${root}`);
  const result = discover(root);
  console.log(`DSH-compatible parser (yaml ${yaml.version}) over ${root}`);
  console.log(`discovered ${result.discovered.length} skill(s), skipped ${result.skipped.length}`);
  for (const skill of result.discovered.sort((a, b) => a.name.localeCompare(b.name))) {
    console.log(`  ${skill.name.padEnd(30)} desc=${skill.description.length} body=${skill.body.length} chars`);
  }
  for (const item of result.skipped) console.log(`  SKIP ${item.file}: ${item.reason}`);
  const problems = packProblems(result);
  if (problems.length) {
    for (const problem of problems) console.error(`FAIL: ${problem}`);
    process.exitCode = 1;
  } else {
    console.log('PASS: all eight distinct expected ctrl-* bundles parse under the compatibility contract.');
    console.log('Live provider activation, configured roots and session visibility were not checked.');
  }
}
if (require.main === module) {
  try { main(); } catch (error) { console.error(error.message); process.exitCode = 2; }
}
module.exports = { main };
