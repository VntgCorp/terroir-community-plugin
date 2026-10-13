#!/usr/bin/env python3
"""한국어 기술 문서를 용어집과 문장 규칙으로 검사한다.

사용
  python3 ko-lint.py <문서.md> [...]          문서를 검사해 걸린 곳을 출력한다. 걸리면 종료 코드 1
  python3 ko-lint.py --profile internal <...> 문체 규칙 없이 문장·어휘 규칙만 본다 (해라체 내부 문서)
  python3 ko-lint.py --hook                   PreToolUse hook 으로 쓴다. stdin 으로 도구 입력을 받는다

프로파일
  docs      전 규칙 + 용어집 + 종결 일관성 + 제목 형식 (기본값)
  internal  문장·어휘 규칙과 모호 표현만. hook 모드에서는 ~/.claude/ 아래 파일이 여기에 해당한다
  diagram   .svg 의 글자만 뽑아 문장 규칙과 용어집으로 본다 (hook 모드)

용어집 위치 (앞에서부터 처음 있는 것)
  1. 환경 변수 KO_STYLE_DIR
  2. ~/.claude/ko-style/            사용자가 쌓는 용어집. ko-doc-write 스킬이 처음 실행할 때 만든다
  3. 이 스크립트 옆의 ../ko-style/   플러그인에 들어 있는 초기본

  glossary-core.tsv · glossary-vague.tsv · domains/*.tsv 를 읽는다.
  glossary-vague.tsv 는 성격이 다르다 — 구어체를 바꾸는 것이 아니라 빠진 정보를 채우라고
  요구하고, 문체와 무관하므로 모든 프로파일에 적용한다. 금지 표현과 표준 표현을
  쌍으로 두는 것이 요점이다 — 금지만 있으면 대체 표현을 그 자리에서 또 지어내게 된다.
  표준 표현의 근거는 ko-style/sources.md 의 벤더 문서 실측이다.

코드는 검사하지 않는다
  코드블록과 인라인 코드를 걷어낸 뒤 검사한다.

규칙 추가 원칙
  1. '거의 항상 틀린' 패턴만 넣는다. 오탐이 한 번 나면 다음부터 KO-LINT-SKIP 를
     습관적으로 붙이게 된다.
  2. 자연스러운 용법과 겹치는 패턴은 뺀다. 뺀 이유를 규칙 옆 주석에 남긴다.
  3. 고치는 법은 방향까지 적는다. '빼라' 가 아니라 '무엇으로 바꿔라' 로 쓴다.
  4. 추가한 뒤 ko-lint.test.py 를 돌린다.

검사를 건너뛰려면 텍스트 어딘가에 KO-LINT-SKIP 를 넣는다.
"""

import json
import os
import re
import sys

HANGUL = re.compile(r"[가-힣]")

USER_STYLE_DIR = os.path.join(os.path.expanduser("~"), ".claude", "ko-style")
SEED_STYLE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "ko-style")


def style_dir():
    env = os.environ.get("KO_STYLE_DIR")
    if env:
        return env
    if os.path.isdir(USER_STYLE_DIR):
        return USER_STYLE_DIR
    return SEED_STYLE_DIR

# 명사 뒤에 붙는 조사. 용어집 noun 항목의 경계를 만들 때 쓴다.
# '앱을'·'앱 카드' 는 걸리고 '앱스토어'·'애플리케이션' 은 통과한다.
JOSA = "이가은는을를의에와과도만로으야여랑나며랄"

ALL = "*"

