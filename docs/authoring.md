# 스킬 제작 방법

이 문서는 **이 마켓의 규약**만 다룬다. 스킬 자체를 잘 만드는 법은 Anthropic 공식 플러그인이
가르치고, 그쪽이 정본이다.

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

`SKILL.md` 를 어떻게 쓰는지, `description` 을 어떻게 트리거로 만드는지, 본문을 어떻게 나누는지는
**전부 저기서 배운다.** 이 문서는 그 내용을 옮겨 적지 않는다 — 옮기면 공식이 업데이트될 때
이 문서만 뒤처진다.

아래부터가 **여기에만 있는 규약**이다.

---

## 1. 가장 빠른 길

```
/plugin install skill-market@terroir-community-plugin
/skill-market:new
```

대화로 물어보고 아래 2~4절을 전부 대신 해준다 — 분류 판정 · 이름 중복 검사 · 뼈대 생성 ·
로컬 검증 · PR 생성까지. **직접 할 이유가 없으면 이걸 쓴다.**

아래는 직접 할 때의 절차이고, 스캐폴더가 무엇을 하는지의 설명이기도 하다.

---

## 2. 어디에 둘 것인가

```
plugins/
├── dev/      소스코드 · 레포 · 배포 · 테스트 · 인프라를 직접 다룬다
└── work/     문서 · 기록 · 조사 · 소통 · 학습
```

**고르는 법 한 줄** — 이 스킬이 소스코드나 인프라를 건드리나? 예 → `dev` · 아니오 → `work`

「누가 쓰는가」가 아니라 **「무엇을 건드리는가」**로 가른다. 개발자가 쓰는 회의록 정리 스킬은
`work` 다.

> 둘 다 아닌 것 같아도 **둘 중 하나를 고른다.** 새 분류는 같은 성격이 5개 이상 모였을 때 만들고,
> 추가에는 플랫폼개발팀 승인이 필요하다(`.github/categories.txt`). 애매하면 `work` 다.

## 3. 이름

```
plugins/<분류>/<이름>/
```

| 규칙 | |
|---|---|
| 문자 | 소문자 · 숫자 · 하이픈만. `^[a-z0-9][a-z0-9-]{1,63}$` |
| 유일성 | **마켓 전체에서 유일해야 한다.** 분류가 달라도 겹치면 안 된다 |
| 일치 | 디렉토리명 == `plugin.json` 의 `name` |
| 금지 | `claude` · `anthropic` 으로 **시작**하면 설치가 안 된다. 이름 안에 단어로 들어가도 경고가 뜬다 |

**이미 있는 이름이면 의미를 더하는 suffix 를 붙인다.**

```
○  curriculum-fe       curriculum-sales
✕  curriculum-2        정보가 없다 — 둘 중 뭘 설치할지 못 고른다
✕  jsik94-curriculum   소유자 접두어는 쓰지 않는다
```

소유자를 이름에 박지 않는 것은 의도된 선택이다. 세션에 `<플러그인>:<스킬>` 로 뜨는데
접두어를 붙이면 `jsik94-curriculum:curriculum` 이 된다. 소유자는 `plugin.json` 이 기록한다.

## 4. 만들 파일

```
plugins/dev/dockerize/
├── .claude-plugin/plugin.json ···· 필수
├── README.md ····················· 필수
├── skills/dockerize/SKILL.md ····· 필수 (최소 하나)
├── CHANGELOG.md ·················· 두 번째 버전부터
└────────── 아래는 전부 자유 ──────────
    references/ · scripts/ · hooks/ · examples/ · agents/ · commands/ · 그 밖에 뭐든
```

**「유효한 플러그인인가」만 확인하고 「어떻게 만들었나」는 묻지 않는다.**
`skills/` 안쪽 구성, 보조 파일, 에이전트를 두든 말든 전부 자유다. 훅·스크립트 같은
실행 코드도 제한하지 않는다 — 대신 설치하는 쪽이 그걸 안다는 전제로 운영한다.

### `plugin.json`

```json
{
  "name":        "dockerize",
  "description": "컨테이너화 절차를 안내한다",
  "version":     "1.0.0",
  "author":      { "name": "정윤식" },
  "metadata":    { "owner": "Jsik94" }
}
```

| 필드 | |
|---|---|
| `name` | 디렉토리명과 같아야 한다 |
| `description` | **설치 전 목록에 보이는 문장.** 무엇을 하는 것인지 한 줄로 |
| `version` | `Major.Minor.Patch`. 처음은 `1.0.0` |
| `author.name` | 사람 이름. 화면에 뜬다 |
| `metadata.owner` | **GitHub 핸들.** 소유자 기록과 리뷰 요청에 쓴다. 없으면 CI 가 떨어뜨린다 |

`category` 는 **적지 않는다.** 디렉토리 위치가 분류의 정본이고, 둘을 다 두면 반드시 갈린다.

### `README.md`

쓰는 사람이 설치 여부를 결정할 수 있을 만큼만 쓴다.

```markdown
# <이름>

한 줄 설명.

## 무엇을 하나
어떤 상황에서 무엇을 해주는지. 결과가 어떻게 나오는지.

## 쓰는 법
호출 예시. `/<플러그인>:<스킬>` 또는 어떤 말을 하면 뜨는지.

## 아는 한계
안 되는 것 · 전제 조건 · 주의할 것.

## 소유자
<이름> (@<GitHub 핸들>)
```

