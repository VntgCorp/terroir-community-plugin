#!/usr/bin/env python3
"""ko-lint.py 회귀 테스트.

    python3 ko-lint.test.py

규칙이나 용어집을 고치면 반드시 돌린다. 일곱 묶음을 본다.

  1. POSITIVE  잡아야 하는 문장. 놓치면 규칙이 활용형에서 빗나간 것이다
               (실제로 '필요로 하' 가 '필요로 한다' 를 못 잡은 적이 있다 — 하/한/함을 함께 넣는다)
  2. NEGATIVE  잡으면 안 되는 문장. 자연스러운 용법과 겹치는 패턴을 걸러낸 근거다
  3. PROFILE   hook 모드의 프로파일 판정. 내부 문서에 문체를 강요하면 안 된다
  4. ENDING    종결어미 일관성. 해라체로 쓴 문서가 걸리면 임계치가 잘못된 것이다
  5. CLI       종료 코드 · 프로파일 옵션 · 읽기 실패 처리
  6. STYLE     용어집 위치 선택 (KO_STYLE_DIR → ~/.claude/ko-style → 플러그인 초기본)
  7. INIT      init-style.py — 없는 파일만 복사하고 사용자가 고친 파일은 덮어쓰지 않는다

용어집은 플러그인 초기본(../ko-style)으로 고정해서 돌린다. 사용자가 쌓은 용어집에
따라 결과가 바뀌면 회귀를 판정할 수 없다.
"""

import json
import os
import pathlib
import subprocess
import sys
import tempfile

HERE = pathlib.Path(__file__).resolve().parent
LINT = str(HERE / "ko-lint.py")
SEED = str(HERE.parent / "ko-style")
ENV = {**os.environ, "KO_STYLE_DIR": SEED}
TMP = pathlib.Path(tempfile.mkdtemp(prefix="ko-lint-test-"))


def run_cli(args, env=ENV):
    return subprocess.run([sys.executable, LINT, *args], capture_output=True, text=True, env=env)


def run_hook(payload):
    out = subprocess.run(
        [sys.executable, LINT, "--hook"], input=json.dumps(payload),
        capture_output=True, text=True, env=ENV,
    ).stdout.strip()
    if not out:
        return None
    return json.loads(out)["hookSpecificOutput"]["permissionDecisionReason"]


_n = 0


def write(text, name=None):
    global _n
    _n += 1
    p = TMP / (name or f"doc{_n}.md")
    p.write_text(text, encoding="utf-8")
    return str(p)


def lint(text):
    """걸리면 걸린 줄들을, 통과하면 None 을 준다."""
    r = run_cli([write(text)])
    if r.returncode == 0:
        return None
    return r.stdout


