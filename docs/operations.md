# 마켓을 바꾸는 절차

이 레포를 바꾸는 모든 경우를 한 자리에 모았다. **각 절차는 「누가 · 무엇을 · 승인이
필요한가」로 시작한다.** 새로 올리는 것만 [스킬 제작 방법](authoring.md)에 있고,
나머지는 전부 여기다.

권한 등급과 그 근거는 [권한](permissions.md)에 있다.

## 한눈에

| 하려는 일 | 누가 | 승인 | 절 |
|---|---|---|---|
| 플러그인 새로 올리기 | write 이상 | 불필요 | [authoring.md](authoring.md) |
| 내 플러그인 고치기 | write 이상 | 불필요 | [1](#1-플러그인을-고친다) |
| **남의** 플러그인 고치기 | write 이상 | 불필요 · **알림은 직접 해야 간다** | [2](#2-남의-플러그인을-고친다) |
| 플러그인 내리기 | write 이상 | 소유자 동의 | [3](#3-플러그인을-내린다) |
| 소유자 이관 | write 이상 | 양쪽 동의 | [4](#4-소유자를-이관한다) |
| 분류 추가·삭제 | write 이상이 PR | **팀 승인** | [5](#5-분류를-늘리거나-줄인다) |
| 마켓 이름·설명 변경 | write 이상이 PR | **팀 승인** | [6](#6-마켓-헤더를-바꾼다) |
| CI 검사 변경 | write 이상이 PR | **팀 승인** | [7](#7-ci-검사를-바꾼다) |
| 레포 권한·보호 변경 | **admin 만** | PR 밖 | [permissions.md](permissions.md) |

「팀 승인」은 `@VntgCorp/r-d` 를 말한다. CODEOWNERS 가 자동으로 리뷰를 요청하고,
**자기 PR 은 자기가 승인할 수 없으므로** 팀원이라도 다른 사람이 봐줘야 한다.

### 팀 승인이 걸리는 것의 정본

세 항목은 **「정본 파일 · 절차 · 승인자」가 한 세트**다. 셋을 따로 찾지 않도록 여기 모았다.

| 바꾸려는 것 | 정본 파일 | 절차 | 승인자가 왜 그 사람인가 |
|---|---|---|---|
| 분류 목록 | `.github/categories.txt` | [5](#5-분류를-늘리거나-줄인다) | `.github/` 가 CODEOWNERS 로 `@VntgCorp/r-d` |
| 마켓 이름·설명·`renames` | `.github/marketplace-header.json` | [6](#6-마켓-헤더를-바꾼다) | 〃 |
| CI 검사 | `.github/workflows/` · `.github/scripts/` | [7](#7-ci-검사를-바꾼다) | 〃 |
| **승인자 자체** | `.github/CODEOWNERS` | 아래 | 그 파일도 `.github/` 안이라 **같은 승인을 거친다** |

마지막 줄이 재귀인 것은 의도한 것이다 — **승인자를 바꾸는 권한도 현재 승인자가 쥔다.**
바꾸려면 `.github/CODEOWNERS` 의 해당 줄을 새 팀으로 고치는 PR 을 올리고 현재 팀의
승인을 받는다. 바꾼 뒤에는 **새 팀이 이 레포에 write 이상을 가졌는지 반드시 확인한다** —
권한 없는 팀을 적으면 GitHub 이 그 줄을 조용히 무시한다([권한](permissions.md)).

---

## 1. 플러그인을 고친다

**누가** 아무나(write 이상) · **승인** 불필요 · **CI** 통과해야 머지된다

```bash
git checkout -b fix-<이름>
# plugins/<분류>/<이름>/ 을 고친다

# version 을 올린다 — 안 올리면 CI 가 떨어뜨린다
# 무엇을 올릴지는 docs/versioning.md
# 두 번째 버전부터는 CHANGELOG.md 도 쓴다

node .github/scripts/check-structure.mjs
node .github/scripts/check-version-bump.mjs origin/main   # 이걸 빼먹어서 떨어지는 일이 잦다
git add . && git commit -m "fix(<분류>): ..." && gh pr create
```

`marketplace.json` 조립은 **이름·위치가 바뀌지 않으면 필요 없다.** 바뀌었다면 돌린다.

## 2. 남의 플러그인을 고친다

**누가** 아무나(write 이상) · **승인** 불필요 · **다만 관례가 있다**

구조상 막혀 있지 않다. CODEOWNERS 에 개별 플러그인을 넣지 않았기 때문이다
(넣으면 소유자가 자기 PR 을 자기가 승인 못 해 영원히 못 고친다 — [권한](permissions.md)).

**그래서 관례로 대신한다.**

```
  오타·링크 깨짐 같은 명백한 것       그냥 고치고 PR 본문에 알린다
  동작이 바뀌는 것                    PR 을 열고 소유자를 리뷰어로 지정한다
                                      plugin.json 의 metadata.owner 가 그 핸들이다
  소유자가 응답이 없다                기다릴 의무는 없다. 다만 PR 본문에
                                      "소유자 @핸들 에게 알렸으나 응답 없음" 을 남긴다
```

소유자에게 **자동 알림은 가지 않는다.** 리뷰어 지정을 직접 해야 전달된다.

## 3. 플러그인을 내린다

**누가** 아무나(write 이상)가 PR · **승인** 소유자 동의 · **되돌리기** 어렵다

내리기 전에 사용자에게 아래를 확인받는다. 추측해서 진행하지 않는다.

```
  □ 소유자가 동의했나 (plugin.json 의 metadata.owner)
  □ 왜 내리나 — 중복 · 폐기 · 다른 곳으로 이사 · 사고
  □ 대체재가 있나 — 있으면 PR 본문과 README 에 어디로 가면 되는지 적는다
```

```bash
git checkout -b remove-<이름>
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

그래서 **내리는 것은 「쓰던 사람을 끊는 것」이 아니라 「새로 못 쓰게 하는 것」에 가깝다.**
확실히 끊어야 하면 PR 과 함께 사용자에게 알리는 수밖에 없다.

> 이름을 **바꾸는** 것이라면 내리지 말고 `marketplace.json` 의 `renames` 를 쓴다.
> 옛 이름 → 새 이름 매핑을 지원하므로 설치한 사람이 끊기지 않는다. 헤더 변경이라
> 팀 승인이 필요하다([6](#6-마켓-헤더를-바꾼다)).

## 4. 소유자를 이관한다

**누가** 아무나(write 이상)가 PR · **승인** 넘기는 쪽과 받는 쪽 둘 다 동의

퇴사·조직 이동·관리 포기로 소유자가 바뀌는 경우다. **이름은 바꾸지 않는다** —
이름에 소유자를 안 박은 이유가 여기 있다([authoring.md](authoring.md) 3절).

```bash
# plugins/<분류>/<이름>/.claude-plugin/plugin.json 에서
#   author.name      새 소유자의 사람 이름
#   metadata.owner   새 소유자의 GitHub 핸들
# README.md 의 「소유자」 절도 같이 고친다
# version 은 Patch 를 올린다 — 동작이 안 바뀌었으므로
```

PR 본문에 **양쪽 동의를 남긴다.** 넘기는 사람이 이미 떠나 응답을 못 받으면 그 사실을 적는다.

받을 사람이 없으면 이관하지 않는다. 관리자 없는 스킬은 [그냥 둔다](about.md) —
쓰는 사람이 있으면 쓰고, 없으면 묻힌다.

## 5. 분류를 늘리거나 줄인다

**누가** 아무나가 PR · **승인 팀 필수** · **정본** `.github/categories.txt`

분류는 **미리 만들지 않는다.** `work` 에 같은 성격이 5개 이상 모였을 때 꺼낸다.

```bash
# .github/categories.txt 에 한 줄 추가 (또는 삭제)
# 기존 플러그인을 옮긴다면 git mv 하고 조립을 다시 돌린다
node .github/scripts/assemble-marketplace.mjs
node .github/scripts/check-structure.mjs
```

PR 본문에 **왜 지금인지**를 적는다 — 어떤 플러그인들이 그 덩어리인지 이름으로.

**줄이는 경우** 그 분류 아래가 비어 있어야 한다. 비어 있지 않으면 CI 가
「허용되지 않은 분류」로 떨어뜨린다. 옮기기를 같은 PR 에 넣는다.

## 6. 마켓 헤더를 바꾼다

**누가** 아무나가 PR · **승인 팀 필수** · **정본** `.github/marketplace-header.json`

마켓 이름·설명·버전·`renames`·`allowCrossMarketplaceDependenciesOn` 이 여기 산다.
`marketplace.json` 이 아니다 — 저쪽은 조립물이라 CODEOWNERS 로 지킬 수 없다.

```bash
# .github/marketplace-header.json 을 고친다
node .github/scripts/assemble-marketplace.mjs    # 조립물에 반영
```

> [!caution]
> `name` 을 바꾸면 **설치 줄이 바뀐다**(`<플러그인>@<마켓이름>`). 등록한 사람 전원이
> 다시 등록해야 하고 설치한 것도 다시 깔아야 한다. 가장 되돌리기 비싼 변경이다.

## 7. CI 검사를 바꾼다

**누가** 아무나가 PR · **승인 팀 필수** · **정본** `.github/`

```
  .github/workflows/validate.yml      언제 무엇을 돌리나
  .github/scripts/check-structure.mjs 구조·이름·매니페스트·스킬
  .github/scripts/check-version-bump.mjs
  .github/scripts/assemble-marketplace.mjs
  .github/scripts/lib.mjs             레포 구조를 읽는 자리 — 여기 하나다
```

**검사를 바꾸면 [authoring.md](authoring.md) 6절의 표도 같이 고친다.** 한쪽만 고치면
문서와 집행이 갈리고, 그때 사람들은 문서가 아니라 CI 를 믿는다.

> CI 는 자기를 지키지 못한다 — PR 이 검사를 약하게 바꿔도 체크 이름만 같으면 초록불이
> 뜬다. 그 구멍을 막는 게 이 경로의 **팀 승인**이다. 그래서 여기만은 반드시 사람이 본다.
