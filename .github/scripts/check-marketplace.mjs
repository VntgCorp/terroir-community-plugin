#!/usr/bin/env node
// marketplace.json 이 plugins/ 와 맞는지 본다.
//
// 이 파일은 사람이 고친다. 플러그인을 올리는 사람이 자기 줄을 직접 더해도 되고,
// assemble-marketplace.mjs 로 한 번에 써도 된다. 둘 다 이 검사를 통과한다.
//
// 정렬 · 들여쓰기 · 필드 순서는 보지 않는다. 뜻이 맞는지만 본다.
// 단 헤더(마켓 이름·설명 등)는 .github/marketplace-header.json 이 정본이라 같아야 한다.

import { readFileSync, existsSync } from 'node:fs';
import { join } from 'node:path';
import { discoverPlugins, readManifest, MARKETPLACE_PATH, HEADER_PATH } from './lib.mjs';

const errors = [];
const fail = (what, how) => errors.push({ what, how });

let market;
try {
  market = JSON.parse(readFileSync(MARKETPLACE_PATH, 'utf8'));
} catch (e) {
  console.error(`✗ ${MARKETPLACE_PATH} 를 읽을 수 없다 — ${e.message}\n\n  → JSON 문법을 확인한다. 쉼표나 괄호가 빠졌을 때 자주 난다\n`);
  process.exit(1);
}

// ── 헤더는 팀 소유다 ────────────────────────────────────────────────────
const header = JSON.parse(readFileSync(HEADER_PATH, 'utf8'));
for (const [key, want] of Object.entries(header)) {
  const got = market[key];
  if (JSON.stringify(got) !== JSON.stringify(want)) {
    fail(
      `${MARKETPLACE_PATH} 의 '${key}' 값이 ${HEADER_PATH} 와 다르다`,
      `마켓 이름·설명 같은 뼈대는 ${HEADER_PATH} 에 산다. 이 값을 바꾸려면 그 파일을 고치는 PR 이 필요하고 플랫폼개발팀 승인을 받는다 — docs/operations.md B2 절`
    );
  }
}

// ── 엔트리 ↔ 디렉토리 ───────────────────────────────────────────────────
const entries = Array.isArray(market.plugins) ? market.plugins : [];
if (!Array.isArray(market.plugins)) {
  fail(`${MARKETPLACE_PATH} 에 plugins 배열이 없다`, '"plugins": [] 를 둔다');
}

const byName = new Map();
for (const e of entries) {
  const where = `${MARKETPLACE_PATH} 의 '${e?.name ?? '(이름 없음)'}' 항목`;

  if (!e?.name) {
    fail(where, '항목마다 name 이 있어야 한다');
    continue;
  }
  if (byName.has(e.name)) {
    fail(where, `같은 이름이 두 번 적혀 있다. 하나를 지운다`);
    continue;
  }
  byName.set(e.name, e);

  if (typeof e.source !== 'string' || !e.source.startsWith('./plugins/')) {
    fail(where, 'source 는 "./plugins/<분류>/<이름>" 형태여야 한다');
    continue;
  }

  const dir = e.source.replace(/^\.\//, '');
  const manifestPath = join(dir, '.claude-plugin', 'plugin.json');
  if (!existsSync(manifestPath)) {
    fail(where, `source 가 가리키는 ${manifestPath} 이 없다. 경로를 확인하거나, 플러그인을 지웠다면 이 항목도 지운다`);
    continue;
  }

  let manifest;
  try {
    manifest = JSON.parse(readFileSync(manifestPath, 'utf8'));
  } catch {
    continue; // 구조 검사가 잡는다
  }

  if (manifest.name !== e.name) {
    fail(where, `${manifestPath} 의 name 은 '${manifest.name}' 이다. 둘을 같게 맞춘다`);
  }

  const category = dir.split('/')[1];
  if (e.category !== category) {
    fail(where, `디렉토리는 '${category}' 아래인데 category 가 '${e.category ?? '없음'}' 이다. 디렉토리 위치가 정본이다`);
  }
}

// ── 디렉토리는 있는데 목록에 없는 것 ────────────────────────────────────
for (const plugin of discoverPlugins().map(readManifest)) {
  if (!plugin.manifest) continue; // 구조 검사가 잡는다
  if (byName.has(plugin.manifest.name)) continue;
  fail(
    `${plugin.path} 가 ${MARKETPLACE_PATH} 에 없다`,
    `Claude Code 는 이 목록만 읽는다 — 목록에 없으면 아무도 설치할 수 없다. 아래를 더하거나 조립기를 돌린다.\n\n      {\n        "name": "${plugin.manifest.name}",\n        "source": "${plugin.path}",\n        "category": "${plugin.category}"\n      }\n\n      node .github/scripts/assemble-marketplace.mjs`
  );
}

// ── 보고 ────────────────────────────────────────────────────────────────
if (!errors.length) {
  console.log(`✔ marketplace.json 이 plugins/ 와 맞는다 — 항목 ${entries.length}개`);
  process.exit(0);
}
console.error(`✗ marketplace.json 검사 실패 — ${errors.length}건\n`);
for (const { what, how } of errors) {
  console.error(`  ${what}`);
  console.error(`    → ${how}\n`);
}
process.exit(1);