POSITIVE = [
    ("연결어미 쉼표", "락을 잡고, 네트워크를 기다린다."),
    ("이중 피동", "매니페스트가 생성되어진다."),
    ("에 의해", "매니페스트는 KMM 에 의해 생성된다."),
    ("필요로 하다", "이 작업은 별도 권한을 필요로 한다."),
    ("에 대해", "락 경합에 대해 논의했다."),
    ("에 있어서", "배포에 있어서 중요한 것은 순서다."),
    ("것이 가능하다", "동시에 처리하는 것이 가능하다."),
    ("중의 하나", "이것은 원인 중의 하나다."),
    ("을 통하여", "Lease 를 통하여 직렬화한다."),
    ("관련하여", "이번 장애와 관련하여 보고한다."),
    ("에 위치한다", "설정 파일은 루트에 위치한다."),
    ("로 하여금", "사용자로 하여금 재시도하게 한다."),
    ("로 판단된다", "일회성 장애로 판단된다."),
    ("것으로 예상된다", "다음 주에 반영될 것으로 예상된다."),
    ("hype", "획기적인 개선이다."),
    ("중요도 선언", "이번 변경의 핵심입니다."),
    ("결산 상투구", "결론적으로 설정은 하나입니다."),
    ("이중 완곡", "재시도할 수 있을 수 있다."),
    # 용어집 (2026-08-31) — 벤더 문서 실측 표현으로 치환한다
    ("용어집 앱", "앱을 배포합니다."),
    ("용어집 앱 - 띄어쓰기", "앱 카드에서 확인합니다."),
    ("용어집 레포", "레포에 커밋합니다."),
    ("용어집 유저", "유저가 요청합니다."),
    ("용어집 FE", "FE 워크로드를 먼저 봅니다."),
    ("용어집 BE", "BE 는 비공개로 둡니다."),
    ("용어집 막는다", "WAF 가 요청을 막는다."),
    ("용어집 통과한다", "80 포트는 그대로 통과한다."),
    ("용어집 새다", "시크릿이 새면 곤란합니다."),
    ("용어집 통째로", "본문을 통째로 기록합니다."),
    ("용어집 긁다", "메트릭을 클러스터 안에서 긁는다."),
    ("용어집 뜨다", "카탈로그에 엔티티가 뜬다."),
    ("용어집 떨구다", "CI wrapper 를 떨구는 도구다."),
    ("도메인 security 비번", "비번을 바꿉니다."),
    ("도메인 security root", "컨테이너를 root 로 실행합니다."),
    ("도메인 container 띄운다", "파드를 띄운다."),
    ("도메인 ci-cd 돌린다", "파이프라인을 돌린다."),
    ("도메인 observability 찍는다", "요청 본문을 로그에 찍는다."),
    ("도메인 frontend 그린다", "목록을 화면에 그린다."),
    ("도메인 api 던진다", "요청을 서버에 던진다."),
    ("도메인 database 날린다", "테이블을 날린다."),
    ("도메인 network 쏜다", "메트릭을 수집기로 쏜다."),
    ("core 자격증명", "자격증명을 폐기합니다."),
    ("core 앞단", "앞단에서 걸러집니다."),
    ("core 죽인다", "파드를 죽인다."),
    # 모호 표현 (2026-09-01) — 빠진 정보를 채우라고 요구하는 규칙
    ("모호 조용히", "에러를 조용히 무시합니다."),
    ("모호 알아서", "나머지는 알아서 처리됩니다."),
    ("모호 적당히", "값을 적당히 늘립니다."),
    ("모호 어느 정도", "어느 정도 시간이 걸립니다."),
    ("모호 사실상", "사실상 같은 결과입니다."),
    ("모호 등등", "로그, 메트릭 등등을 확인합니다."),
    ("모호 원활히", "서비스가 원활히 동작합니다."),
    ("모호 필요시", "필요시 재시도합니다."),
    ("모호 여러 가지", "여러 가지 방법이 있습니다."),
    ("모호 적절히 처리", "예외를 적절히 처리합니다."),
    ("모호 잘 동작", "배포 후에도 잘 동작합니다."),
    ("모호 문제없이", "문제없이 배포됩니다."),
    ("모호 경우에 따라 다릅니다", "설정은 경우에 따라 다릅니다."),
]

