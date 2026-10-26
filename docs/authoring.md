# 스킬 제작 방법

**처음 올리는 사람을 위한 절차.** 무엇이 규칙인지는 [플러그인 표준](standard.md)에 있고,
이 문서는 그걸 **어떻게 하는지**만 말한다. 규칙 값이 어긋나면 표준을 따른다.

## 0. 먼저 — 스킬 만드는 법은 공식이 가르친다

`claude-plugins-official` 마켓은 **첫 세션에 자동 등록되고 자동 업데이트도 켜져 있다.**
다음 두 플러그인은 설치만 하면 바로 쓸 수 있다.

| 플러그인 | 무엇을 가르치나 |
|---|---|
| `skill-creator` | 스킬을 처음부터 만들기 · 기존 스킬 개선 · eval 로 성능 측정 |
| `plugin-dev` | 플러그인 구조 · 스킬 작성 · 에이전트 · 커맨드 · 훅 · MCP 연동 · 설정 (스킬 7개) |

```
/plugin install skill-creator@claude-plugins-official
/plugin install plugin-dev@claude-plugins-official
```

`SKILL.md` 를 어떻게 쓰는지, 본문을 어떻게 나누는지는 **Anthropic 공식 마켓(`claude-plugins-official`)의
`skill-creator` 와 `plugin-dev` 가 가르친다.** 이 마켓의 문서는 그 내용을 옮겨 적지 않는다 — 옮기면 공식이 갱신될 때 이 마켓의 문서만 뒤처진다.

