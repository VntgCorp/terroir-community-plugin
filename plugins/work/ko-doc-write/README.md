# ko-doc-write

한국어 기술 문서를 쓰기 전에 유형과 목차를 정하고 국내 벤더 공식 문서에서 실측한 표현으로 쓴 뒤 검사한다.

## 무엇을 하는가

가이드·README·튜토리얼·트러블슈팅 문서를 새로 쓰거나 크게 고칠 때 아래 순서로 진행한다.

| 단계 | 내용 |
|---|---|
| 유형 정하기 | 학습 · 문제 해결 · 참조 · 설명 중 하나. 토스 테크니컬 라이팅 가이드 기준 |
| 목차 먼저 | 한 페이지 한 주제 · 첫 제목 아래 개요 · 30자 이내 평서문 제목 |
| 용어 구하기 | 주제의 용어집이 없으면 NHN Cloud · 카카오클라우드 · 네이버 클라우드 · 토스페이먼츠 · Kubernetes 한국어 · React · Vue · MDN 문서를 열어 원문 표현을 수집하고 용어집에 쌓는다 |
| 쓰기 | 수집한 표현과 종결어미 규칙으로 쓴다 |
| 검사 | `structure-check.py` 로 목차 구조를, `ko-lint.py` 로 용어집·번역투·이중 피동·종결어미 혼용을 본다 |

용어집 초기본이 함께 들어 있다 — core · vague(모호 표현) 와 도메인 열 개(security · network ·
container · observability · database · storage · ci-cd · frontend · api · console-ui).
처음 실행할 때 `~/.claude/ko-style/` 로 복사하고 그 뒤로는 거기에 쌓는다. 플러그인을
업데이트해도 사용자가 쌓은 용어집은 덮어쓰지 않는다.

## 쓰는 법

```
/plugin install ko-doc-write@terroir-community-plugin
/ko-doc-write:ko-doc-write
```

"가이드 써줘", "README 정리해줘", "트러블슈팅 문서 써줘" 같은 요청에도 스킬이 실행된다.

검사만 따로 돌릴 수도 있다. `<설치 경로>` 는 `/plugin` 상세에서 확인한다.

```bash
python3 <설치 경로>/skills/ko-doc-write/scripts/ko-lint.py docs/guide.md
python3 <설치 경로>/skills/ko-doc-write/scripts/structure-check.py docs/guide.md
```

### 저장할 때마다 자동 검사 (선택)

이 플러그인은 hook 을 등록하지 않는다. 등록하면 설치한 사람의 모든 세션에서 `.md` 저장이
규칙에 걸릴 때마다 차단되기 때문이다. 원하면 직접 등록한다 — 스크립트를 고정 경로로 복사한 뒤
`~/.claude/settings.json` 에 아래 설정을 추가한다. 플러그인 설치 경로는 버전마다 바뀌므로 그 경로를 바로 쓰지 않는다.

```bash
mkdir -p ~/.claude/hooks
cp <설치 경로>/skills/ko-doc-write/scripts/ko-lint.py ~/.claude/hooks/
```

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [{ "type": "command", "command": "python3 ~/.claude/hooks/ko-lint.py --hook" }]
      }
    ]
  }
}
```

hook 모드는 `.md` · `.txt` · `.html` · `.svg` 저장만 본다. `~/.claude/` 아래 파일은 해라체 내부
문서로 보고 문장 규칙과 모호 표현만 검사한다. 스크립트에서 예외가 나면 차단하지 않고 저장을 그대로 진행시킨다.

## 전제 조건

| | |
|---|---|
| 외부 도구 | `python3` (표준 라이브러리만 쓴다) |
| 접근 권한 | 없음. 용어집을 새로 수집할 때 WebSearch · WebFetch 로 공개 문서를 연다 |
| 다른 플러그인 | 없음 |

## 아는 한계

- **처음 보는 주제는 시간이 든다.** 도메인 용어집이 없으면 벤더 문서 여러 개를 열어 수집한 뒤에 쓴다. 한 번 모으면 다음부터 재사용한다
- **`ko-lint.py` 는 아는 표현만 잡는다.** 용어집과 규칙에 없는 어색한 표현은 걸리지 않는다. 오탐을 줄이려고 자연스러운 용법과 겹치는 패턴은 일부러 뺐다
- **이미 쓴 글의 문체만 다듬는 데는 맞지 않는다.** 유형·목차부터 다시 정하는 절차라 윤문 용도로는 과하다
- 사용자 가이드는 경어체(`~합니다` · `~하세요`)를 기본으로 본다. 레포지토리에 정한 문체가 따로 있으면 그것을 따른다
- 용어집 초기본의 실측일은 2026-08 ~ 2026-10 이다. 6개월이 지난 도메인은 스킬이 다시 열어 확인한다

## 소유자

박세윤 (@seyunpark)