# 일부러 규칙에서 뺀 표현들. 여기가 깨지면 패턴이 너무 넓어진 것이다.
NEGATIVE = [
    ("에 대한", "이 프로젝트에 대한 권한이 없다."),
    ("로부터", "고객으로부터 받은 요청이다."),
    ("로 인해", "fetch 정지로 인해 대기자가 죽었다."),
    ("확인된다", "그 사실은 로그에서 확인된다."),
    ("안에 있어 (존재)", "role은 토큰 안에 있어 조회가 필요 없습니다."),
    ("-고 (쉼표 없음)", "락을 잡고 네트워크를 기다린다."),
    ("고로 끝나는 명사", "이번 사고 보고서를 참고 자료로 남긴다."),
    ("평범한 기술 문장", "KMM 이 매니페스트를 만든다. 파드가 갈려도 결과는 같다."),
    # 어휘 규칙이 넘치면 안 되는 자리 — '축' 이 들어간 정상 낱말들
    ("구축", "클러스터를 구축한다."),
    ("압축", "이미지를 압축한다."),
    ("축소", "조회 범위를 축소한다."),
    ("축적", "운영 경험이 축적된다."),
    ("단축", "빌드 시간을 단축한다."),
    ("감축", "인원을 감축한다."),
    ("기축", "기축통화 이야기다."),
    ("축약", "문장을 축약한다."),
    ("수축", "커넥션 풀이 수축한다."),
    ("실체계", "실체계 연동을 확인했다."),
    ("개인 금지어는 넣지 않았다", "건물 천장 높이와 회전 축을 잰다."),
    ("핵심 내용 (절 제목)", "## 핵심 내용\n변경 사항을 적습니다."),
    ("엔드포인트입니다", "이 주소가 엔드포인트입니다."),
    # 용어집이 넘치면 안 되는 자리
    ("표준 표현 애플리케이션", "애플리케이션을 배포합니다."),
    ("앱스토어", "앱스토어 심사를 통과했습니다."),
    ("PR을 올린다", "수정한 뒤 PR을 올립니다."),
    ("검토합니다", "먼저 그 경로를 검토합니다."),
    ("핵심은", "핵심은 안정적인 정렬 키입니다."),
    ("하나로 묶습니다", "에러 코드를 하나로 묶습니다."),
    ("prefix가 붙습니다", "실제로는 앞에 api/v1 이 붙습니다."),
    ("웹앱", "웹앱 형태로 제공합니다."),
    ("레포지토리", "레포지토리 히스토리에 남습니다."),
    ("영문 FE 아닌 것", "LIFE 와 SAFE 는 그대로 둡니다."),
    ("파일명 FE_", "FE_ARCHITECTURE 문서를 참고하세요."),
    ("코드블록 안", "설명입니다.\n```bash\n앱을 배포한다 && 막는다\n```\n끝입니다."),
    ("인라인 코드", "화면 라벨은 `앱` 입니다."),
    ("코드 안 FE", "변수는 `FE_HOST` 입니다."),
    ("통과시킵니다", "헤더가 없는 요청은 그대로 통과시킵니다."),
    ("라고 부른다 (명명)", "이런 방식을 Fast forward 라고 부른다."),
    ("큐에 쌓인", "큐에 쌓인 커밋을 한 번에 합칩니다."),
    ("이름을 붙이다", "컴포넌트에 이름을 붙이면서 시작합니다."),
    ("자격 요건", "자격 요건을 확인합니다."),
    ("자격 단독", "남의 자격으로 행동할 수 있습니다."),
    ("자격 증명", "자격 증명을 안전하게 보관합니다."),
    ("만든다", "브랜치를 만들면서 작업을 시작합니다."),
    ("돌아옵니다", "결제 승인에 성공하면 Payment 객체가 돌아옵니다."),
    ("노출한다", "서비스를 네트워크에 노출합니다."),
    ("화이트리스트", "화이트리스트 방식으로 동작합니다."),
    # 모호 표현 규칙이 넘치면 안 되는 자리 — 벤더가 실제로 쓰는 형태
    ("제대로 동작하지 않을", "일반적인 몇몇 문제들 때문에 서비스가 제대로 동작하지 않을 수 있다."),
    ("더 적절한 방법", "사용자 환경에 더 적절한 방법이 있다면 그것을 씁니다."),
    ("경우에 따라 발생", "애플리케이션 특성에 따라 발생할 수 있습니다."),
    ("다양한 문제", "겪을 수 있는 다양한 문제의 해결 방법입니다."),
    ("적절한 권한", "적절한 권한을 부여합니다."),
    ("따옴표 낱말 지칭", '사용자가 "알아서" 라고 하면 기본값으로 진행합니다.'),
    ("따옴표 낱말 지칭 2", '문서에 "조용히" 라고 쓰지 않습니다.'),
]

# (라벨, payload, 걸려야 하나) — hook 모드
PROFILE = [
    ("internal 문서는 용어집 미적용",
     {"tool_name": "Write", "tool_input": {"file_path": "/Users/x/.claude/memory/a.md", "content": "앱을 레포에 올린다."}},
     False),
    ("internal 문서도 문장 규칙은 적용",
     {"tool_name": "Write", "tool_input": {"file_path": "/Users/x/.claude/memory/a.md", "content": "매니페스트가 생성되어진다."}},
     True),
    ("internal 문서도 모호 표현은 적용",
     {"tool_name": "Write", "tool_input": {"file_path": "/Users/x/.claude/memory/a.md", "content": "예외가 나면 조용히 통과시킨다."}},
     True),
    ("docs 문서는 용어집 적용",
     {"tool_name": "Write", "tool_input": {"file_path": "/Users/x/work/repo/docs/a.md", "content": "앱을 배포합니다."}},
     True),
    ("Edit 의 new_string 도 검사",
     {"tool_name": "Edit", "tool_input": {"file_path": "/x/docs/a.md", "old_string": "a", "new_string": "앱을 배포합니다."}},
     True),
    ("svg 는 글자만 검사",
     {"tool_name": "Write", "tool_input": {"file_path": "/x/a.svg", "content": "<svg><text>앱 서버</text></svg>"}},
     True),
    ("svg 의 태그·스타일은 검사 안 함",
     {"tool_name": "Write", "tool_input": {"file_path": "/x/a.svg", "content": "<svg><style>.앱 {}</style><text>애플리케이션</text></svg>"}},
     False),
    ("Bash 는 검사 안 함",
     {"tool_name": "Bash", "tool_input": {"command": "echo '나머지는 알아서 처리됩니다'"}},
     False),
    ("py 파일은 검사 안 함",
     {"tool_name": "Write", "tool_input": {"file_path": "/tmp/a.py", "content": "앱을 배포합니다."}},
     False),
    ("KO-LINT-SKIP 은 통과",
     {"tool_name": "Write", "tool_input": {"file_path": "/x/docs/a.md", "content": "KO-LINT-SKIP\n앱을 배포합니다."}},
     False),
    ("한글 없는 문서는 통과",
     {"tool_name": "Write", "tool_input": {"file_path": "/x/docs/a.md", "content": "deploy the app, quietly."}},
     False),
]

