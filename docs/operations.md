# 마켓을 바꾸는 절차

**누가 하느냐로 먼저 갈린다.** 본인이 어느 쪽인지 확인하고 그 절만 보면 된다.

## 영역이 둘이다

```
┌─ 떼루아 사용자 영역 ─ 구성원 누구나 ─────────────────────────────────────┐
│                                                                         │
│   plugins/dev/**        plugins/work/**        (skill-market 제외)       │
│                                                                         │
│   올린 사람이 자기 것을 관리한다.                                          │
│   자기 것은 CI 통과 후 바로 머지한다. 남의 것은 그 소유자 승인이 필요하다.   │
│                                                                         │
│   → A. 사용자가 하는 일                                                   │
└─────────────────────────────────────────────────────────────────────────┘

┌─ 플랫폼개발팀 영역 ─ @VntgCorp/r-d ──────────────────────────────────────┐
│                                                                         │
│   plugins/ 와 .claude-plugin/ 을 뺀 나머지 전부.                          │
│   .github/ · docs/ · README.md                                           │
│   plugins/dev/skill-market/ 도 여기다 — 모든 기여자가 거쳐 가는 도구라서    │
│                                                                         │
│   .github/CODEOWNERS 가 정본이다. 기본값이 팀 소유이고                     │
│   .claude-plugin/ 만 소유를 비운다. 플러그인은 각자 소유자가 있다.          │
│                                                                         │
│   타팀이 고치려면 팀 승인이 필요하고, 팀원은 bypass 로 단독 머지한다.        │
│                                                                         │
│   → B. 플랫폼개발팀만 하는 일                                             │
└─────────────────────────────────────────────────────────────────────────┘

   .claude-plugin/marketplace.json  ← 둘이 만나는 곳. 올리는 사람이 자기 줄을 더하고
                                      마켓 이름·설명은 팀 소유 헤더에서 온다
```

권한 등급과 그 근거는 [권한](permissions.md)에, 무엇이 규칙인지는
[플러그인 표준](standard.md)에 있다.

---

# A. 사용자가 하는 일

**대상** 구성원 누구나(write 이상)

