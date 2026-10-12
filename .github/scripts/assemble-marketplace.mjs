#!/usr/bin/env node
// marketplace.json 의 plugins 목록을 plugins/ 에서 다시 쓴다.
//
// **편의 도구다. 반드시 써야 하는 것은 아니다.** 목록에 자기 줄을 직접 더해도 되고,
// 브라우저로 기여할 때는 그렇게 한다. 맞는지는 check-marketplace.mjs 가 본다.
//
// 헤더(마켓 이름·설명 등)는 .github/marketplace-header.json 에서 가져온다.

import { writeFileSync } from 'node:fs';
import { assemble, MARKETPLACE_PATH } from './lib.mjs';

writeFileSync(MARKETPLACE_PATH, JSON.stringify(assemble(), null, 2) + '\n');
console.log(`✔ ${MARKETPLACE_PATH} 의 목록을 다시 썼다`);