**「아는 한계」를 비우지 않는다.** 품질 심사가 없는 마켓이라, 무엇이 안 되는지를
만든 사람이 적는 것이 유일한 안전장치다.

### `SKILL.md` 의 `description`

```yaml
---
name: dockerize
description: 서비스를 컨테이너화할 때 사용. Dockerfile 작성·빌드·레지스트리 푸시 절차를 안내한다.
---
```

**description 은 "언제 이 스킬을 써야 하는가" 를 적는 자리다.** 스킬이 무엇을 하는지의
설명을 전부 여기 쏟아붓지 않는다 — 길어지면 모든 세션의 컨텍스트를 잡아먹고, 트리거 판정도
오히려 흐려진다. 상세는 본문에 쓴다.

```
✕  description: 이 스킬은 Docker 를 사용하여 애플리케이션을 컨테이너화하는 과정을 단계별로
                안내합니다. 먼저 베이스 이미지를 선택하고, 의존성을 설치하고, 멀티스테이지
                빌드를 구성하고, 레이어 캐싱을 최적화하고, 보안 스캔을 수행하고, ...

○  description: 서비스를 컨테이너화할 때 사용. Dockerfile 작성·빌드·푸시 절차를 안내한다.
```

상한은 **500자**다. 참고로 `plugin.json` 의 `description` 은 **300자** — 설치 전 목록에
한 줄로 보이는 자리라 더 짧다.

## 5. 올리기

```bash
git clone https://github.com/VntgCorp/terroir-community-plugin
cd terroir-community-plugin
git checkout -b add-dockerize

# plugins/dev/dockerize/ 를 만든다

node .github/scripts/assemble-marketplace.mjs           # marketplace.json 을 다시 조립한다
node .github/scripts/check-structure.mjs                # 구조 검사
node .github/scripts/check-version-bump.mjs origin/main  # 고치는 경우에만 걸린다

git add . && git commit -m "feat(dev): dockerize 스킬 추가"
gh pr create
```

조립을 빼먹으면 CI 가 떨어지면서 이 명령을 알려 준다. `marketplace.json` 은
**손으로 고치지 않는다** — 고쳐도 다음 조립에서 되돌아간다.

**CI 가 통과하면 본인이 머지한다.** 누구의 승인도 기다리지 않는다.

다만 아래를 건드리면 플랫폼개발팀 승인이 필요하다.

| 경로 | 왜 |
|---|---|
| `docs/` · `README.md` · `.github/` | 마켓의 뼈대 — 문서 · CI · 분류 목록 · 마켓 헤더 |
| `plugins/dev/skill-market/` | 기여 도구 |

`.claude-plugin/marketplace.json` 은 **여기 없다.** 그 파일은 `plugins/` 에서 조립되는
생성물이라, 플러그인을 추가하면 반드시 바뀐다. 승인 대상으로 두면 모든 기여가 막힌다.
손으로 고친 것은 CI 가 잡는다.

**실행 코드가 들어 있어도 같다.** 훅·스크립트가 있는 플러그인에 추가 승인을 요구하지
않는다. 대신 설치하는 쪽이 그걸 알고 고르도록 [이 마켓은 무엇인가](about.md)가 밝힌다.

올리기 말고 다른 일 — 내리기 · 소유자 이관 · 남의 플러그인 고치기 · 분류 변경 —
은 [마켓을 바꾸는 절차](operations.md)에 있다.

## 6. CI 가 보는 것

| 검사 | |
|---|---|
| 분류 | `plugins/` 바로 아래가 `categories.txt` 안의 디렉토리인가 · 그 아래가 정확히 1단계인가 |
| 이름 | 문자 규칙 · 마켓 전체에서 유일한가 · 디렉토리명 == `plugin.json` 의 `name` |
| 매니페스트 | `description` · `version` · `author` · `metadata.owner` 가 있는가 |
| 파일 | `README.md` 가 있는가 · `skills/` 에 `SKILL.md` 가 최소 하나 있는가 |
| 스킬 | `SKILL.md` frontmatter 의 `name` · `description` 존재 · `description` 길이 |
| 버전 | 파일이 바뀌었는데 `version` 이 그대로인가 |
| 스키마 | `claude plugin validate` 통과 |

**떨어지면 메시지가 고치는 법을 알려준다.** 안 알려주면 그건 CI 의 버그다 — 이슈를 올려 달라.

## 7. 자주 걸리는 것

| 증상 | |
|---|---|
| 이름 중복으로 떨어짐 | 의미를 더하는 suffix 를 붙인다(3절). 숫자는 쓰지 않는다 |
| `version` 미증가로 떨어짐 | 파일을 고쳤으면 `version` 도 올린다. 기준은 [버전업 경로](versioning.md) |
| `metadata.owner` 없음 | GitHub 핸들을 적는다. 사람 이름이 아니라 `@` 뒤에 쓰는 그 핸들 |
| `/` 자동완성에 안 뜸 | 설치 후 세션을 다시 시작한다. `/reload-plugins` 는 변경분만 반영한다 |
| 설치는 됐는데 스킬 0개 | `skills/<이름>/SKILL.md` 경로를 확인한다. `skills/SKILL.md` 는 다른 형태다 |
