# 권한

누가 무엇을 할 수 있고, 무엇이 그것을 강제하는가.

절차 자체는 [마켓을 바꾸는 절차](operations.md)에 있다. 이 문서는 **왜 그렇게 되는지**와
**접근이 없을 때 어떻게 받는지**를 다룬다.

## 등급

레포 접근은 GitHub 팀으로만 준다. 개인에게 직접 붙이지 않는다 — 출처를 못 가르게 된다.

| 팀 | 등급 | 할 수 있는 것 |
|---|---|---|
| `@VntgCorp/r-d` | admin | 아래 전부 + 레포 설정(보호 규칙·팀 권한) |
| `@VntgCorp/vntg_internal` | write | 브랜치 push · PR 생성 · 자기 PR 머지(CI 통과 시) |
| (팀 없음) | read | 열람 · 설치 · 이슈. **브랜치를 못 올린다** |

선은 **read 와 write 사이**다. read 는 가져간 행위가 레포에 남지 않고, 그 위는 전부
커밋으로 남는다.

> 숫자는 바뀐다. 지금 상태는 아래로 확인한다.
> ```bash
> gh api repos/VntgCorp/terroir-community-plugin/teams --jq '.[] | "\(.slug)\t\(.permission)"'
> ```

## 기여하고 싶은데 read 라면

`vntg_internal` 팀에 들어 있지 않은 상태다. 두 길이 있다.

```
  1  팀에 들어간다 (권장)
     조직 담당자에게 vntg_internal 추가를 요청한다.
     이후 모든 사내 레포에 같은 등급이 적용된다

  2  fork 해서 PR 을 올린다
     read 만 있어도 된다. 다만 fork PR 은 CI 가 제한적으로 돌 수 있고,
     브랜치를 레포에 못 두므로 협업이 번거롭다
```

**1번이 맞다.** 이 마켓의 전제가 「구성원 누구나」이고, read 에 머무는 사람이 많다는 건
팀 구성이 안 맞는다는 뜻이지 이 레포가 풀 문제가 아니다.

## 누가 무엇을 할 수 있나

**뼈대를 고칠 때만 갈린다.** 플러그인은 누구에게나 같다.

```
                          R&D (14명)             타팀 write (70명)
  ──────────────────────────────────────────────────────────────────
  main 직접 push           ✗ 차단                 ✗ 차단
  플러그인 PR              CI 통과 후 본인 머지     CI 통과 후 본인 머지
  뼈대 PR                  CI 통과 후 본인 머지     코드오너 승인 필요
  CI 통과                  필수                   필수
```

플랫폼개발팀이 자기 영역을 고칠 때 팀 안에서 서로를 기다리지 않게 한 것이다.
**타팀이 뼈대를 건드릴 때는 반드시 팀 승인을 거친다.**

## 무엇이 그것을 강제하나 — 네 층

층마다 막는 것이 다르다. **하나만으로는 구멍이 난다.**

```
 ① 레포 보호 설정 ─ 전원 적용. enforce_admins 라 admin 도 예외 없다
    ┌────────────────────────────────────────────────────────────┐
    │  validate 통과     필수 · strict(최신 main 기준)            │
    │  force push·삭제   차단                                     │
    └────────────────────────────────────────────────────────────┘

 ② 룰셋「main 은 PR 로만」 ─ bypass 목록이 비어 있다. R&D 도 못 뚫는다
    ┌────────────────────────────────────────────────────────────┐
    │  main 에 직접 push 금지. 무엇이든 PR 을 거친다               │
    └────────────────────────────────────────────────────────────┘
                              │
                              │  ①②는 "validate 라는 체크가 초록인가"만 본다.
                              │  PR 이 검사를 빈 껍데기로 바꿔도 이름만 같으면 초록이다
                              ▼
 ③ 룰셋「뼈대 변경은 코드오너 승인」+ CODEOWNERS
    ─ ①②가 못 보는 「검사 내용의 약화」를 막는다. bypass = @VntgCorp/r-d
    ┌────────────────────────────────────────────────────────────┐
    │  /.github/                    @VntgCorp/r-d                 │
    │  /docs/                       @VntgCorp/r-d                 │
    │  /README.md                   @VntgCorp/r-d                 │
    │  /plugins/dev/skill-market/   @VntgCorp/r-d                 │
    └────────────────────────────────────────────────────────────┘
                              │
                              │  ③이 살아야 ①②의 초록불이 의미를 갖는다
                              ▼
 ④ CI ─ 실제 규칙 집행
    ┌────────────────────────────────────────────────────────────┐
    │  분류 · 깊이 · 이름 · 매니페스트 · 필수 파일 · 버전 · 스키마  │
    └────────────────────────────────────────────────────────────┘
```

> [!warning]
> **③의 bypass 는 「검사 내용의 약화」를 R&D 14명에게는 열어 둔다는 뜻이다.**
> 타팀 70명은 여전히 못 한다. 위험 범위를 0 으로 두는 대신 팀을 신뢰하는 선택이고,
> 되돌리려면 룰셋 `뼈대 변경은 코드오너 승인` 의 `bypass_actors` 를 비우면 된다.