**하나만 다르다 — `description` 과 `when_to_use` 에 무엇을 적는가.** 이 마켓은 `description` 에
목적 한 문장만 두고 트리거 문구는 `when_to_use` 로 뺀다. [플러그인 표준 5절](standard.md#5-skillmd)을 따른다.

아래부터가 **여기에만 있는 절차**다. 스킬은 `skill-creator` 로 만들고, 만든 스킬을 `/skill-market:new` 로 올린다. `skill-market` 은 `SKILL.md` 본문을 써 주지 않는다.

---

## 1. 가장 빠른 길

```
/plugin install skill-market@terroir-community-plugin
/skill-market:new
```

대화로 물어보고 아래 2절을 전부 대신해 준다 — 분류 판정 · 이름 중복 검사 · 뼈대 생성 ·
로컬 검증 · PR 생성까지. **직접 할 이유가 없으면 이걸 쓴다.**

## 2. 터미널 없이 올리기

`git` 이나 `node` 를 쓰지 않는다. **GitHub 웹에서 끝난다.**

1. 레포에서 **Add file → Create new file** 을 연다
2. 파일 이름 칸에 전체 경로를 적는다 — `/` 를 치면 폴더가 생긴다

```
plugins/<분류>/<이름>/.claude-plugin/plugin.json
plugins/<분류>/<이름>/README.md
plugins/<분류>/<이름>/skills/<이름>/SKILL.md
```

3. 각 파일의 내용은 [플러그인 표준](standard.md)을 보고 채운다.
   `README.md` 의 **「전제 조건」과 「아는 한계」는 비우지 않는다** — 없으면 「없음」이라고
   적는다. 설치하는 사람이 그걸 보고 고른다

4. `.claude-plugin/marketplace.json` 을 **Edit** 로 열어 목록에 한 줄 더한다

```json
  {
    "name": "<이름>",
    "source": "./plugins/<분류>/<이름>",
    "description": "<plugin.json 의 description 과 같은 문장>",
    "category": "<분류>"
  }
```

`description` 은 **`/plugin` 목록에 보이는 한 줄이다.** `plugin.json` 과 같아야 하고,
다르면 CI 가 떨어뜨린다 — Claude Code 는 이 목록만 읽고 `plugin.json` 을 열어 보지 않는다.

5. `.github/CODEOWNERS` 를 **Edit** 로 열어 소유자 한 줄 더한다

```
  /plugins/<분류>/<이름>/   @<GitHub 핸들>
```

6. **Commit changes** 에서 「Create a new branch」를 고르고 PR 을 연다

검사는 PR 에서 자동으로 돈다. 떨어지면 메시지가 고치는 법을 알려준다.

> 정렬·들여쓰기·필드 순서는 검사하지 않는다. 자리만 맞으면 통과한다.

## 3. 터미널로 올리기

### 만든다

```bash
git clone https://github.com/VntgCorp/terroir-community-plugin
cd terroir-community-plugin
git checkout -b feat/meeting-notes
```

무엇을 어디에 만드는지는 [플러그인 표준](standard.md)을 보고 그대로 채운다. 요약하면
`plugins/<분류>/<이름>/` 아래에 `plugin.json` · `README.md` · `skills/<이름>/SKILL.md`
셋이고, **`.claude-plugin/marketplace.json` 의 목록에 한 줄을 더한다.**

```json
  {
    "name": "<이름>",
    "source": "./plugins/<분류>/<이름>",
    "description": "<plugin.json 의 description 과 같은 문장>",
    "category": "<분류>"
  }
```

Claude Code 는 그 목록만 읽는다 — 디렉토리를 만들어도 목록에 없으면 아무도 설치할 수 없다.
목록은 **직접 편집하는 파일이다.** 터미널이 있으면 조립기가 대신 적어준다(아래).

그리고 **`.github/CODEOWNERS` 에 소유자 한 줄을 더한다.**

```
  /plugins/<분류>/<이름>/   @<GitHub 핸들>
```

이 줄이 있으면 **자기 플러그인은 승인 없이 고치고, 남이 고칠 때는 내 승인이 필요해진다.**
빠뜨리면 소유자가 없어 아무나 고칠 수 있고, CI 가 그것을 잡는다. 팀이 소유하면
`@VntgCorp/<팀슬러그>` 를 적는다.

**분류는 한 줄로 고른다** — 이 스킬이 소스코드나 인프라를 직접 건드리나? 허용되는 분류는
[`.github/categories.txt`](../.github/categories.txt) 가 정본이다.

### 검사한다

```bash
node .github/scripts/assemble-marketplace.mjs           # 목록을 대신 적어준다 (선택)
node .github/scripts/check-structure.mjs                # 구조 검사
node .github/scripts/check-marketplace.mjs              # 목록이 plugins/ 와 맞는가
node .github/scripts/check-codeowners.mjs               # 소유자 줄이 있는가
node .github/scripts/check-version-bump.mjs origin/main  # 고치는 경우에만 걸린다
claude plugin validate .                                # 스키마
```

아래 넷이 CI 가 돌리는 것과 같다. 첫 줄은 **편의 도구라 안 써도 된다** — 목록을 손으로
적었으면 건너뛴다.

### 올린다

```bash
git add . && git commit -m "feat(<분류>): <이름> 추가"
gh pr create
```

**자기 플러그인은 CI 가 통과하면 본인이 머지한다.** 승인을 기다리지 않는다 —
소유자 줄을 더하는 `.github/CODEOWNERS` 에는 소유자를 걸지 않았다.

다만 아래를 건드리면 플랫폼개발팀 승인이 필요하다.

| 경로 | 왜 |
|---|---|
| `docs/` · `README.md` · `.github/` 의 `workflows` · `scripts` · `categories.txt` · `marketplace-header.json` | 마켓의 뼈대 — 문서 · CI · 분류 목록 · 마켓 헤더 |
| | `.github/CODEOWNERS` 는 **승인이 필요 없다** — 소유자 줄을 더하는 파일이라서 |
| `plugins/dev/skill-market/` | 기여 도구 |

`.claude-plugin/marketplace.json` 은 **여기 없다.** 플러그인을 올리는 사람이 자기 줄을
더하는 파일이라 기여마다 바뀐다. 승인 대상으로 두면 모든 기여가 막힌다. 마켓 이름·설명
같은 뼈대는 `.github/marketplace-header.json` 에 따로 두었고, 둘이 어긋나면 CI 가 떨어뜨린다.

**실행 코드가 들어 있어도 같다.** 훅·스크립트가 있는 플러그인에 추가 승인을 요구하지
않는다. 대신 설치하는 쪽이 그걸 알고 고르도록 [이 마켓은 무엇인가](about.md)가 밝힌다.

올리기 말고 다른 일 — 내리기 · 소유자 이관 · 남의 플러그인 고치기 · 분류 변경 — 은
[마켓을 바꾸는 절차](operations.md)에 있다.

## 4. 자주 걸리는 것

| 증상 | |
|---|---|
| 내 환경에서만 되는 스킬을 올렸다 | 절대 경로·사설 IP·플러그인 밖 참조를 걷어낸다. 정말 필요하면 「전제 조건」에 선언한다 — [표준 6절](standard.md#6-남의-환경에서-돌아가야-한다) |
| 이름 중복으로 떨어짐 | **남의 것을 건드리지 않는다. 내 이름을 바꾼다** — [표준 「이름이 겹치면」](standard.md#이름이-겹치면) |
| `version` 미증가 경고 | 사용자에게 닿는 것을 고쳤으면 올린다. README·CHANGELOG 만 고쳤으면 그대로 둬도 된다 — [버전업 경로](versioning.md) |
| `metadata.owner` 없음 | GitHub 핸들을 적는다. 사람 이름이 아니라 `@` 뒤에 쓰는 그 핸들 |
| 목록에 없다고 떨어짐 | 메시지에 붙여넣을 줄이 그대로 나온다. 그걸 `marketplace.json` 에 더한다 |
| 헤더가 다르다고 떨어짐 | 마켓 이름·설명을 건드렸다. 원래대로 되돌린다 — 그건 팀 영역이다 |
| 허용되지 않은 분류 | [`.github/categories.txt`](../.github/categories.txt) 안의 이름을 쓴다 |
| `/` 자동완성에 뜨지 않음 | 설치 후 세션을 다시 시작한다. `/reload-plugins` 는 변경분만 반영한다 |
| 설치는 됐는데 스킬 0개 | `skills/<이름>/SKILL.md` 경로를 확인한다. `skills/SKILL.md` 는 다른 형태다 |
