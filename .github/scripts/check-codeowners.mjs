#!/usr/bin/env node
// 플러그인마다 CODEOWNERS 줄이 있고, 그 소유자가 plugin.json 과 같은지 본다.
//
// 소유를 **집행하는 것은 GitHub 이다** — CODEOWNERS 에 줄이 있으면 소유자 본인은
// 승인 없이 고치고, 남이 고치면 소유자 승인이 필요해진다. 이 검사는 집행하지 않고
// **줄이 빠지지 않았는지만** 본다. 빠지면 소유자가 없어 아무나 고칠 수 있고,
// CODEOWNERS 는 없는 줄을 알려주지 않는다.
//
// 소유자가 두 곳에 적히는 것은 피할 수 없다 — CODEOWNERS 는 권한, plugin.json 의
// metadata.owner 는 사람이 읽는 연락처다. 둘이 갈리지 않게 여기서 대조한다.

import { readFileSync, existsSync } from 'node:fs';
import { discoverPlugins, readManifest, CODEOWNERS_PATH, SKELETON_OWNER, SKELETON_PATHS } from './lib.mjs';

const errors = [];
const fail = (where, what, how) => errors.push({ where, what, how });

if (!existsSync(CODEOWNERS_PATH)) {
  console.error(`✗ ${CODEOWNERS_PATH} 이 없다\n\n  → 만든다. 없으면 뼈대도 플러그인도 소유자가 없다\n`);
  process.exit(1);
}

/** 경로 → 소유자 목록. 주석과 빈 줄은 뺀다. */
const rules = new Map();
for (const line of readFileSync(CODEOWNERS_PATH, 'utf8').split('\n')) {
  const t = line.trim();
  if (!t || t.startsWith('#')) continue;
  const [path, ...owners] = t.split(/\s+/);
  rules.set(path.replace(/\/$/, ''), owners);
}

// ── 뼈대 경로에 소유 팀이 그대로 있는가 ────────────────────────────────
//
// CODEOWNERS 자신에는 소유자가 없다. 플러그인을 올릴 때마다 팀 승인과 알림이
// 따라붙는 것을 막으려는 선택이고, 그 대가로 이 파일은 아무나 고칠 수 있다.
// 그래서 뼈대 줄에서 팀이 빠지는 것은 GitHub 이 아니라 여기서 잡는다.
for (const declaredPath of SKELETON_PATHS) {
  const key = declaredPath.replace(/\/$/, '');
  const owners = rules.get(key);
  const has = (list) => list.some((o) => o.toLowerCase() === SKELETON_OWNER.toLowerCase());

  if (!owners) {
    fail(
      declaredPath,
      `${CODEOWNERS_PATH} 에 이 뼈대 줄이 없다`,
      `뼈대는 팀이 소유한다. 아래를 더한다.\n` +
        `\n      ${declaredPath}   ${SKELETON_OWNER}\n` +
        `\n      소유 팀을 바꾸려면 .github/scripts/lib.mjs 의 SKELETON_OWNER 도 함께 고친다`
    );
    continue;
  }

  if (!has(owners)) {
    fail(
      declaredPath,
      `${CODEOWNERS_PATH} 의 이 줄에 ${SKELETON_OWNER} 가 없다 — 현재 '${owners.join(' · ')}'`,
      `뼈대는 이 팀이 소유해야 한다. **뒤에 다른 소유자를 더 적는 것은 괜찮고**, 이 팀만 빠지면 안 된다.\n` +
        `\n      ${declaredPath}   ${SKELETON_OWNER}${owners.filter((o) => o.toLowerCase() !== SKELETON_OWNER.toLowerCase()).map((o) => ' ' + o).join('')}\n` +
        `\n      소유 팀 자체를 바꾸려면 .github/scripts/lib.mjs 의 SKELETON_OWNER 를 고친다 —\n` +
        `      그 파일은 팀 소유라 변경에 팀 승인이 필요하다`
    );
  }
}

for (const plugin of discoverPlugins().map(readManifest)) {
  if (!plugin.manifest) continue; // 구조 검사가 잡는다

  const path = plugin.path.replace(/^\./, ''); // ./plugins/work/foo → /plugins/work/foo
  const owners = rules.get(path);
  const declared = plugin.manifest.metadata?.owner;

  if (!owners) {
    fail(
      plugin.path,
      `${CODEOWNERS_PATH} 에 이 플러그인 줄이 없다`,
      `줄이 없으면 소유자가 없어 아무나 고쳐 머지할 수 있다. 아래를 더한다.\n` +
        `\n      ${path}/   @${declared ?? '<GitHub 핸들>'}\n` +
        `\n      팀이 소유하면 @VntgCorp/<팀슬러그> 를 적는다`
    );
    continue;
  }

  if (!owners.length) {
    fail(plugin.path, `${CODEOWNERS_PATH} 의 줄에 소유자가 없다`, `경로만 적으면 소유가 해제된다. @핸들 이나 @VntgCorp/<팀슬러그> 를 적는다`);
    continue;
  }

  // 개인 소유면 metadata.owner 와 같아야 한다. 팀 소유(@org/team)는 대조 대상이 아니다.
  const individuals = owners.filter((o) => !o.includes('/')).map((o) => o.replace(/^@/, ''));
  if (individuals.length && declared && !individuals.some((o) => o.toLowerCase() === String(declared).toLowerCase())) {
    fail(
      plugin.path,
      `소유자가 두 곳에서 다르다 — ${CODEOWNERS_PATH} 는 '${individuals.join(' · ')}', plugin.json 은 '${declared}'`,
      `둘을 같게 맞춘다. CODEOWNERS 가 승인 권한을 정하고 plugin.json 은 사람이 읽는 연락처다 — 갈리면 누구에게 물어야 할지 알 수 없다`
    );
  }
}

if (!errors.length) {
  console.log(`✔ 플러그인마다 CODEOWNERS 줄이 있다`);
  process.exit(0);
}
console.error(`✗ CODEOWNERS 검사 실패 — ${errors.length}건\n`);
for (const { where, what, how } of errors) {
  console.error(`  ${where}`);
  console.error(`    ${what}`);
  console.error(`    → ${how}\n`);
}
process.exit(1);
