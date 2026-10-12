#!/usr/bin/env node
// 레포 구조와 플러그인 매니페스트를 검사한다.
// 검사 목록은 docs/standard.md 9절과 같아야 한다 — 한쪽만 고치면 갈린다.
//
// 떨어질 때는 반드시 고치는 법을 같이 적는다. 안 적혀 있으면 그건 이 스크립트의 버그다.

import { existsSync, readFileSync, readdirSync, statSync } from 'node:fs';
import { join } from 'node:path';
import { discoverPlugins, readManifest, readCategories, PLUGINS_DIR, CATEGORIES_PATH } from './lib.mjs';

const NAME_RE = /^[a-z0-9][a-z0-9-]{1,63}$/;
const SEMVER_RE = /^\d+\.\d+\.\d+$/;
const PLUGIN_DESC_MAX = 300;
const SKILL_DESC_MAX = 500;

const errors = [];
const fail = (where, what, how) => errors.push({ where, what, how });

const categories = readCategories();

// ── 분류 ────────────────────────────────────────────────────────────────
const topLevel = existsSync(PLUGINS_DIR) ? readdirSync(PLUGINS_DIR) : [];
for (const entry of topLevel) {
  if (entry.startsWith('.')) continue;
  const p = join(PLUGINS_DIR, entry);

  if (!statSync(p).isDirectory()) {
    fail(p, 'plugins/ 바로 아래에는 분류 디렉토리만 온다', `플러그인은 plugins/<분류>/<이름>/ 에 둔다. 분류: ${categories.join(' · ')}`);
    continue;
  }
  if (!categories.includes(entry)) {
    fail(p, `'${entry}' 는 허용된 분류가 아니다`, `${categories.join(' · ')} 중 하나에 둔다. 고르는 기준은 ${CATEGORIES_PATH} 안에 있다 — 분류를 새로 만드는 것은 플랫폼개발팀만 할 수 있으므로, 있는 것 중에서 고른다`);
  }
}

// ── 깊이 ────────────────────────────────────────────────────────────────
// plugins/<분류>/<이름>/ 이 정확히 1단계여야 한다.
// 매니페스트가 없는데 아래에 매니페스트를 가진 디렉토리가 있으면 깊이가 틀린 것이다.
for (const plugin of discoverPlugins()) {
  if (existsSync(plugin.manifestPath)) continue;
  const base = join(PLUGINS_DIR, plugin.category, plugin.dir);
  const nested = readdirSync(base)
    .filter((n) => !n.startsWith('.') && statSync(join(base, n)).isDirectory())
    .filter((n) => existsSync(join(base, n, '.claude-plugin', 'plugin.json')));
  if (nested.length) {
    fail(base, '분류 아래가 2단계 이상이다', `플러그인은 plugins/<분류>/<이름>/ 에 바로 둔다. ${nested.map((n) => `${base}/${n}`).join(' · ')} 을 ${join(PLUGINS_DIR, plugin.category)}/ 바로 아래로 옮긴다`);
  }
}

// ── 플러그인마다 ────────────────────────────────────────────────────────
const seen = new Map();