# (정규식, 규칙 이름, 고치는 법, 적용 프로파일)
# 오탐을 줄이려고 "거의 항상 틀린" 패턴만 넣었다.
RULES = [
    (
        # '고' 로 끝나는 명사(사고·참고·보고·광고·창고·신고·경고)와 겹치지 않는 어미만 넣는다.
        r"(?:하고|되고|있고|없고|않고|이고|았고|었고|였고|했고|겠고|같고|많고|좋고|싶고|아니고"
        r"|맞고|쓰고|넣고|빼고|받고|주고|만들고|걸고|잡고|찾고"
        r"|거나|지만|면서|으며|하며|는데|은데|아서|어서|해서|라서|이라|므로|니까"
        # 축약 '-어서' (박혀서·어려워서·들어가서). 명사(문서·순서·인증서)와 안 겹치는 형태만.
        r"|혀서|겨서|셔서|여서|워서|져서|쳐서|켜서|봐서|와서|가서|돼서|나서"
        # 띄어 쓴 '라' (…prod 라, 이). '인프라,'·'나라,' 는 앞에 공백이 없어 안 걸린다.
        r"|(?<=\s)라),",
        "연결어미 뒤 쉼표",
        "쉼표를 뺀다. 연결어미가 이미 두 절을 잇고 있다",
        ALL,
    ),
    (
        r"되어지|되어진|되어졌|보여지|보여진|보여졌|불려지|불리어지|쓰여지|쓰여진"
        r"|나뉘어지|나뉘어진|잊혀지|잊혀진|모여지|짜여지|담겨지|놓여지",
        "이중 피동",
        "피동을 한 번만 쓰거나 행위자를 주어로 세운다 (되어진다 → 된다)",
        ALL,
    ),
    (
        r"수 있을 수 있|가능성이 있을 수|것으로 보일 수도|일 수도 있을",
        "이중 완곡",
        "완곡을 한 겹만 쓴다. 아는 건 단정한다",
        ALL,
    ),
    (
        # 번역투 — 영어·일본어 문형을 한국어 조사로 풀지 않고 그대로 옮긴 자리.
        # 고치는 방향은 하나다: 행위자를 주어로 세우고 나머지는 조사로 직결한다.
        #
        # 일부러 뺀 패턴 (오탐이 잦아 규칙 신뢰를 깎는다)
        #   '에 대한'  — "이 프로젝트에 대한 권한" 처럼 조사 직결이 어색한 자리가 많다
        #   '에 있어'  — "토큰 안에 있어 조회가 필요 없다" 처럼 존재를 뜻하는 자리와 겹친다.
        #                번역투인 '에 있어서' 만 남긴다
        #   '로부터'   — "고객으로부터" 같은 표준 용법과 구분이 안 된다
        #   '로 인해'  — 인과를 밝히는 자리에서 자연스러운 경우가 절반이다
        r"에 있어서|에 대하여|에 대해서|에 대해(?=\s)"
        r"|에 관하여|에 관해서|관련하여"
        r"|을 가지고 있|를 가지고 있|[을를] 필요로 (?:하|한|함)"
        r"|에 의해|에 의한|로 하여금|을 통하여|를 통하여"
        r"|에 위치(?:하|한)|중의 하나|가운데 하나|위한 목적으로"
        r"|것이 (?:불)?가능(?:하|한)|라고 말할 수 있",
        "번역투",
        "행위자를 주어로 세우고 조사로 직결한다 "
        "(A 에 의해 생성된 B → A 가 만든 B / ~을 필요로 한다 → ~가 필요하다 / "
        "~에 대해 논의한다 → ~를 논의한다)",
        ALL,
    ),
    (
        # 주체를 지운 판단·추측. 누가 그렇게 봤는지 밝히면 문장이 짧아지고 책임도 분명해진다.
        # '확인된다' 는 뺐다 — "로그에서 확인된다" 는 근거를 가리키는 자연스러운 한국어다.
        r"로 판단된다|로 보여진다|것으로 예상된다|것으로 기대된다|것으로 사료된다"
        r"|것으로 파악된다|라고 여겨진다|로 여겨진다",
        "무주체 판단",
        "판단한 주체를 주어로 세우거나 그냥 단정한다 (~로 판단된다 → ~다 / 우리는 ~로 본다)",
        ALL,
    ),
    (
        r"결론적으로|요약하면|정리하자면|시사하는 바|주목할 만|다음과 같습니다"
        r"|크게 (?:두|세|네|다섯|2|3|4|5)\s*가지로",
        "결산 상투구·열거 도입",
        "빼고 바로 본론을 쓴다",
        ALL,
    ),
    (
        r"혁신적|획기적|압도적|전례\s?없는|비약적",
        "hype 형용사",
        "수치나 사실로 바꾼다",
        ALL,
    ),
    (
        # 자기 산출물에 중요도를 선언하는 상투구. 읽는 쪽에는 정보가 없고 바로 뒤에 오는
        # 예시가 이미 다 말해 준다. 사용자가 "AI 가 자주 쓰는 문장"으로 지목했다 (2026-09-01).
        #
        # 오탐 관리 — 서술어 형태만 잡는다. '핵심 내용'(티켓 리뷰 요청 양식의 절 제목) ·
        # '핵심 모듈' 처럼 명사를 꾸미는 자리는 걸리지 않는다.
        # '포인트' 는 앞 경계를 둔다 — '엔드포인트입니다'·'체크포인트입니다' 가 걸린다.
        r"핵심입니다|핵심이다|핵심이었|관건입니다|관건이다|(?<![가-힣])포인트입니다"
        r"|이(?:번)? ?(?:작업|변경|수정|리팩터링|PR|커밋|문서)의 핵심",
        "중요도 선언",
        "빼고 무엇을 어떻게 바꿨는지만 쓴다. 중요하다고 말하는 대신 예시를 보여 준다",
        ALL,
    ),
    (
        # 절 제목 — 국내 클라우드 문서 3사에서 1인칭 제목과 의문형 제목이 0건이다.
        # 실측은 ko-style/sources.md. 경어체로 쓴 사용자 문서에만 건다 —
        # 해라체로 쓰는 내부 ADR 은 의문형 제목을 쓰기도 한다.
        # 앞에 한글이 붙은 것(사내·안내·이내)은 배제한다 — '사내 정보'가 걸린 적이 있다.
        r"^#{1,6}\s+[^\n]*(?<![가-힣])(?:내가|내 |우리가|나의 )",
        "1인칭 절 제목",
        "명사구로 바꾼다 (내가 챙길 것 → 직접 설정할 항목)",
        "docs-polite",
    ),
    (
        r"^#{1,6}\s+[^\n]*(?:\?|는가|나요|까요|하나|있나|없나|되나|오나|가나|일까|을까)\s*$",
        "의문형 절 제목",
        "명사구로 바꾼다 (내 요청은 어디를 지나오나 → 요청 처리 경로)",
        "docs-polite",
    ),
]

