// 검사와 조립기가 같이 쓰는 것. 레포 구조를 읽는 자리는 여기 하나다.

import { readFileSync, readdirSync, existsSync, statSync } from 'node:fs';
import { join } from 'node:path';

export const PLUGINS_DIR = 'plugins';
export const MARKETPLACE_PATH = '.claude-plugin/marketplace.json';
export const CATEGORIES_PATH = '.github/categories.txt';
// 소유의 정본. 플러그인마다 한 줄 — 집행은 GitHub 이 하고 CI 는 줄이 있는지만 본다.
export const CODEOWNERS_PATH = '.github/CODEOWNERS';
// 마켓 이름·설명 같은 뼈대. marketplace.json 이 아니라 여기 산다 —
// 저쪽은 기여자가 자기 줄을 더하는 파일이라 CODEOWNERS 로 지킬 수 없다.
export const HEADER_PATH = '.github/marketplace-header.json';

/** categories.txt 의 허용 목록. 주석과 빈 줄은 뺀다. */
export function readCategories() {
  return readFileSync(CATEGORIES_PATH, 'utf8')
    .split('\n')
    .map((l) => l.trim())
    .filter((l) => l && !l.startsWith('#'));
}

const dirsIn = (p) =>
  existsSync(p)
    ? readdirSync(p).filter((n) => !n.startsWith('.') && statSync(join(p, n)).isDirectory())
    : [];

/**
 * plugins/<카테고리>/<이름>/ 을 훑는다.
 * 카테고리가 허용 목록에 있는지는 보지 않는다 — 그건 검사의 몫이다.
 */
export function discoverPlugins() {
  const out = [];
  for (const category of dirsIn(PLUGINS_DIR)) {
    for (const dir of dirsIn(join(PLUGINS_DIR, category))) {
      out.push({
        category,
        dir,
        path: `./${PLUGINS_DIR}/${category}/${dir}`,
        manifestPath: join(PLUGINS_DIR, category, dir, '.claude-plugin', 'plugin.json'),
      });
    }
  }
  return out.sort((a, b) => a.dir.localeCompare(b.dir));
}

/** 매니페스트를 읽는다. 없거나 깨졌으면 manifest 가 null 이고 error 에 사유가 담긴다. */
export function readManifest(plugin) {
  if (!existsSync(plugin.manifestPath)) {
    return { ...plugin, manifest: null, error: `${plugin.manifestPath} 이 없다` };
  }
  try {
    return { ...plugin, manifest: JSON.parse(readFileSync(plugin.manifestPath, 'utf8')), error: null };
  } catch (e) {
    return { ...plugin, manifest: null, error: `${plugin.manifestPath} 파싱 실패 — ${e.message}` };
  }
}

/** 헤더 + plugins/ 를 훑어 만든 marketplace.json. 조립기가 쓴다. 이름순으로 둔다. */
export function assemble() {
  const header = JSON.parse(readFileSync(HEADER_PATH, 'utf8'));
  const plugins = discoverPlugins()
    .map(readManifest)
    .filter((p) => p.manifest)
    .map((p) => ({
      name: p.manifest.name,
      source: p.path,
      // Claude Code 는 이 목록만 읽는다. plugin.json 을 열어 보지 않으므로
      // 여기 없으면 /plugin 목록에 설명이 비어 보인다. 정본은 plugin.json 이다.
      description: p.manifest.description,
      category: p.category,
    }));
  return { ...header, plugins };
}