| 하려는 일 | 승인 | |
|---|---|---|
| 플러그인 새로 올리기 | 불필요 | [스킬 제작 방법](authoring.md) |
| 내 플러그인 고치기 | 불필요 | [A1](#a1-내-플러그인을-고친다) |
| **남의** 플러그인 고치기 | 불필요 · 알림은 직접 | [A2](#a2-남의-플러그인을-고친다) |
| 플러그인 내리기 | 소유자 동의 | [A3](#a3-플러그인을-내린다) |
| 소유자 이관 | 양쪽 동의 | [A4](#a4-소유자를-이관한다) |

> **분류를 새로 만드는 것은 사용자가 할 수 없다.** 플랫폼개발팀 영역이다([B1](#b1-분류를-늘리거나-줄인다)).
> 있는 분류 중에서 고른다 — 목록과 고르는 기준이 모두
> [`.github/categories.txt`](../.github/categories.txt) 에 있다.

## A1. 내 플러그인을 고친다

```bash
git checkout -b fix/<이름>
# plugins/<분류>/<이름>/ 을 고친다
# version 을 올린다 — 올리지 않으면 CI 가 경고한다. 막지는 않는다 (docs/versioning.md)
# 두 번째 버전부터는 CHANGELOG.md 도 쓴다

node .github/scripts/check-structure.mjs
node .github/scripts/check-version-bump.mjs origin/main   # 이걸 빼먹어서 떨어지는 일이 잦다
git add . && git commit -m "fix(<분류>): ..." && gh pr create
```

`marketplace.json` 은 **이름·위치가 바뀌지 않으면 손댈 일이 없다.** 바뀌었다면 그 줄도 고친다.

## A2. 남의 플러그인을 고친다

**소유자 승인이 필요하다.** 플러그인마다 `.github/CODEOWNERS` 에 소유자가 적혀 있어서,
남의 플러그인을 건드린 PR 은 그 소유자가 승인해야 머지된다. 소유자는 리뷰어로
자동 지정되므로 따로 알릴 필요가 없다([권한](permissions.md)).

```
  PR 을 연다
     → 소유자가 리뷰어로 자동 지정된다
     → 소유자가 승인하면 머지된다
```

PR 본문에 **무엇을 왜 고쳤는지** 적는다. 오타 하나라도 남의 것이므로 승인을 받는다.

**소유자가 응답하지 않으면** 막힌다. 퇴사·장기 부재처럼 응답을 받을 수 없는 상황이면
소유자 이관([A4](#a4-소유자를-이관한다))이 먼저다. 팀이 소유자로 적혀 있으면 그 팀의
다른 사람이 승인할 수 있다.

## A3. 플러그인을 내린다

**되돌리기 어렵다.** 내리기 전에 아래를 확인받는다. 추측해서 진행하지 않는다.

```
  □ 소유자가 동의했나 (plugin.json 의 metadata.owner)
  □ 왜 내리나 — 중복 · 폐기 · 다른 곳으로 이사 · 사고
  □ 대체재가 있나 — 있으면 PR 본문에 어디로 가면 되는지 적는다
```

```bash
git checkout -b chore/remove-<이름>
git rm -r plugins/<분류>/<이름>
node .github/scripts/assemble-marketplace.mjs    # 반드시 — 엔트리가 빠져야 한다
node .github/scripts/check-structure.mjs
git commit -m "remove(<분류>): <이름> 내림 — <사유>" && gh pr create
```

**이미 설치한 사람에게 무슨 일이 생기나.**

| | |
|---|---|
| 확인된 것 | 설치본은 `~/.claude/plugins/cache/terroir-community-plugin/<이름>/<버전>/` 에 **버전별로 캐시된다.** 내려도 그 사본은 지워지지 않는다 |
| 확인된 것 | 카탈로그에서 사라지므로 **새로 설치할 수 없다** |
| 모르는 것 | 캐시가 없는 상태에서 세션이 뜰 때의 동작. 환경에 따라 다를 수 있다 |

그래서 **내리는 것은 「쓰던 사람을 끊는 것」이 아니라 「새로 쓸 수 없게 하는 것」에 가깝다.**
확실히 끊어야 하면 PR 과 함께 사용자에게 알리는 수밖에 없다.

> 이름을 **바꾸는** 것이라면 내리지 않는다. 마켓 헤더의 `renames` 가 옛 이름 → 새 이름
> 매핑을 지원해 설치한 사람이 계속 쓸 수 있다. 그건 팀 영역이다([B2](#b2-마켓-헤더를-바꾼다)).

## A4. 소유자를 이관한다

퇴사·조직 이동·관리 포기로 소유자가 바뀌는 경우다. **이름은 바꾸지 않는다** —
이름에 소유자를 넣지 않은 이유가 여기 있다([플러그인 표준 3절](standard.md#3-이름)).

```bash
# plugins/<분류>/<이름>/.claude-plugin/plugin.json 에서
#   author.name      새 소유자 본인
#   metadata.owner   새 소유자의 GitHub 핸들
#   metadata.team    바뀌었다면 같이 고친다
# README.md 의 「소유자」 절도 같이 고친다
# version 은 Patch 를 올린다 — 동작이 바뀌지 않았으므로
```

PR 본문에 **양쪽 동의를 남긴다.** 넘기는 사람이 이미 떠나 응답을 받지 못하면 그 사실을 적는다.

받을 사람이 없으면 이관하지 않는다. 관리자 없는 스킬은 [그냥 둔다](about.md) —
쓰는 사람이 있으면 쓰고, 없으면 쓰이지 않는다.

---

# B. 플랫폼개발팀만 하는 일

**대상** `@VntgCorp/r-d` · 타팀이 올린 PR 은 팀 승인 없이 들어올 수 없다

| 바꾸려는 것 | 정본 파일 | |
|---|---|---|
| 분류 목록과 고르는 기준 | [`.github/categories.txt`](../.github/categories.txt) | [B1](#b1-분류를-늘리거나-줄인다) |
| 마켓 이름·설명·`renames` | `.github/marketplace-header.json` | [B2](#b2-마켓-헤더를-바꾼다) |
| CI 검사 | `.github/workflows/` · `.github/scripts/` | [B3](#b3-ci-검사를-바꾼다) |
| 승인자 | `.github/CODEOWNERS` | [B4](#b4-승인자를-바꾼다) |
| 규약 문서 | `docs/` · `README.md` | 일반 PR |
| 기여 도구 | `plugins/dev/skill-market/` | 일반 PR |

**전부 `.github/` · `docs/` 아래라 CODEOWNERS 한 줄이 모두에 적용된다.** 머지하는 법은
[권한](permissions.md)에 있다 — 웹의 bypass 체크박스를 쓴다.

## B1. 분류를 늘리거나 줄인다

**사용자는 할 수 없다.** 목록에 없는 분류가 필요해 보여도 사용자는 기준에 따라 있는 것
중 하나를 고른다. 늘릴지 말지는 팀이 판단한다.

**미리 만들지 않는다.** 같은 성격이 5개 이상 모였을 때 만든다.

```bash
# .github/categories.txt 에 분류 한 줄 + 설명 주석을 더한다 (또는 지운다)
# 기존 플러그인을 옮긴다면 git mv 하고 marketplace.json 의 source·category 도 고친다
node .github/scripts/check-structure.mjs
node .github/scripts/check-marketplace.mjs
```

`categories.txt` 에는 **목록만이 아니라 고르는 기준도 들어 있다.** 분류를 늘리면 기준도
같이 고친다 — 새 분류를 언제 고르는지가 거기 없으면 사용자가 적재 위치를 판단하지 못한다.

PR 본문에 **왜 지금인지**를 적는다 — 어떤 플러그인들이 같은 성격으로 묶이는지 이름으로.

**줄이는 경우** 그 분류 아래가 비어 있어야 한다. 비어 있지 않으면 CI 가
「허용되지 않은 분류」로 떨어뜨린다. 옮기기를 같은 PR 에 넣는다.

## B2. 마켓 헤더를 바꾼다

`.github/marketplace-header.json` 이 마켓 이름·설명·버전·`renames`·
`allowCrossMarketplaceDependenciesOn` 을 가진다.

**`.claude-plugin/marketplace.json` 이 아니다.** 저 파일은 올리는 사람이 자기 줄을 더하는
곳이라 기여마다 바뀌고, 그래서 CODEOWNERS 로 지킬 수 없다. 뼈대를 여기 따로 둔 이유다.

```bash
# .github/marketplace-header.json 을 고친다
# marketplace.json 의 해당 값도 같이 고친다 — 둘이 다르면 CI 가 떨어뜨린다
node .github/scripts/check-marketplace.mjs
```

> [!caution]
> `name` 을 바꾸면 **설치 줄이 바뀐다**(`<플러그인>@<마켓이름>`). 등록한 사람 전원이
> 다시 등록해야 하고 설치한 것도 다시 깔아야 한다. 가장 되돌리기 비싼 변경이다.

**플러그인 이름이 바뀌는 경우**는 `renames` 에 옛 이름 → 새 이름을 더한다. 그러면
설치한 사람이 계속 쓸 수 있다. 내렸다 다시 올리지 않는다([A3](#a3-플러그인을-내린다)).

## B3. CI 검사를 바꾼다

```
  .github/workflows/validate.yml        언제 무엇을 돌리나
  .github/scripts/check-structure.mjs   구조·이름·매니페스트·스킬 + 길이 상한 상수
  .github/scripts/check-version-bump.mjs
  .github/scripts/assemble-marketplace.mjs
  .github/scripts/lib.mjs               레포 구조를 읽는 자리 — 여기 하나다
```

**검사를 바꾸면 [플러그인 표준 9절](standard.md#9-ci-가-보는-것)의 표도 같이 고친다.**
한쪽만 고치면 문서와 집행이 갈리고, 그때 사람들은 문서가 아니라 CI 를 믿는다.

> CI 는 자기를 지키지 못한다 — PR 이 검사를 약하게 바꿔도 체크 이름만 같으면 초록불이
> 뜬다. 그것을 막는 것이 이 경로의 **팀 승인**이다.

## B4. 승인자를 바꾼다

`.github/CODEOWNERS` 를 고친다. **그 파일도 `.github/` 안이라 현재 승인자의 승인을 거친다** —
승인자를 바꾸는 권한도 현재 승인자에게 있다. 의도한 재귀다.

CODEOWNERS 에는 **뼈대와 플러그인 소유자가 함께** 들어간다. 뼈대는 팀 소유로 열거하고,
플러그인은 올릴 때 한 줄씩 더한다. `.claude-plugin/` 만 비워 둔다 — 기여마다 바뀌는
목록이라 걸면 모든 기여가 팀 승인에 걸린다.

**새 뼈대 파일을 만들면 여기에도 한 줄 더한다.** 빠뜨리면 아무나 고칠 수 있다.
플러그인 줄이 빠진 것은 `check-codeowners.mjs` 가 잡지만, 뼈대는 잡아 주지 않는다.

바꾼 뒤 **새 팀이 이 레포에 write 이상을 가졌는지 반드시 확인한다** — 권한 없는 팀을
적으면 GitHub 이 그 줄을 조용히 무시한다.

```bash
gh api repos/VntgCorp/terroir-community-plugin/codeowners/errors --jq '.errors | length'   # 0 이어야 한다
```
