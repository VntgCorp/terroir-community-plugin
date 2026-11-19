# terroir-community-plugin

> **VNTG 구성원이 만든 Claude Code 스킬을 서로 나눠 쓰는 사내 공유 마켓입니다.**
> 내가 만든 스킬을 동료가 쓰고, 동료가 만든 스킬을 내가 가져다 씁니다.

스킬은 누구나 만들 수 있습니다. 이 마켓은 만든 스킬이 만든 사람에게만 남지 않도록 하려고 있습니다.
그래서 심사를 두지 않습니다. 심사가 있으면 등록한 뒤 기다려야 하고, 그만큼 공유가 느려집니다.
대신 품질 책임은 등록한 사람에게 있습니다.

## 마켓 추가

Claude Code에 자연어로 입력합니다. 안 되면 명령어를 입력합니다.

| 자연어 | 안 될 때 명령어 |
|---|---|
| 「https://github.com/VntgCorp/terroir-community-plugin 마켓을 추가해줘」 | `/plugin marketplace add VntgCorp/terroir-community-plugin` |

**Terroir 온보딩을 마쳤으면 이미 추가돼 있습니다.** `/plugin`을 먼저 열어 확인합니다.

마켓을 추가하면 목록만 생기고, 아무것도 설치되지 않습니다. 무엇을 쓸지는 목록을 보고 고릅니다.

## 무엇이 있는지 보기

| 자연어 | 안 될 때 명령어 |
|---|---|
| 「terroir-community-plugin 마켓에 어떤 플러그인이 있는지 보여줘」 | `/plugin` 입력 후 **Discover** |

