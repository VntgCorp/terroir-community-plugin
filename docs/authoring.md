# 스킬 제작 방법

**처음 올리는 사람을 위한 절차.** 무엇이 규칙인지는 [플러그인 표준](standard.md)에 있고,
이 문서는 그걸 **어떻게 하는지**만 말한다. 규칙 값이 어긋나면 표준이 이긴다.

## 0. 먼저 — 스킬 만드는 법은 공식이 가르친다

`claude-plugins-official` 마켓은 **첫 세션에 자동 등록되고 자동 업데이트도 켜져 있다.**
아래 둘은 설치만 하면 바로 쓸 수 있다.

| 플러그인 | 무엇을 가르치나 |
|---|---|
| `skill-creator` | 스킬을 처음부터 만들기 · 기존 스킬 개선 · eval 로 성능 측정 |
| `plugin-dev` | 플러그인 구조 · 스킬 작성 · 에이전트 · 커맨드 · 훅 · MCP 연동 · 설정 (스킬 7개) |

```
/plugin install skill-creator@claude-plugins-official
/plugin install plugin-dev@claude-plugins-official
```

`SKILL.md` 를 어떻게 쓰는지, `description` 을 어떻게 트리거로 만드는지, 본문을 어떻게
나누는지는 **전부 저기서 배운다.** 이 마켓의 문서는 그 내용을 옮겨 적지 않는다 — 옮기면
공식이 업데이트될 때 이쪽만 뒤처진다.

아래부터가 **여기에만 있는 절차**다.

---

## 1. 가장 빠른 길

```
/plugin install skill-market@terroir-community-plugin
/skill-market:new
```

대화로 물어보고 아래 2절을 전부 대신해 준다 — 분류 판정 · 이름 중복 검사 · 뼈대 생성 ·
로컬 검증 · PR 생성까지. **직접 할 이유가 없으면 이걸 쓴다.**

## 2. 직접 할 때

### 만든다

```bash
git clone https://github.com/VntgCorp/terroir-community-plugin
cd terroir-community-plugin
git checkout -b add-dockerize
```

무엇을 어디에 만드는지는 [플러그인 표준](standard.md)을 보고 그대로 채운다. 요약하면
`plugins/<분류>/<이름>/` 아래에 `plugin.json` · `README.md` · `skills/<이름>/SKILL.md`
셋이다.

**분류는 한 줄로 고른다** — 이 스킬이 소스코드나 인프라를 직접 건드리나? 허용되는 분류는
[`.github/categories.txt`](../.github/categories.txt) 가 정본이다.

### 검사한다

```bash
node .github/scripts/assemble-marketplace.mjs           # marketplace.json 재조립
node .github/scripts/check-structure.mjs                # 구조 검사
node .github/scripts/check-version-bump.mjs origin/main  # 고치는 경우에만 걸린다
claude plugin validate .                                # 스키마
```

CI 가 돌리는 것과 같다. **첫 줄을 빼먹으면 떨어진다** — `marketplace.json` 은 생성물이라
손으로 고치지 않는다.

### 올린다

```bash
git add . && git commit -m "feat(<분류>): <이름> 추가"
gh pr create
```

**CI 가 통과하면 본인이 머지한다.** 누구의 승인도 기다리지 않는다.

다만 아래를 건드리면 플랫폼개발팀 승인이 필요하다.

| 경로 | 왜 |
|---|---|
| `docs/` · `README.md` · `CLAUDE.md` · `.github/` | 마켓의 뼈대 — 문서 · CI · 분류 목록 · 마켓 헤더 |
| `plugins/dev/skill-market/` | 기여 도구 |

`.claude-plugin/marketplace.json` 은 **여기 없다.** 조립되는 생성물이라 플러그인을
추가하면 반드시 바뀐다. 승인 대상으로 두면 모든 기여가 막힌다. 손으로 고친 것은 CI 가 잡는다.

**실행 코드가 들어 있어도 같다.** 훅·스크립트가 있는 플러그인에 추가 승인을 요구하지
않는다. 대신 설치하는 쪽이 그걸 알고 고르도록 [이 마켓은 무엇인가](about.md)가 밝힌다.

올리기 말고 다른 일 — 내리기 · 소유자 이관 · 남의 플러그인 고치기 · 분류 변경 — 은
[마켓을 바꾸는 절차](operations.md)에 있다.

## 3. 자주 걸리는 것

| 증상 | |
|---|---|
| 이름 중복으로 떨어짐 | 의미를 더하는 suffix 를 붙인다. 숫자는 쓰지 않는다 — [표준 3절](standard.md#3-이름) |
| `version` 미증가로 떨어짐 | 파일을 고쳤으면 `version` 도 올린다. 기준은 [버전업 경로](versioning.md) |
| `metadata.owner` 없음 | GitHub 핸들을 적는다. 사람 이름이 아니라 `@` 뒤에 쓰는 그 핸들 |
| `marketplace.json` 이 어긋남 | 조립기를 돌리고 다시 커밋한다. 손으로 고치지 않는다 |
| 허용되지 않은 분류 | [`.github/categories.txt`](../.github/categories.txt) 안의 이름을 쓴다 |
| `/` 자동완성에 안 뜸 | 설치 후 세션을 다시 시작한다. `/reload-plugins` 는 변경분만 반영한다 |
| 설치는 됐는데 스킬 0개 | `skills/<이름>/SKILL.md` 경로를 확인한다. `skills/SKILL.md` 는 다른 형태다 |