### 확인하는 법

```bash
R=VntgCorp/terroir-community-plugin
gh api repos/$R/branches/main/protection --jq '{checks:.required_status_checks.contexts, enforce_admins:.enforce_admins.enabled}'
gh api repos/$R/rulesets --jq '.[] | "\(.name) [\(.enforcement)]"'
gh api repos/$R/codeowners/errors --jq '.errors | length'    # 0 이어야 한다
```

> [!important]
> **CODEOWNERS 는 write 이상을 가진 팀만 유효하다.** 접근 권한 없는 팀을 적으면 GitHub 이
> 그 줄을 **조용히 무시한다** — 에러가 아니라 침묵이라 모르고 지나가기 쉽다. 위의
> `codeowners/errors` 가 0 인지 보는 이유다.

### R&D 가 뼈대 PR 을 머지하는 법

**웹에서 한다.** PR 하단 머지 상자에 R&D 에게만 보이는 체크박스가 있다.

```
  ⚠ Merging is blocked
    Waiting on code owner review from VntgCorp/r-d

  ☐ Merge without waiting for requirements to be met (bypass rules)   ← 이것을 켠다
    [ Squash and merge ]
```

**이게 기본 경로다.** 「요건을 안 기다리고 머지한다」를 명시적으로 묻고, bypass 했다는
사실이 기록에 남는다. 타팀 사람에게는 이 체크박스가 **보이지 않는다** — 그쪽은
`Review required` 에서 실제로 멈춘다.

> [!note]
> **`gh pr merge` 는 거부한다.** bypass 가 안 걸린 것이 아니라, GitHub 이 주는
> `mergeStateStatus` 가 **누가 보는지와 무관하게 계산되어 bypass 를 반영하지 않기**
> 때문이다. `gh` 는 그 값을 보고 클라이언트에서 막는다. 서버는 통과시킨다.
>
> 터미널에서 해야 하면 REST 를 직접 쓴다.
> ```bash
> gh api -X PUT repos/VntgCorp/terroir-community-plugin/pulls/<번호>/merge -f merge_method=squash
> ```

내가 bypass 대상인지는 이것으로 확인한다 — `always` 면 대상이다.

```bash
gh api repos/VntgCorp/terroir-community-plugin/rulesets --jq '.[] | "\(.name): \(.current_user_can_bypass)"'
```

## 왜 개별 플러그인은 CODEOWNERS 에 없나

넣으면 **소유자가 자기 플러그인을 영원히 못 고친다.** GitHub 은 PR 작성자가 자기 PR 을
승인하는 것을 허용하지 않기 때문이다.

```
  @A 가 plugins/work/foo/ 를 고치는 PR 을 연다
        │
        ├─ CODEOWNERS 에 /plugins/work/foo/ @A 가 있다면
        │     → code owner 승인이 필요한데, 그 owner 가 작성자다
        │     → 자기가 승인 못 한다 → 남을 기다린다 → 「대기 없음」이 깨진다
        │
        └─ 없으면
              → 요구되는 승인이 없다 → CI 통과 후 본인이 머지
```

**대가가 하나 있다.** 남이 내 플러그인을 고쳐도 자동 리뷰 요청이 오지 않는다.
소유 기록은 `plugin.json` 의 `metadata.owner` 가 하고, 그건 권한이 아니라 **연락처**다.
어떻게 다루는지는 [절차 2절](operations.md#2-남의-플러그인을-고친다)에 있다.

## 지금 없는 것

| | 왜 없나 |
|---|---|
| 경로 제한 룰셋 | `file_path_restriction` 은 **GitHub Enterprise Cloud 전용**이다. 조직 플랜이 team 이라 못 쓴다. 분류 게이트는 ③ CI 가 대신하고, ③ 의 방어는 ② 가 한다 |
| 승인 당번 | 뼈대 PR 을 며칠 안에 누가 본다는 약속이 없다. 「아무나」는 「아무도」가 될 수 있다. 뼈대 변경이 잦아지면 정해야 한다 |
| 소유자 자동 핑 | 위 「대가」 참고. CI 가 `metadata.owner` 로 리뷰 요청을 거는 것으로 보완할 수 있고, 아직 안 했다 |

## 레포 설정을 바꾸려면

보호 규칙·팀 권한은 **PR 로 못 바꾼다.** 레포 설정이라 admin 이 직접 한다.

```bash
R=VntgCorp/terroir-community-plugin
# 팀 권한
gh api -X PUT orgs/VntgCorp/teams/<슬러그>/repos/$R -f permission=<pull|push|admin>
# 보호 규칙은 Settings → Branches, 또는 repos/$R/branches/main/protection
```

바꿨으면 **이 문서를 같이 고친다.** 설정과 문서가 갈리면 문서가 쓸모없어진다.
