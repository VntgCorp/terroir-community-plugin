# skill-market

이 마켓에 스킬을 올릴 때 쓰는 도구.

스킬은 Anthropic 공식 `skill-creator` 로 만들고, 만든 스킬을 `/skill-market:new` 로 올린다. `skill-market` 은 `SKILL.md` 본문을 써 주지 않는다.

## 무엇을 하나

`/skill-market:new` 를 부르면 대화로 물어보고 아래를 대신한다.

| | |
|---|---|
| 분류 판정 | 소스코드·인프라를 건드리나로 `dev` / `work` 를 가른다 |
| 이름 | 문자 규칙을 맞추고 **마켓 전체에서 중복을 실제로 조회한다** |
| 뼈대 생성 | `plugin.json` · `README.md` · `skills/<이름>/SKILL.md` |
| 로컬 검증 | 목록 등재 + CI 와 같은 검사 + `claude plugin validate` |
| PR | 브랜치 · 커밋 · `gh pr create` 까지 |

[플러그인 표준](../../../docs/standard.md)과 [스킬 제작 방법](../../../docs/authoring.md)을 그대로 수행한다. 규칙 값은
외워 두지 않고 그 문서를 읽어서 쓴다 — 문서가 바뀌면 이 스킬도 같이 바뀐다.

## 쓰는 법

```
/plugin install skill-market@terroir-community-plugin
/skill-market:new
```

"마켓에 스킬 올리고 싶어" 같은 말에도 뜬다.

## 전제 조건

| | |
|---|---|
| 외부 도구 | `git` · `gh`(로그인됨) · `node` |
| 접근 권한 | `VntgCorp/terroir-community-plugin` 레포에 write 이상 |
| 다른 플러그인 | 없음. `terroir-context` 가 있으면 CHANGELOG 항목을 그 스킬로 쓰고, 없으면 작성 기준 문서를 읽는다 |

터미널 없이 올리려면 이 스킬을 쓰지 않고 [터미널 없이 올리기](../../../docs/authoring.md)
절차를 따른다.

## 아는 한계

- **`SKILL.md` 본문을 대신 쓰지 않는다.** 무엇을 하는 스킬인지는 만드는 사람이 안다.
  초안이 필요하면 공식 `skill-creator@claude-plugins-official` 로 넘긴다
- **머지하지 않는다.** PR 생성까지가 끝이다
- 이미 있는 플러그인의 **버전업은 다루지 않는다.** 그건 [버전업 경로](../../../docs/versioning.md)
  를 보고 직접 한다

## 소유자

플랫폼개발팀 (@VntgCorp/r-d) — 기여 도구라 뼈대로 취급한다. 변경에는 팀 승인이 필요하다.
