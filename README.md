# terroir-community-plugin

> **구성원이 만든 Claude Code 스킬을 서로 나눠 쓰는** 사내 공유 마켓플레이스.
> 내가 만든 것이 옆자리에 닿고, 옆자리가 만든 것을 내가 가져다 쓴다.

스킬은 누구나 만든다. 만든 것이 만든 사람에게만 남는 것을 막으려고 이 마켓이 있다.
그래서 심사를 두지 않는다 — 심사하면 올린 뒤 기다려야 하고, 그러면 공유가 느려진다.

## 떼루아 마켓 셋 중 어디인가

셋은 **같은 세 가지로 갈린다** — 누가 넣나 · 누가 쓸 수 있나 · 누가 품질을 책임지나.

| 마켓 | 누가 넣나 | 쓸 수 있는 사람 | 품질 책임 | 담기는 것 |
|---|---|---|---|---|
| [`terroir-claude-plugin-public`](https://github.com/VntgCorp/terroir-claude-plugin-public) | 플랫폼개발팀 | 누구나 — 인증 없이 | 팀 | 온보딩 · 단계 무관 부가 기능 |
| [`terroir-claude-plugin`](https://github.com/VntgCorp/terroir-claude-plugin) | 플랫폼개발팀 | 조직 멤버 | 팀 | 떼루아 맵 단계별 표준 흐름 |
| **`terroir-community-plugin`** (여기) | **구성원 누구나** | 누구나 — 인증 없이 | **올린 사람** | **무엇이든** |

**어디에 올릴지 가르는 질문은 하나다** — 떼루아 표준 흐름을 바꾸는 것인가, 내가 쓰려고
만든 것인가. 앞이면 [`terroir-claude-plugin`](https://github.com/VntgCorp/terroir-claude-plugin) 에
문의하고, 뒤면 여기다. 자세한 역할 구분은 [이 마켓은 무엇인가](docs/about.md)에 있다.

## 등록

```
/plugin marketplace add VntgCorp/terroir-community-plugin
```

**등록하면 목록만 생긴다.** 아무것도 설치되지 않는다 — 무엇을 쓸지는 보고 고른다.
온보딩을 거쳤으면 이미 등록돼 있을 수 있으니 `/plugin` 을 먼저 열어 본다.

## 무엇이 있는지 보기

```
/plugin → Discover
```

목록에서 이름과 한 줄 설명이 보인다. 더 보고 싶으면 아래 [분류](#분류)에서 디렉토리를
열어 그 플러그인의 `README.md` 를 읽는다.

**무엇을 보고 고르나.**

| 어디를 | 무엇을 알 수 있나 |
|---|---|
| `description` | 무엇을 하는 것인지 한 줄 |
| README 의 **전제 조건** | 외부 도구·접근 권한·다른 플러그인이 필요한가 |
| README 의 **아는 한계** | 무엇이 안 되는가. 만든 사람이 직접 적은 것 |
| `plugin.json` 의 `metadata.owner` | 누가 만들었나 — 물어볼 사람 |

## 설치

```
/plugin install <플러그인-이름>@terroir-community-plugin
```

> [!important]
> 여기 올라온 스킬은 **동료가 만든 것이고 품질 심사를 거치지 않았다.**
> 설치는 각자의 선택이다. 무엇이 설치되는지 `/plugin` 상세의 **Will install** 로 확인하고,
> 모르는 스킬은 디렉토리를 열어 `SKILL.md` 를 읽어 보는 것을 권한다.
> 훅이 있으면 그 파일을 열어 본다 — 훅은 세션이 시작될 때 저절로 돈다.

쓰다가 막히면 소유자에게 묻는다(`metadata.owner`). 직접 고쳐도 되고, 그때는
[마켓을 바꾸는 절차](docs/operations.md#a2-남의-플러그인을-고친다)를 따른다.

## 올리기

```
/plugin install skill-market@terroir-community-plugin
/skill-market:new
```

대화로 물어보고 뼈대 생성부터 PR 까지 해준다. 직접 하려면 [스킬 제작 방법](docs/authoring.md)을 본다.

**자기 플러그인은 처음부터 본인이 머지한다.** 승인을 기다리지 않는다 — 소유자 줄을
더하는 `.github/CODEOWNERS` 에는 소유자를 걸지 않았다. 남의 플러그인을 고치면
그 소유자의 승인이 필요하다.

## 분류

플러그인은 두 디렉토리 중 하나에 들어간다.

| 디렉토리 | 담는 것 |
|---|---|
| [`plugins/dev/`](plugins/dev) | 소스코드 · 레포 · 배포 · 테스트 · 인프라를 **직접 다루는** 것 |
| [`plugins/work/`](plugins/work) | 문서 · 기록 · 조사 · 소통 · 학습 |

**고르는 법 한 줄** — 이 스킬이 소스코드나 인프라를 건드리나? 예 → `dev` · 아니오 → `work`

분류를 늘리는 것은 같은 성격이 5개 이상 모였을 때 한다. 미리 칸을 만들지 않는다.
[`.github/categories.txt`](.github/categories.txt) 가 정본이고, 추가에는 플랫폼개발팀 승인이 필요하다.

## 하려는 일에 따라 읽을 곳

| 하려는 일 | 어디 | 승인 |
|---|---|---|
| **무엇이 규칙인가** — 어디에 · 무엇을 · 어떤 이름으로 | [docs/standard.md](docs/standard.md) | — |
| 이 마켓이 무엇인지 알기 | [docs/about.md](docs/about.md) | — |
| 스킬을 **새로 올리기** (절차) | [docs/authoring.md](docs/authoring.md) | 불필요 |
| 올린 것을 **고치기 · 버전 올리기** | [docs/versioning.md](docs/versioning.md) | 불필요 |
| **남의** 플러그인 고치기 | [docs/operations.md](docs/operations.md#a2-남의-플러그인을-고친다) | 소유자 승인 |
| **내리기 · 이관** | [docs/operations.md](docs/operations.md#a3-플러그인을-내린다) | 소유자 동의 |
| **분류 · 마켓 이름 · CI** 변경 | [docs/operations.md](docs/operations.md#b-플랫폼개발팀만-하는-일) | 팀 승인 |
| 누가 무엇을 할 수 있는지 | [docs/permissions.md](docs/permissions.md) | — |

> [!important]
> **이 표는 어디로 갈지만 말한다. 답이 아니다.** 「승인 불필요」가 「그냥 하면 된다」는
> 뜻은 아니다 — 절차 · 예외 · 관례는 해당 문서에 있다.

**규칙 값의 정본은 위 문서들이다.** 길이 상한 · 이름 규칙 같은 것을 외워서 답하지 말고
해당 문서를 읽는다. 외워 두면 문서가 바뀔 때 갈린다.

스킬을 **잘 만드는 법** 자체는 Anthropic 공식 플러그인이 가르친다. 여기서 다시 설명하지 않는다 —
[스킬 제작 방법](docs/authoring.md)의 첫 절을 보라.

## 업데이트

**이 마켓은 자동 업데이트를 켜지 않는다.** 서드파티 마켓은 기본이 OFF 이고, 여기서는
그대로 둔다 — 켜면 동료가 버전을 올릴 때 내 설치본이 **내가 보지 않은 코드로** 바뀌고,
훅이 있으면 다음 세션이 시작될 때 저절로 돈다. 꺼 두면 설치할 때 확인한 코드가 그대로
남는다. 팀이 검증하는 채널과 다르게 다루는 유일한 지점이다.

새 버전은 필요할 때 직접 받는다.

```bash
claude plugin marketplace update terroir-community-plugin
claude plugin update <플러그인-이름>@terroir-community-plugin
```

갱신 후 `/reload-plugins` 를 실행하거나 세션을 다시 시작한다.

## 요구사항

| 하려는 일 | 필요한 것 |
|---|---|
| **등록 · 조회 · 설치** | 없음. GitHub 계정도 필요 없다 |
| **올리기 · 고치기** | GitHub 계정 + `VntgCorp/vntg_internal` 팀 가입 |

**계정만으로는 부족하다.** `CODEOWNERS` 는 write 이상을 가진 사람만 유효해서,
팀에 없으면 소유자 줄이 조용히 무시된다 — 내 플러그인을 아무나 고칠 수 있게 된다.