TEXT_EXT = (".md", ".txt", ".markdown", ".html", ".htm")

# 도식은 프로파일이 따로다. 상자 라벨은 문장이 아니라 명사구를 쓴다.
DIAGRAM_EXT = (".svg",)


def noun_pattern(word):
    """명사 항목을 조사 경계가 있는 정규식으로 바꾼다.

    '앱을'·'앱 카드' 는 걸리고 '앱스토어'·'웹앱'·'애플리케이션' 은 통과한다.
    """
    esc = re.escape(word)
    return (
        r"(?<![가-힣A-Za-z])" + esc + r"(?=[\s.,·)\]}」』!?:;/]|$|[" + JOSA + r"])"
    )


def load_glossary():
    """ko-style 의 용어집을 RULES 와 같은 모양으로 읽어 온다.

    파일이 없거나 깨져 있으면 빈 목록을 준다 — 용어집 때문에 도구가 막히면 안 된다.
    """
    paths = [
        os.path.join(style_dir(), "glossary-core.tsv"),
        os.path.join(style_dir(), "glossary-vague.tsv"),
    ]
    domains = os.path.join(style_dir(), "domains")
    if os.path.isdir(domains):
        paths += sorted(
            os.path.join(domains, f) for f in os.listdir(domains) if f.endswith(".tsv")
        )

    out = []
    for path in paths:
        label = os.path.splitext(os.path.basename(path))[0].replace("glossary-", "")
        try:
            with open(path, encoding="utf-8") as f:
                rows = f.read().splitlines()
        except OSError:
            continue
        for row in rows:
            if not row.strip() or row.startswith("##"):
                continue
            cols = row.split("\t")
            if len(cols) < 3:
                continue
            kind, pattern, repl = cols[0].strip(), cols[1].strip(), cols[2].strip()
            source = cols[3].strip() if len(cols) > 3 else ""
            if kind == "noun":
                pattern = noun_pattern(pattern)
            fix = repl + (f" (실측: {source})" if source else "")
            if label == "vague":
                # 모호 표현은 문체와 무관하다. 내부 문서·커밋·대화까지 전부 검사한다 —
                # 문서마다 문체는 달라도 되지만 읽는 사람이 못 알아듣는 것은 어디서도 안 된다.
                out.append((pattern, "모호 표현", fix, ALL))
            else:
                out.append((pattern, f"용어집 {label}", fix, "docs diagram"))
    return out


