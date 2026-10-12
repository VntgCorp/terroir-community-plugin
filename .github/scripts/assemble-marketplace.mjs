#!/usr/bin/env node
// marketplace.json 을 plugins/ 에서 조립한다.
//
//   --check  조립 결과가 커밋된 것과 같은지만 보고, 다르면 실패한다 (CI)
//   (없으면) 파일을 덮어쓴다 (사람이 로컬에서)
//
// marketplace.json 을 손으로 고치지 않는 이유는 docs/authoring.md 에 있다.

import { readFileSync, writeFileSync } from 'node:fs';
import { assemble, MARKETPLACE_PATH } from './lib.mjs';

const next = JSON.stringify(assemble(), null, 2) + '\n';

if (process.argv.includes('--check')) {
  if (readFileSync(MARKETPLACE_PATH, 'utf8') === next) {
    console.log(`✔ ${MARKETPLACE_PATH} 이 plugins/ 와 일치한다`);
    process.exit(0);
  }
  console.error(
    `✗ ${MARKETPLACE_PATH} 이 plugins/ 와 어긋난다.\n` +
      `\n  이 파일은 생성물이다. 손으로 고치지 말고 아래를 돌린 뒤 커밋한다.\n` +
      `\n      node .github/scripts/assemble-marketplace.mjs\n`
  );
  process.exit(1);
}

writeFileSync(MARKETPLACE_PATH, next);
console.log(`✔ ${MARKETPLACE_PATH} 을 다시 썼다`);
