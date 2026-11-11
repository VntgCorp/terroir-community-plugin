# 스킬 등록 절차

**처음 스킬을 등록하는 사람을 위한 절차입니다.** 무엇이 규칙인지는 [플러그인 표준](standard.md)에 있고,
이 문서는 그 규칙을 **어떻게 지키며 등록하는지**를 다룹니다. 규칙 값이 이 문서와 다르면 표준이 맞습니다.

| 순서 | 할 일 |
|---|---|
| 1 | [준비](#1-준비) — Terroir 온보딩으로 GitHub 조직 가입과 개발 환경 셋팅 |
| 2 | [공식 도구로 제작](#2-공식-도구로-제작) — Anthropic 공식 `skill-creator` 로 스킬 만들기 |
| 3 | [등록 전에 맞출 규칙](#3-등록-전에-맞출-규칙) — 이름, 분류, 메타데이터, README |
| 4 | [등록 도구로 등록](#4-등록-도구로-등록) — `skill-market` 이 PR 까지 대신 진행 |
| 5, 6 | [터미널 없이 등록](#5-터미널-없이-등록), [터미널로 등록](#6-터미널로-등록) — 등록 도구 없이 직접 할 때 |
| 7 | [자주 발생하는 문제](#7-자주-발생하는-문제) |

## 1. 준비

> [!tip]
> **Terroir 온보딩을 이미 마쳤으면 이 절을 건너뛰고 [2. 공식 도구로 제작](#2-공식-도구로-제작)으로 넘어갑니다.**

| 하려는 일 | 필요한 것 |
|---|---|
| 설치해서 쓰기 | Claude Code 만 있으면 됩니다. GitHub 계정은 필요 없습니다 |
| 스킬을 만들어 등록하기 | VNTG GitHub 조직 구성원. Terroir 온보딩에서 「소프트웨어 개발」을 고르고 끝까지 진행하면 가입됩니다 |

단계마다 Claude Code 에 자연어로 입력합니다. 안 되면 오른쪽 명령어를 입력합니다.

| 단계 | 자연어 | 안 될 때 명령어 |
|---|---|---|
| 공개 플러그인 설치 | 「https://github.com/VntgCorp/terroir-claude-plugin-public 의 모든 내용을 User 설정에 모두 설치해줘」 | `/plugin marketplace add VntgCorp/terroir-claude-plugin-public`<br>`/plugin install terroir-onboarding@terroir-claude-plugin-public` |
| 지금 세션에 불러오기 | 「플러그인 다시 불러와줘」 | `/reload-plugins` |
| 온보딩 시작 | 「온보딩 시작해줘」 | `/onboarding` |

온보딩이 GitHub 가입, 2단계 인증, 조직 가입, `git` 과 `gh` 연결, `node` 설치까지 안내합니다.
중간에 「개발 환경 셋팅」을 진행할지 묻는데, 건너뛰지 말고 진행합니다. 등록 도구가 `node` 를 씁니다.
온보딩은 이 마켓도 미리 추가하고 자동 업데이트까지 켜 둡니다.

## 2. 공식 도구로 제작

Anthropic 공식 마켓(`claude-plugins-official`)은 **Claude Code 를 처음 실행할 때 자동으로 추가되고, 자동 업데이트도 켜져 있습니다.**
아래 두 플러그인은 설치만 하면 바로 쓸 수 있습니다.

| 단계 | 자연어 | 안 될 때 명령어 |
|---|---|---|
| 스킬 만들기 도구 설치 | 「skill-creator 플러그인 설치해줘」 | `/plugin install skill-creator@claude-plugins-official` |
| 플러그인 만들기 도구 설치 | 「plugin-dev 플러그인 설치해줘」 | `/plugin install plugin-dev@claude-plugins-official` |
| 지금 세션에 불러오기 | 「플러그인 다시 불러와줘」 | `/reload-plugins` |

| 플러그인 | 무엇을 돕나 |
|---|---|
| `skill-creator` | 스킬을 처음부터 만들기, 기존 스킬 고치기, 평가(eval)로 성능 재기 |
| `plugin-dev` | 플러그인 구조, 스킬 작성, 에이전트, 커맨드, 훅, MCP 연동, 설정 (스킬 7개) |

설치한 뒤 무엇을 하는 스킬을 만들고 싶은지 Claude Code 에 말하면 `skill-creator` 가 대화로 만들어 줍니다.

`SKILL.md` 를 어떻게 쓰고 본문을 어떻게 나누는지는 **이 두 공식 플러그인을 따릅니다.**
이 마켓의 문서는 그 내용을 옮겨 적지 않습니다. 옮겨 적으면 공식 도구가 바뀔 때 이 마켓의 문서만 뒤처집니다.

**다른 점은 하나뿐입니다. `description` 과 `when_to_use` 에 무엇을 적는가입니다.**
이 마켓은 `description` 에 목적 한 문장만 두고, 트리거 문구는 `when_to_use` 로 뺍니다. 자세한 내용은 [3절](#skillmd-메타데이터)과 [플러그인 표준 5절](standard.md#5-skillmd)에 있습니다.

## 3. 등록 전에 맞출 규칙

등록 도구가 대부분을 확인해 주지만, 만들 때부터 알고 있으면 다시 고칠 일이 줄어듭니다.
아래는 [플러그인 표준](standard.md)을 풀어 쓴 요약이고, 값이 다르면 표준이 맞습니다.

### 플러그인 이름과 스킬 이름은 따로 정합니다

마켓에는 스킬만 따로 등록할 수 없고, 플러그인 안에 넣어 등록합니다. 플러그인 하나에 스킬을 하나 이상 넣을 수 있습니다.

```
plugins/<분류>/<플러그인 이름>/
│     ← 마켓에서 설치하는 단위
├── .claude-plugin/plugin.json
│     ← "name": "<플러그인 이름>"
├── README.md
└── skills/<스킬 이름>/SKILL.md
      ← name: <스킬 이름>
```

| | 정하는 곳 | 쓰이는 곳 |
|---|---|---|
| 플러그인 이름 | 분류 폴더 바로 아래 폴더, `plugin.json` 의 `name` | 설치: `/plugin install <플러그인 이름>@terroir-community-plugin` |
| 스킬 이름 | `skills/` 아래 폴더, `SKILL.md` 의 `name` | 부르기: `/<플러그인 이름>:<스킬 이름>` |

두 이름은 같아도 되고 달라도 됩니다. 스킬 하나만 담는 플러그인이면 같은 이름으로 두는 경우가 많습니다.

### 플러그인 이름 규칙

- 소문자, 숫자, 하이픈만 씁니다. 폴더 이름과 `plugin.json` 의 `name` 이 같아야 합니다.
- 마켓 전체에서 유일해야 합니다. 분류가 달라도 겹칠 수 없고, 먼저 등록된 이름이 우선입니다.

| | 예 | 이유 |
|---|---|---|
| ○ | `curriculum-fe`, `curriculum-sales` | 어떤 범위에 쓰는지 이름이 말해 줍니다 |
| ✕ | `curriculum-2` | 이름만 보고는 둘 중 무엇을 설치할지 고를 수 없습니다 |
| ✕ | `hong-curriculum` | 소유자는 `plugin.json` 에 적으므로 이름에 넣지 않습니다 |

자세한 규칙과 이름이 겹칠 때 할 일은 [플러그인 표준 3절](standard.md#3-이름)에 있습니다.

### 분류는 질문 하나로 정합니다

**이 스킬이 소스코드나 인프라를 직접 건드리나요?** 「예」면 `dev`, 「아니오」면 `work` 입니다.
누가 쓰는지가 아니라 무엇을 건드리는지로 정합니다. 애매하면 `work` 에 둡니다.
허용되는 분류의 정본은 [`.github/categories.txt`](../.github/categories.txt) 입니다.

### SKILL.md 메타데이터

`SKILL.md` 맨 위 `---` 사이에 적습니다.

```
---
name: meeting-notes
description: 회의 메모를 안건별로 정리해 바로 공유할 수 있게 한다.
when_to_use: 회의가 끝나고 메모나 녹취를 정리하려 할 때. 예 "회의록 정리해줘".
---
```

- `description` 에는 스킬의 목적을 한 문장으로만 적습니다. 하는 일 나열, 절차, 트리거 문구는 넣지 않습니다.
- 언제 부르는지는 `when_to_use` 에 둡니다. 하는 일과 절차는 본문에 씁니다.

### plugin.json 의 소유자

`metadata.owner` 에 GitHub 아이디(`@` 뒤에 쓰는 이름)를 적습니다. 사람 이름은 안 됩니다.
`.github/CODEOWNERS` 의 소유자와 같아야 합니다. 자세한 필드는 [플러그인 표준 4절](standard.md#4-매니페스트)에 있습니다.

### 다른 사용자 PC 에서도 동작해야 합니다

설치되는 것은 플러그인 폴더 하나뿐입니다. 내 PC 에서만 통하는 경로나 주소가 남아 있으면
등록 도구가 찾아 알려 줍니다([4절](#등록-도구와-ci-가-확인하는-것)).
꼭 필요한 외부 도구나 접근 권한은 README 의 「전제 조건」에 적습니다. 자세한 내용은 [플러그인 표준 6절](standard.md#6-남의-환경에서-돌아가야-한다)에 있습니다.

> [!warning]
> **공개 저장소입니다.** 등록한 파일은 조직 밖에서도 보입니다. 계정, 토큰, 고객 데이터, 사내 문서 원문을 넣지 않습니다.

### README.md 는 다섯 절로 씁니다

무엇을 하는가, 쓰는 법, 전제 조건, 알려진 한계, 소유자입니다.
**「전제 조건」과 「알려진 한계」는 비우지 않고, 없으면 「없음」이라고 적습니다.**
심사가 없는 마켓이라 사용자는 이 두 절을 보고 고릅니다. 뼈대는 [플러그인 표준 7절](standard.md#7-readmemd)에 있습니다.

## 4. 등록 도구로 등록

등록 도구 `skill-market` 이 대화로 진행합니다. **직접 할 이유가 없으면 이 방법을 씁니다.**
`SKILL.md` 본문은 이 도구가 써 주지 않으니, 등록을 시작하기 전에 [2절](#2-공식-도구로-제작)의 `skill-creator` 로 스킬을 먼저 만들어 둡니다.

온보딩을 마쳤으면 이 마켓은 이미 추가돼 있습니다. 단계마다 자연어로 입력하고, 안 되면 오른쪽 명령어를 입력합니다.

| 단계 | 자연어 | 안 될 때 명령어 |
|---|---|---|
| 등록 도구 설치 (처음 한 번) | 「terroir-community-plugin 마켓에서 skill-market 설치해줘」 | `/plugin install skill-market@terroir-community-plugin` |
| 지금 세션에 불러오기 (설치 직후) | 「플러그인 다시 불러와줘」 | `/reload-plugins` |
| 등록 시작 | 「내가 만든 스킬을 사내 공유 마켓에 등록하고 싶어」 | `/skill-market:new` |

### 등록 도구와 CI 가 확인하는 것

| 누가, 언제 | 무엇을 확인하나 |
|---|---|
| 등록 도구<br>(내 PC 에서, PR 전) | 분류를 정하고, 이름이 겹치는지 확인합니다<br>외부 도구, 접근 권한, 다른 플러그인이 필요한지 묻고 README 「전제 조건」에 적습니다<br>초안을 읽고 내 홈 경로(`/Users/<나>/...`, `C:\Users\...`), 사설 IP 와 내부 호스트 이름, `../` 처럼 플러그인 밖을 가리키는 경로, 다른 플러그인의 스킬을 부르는 부분을 찾아 알려 줍니다<br>기본 파일을 만들고, 내 PC 에서 검사한 뒤 PR(변경 요청)을 올립니다 |
| CI(자동 검사)<br>(PR 을 연 뒤) | 형식만 검사합니다. 설치가 되는지, 이름이 겹치지 않는지, 소유자가 적혀 있는지, 필수 파일이 있는지<br>스킬 내용과 품질은 검사하지 않습니다 |

CI 가 실패하면 메시지에 고치는 법이 나옵니다. **통과하면 승인을 기다리지 않고 직접 머지합니다.**

## 5. 터미널 없이 등록

`git` 이나 `node` 를 쓰지 않습니다. **GitHub 웹에서 끝납니다.**

1. 레포에서 **Add file → Create new file** 을 엽니다.
2. 파일 이름 칸에 전체 경로를 적습니다. `/` 를 입력하면 폴더가 생깁니다.

```
plugins/<분류>/<이름>/.claude-plugin/plugin.json
plugins/<분류>/<이름>/README.md
plugins/<분류>/<이름>/skills/<이름>/SKILL.md
```

3. 각 파일의 내용은 [플러그인 표준](standard.md)을 보고 채웁니다.
   `README.md` 의 **「전제 조건」과 「알려진 한계」는 비우지 않습니다.** 없으면 「없음」이라고 적습니다.
   사용자가 그것을 보고 고릅니다.

4. `.claude-plugin/marketplace.json` 을 **Edit** 로 열어 목록에 한 줄을 더합니다.

```json
  {
    "name": "<이름>",
    "source": "./plugins/<분류>/<이름>",
    "description": "<plugin.json 의 description 과 같은 문장>",
    "category": "<분류>"
  }
```

`description` 은 **`/plugin` 목록에 보이는 한 줄입니다.** `plugin.json` 과 같아야 하고,
다르면 CI 가 실패합니다. Claude Code 는 이 목록만 읽고 `plugin.json` 을 열어 보지 않습니다.

5. `.github/CODEOWNERS` 를 **Edit** 로 열어 소유자 한 줄을 더합니다.

```
  /plugins/<분류>/<이름>/   @<GitHub 아이디>
```

6. **Commit changes** 에서 「Create a new branch」를 고르고 PR 을 엽니다.

검사는 PR 에서 자동으로 실행됩니다. 실패하면 메시지에 고치는 법이 나옵니다.

> 정렬, 들여쓰기, 필드 순서는 검사하지 않습니다. 자리만 맞으면 통과합니다.

## 6. 터미널로 등록

### 만들기

```bash
git clone https://github.com/VntgCorp/terroir-community-plugin
cd terroir-community-plugin
git checkout -b feat/meeting-notes
```

무엇을 어디에 만드는지는 [플러그인 표준](standard.md)을 보고 그대로 채웁니다. 요약하면
`plugins/<분류>/<이름>/` 아래에 `plugin.json`, `README.md`, `skills/<이름>/SKILL.md` 세 개를 두고,
**`.claude-plugin/marketplace.json` 의 목록에 한 줄을 더합니다.**

```json
  {
    "name": "<이름>",
    "source": "./plugins/<분류>/<이름>",
    "description": "<plugin.json 의 description 과 같은 문장>",
    "category": "<분류>"
  }
```

Claude Code 는 이 목록만 읽습니다. 폴더를 만들어도 목록에 없으면 아무도 설치할 수 없습니다.
목록은 **직접 고치는 파일입니다.** 터미널이 있으면 조립 스크립트가 대신 적어 줍니다(아래).

그리고 **`.github/CODEOWNERS` 에 소유자 한 줄을 더합니다.**

```
  /plugins/<분류>/<이름>/   @<GitHub 아이디>
```

이 줄이 있으면 **내 플러그인은 승인 없이 고치고, 남이 고칠 때는 내 승인이 필요해집니다.**
빠뜨리면 소유자가 없어 아무나 고칠 수 있고, CI 가 그것을 잡습니다. 팀이 소유하면
`@VntgCorp/<팀 슬러그>` 를 적습니다.

**분류는 질문 하나로 고릅니다.** 이 스킬이 소스코드나 인프라를 직접 건드리나요? 허용되는 분류는
[`.github/categories.txt`](../.github/categories.txt) 가 정본입니다.

### 검사

```bash
node .github/scripts/assemble-marketplace.mjs           # 목록을 대신 적어 줍니다 (선택)
node .github/scripts/check-structure.mjs                # 구조 검사
node .github/scripts/check-marketplace.mjs              # 목록이 plugins/ 와 맞는가
node .github/scripts/check-codeowners.mjs               # 소유자 줄이 있는가
node .github/scripts/check-version-bump.mjs origin/main  # 고치는 경우에만 걸립니다
claude plugin validate .                                # 스키마
```

아래 네 줄이 CI 가 실행하는 것과 같습니다. 첫 줄은 **편의 도구라 쓰지 않아도 됩니다.** 목록을 손으로
적었으면 건너뜁니다.

### PR 올리기

```bash
git add . && git commit -m "feat(<분류>): <이름> 추가"
gh pr create
```

**내 플러그인은 CI 가 통과하면 내가 머지합니다.** 승인을 기다리지 않습니다.
소유자 줄을 더하는 `.github/CODEOWNERS` 파일 자체에는 소유자를 걸지 않았기 때문입니다.

다만 아래를 건드리면 플랫폼개발팀 승인이 필요합니다.

| 경로 | 이유 |
|---|---|
| `docs/`, `README.md`, `.github/` 의 `workflows`, `scripts`, `categories.txt`, `marketplace-header.json` | 마켓의 뼈대입니다. 문서, CI, 분류 목록, 마켓 헤더 |
| | `.github/CODEOWNERS` 는 **승인이 필요 없습니다.** 소유자 줄을 더하는 파일이기 때문입니다 |
| `plugins/dev/skill-market/` | 등록 도구 |

`.claude-plugin/marketplace.json` 은 **위 표에 없습니다.** 플러그인을 등록하는 사람이 자기 줄을
더하는 파일이라 등록할 때마다 바뀝니다. 승인 대상으로 두면 모든 등록이 막힙니다. 마켓 이름과 설명
같은 뼈대는 `.github/marketplace-header.json` 에 따로 두었고, 둘이 어긋나면 CI 가 실패합니다.

**실행 코드가 들어 있어도 같습니다.** 훅이나 스크립트가 있는 플러그인에 추가 승인을 요구하지
않습니다. 대신 사용자가 그것을 알고 고르도록 [이 마켓은 무엇인가](about.md)에 밝혀 두었습니다.

등록 말고 다른 일(등록 취소, 소유자 이관, 남의 플러그인 고치기, 분류 변경)은
[마켓을 바꾸는 절차](operations.md)에 있습니다.

## 7. 자주 발생하는 문제

| 증상 | 조치 |
|---|---|
| 내 환경에서만 되는 스킬을 등록했다 | 절대 경로, 사설 IP, 플러그인 밖 참조를 지웁니다. 꼭 필요하면 「전제 조건」에 적습니다. [표준 6절](standard.md#6-남의-환경에서-돌아가야-한다) |
| 이름 중복으로 실패 | **남의 것을 건드리지 않고 내 이름을 바꿉니다.** 같은 일을 하는 스킬이면 바꾸기 전에 소유자에게 먼저 물어봅니다. [표준 「이름이 겹치면」](standard.md#이름이-겹치면) |
| `version` 을 안 올렸다는 경고 | 스킬 동작이나 사용법이 바뀌었으면 올립니다. README·CHANGELOG 만 고쳤으면 그대로 둬도 됩니다. [버전 올리기](versioning.md) |
| `metadata.owner` 없음 | `plugin.json` 의 `metadata.owner` 에 GitHub 아이디(`@` 뒤에 쓰는 이름)를 적습니다. 사람 이름은 안 됩니다 |
| 목록에 없다고 실패 | 메시지에 붙여 넣을 줄이 그대로 나옵니다. 그 줄을 `marketplace.json` 에 더합니다 |
| 헤더가 다르다고 실패 | 마켓 이름이나 설명을 건드렸습니다. 원래대로 되돌립니다. 플랫폼개발팀 영역입니다 |
| 허용되지 않은 분류 | [`.github/categories.txt`](../.github/categories.txt) 에 있는 이름(`dev`, `work`)을 씁니다 |
| `/` 자동완성에 뜨지 않음 | 설치 후 세션을 다시 시작합니다. `/reload-plugins` 는 바뀐 부분만 반영합니다 |
| 설치는 됐는데 스킬이 0개 | `skills/<스킬 이름>/SKILL.md` 경로인지 봅니다. `skills/SKILL.md` 는 인식되지 않습니다 |
