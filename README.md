# terroir-community-plugin

> 사내 구성원이 **직접 만든 Claude Code 스킬을 올리고 가져다 쓰는** 마켓플레이스.
> 플랫폼개발팀이 검증해 제공하는 [`terroir-claude-plugin`](https://github.com/VntgCorp/terroir-claude-plugin) 과는 **다른 채널**이다.

| | 팀 큐레이션 | 여기 |
|---|---|---|
| 레포 | `terroir-claude-plugin` | `terroir-community-plugin` |
| 누가 올리는가 | 플랫폼개발팀 | **구성원 누구나** |
| 무엇을 보증하는가 | 팀이 검증한 품질 | **형식만** — 품질 심사는 하지 않는다 |
| 다루는 것 | 떼루아 맵 단계별 표준 흐름 | 개인이 만든 무엇이든 |

자세한 역할 구분은 [이 마켓은 무엇인가](docs/about.md)에 있다.

## 설치

```
/plugin marketplace add VntgCorp/terroir-community-plugin
```

```
/plugin install <플러그인-이름>@terroir-community-plugin
```

무엇이 있는지는 `/plugin` 의 **Discover** 탭에서 보거나, 아래 [분류](#분류)에서 디렉토리를 열어 본다.

> [!important]
> 여기 올라온 스킬은 **동료가 만든 것이고 품질 심사를 거치지 않았다.**
> 설치는 각자의 선택이다. 무엇이 설치되는지 `/plugin` 상세의 **Will install** 로 확인하고,
> 모르는 스킬은 디렉토리를 열어 `SKILL.md` 를 읽어 보는 것을 권한다.

## 올리기

```
/plugin install skill-market@terroir-community-plugin
/skill-market:new
```

대화로 물어보고 뼈대 생성부터 PR 까지 해준다. 직접 하려면 [스킬 제작 방법](docs/authoring.md)을 본다.

올린 뒤 고치는 것은 **본인이 PR 올리고 본인이 머지한다.** 누구의 승인도 기다리지 않는다.

## 분류

플러그인은 두 디렉토리 중 하나에 들어간다.

| 디렉토리 | 담는 것 |
|---|---|
| [`plugins/dev/`](plugins/dev) | 소스코드 · 레포 · 배포 · 테스트 · 인프라를 **직접 다루는** 것 |
| [`plugins/work/`](plugins/work) | 문서 · 기록 · 조사 · 소통 · 학습 |

**고르는 법 한 줄** — 이 스킬이 소스코드나 인프라를 건드리나? 예 → `dev` · 아니오 → `work`

분류를 늘리는 것은 같은 성격이 5개 이상 모였을 때 한다. 미리 칸을 만들지 않는다.
[`.github/categories.txt`](.github/categories.txt) 가 정본이고, 추가에는 플랫폼개발팀 승인이 필요하다.

## 문서

| | |
|---|---|
| [**플러그인 표준**](docs/standard.md) | **무엇이 규칙인가** — 어디에 · 무엇을 · 어떤 이름으로 · CI 가 보는 것 |
| [이 마켓은 무엇인가](docs/about.md) | 목적 · 팀 채널과의 역할 구분 · 무엇을 보증하지 않는가 |
| [스킬 제작 방법](docs/authoring.md) | 처음 올리는 사람을 위한 절차 |
| [버전업 경로](docs/versioning.md) | 언제 어떤 자리를 올리는가 · CHANGELOG · 사용자에게 어떻게 닿는가 |
| [마켓을 바꾸는 절차](docs/operations.md) | 내리기 · 이관 · 분류 변경 · 헤더 변경 — 각 절차의 승인 조건 |
| [권한](docs/permissions.md) | 누가 무엇을 할 수 있는가 · 무엇이 그것을 강제하는가 · 접근 받는 법 |

스킬을 **잘 만드는 법** 자체는 Anthropic 공식 플러그인이 가르친다. 여기서 다시 설명하지 않는다 —
[스킬 제작 방법](docs/authoring.md)의 첫 절을 보라.

## 업데이트

서드파티 마켓플레이스는 자동 업데이트가 기본 OFF 다. 최초 1회 켠다.

1. `/plugin` 입력
2. **Marketplaces** 탭에서 `terroir-community-plugin` 선택
3. **Enable auto-update**

즉시 받으려면 셸에서:

```bash
claude plugin marketplace update terroir-community-plugin
claude plugin update <플러그인-이름>@terroir-community-plugin
```

갱신 후 `/reload-plugins` 를 실행하거나 세션을 다시 시작한다.

## 요구사항

- VntgCorp 조직 멤버십 (private 레포)
- `gh auth login` 으로 GitHub 인증