더 자세히 보려면 아래 [분류](#분류)에서 폴더를 열어 그 플러그인의 `README.md`를 읽습니다.

**고를 때 볼 곳**

| 어디를 | 무엇을 알 수 있나 |
|---|---|
| `description` | 무엇을 위해 만든 플러그인인지 한 줄 |
| README의 **전제 조건** | 외부 도구, 접근 권한, 다른 플러그인이 필요한지 |
| README의 **알려진 한계** | 무엇이 안 되는지. 만든 사람이 직접 적은 것 |
| `plugin.json`의 `metadata.owner` | 누가 만들었는지. 물어볼 사람 |

## 설치

| 자연어 | 안 될 때 명령어 |
|---|---|
| 「terroir-community-plugin 마켓에서 &lt;플러그인 이름&gt; 설치해줘」 | `/plugin install <플러그인 이름>@terroir-community-plugin` |

> [!important]
> 이 마켓의 스킬은 **동료가 만든 것이고, 품질 심사를 거치지 않았습니다.**
> 설치는 각자 판단합니다. 무엇이 설치되는지 `/plugin` 상세 화면의 **Will install**에서 확인하고,
> 모르는 스킬은 폴더를 열어 `SKILL.md`를 읽어 보기를 권합니다.
> 훅이 있으면 그 파일도 열어 봅니다. 훅은 세션이 시작될 때 저절로 실행됩니다.

쓰다가 막히면 소유자(`metadata.owner`)에게 묻습니다. 직접 고쳐도 되고, 그때는
[남의 플러그인을 고치는 절차](docs/operations.md#a2-남의-플러그인을-고친다)를 따릅니다.

## 스킬 등록

스킬은 Anthropic 공식 `skill-creator`로 만들고, 만든 스킬을 등록 도구 `skill-market`으로 등록합니다.
`skill-market`은 `SKILL.md` 본문을 써 주지 않습니다.

| 단계 | 자연어 | 안 될 때 명령어 |
|---|---|---|
| 등록 도구 설치 (처음 한 번) | 「terroir-community-plugin 마켓에서 skill-market 설치해줘」 | `/plugin install skill-market@terroir-community-plugin` |
| 지금 세션에 불러오기 (설치 직후) | 「플러그인 다시 불러와줘」 | `/reload-plugins` |
| 등록 시작 | 「내가 만든 스킬을 사내 공유 마켓에 등록하고 싶어」 | `/skill-market:new` |

등록 도구가 대화로 분류를 정하고, 기본 파일을 만들고, PR(변경 요청)까지 올려 줍니다.
준비부터 등록 뒤까지 전체 순서는 [스킬 등록 절차](docs/authoring.md)에 있습니다.

**내 플러그인은 처음부터 내가 머지합니다.** 승인을 기다리지 않습니다.
소유자 줄을 더하는 `.github/CODEOWNERS` 파일 자체에는 소유자를 걸지 않았기 때문입니다.
남의 플러그인을 고치면 그 소유자의 승인이 필요합니다.

## 분류

플러그인은 두 폴더 중 하나에 들어갑니다.

| 폴더 | 담는 것 |
|---|---|
| [`plugins/dev/`](plugins/dev) | 소스코드, 레포, 배포, 테스트, 인프라를 **직접 다루는** 것 |
| [`plugins/work/`](plugins/work) | 문서, 기록, 조사, 소통, 학습 |

**고르는 법은 질문 하나입니다.** 이 스킬이 소스코드나 인프라를 직접 건드리나요? 「예」면 `dev`, 「아니오」면 `work`입니다.

분류는 같은 성격의 플러그인이 5개 이상 모였을 때 늘립니다. 칸을 미리 만들지 않습니다.
허용되는 분류의 정본은 [`.github/categories.txt`](.github/categories.txt)이고, 추가하려면 플랫폼개발팀 승인이 필요합니다.

## 하려는 일에 따라 읽을 곳

| 하려는 일 | 어디 | 승인 |
|---|---|---|
| **무엇이 규칙인지** 알기: 어디에, 무엇을, 어떤 이름으로 | [docs/standard.md](docs/standard.md) | 없음 |
| 이 마켓이 무엇인지 알기 | [docs/about.md](docs/about.md) | 없음 |
| 스킬을 **새로 등록하기** | [docs/authoring.md](docs/authoring.md) | 필요 없음 |
| 등록한 것을 **고치기, 버전 올리기** | [docs/versioning.md](docs/versioning.md) | 필요 없음 |
| **남의** 플러그인 고치기 | [docs/operations.md](docs/operations.md#a2-남의-플러그인을-고친다) | 소유자 승인 |
| **등록 취소, 소유자 이관** | [docs/operations.md](docs/operations.md#a3-플러그인을-내린다) | 소유자 동의 |
| **분류, 마켓 이름, CI** 변경 | [docs/operations.md](docs/operations.md#b-플랫폼개발팀만-하는-일) | 플랫폼개발팀 승인 |
| 누가 무엇을 할 수 있는지 | [docs/permissions.md](docs/permissions.md) | 없음 |

> [!important]
> **이 표는 어디로 갈지만 알려 줍니다. 답이 아닙니다.** 「승인 필요 없음」이 「그냥 하면 된다」는
> 뜻은 아닙니다. 절차, 예외, 관례는 해당 문서에 있습니다.

**규칙 값의 정본은 위 문서들입니다.** 길이 상한이나 이름 규칙 같은 값은 외워서 답하지 말고
해당 문서를 읽습니다. 외워 두면 문서가 바뀔 때 어긋납니다.

스킬을 **잘 만드는 법**은 Anthropic 공식 플러그인이 알려 줍니다. 여기서 다시 설명하지 않습니다.
[스킬 등록 절차](docs/authoring.md)의 「공식 도구로 제작」 절을 봅니다.

## 업데이트

**자동 업데이트를 켭니다.** Terroir 온보딩을 마쳤으면 이미 켜져 있습니다.
직접 켜려면 아래 순서대로 합니다. 서드파티 마켓은 기본값이 꺼짐이라 처음 한 번 켜야 합니다.

1. `/plugin` 입력
2. **Marketplaces** 탭에서 `terroir-community-plugin` 선택
3. **Enable auto-update**

끄면 동료가 고친 내용이 내 설치본에 들어오지 않습니다. 켜면 설치본이 최신으로 유지되는 대신,
**동료가 버전을 올릴 때 내 설치본이 내가 보지 않은 코드로 바뀝니다.** 훅이 있으면 다음 세션이
시작될 때 저절로 실행되므로, 무엇이 들어오는지 본 뒤에 켜는 것이 좋습니다.

**목록에 새 플러그인이 안 보이면** 받아 둔 목록이 오래된 것입니다. 직접 받습니다.

```bash
claude plugin marketplace update terroir-community-plugin
claude plugin update <플러그인 이름>@terroir-community-plugin
```

받은 뒤 `/reload-plugins`를 입력하거나 세션을 다시 시작합니다.

## 요구사항

| 하려는 일 | 필요한 것 |
|---|---|
| **마켓 추가, 조회, 설치** | 없음. GitHub 계정도 필요 없습니다 |
| **스킬 등록, 수정** | VNTG GitHub 조직 구성원. Terroir 온보딩에서 「소프트웨어 개발」을 고르고 끝까지 진행하면 조직에 가입됩니다 |

**GitHub 계정만으로는 부족합니다.** `CODEOWNERS`의 소유자 줄은 이 레포에 쓰기 권한이 있는 사람만 인정됩니다.
쓰기 권한이 없으면 소유자 줄이 조용히 무시되고, 내 플러그인을 아무나 고칠 수 있게 됩니다.