def strip_code(text):
    """코드블록·인라인 코드·낱말 지칭을 걷어낸다. 명령·로그·인용은 내 문장이 아니다.

    따옴표로 감싼 짧은 토막은 낱말을 가리키는 자리다 — 런북의 `사용자가 "알아서" 라고 하면`
    이 실제로 걸렸다. 15자까지만 걷어내므로 따옴표로 감싼 긴 문장은 그대로 검사한다.
    """
    text = re.sub(r"```.*?```", " ", text, flags=re.S)
    text = re.sub(r"`[^`\n]*`", " ", text)
    text = re.sub(r'["“][^"“”\n]{1,15}["”]', " ", text)
    return text


def label_text(markup):
    """SVG 에서 사람이 읽는 글자만 뽑는다. 스타일·주석·좌표는 내 문장이 아니다.

    Edit 로 조각만 넘어와도 같은 방식으로 동작한다 — 태그가 없으면 원문 그대로 남는다.
    """
    markup = re.sub(r"<style.*?</style>", " ", markup, flags=re.S)
    markup = re.sub(r"<!--.*?-->", " ", markup, flags=re.S)
    markup = re.sub(r"<[^>]*>", "\n", markup)
    lines = [ln.strip() for ln in markup.splitlines()]
    return "\n".join(ln for ln in lines if ln)


def pick(payload):
    """(프로파일, 검사할 텍스트) 를 정한다."""
    tool = payload.get("tool_name", "")
    ti = payload.get("tool_input") or {}

    if tool in ("Write", "Edit"):
        path = ti.get("file_path") or ""
        raw = ti.get("content") or ti.get("new_string") or ""
        if path.lower().endswith(DIAGRAM_EXT):
            return "diagram", label_text(raw)
        if not path.lower().endswith(TEXT_EXT):
            return "", ""
        text = raw
        # 메모리·CLAUDE.md·스킬·용어집은 해라체로 쓰는 내부 문서다. 문체를 강제하지 않는다.
        if "/.claude/" in path:
            return "internal", text
        return "docs", text

    return "", ""


# 소수파가 이만큼 있어야 '섞였다' 로 본다. 절대 건수만 보면 해라체 문서의 인용 몇 줄이
# 걸린다 — ADR-004 는 해라체 185곳에 경어체 4곳(2%)이라 통과해야 한다.
MIX_MIN_COUNT = 5
MIX_MIN_RATIO = 0.10


def count_endings(text):
    """(경어체, 해라체) 종결 횟수. '입니다'·'습니다' 는 (?<!니) 가 해라체에서 빼 준다."""
    polite = len(
        re.findall(r"(?:니다|하세요|주세요|십시오|해요|예요)(?=[\s.,!?)\]」』]|$)", text, re.M)
    )
    plain = len(re.findall(r"(?<!니)다(?=\.(?:\s|$))", text, re.M))
    return polite, plain