POLITE = "\n".join(f"{i}번 항목을 확인하세요. 값을 입력합니다." for i in range(12))
PLAIN = "\n".join(f"{i}번 항목을 확인한다. 값을 넣는다." for i in range(12))
MIXED = POLITE + "\n" + PLAIN

ENDING = [
    ("경어체 일색", POLITE, False),
    ("해라체 일색", PLAIN, False),
    ("반반 혼용", MIXED, True),
    ("해라체에 인용 몇 줄", PLAIN + "\n확인했습니다. 반영했습니다. 배포했습니다.", False),
    ("경어체 문서의 의문형 제목", POLITE + "\n\n## 요청은 어디를 지나오나\n", True),
    ("해라체 문서의 의문형 제목", PLAIN + "\n\n## 요청은 어디를 지나오나\n", False),
    ("사내 정보 (1인칭 아님)", POLITE + "\n\n## 나가는 경계 — 사내 정보 외부 전송\n", False),
    ("안내 문구 (1인칭 아님)", POLITE + "\n\n## 안내 문구 작성\n", False),
    ("경어체 문서의 1인칭 제목", POLITE + "\n\n## 내가 챙길 것\n", True),
]

def names_of(out):
    return [l.split(":")[0].lstrip("- ") for l in out.splitlines() if l.startswith("- ")]


def check_cli():
    """(라벨, 통과 여부) 목록."""
    res = []
    clean, dirty = write("애플리케이션을 배포합니다."), write("앱을 배포합니다.")
    res.append(("통과하면 종료 코드 0", run_cli([clean]).returncode == 0))
    res.append(("걸리면 종료 코드 1", run_cli([dirty]).returncode == 1))
    r = run_cli([clean, dirty])
    res.append(("여러 파일 중 하나라도 걸리면 1", r.returncode == 1 and "통과" in r.stdout))
    res.append(("인자 없으면 사용법과 종료 코드 2", run_cli([]).returncode == 2))
    res.append(("없는 프로파일은 종료 코드 2", run_cli(["--profile", "chat", clean]).returncode == 2))
    r = run_cli([str(TMP / "없는파일.md")])
    res.append(("없는 파일은 실패로 센다", r.returncode == 1 and "읽을 수 없다" in r.stderr))
    r = run_cli(["--profile", "internal", dirty])
    res.append(("internal 은 용어집 미적용", r.returncode == 0))
    r = run_cli(["--profile", "internal", write("생성되어진다.")])
    res.append(("internal 도 문장 규칙 적용", r.returncode == 1))
    r = run_cli([write("KO-LINT-SKIP\n앱을 배포합니다.")])
    res.append(("KO-LINT-SKIP 은 건너뜀", r.returncode == 0 and "건너뜀" in r.stdout))
    r = run_cli([write("설명입니다.\n```\n앱을 배포합니다\n```\n")])
    res.append(("코드블록 안은 검사 안 함", r.returncode == 0))
    return res