for (const plugin of discoverPlugins().map(readManifest)) {
  const { category, dir, manifest, error } = plugin;
  const base = join(PLUGINS_DIR, category, dir);

  if (!manifest) {
    // 깊이 오류로 이미 보고된 경우는 중복해서 말하지 않는다
    if (!errors.some((e) => e.where === base)) {
      fail(base, error, '모든 플러그인은 .claude-plugin/plugin.json 을 가진다. 작성법은 docs/standard.md 4절');
    }
    continue;
  }

  const { name, description, version, author, metadata } = manifest;

  if (name !== dir) fail(base, `plugin.json 의 name('${name}') 이 디렉토리명('${dir}') 과 다르다`, '둘을 같게 맞춘다. 설치 ID 와 스킬 네임스페이스가 여기서 갈린다');
  if (!NAME_RE.test(name ?? '')) fail(base, `name '${name}' 이 문자 규칙에 맞지 않는다`, '소문자·숫자·하이픈만, 2~64자, 첫 글자는 소문자나 숫자');

  const desc = description ?? '';
  if (!desc.trim()) fail(base, 'description 이 없다', '설치 전 목록에 보이는 문장이다. 무엇을 하는 것인지 한 줄로 적는다');
  else if (desc !== desc.trim()) fail(base, 'description 앞뒤에 공백이 있다', '공백을 없앤다');
  else if (desc.length > PLUGIN_DESC_MAX) fail(base, `description 이 ${desc.length}자다 (상한 ${PLUGIN_DESC_MAX})`, '한 줄로 줄인다. 자세한 설명은 README.md 에 쓴다');

  if (!SEMVER_RE.test(version ?? '')) fail(base, `version '${version}' 이 Major.Minor.Patch 가 아니다`, '처음 올리는 것이면 1.0.0. 기준은 docs/versioning.md');
  if (!author?.name) fail(base, 'author.name 이 없다', '화면에 뜨는 사람 이름을 적는다');
  if (!metadata?.owner) fail(base, 'metadata.owner 가 없다', 'GitHub 핸들을 적는다 — 사람 이름이 아니라 @ 뒤에 쓰는 그 핸들이다. 소유자 기록과 리뷰 요청에 쓴다');
  if (manifest.category) fail(base, 'plugin.json 에 category 를 적었다', '분류의 정본은 디렉토리 위치다. 둘을 다 두면 반드시 갈린다 — 이 줄을 지운다');

  if (!existsSync(join(base, 'README.md'))) fail(base, 'README.md 가 없다', '만든다. 쓰는 사람이 설치할지 말지 결정할 수 있을 만큼 적고, 양식은 docs/standard.md 7절을 따른다');

  // ── 스킬 ──
  const skillsDir = join(base, 'skills');
  const skillDirs = existsSync(skillsDir)
    ? readdirSync(skillsDir).filter((n) => !n.startsWith('.') && statSync(join(skillsDir, n)).isDirectory())
    : [];
  const skillFiles = skillDirs.map((n) => join(skillsDir, n, 'SKILL.md')).filter(existsSync);

  if (!skillFiles.length) {
    fail(base, 'SKILL.md 가 하나도 없다', 'skills/<이름>/SKILL.md 를 최소 하나 둔다');
  }
  for (const f of skillFiles) {
    const fm = readFileSync(f, 'utf8').match(/^---\r?\n([\s\S]*?)\r?\n---/);
    if (!fm) {
      fail(f, 'frontmatter 가 없다', '파일 맨 앞에 --- 로 감싼 name 과 description 을 둔다');
      continue;
    }
    const field = (k) => fm[1].match(new RegExp(`^${k}:\\s*(.+)$`, 'm'))?.[1]?.trim().replace(/^["']|["']$/g, '');
    const sName = field('name');
    const sDesc = field('description');
    if (!sName) fail(f, 'frontmatter 에 name 이 없다', '스킬 이름을 적는다');
    if (!sDesc) fail(f, 'frontmatter 에 description 이 없다', '"언제 이 스킬을 써야 하는가" 를 적는다');
    else if (sDesc.length > SKILL_DESC_MAX)
      fail(f, `description 이 ${sDesc.length}자다 (상한 ${SKILL_DESC_MAX})`, 'description 은 트리거 판정에만 쓰이고 모든 세션의 컨텍스트를 차지한다. 무엇을 하는지의 상세는 본문에 쓴다 — docs/standard.md 5절');
  }

  // ── 이름 중복 ──
  if (seen.has(name)) fail(base, `이름 '${name}' 이 ${seen.get(name)} 와 겹친다`, '의미를 더하는 suffix 를 붙인다. 숫자는 쓰지 않는다 — docs/standard.md 3절');
  else seen.set(name, base);
}

// ── 보고 ────────────────────────────────────────────────────────────────
if (!errors.length) {
  console.log(`✔ 구조 검사 통과 — 플러그인 ${seen.size}개`);
  process.exit(0);
}
console.error(`✗ 구조 검사 실패 — ${errors.length}건\n`);
for (const { where, what, how } of errors) {
  console.error(`  ${where}`);
  console.error(`    ${what}`);
  console.error(`    → ${how}\n`);
}
process.exit(1);