def mixed_endings(text):
    """한 문서 안에 경어체와 해라체가 섞였는지 본다.

    경로 목록을 관리하는 대신 일관성만 본다. 어느 한쪽으로 쓴 문서는 그대로 통과한다.
    """
    polite, plain = count_endings(text)
    minor, major = min(polite, plain), max(polite, plain)
    mixed = minor >= MIX_MIN_COUNT and major and minor / major >= MIX_MIN_RATIO
    return mixed, polite, plain


def check(profile, text):
    hits = []

    # 경어체로 쓴 사용자 문서에만 거는 규칙이 있다. 문체로 문서 성격을 가려내면
    # 경로 목록을 따로 관리하지 않아도 된다.
    scopes = {profile}
    polite, plain = count_endings(text) if profile == "docs" else (0, 0)
    if profile == "docs" and polite > plain:
        scopes.add("docs-polite")

    for pattern, name, fix, scope in RULES + load_glossary():
        if scope != ALL and not (scopes & set(scope.split())):
            continue
        found = re.findall(pattern, text, re.M)
        if not found:
            continue
        sample = ", ".join(
            sorted({f if isinstance(f, str) else f[0] for f in found})[:4]
        )
        hits.append(f"- {name}: {sample} → {fix}")

    if profile == "docs":
        mixed, polite, plain = mixed_endings(text)
        if mixed:
            hits.append(
                f"- 종결어미 혼용: 경어체 {polite}곳 · 해라체 {plain}곳 → "
                "사용자 문서는 경어체로 통일한다. 서술은 ~합니다, 지시는 ~하세요 "
                "(NHN·카카오·NCP·토스 4종 실측, ko-style/sources.md)"
            )

    return hits


def hook():
    payload = json.loads(sys.stdin.read())
    profile, text = pick(payload)

    if not profile or not text:
        return
    if "KO-LINT-SKIP" in text:
        return
    if not HANGUL.search(text):
        return

    hits = check(profile, strip_code(text))
    if not hits:
        return

    reason = (
        f"한국어 규칙에 걸렸다 (프로파일: {profile}). 아래를 고쳐서 다시 호출한다.\n"
        + "\n".join(hits)
        + "\n(원문 인용·로그라면 텍스트에 KO-LINT-SKIP 를 넣어 통과시킨다. "
        f"용어집은 {style_dir()} 이고 근거는 sources.md 다)"
    )
    print(
        json.dumps(
            {
                "hookSpecificOutput": {
                    "hookEventName": "PreToolUse",
                    "permissionDecision": "deny",
                    "permissionDecisionReason": reason,
                }
            },
            ensure_ascii=False,
        )
    )


def cli(argv):
    profile = "docs"
    if argv[:1] == ["--profile"]:
        if len(argv) < 2 or argv[1] not in ("docs", "internal"):
            print("--profile 은 docs 또는 internal 이다", file=sys.stderr)
            return 2
        profile, argv = argv[1], argv[2:]
    if not argv:
        print(__doc__.split("\n\n")[1], file=sys.stderr)
        return 2

    failed = 0
    for path in argv:
        try:
            with open(path, encoding="utf-8") as f:
                text = f.read()
        except OSError as e:
            print(f"{path}: 읽을 수 없다 — {e.strerror}", file=sys.stderr)
            failed += 1
            continue
        if "KO-LINT-SKIP" in text or not HANGUL.search(text):
            print(f"{path}: 건너뜀")
            continue
        hits = check(profile, strip_code(text))
        if not hits:
            print(f"{path}: 통과")
            continue
        failed += 1
        print(f"{path}: {len(hits)}건")
        print("\n".join(hits))
    print(f"\n용어집: {os.path.abspath(style_dir())}")
    return 1 if failed else 0


if __name__ == "__main__":
    if sys.argv[1:2] == ["--hook"]:
        try:
            hook()
        except Exception:
            pass
    else:
        sys.exit(cli(sys.argv[1:]))