def check_style():
    res = []
    home = pathlib.Path(tempfile.mkdtemp(prefix="ko-lint-home-"))
    base = {k: v for k, v in os.environ.items() if k != "KO_STYLE_DIR"}
    doc = write("앱을 배포합니다.")

    r = run_cli([doc], env={**base, "HOME": str(home)})
    res.append(("사용자 용어집이 없으면 초기본을 쓴다",
                r.returncode == 1 and os.path.realpath(SEED) in r.stdout))

    user = home / ".claude" / "ko-style"
    user.mkdir(parents=True)
    (user / "glossary-core.tsv").write_text("noun\t앱\t응용 프로그램\t테스트\n", encoding="utf-8")
    r = run_cli([doc], env={**base, "HOME": str(home)})
    res.append(("사용자 용어집이 있으면 그것만 쓴다",
                r.returncode == 1 and "응용 프로그램" in r.stdout and "애플리케이션" not in r.stdout))

    r = run_cli([doc], env={**base, "HOME": str(home), "KO_STYLE_DIR": SEED})
    res.append(("KO_STYLE_DIR 이 가장 앞선다", r.returncode == 1 and "애플리케이션" in r.stdout))

    r = run_cli([doc], env={**base, "HOME": str(home), "KO_STYLE_DIR": str(home / "없음")})
    res.append(("용어집 디렉토리가 없어도 실패하지 않는다", r.returncode == 0))

    broken = home / "broken"
    broken.mkdir()
    (broken / "glossary-core.tsv").write_text("한 칸짜리 줄\n## 주석\n\n", encoding="utf-8")
    r = run_cli([doc], env={**base, "KO_STYLE_DIR": str(broken)})
    res.append(("형식이 깨진 줄은 건너뛴다", r.returncode == 0))
    return res


def check_init():
    res = []
    init = str(HERE / "init-style.py")
    dest = pathlib.Path(tempfile.mkdtemp(prefix="ko-style-")) / "ko-style"
    seed_files = sorted(str(p.relative_to(SEED)) for p in pathlib.Path(SEED).rglob("*") if p.is_file())

    r = subprocess.run([sys.executable, init, str(dest)], capture_output=True, text=True)
    got = sorted(str(p.relative_to(dest)) for p in dest.rglob("*") if p.is_file())
    res.append(("빈 디렉토리에 초기본 전부 복사", r.returncode == 0 and got == seed_files))

    core = dest / "glossary-core.tsv"
    core.write_text(core.read_text(encoding="utf-8") + "noun\t사용자추가\t표준\t테스트\n", encoding="utf-8")
    (dest / "domains" / "api.tsv").unlink()
    r = subprocess.run([sys.executable, init, str(dest)], capture_output=True, text=True)
    res.append(("다시 실행해도 종료 코드 0", r.returncode == 0))
    res.append(("사용자가 고친 파일은 덮어쓰지 않는다", "사용자추가" in core.read_text(encoding="utf-8")))
    res.append(("지워진 파일만 다시 추가", (dest / "domains" / "api.tsv").exists() and "추가한 파일 1개" in r.stdout))
    return res


def main():
    fail = 0

    print("── 잡아야 하는 것 ──")
    for label, text in POSITIVE:
        ok = lint(text) is not None
        print(f"{'PASS' if ok else 'MISS':6} {label}")
        fail += 0 if ok else 1

    print("\n── 잡으면 안 되는 것 ──")
    for label, text in NEGATIVE:
        out = lint(text)
        ok = out is None
        print(f"{'PASS' if ok else 'FALSE+':6} {label}")
        if not ok:
            print(f"       {names_of(out)}")
            fail += 1

    print("\n── 프로파일 (hook 모드) ──")
    for label, payload, want in PROFILE:
        got = run_hook(payload) is not None
        ok = got == want
        print(f"{'PASS' if ok else 'FAIL':6} {label} (걸림={got}, 기대={want})")
        fail += 0 if ok else 1

    print("\n── 종결어미 ──")
    for label, text, want in ENDING:
        out = lint(text)
        got = out is not None and any(
            n.startswith(("종결어미", "의문형", "1인칭")) for n in names_of(out)
        )
        ok = got == want
        print(f"{'PASS' if ok else 'FAIL':6} {label} (걸림={got}, 기대={want})")
        fail += 0 if ok else 1

    for title, results in (("CLI", check_cli()), ("용어집 위치", check_style()), ("init-style", check_init())):
        print(f"\n── {title} ──")
        for label, ok in results:
            print(f"{'PASS' if ok else 'FAIL':6} {label}")
            fail += 0 if ok else 1

    print(f"\n실패 {fail}건")
    return 1 if fail else 0


if __name__ == "__main__":
    sys.exit(main())
