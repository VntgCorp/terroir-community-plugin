#!/usr/bin/env node
// 플러그인 파일이 바뀌었는데 version 이 그대로면 알린다. **떨어뜨리지 않는다.**
//
//   node .github/scripts/check-version-bump.mjs <base-ref>
//
// 버전을 올리지 않으면 이미 설치한 사람에게 변경이 가지 않는다. 다만 올리지 않는 것이
// 의도일 수 있다 — README 나 CHANGELOG 만 고친 경우가 그렇고, docs/versioning.md 도
// 그때는 올리지 않아도 된다고 적는다. 파일 종류로 그 의도를 기계가 가르려 하면 반드시
// 틀리므로, 알리기만 하고 판단은 올리는 사람에게 맡긴다.

import { execFileSync } from 'node:child_process';
import { discoverPlugins, readManifest, PLUGINS_DIR } from './lib.mjs';

const base = process.argv[2];
if (!base) {
  console.error('base ref 가 필요하다: node .github/scripts/check-version-bump.mjs <base-ref>');
  process.exit(2);
}

const git = (...args) => execFileSync('git', args, { encoding: 'utf8' }).trim();

const changed = git('diff', '--name-only', `${base}...HEAD`).split('\n').filter(Boolean);

/** 바뀐 파일이 속한 플러그인. 매니페스트만 바뀐 경우도 포함한다. */
const touched = new Map();
for (const plugin of discoverPlugins()) {
  const prefix = `${PLUGINS_DIR}/${plugin.category}/${plugin.dir}/`;
  const files = changed.filter((f) => f.startsWith(prefix));
  if (files.length) touched.set(plugin, files);
}

if (!touched.size) {
  console.log('✔ 바뀐 플러그인이 없다');
  process.exit(0);
}

const errors = [];
for (const [plugin, files] of touched) {
  const { manifest } = readManifest(plugin);
  if (!manifest) continue; // 구조 검사가 이미 잡는다

  const where = `${PLUGINS_DIR}/${plugin.category}/${plugin.dir}`;
  let before = null;
  try {
    before = JSON.parse(git('show', `${base}:${plugin.manifestPath}`)).version;
  } catch {
    continue; // base 에 없던 플러그인 — 신규다
  }

  if (before === manifest.version) {
    errors.push(
      `  ${where}\n` +
        `    파일 ${files.length}개가 바뀌었는데 version 이 ${before} 그대로다\n` +
        `    → 사용자에게 닿는 것을 고쳤으면 version 도 올린다. 기준은 docs/versioning.md\n` +
        `    → 올리지 않는 것이 의도라면 그대로 둔다. 이 검사는 머지를 막지 않는다\n`
    );
  }
}

if (!errors.length) {
  console.log(`✔ 버전 검사 통과 — 바뀐 플러그인 ${touched.size}개`);
  process.exit(0);
}
// GitHub Actions 에서 PR 에 경고로 뜨게 한다. 종료 코드는 0 — 머지를 막지 않는다.
console.log(`⚠ version 이 그대로인 플러그인 ${errors.length}개\n`);
errors.forEach((e) => {
  console.log(e);
  console.log(`::warning title=version 미증가::${e.replace(/\n/g, ' ').trim()}`);
});
console.log('README 나 CHANGELOG 만 고쳤다면 올리지 않아도 된다 — docs/versioning.md');
process.exit(0);
