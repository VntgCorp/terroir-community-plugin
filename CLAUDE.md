# terroir-community-plugin

사내 구성원이 직접 만든 Claude Code 스킬을 올리고 가져다 쓰는 **마켓플레이스 레포**다.
플랫폼개발팀이 검증해 제공하는 `terroir-claude-plugin` 과는 다른 채널이다 — 여기는
품질 심사를 하지 않고 형식만 검사한다.

## 구조 — 누가 무엇을 소유하나

```
  .github/        docs/        README.md     plugins/dev/skill-market/
  ────────────────────────────────────────────────────────────────────  팀 소유
  CI · 분류 목록 · 마켓 헤더 · 규약 문서 · 기여 도구
  바꾸려면 @VntgCorp/r-d 승인이 필요하다 (CODEOWNERS)

  plugins/dev/**   plugins/work/**
  ────────────────────────────────────────────────────────────────────  기여자 소유
  각자의 플러그인. CI 만 통과하면 본인이 머지한다 — 승인 대기 없음

  .claude-plugin/marketplace.json
  ────────────────────────────────────────────────────────────────────  생성물
  위 둘을 CI 가 조립한 결과. 손으로 고치지 않는다
```

## 하려는 일에 따라 읽을 곳

| 하려는 일 | 어디 | 승인 |
|---|---|---|
| **무엇이 규칙인가** — 어디에·무엇을·어떤 이름으로 | [docs/standard.md](docs/standard.md) | — |
| 이 마켓이 무엇인지 알기 | [docs/about.md](docs/about.md) | — |
| 스킬을 **새로 올리기** (절차) | [docs/authoring.md](docs/authoring.md) | 불필요 |
| 올린 것을 **고치기 · 버전 올리기** | [docs/versioning.md](docs/versioning.md) | 불필요 |
| **남의** 플러그인 고치기 | [docs/operations.md](docs/operations.md#a2-남의-플러그인을-고친다) | 불필요 · 알림은 직접 |
| **내리기 · 이관** | [docs/operations.md](docs/operations.md#a3-플러그인을-내린다) | 소유자 동의 |
| **분류 · 마켓 이름 · CI** 변경 | [docs/operations.md](docs/operations.md#b-플랫폼개발팀만-하는-일) | 팀 승인 |
| 누가 무엇을 할 수 있는지 | [docs/permissions.md](docs/permissions.md) | — |

> [!important]
> **이 표는 어디로 갈지만 말한다. 답이 아니다.** 「승인 불필요」가 「그냥 하면 된다」는
> 뜻은 아니다 — 절차·예외·관례는 해당 문서에 있다. 표 한 줄로 답을 끝내지 않는다.

**규칙 값의 정본은 위 문서들이다.** 길이 상한·이름 규칙 같은 것을 외워서 답하지 말고
해당 문서를 읽어서 답한다. 외워 두면 문서가 바뀔 때 갈린다.

## 무엇을 바꾸든 지키는 것

```
  1  main 에 직접 push 하지 않는다 — 전원 차단돼 있다(admin 포함). 반드시 PR
  2  .claude-plugin/marketplace.json 을 손으로 고치지 않는다 — 조립기를 돌린다
  3  plugin.json 에 category 를 적지 않는다 — 분류의 정본은 디렉토리 위치다
  4  plugins/ 바로 아래에 플러그인을 두지 않는다 — plugins/<분류>/<이름>/ 이다
```

## 올리기 전에 돌리는 것

```bash
node .github/scripts/assemble-marketplace.mjs           # marketplace.json 재조립
node .github/scripts/check-structure.mjs                # 구조 검사
node .github/scripts/check-version-bump.mjs origin/main  # 고쳤으면 version 올렸나
claude plugin validate .                                # 스키마
```

CI 가 돌리는 것과 같다. **떨어지면 메시지가 고치는 법을 알려준다** — 그대로 따르면 된다.
안 알려주면 그건 CI 의 버그다.

## 사람이 결정해야 하는 것

아래는 추측하지 말고 사용자에게 묻는다.

| | 왜 |
|---|---|
| `author.name` · `metadata.owner` | 누구 것인지는 본인만 안다. `owner` 는 GitHub 핸들이지 사람 이름이 아니다 |
| 분류(`dev`/`work`) | 판정 근거를 한 줄로 말하고 확인받는다 |
| 플러그인 삭제 | 되돌리기 어렵다. [docs/operations.md](docs/operations.md) 의 절차를 따른다 |
| `README.md` 의 「아는 한계」 | 품질 심사가 없는 마켓이라, 만든 사람이 적는 게 유일한 안전장치다 |
