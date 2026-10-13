#!/usr/bin/env python3
"""마크다운 문서의 정보 구조를 점검한다. 토스 테크니컬 라이팅 가이드 「정보 구조 만들기」 기준.

판정이 아니라 목록이다. 나온 항목을 보고 사람이 고칠지 정한다.

사용: python3 structure-check.py <문서.md> [...]
"""
import re
import sys

# 독자가 풀어 쓰지 않아도 아는 약어. 이것 말고는 첫 등장 때 괄호로 풀어 썼는지 본다.
KNOWN_ABBR = {
    "API", "URL", "URI", "HTTP", "HTTPS", "JSON", "YAML", "HTML", "CSS", "SQL", "CLI", "UI",
    "ID", "IP", "DNS", "TLS", "SSL", "SSH", "OS", "CPU", "GPU", "PR", "CI", "CD", "GCP",
    "AWS", "GKE", "IAM", "SDK", "OK", "MB", "GB", "KB", "TB", "PDF", "PNG", "SVG", "MCP",
    "AI", "LLM", "FAQ", "README", "TODO", "UTC", "KST", "UUID", "JWT", "OIDC", "OAuth",
    "REST", "RBAC", "PVC", "PV", "VM", "LB", "DB", "ADR", "SHA", "QA",
    # 약어가 아니라 이름인 것 — 환경 이름 · git 참조
    "DEV", "PROD", "LAB", "STG", "STAGING", "HEAD",
}
# 대문자로 쓰지만 약어가 아닌 것 — HTTP 메서드 · 설정 값
NOT_ABBR = {"GET", "POST", "PUT", "PATCH", "DELETE", "HEAD", "ON", "OFF", "DENY", "ALLOW", "TRUE", "FALSE", "NULL", "NONE", "ALL", "AND", "OR", "NOT"}
HEADING = re.compile(r"^(#{1,6})\s+(.+?)\s*#*\s*$")


def strip_code(text):
    return re.sub(r"```.*?```", lambda m: "\n" * m.group(0).count("\n"), text, flags=re.S)


def plain(title):
    title = re.sub(r"`([^`]*)`", r"\1", title)
    title = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", title)
    return re.sub(r"[*_]", "", title).strip()


def check(path):
    text = strip_code(open(path, encoding="utf-8").read())
    text = re.sub(r"^---\n.*?\n---\n", "", text, flags=re.S)
    lines = text.splitlines()
    heads = []
    for no, line in enumerate(lines, 1):
        m = HEADING.match(line)
        if m:
            heads.append((no, len(m.group(1)), plain(m.group(2))))

    out = []

    # 한 페이지에서 하나만 다루기
    h1 = [h for h in heads if h[1] == 1]
    if len(h1) > 1:
        out.append(f"H1 이 {len(h1)}개입니다 — 한 페이지에 주제가 둘 이상인지 봅니다")
    deep = [h for h in heads if h[1] >= 4]
    for no, lv, t in deep:
        out.append(f"{no}행 H{lv} 「{t}」 — 제목이 4단계까지 내려갔습니다. 하위 개념을 별도 문서로 나눌지 봅니다")

    # 개요 빠트리지 않기 — 첫 제목 바로 아래에 본문 단락이 있는가
    if heads:
        first = heads[0][0]
        nxt = next((h[0] for h in heads[1:]), len(lines) + 1)
        body = [l for l in lines[first:nxt - 1] if l.strip() and not l.lstrip().startswith(("|", ">", "<"))]
        if not body:
            out.append(f"{first}행 첫 제목 아래 개요 단락이 없습니다 — 이 문서를 읽으면 무엇을 할 수 있는지 씁니다")

    # 효과적인 제목 쓰기
    for no, lv, t in heads:
        # 한글이 없는 제목은 파일 경로·식별자다. 길이를 줄일 수 없으니 세지 않는다
        if len(t) > 30 and re.search(r"[가-힣]", t):
            out.append(f"{no}행 제목 {len(t)}자 「{t}」 — 30자 이내로 줄입니다")
        if t.endswith(("?", "!")):
            out.append(f"{no}행 제목 「{t}」 — 물음표·느낌표 대신 평서문으로 씁니다")

    # 같은 수준 제목의 형태 — '~하기' 와 명사구가 섞였는가
    by_level = {}
    for no, lv, t in heads:
        if lv >= 2:
            by_level.setdefault(lv, []).append((no, t))
    for lv, items in by_level.items():
        if len(items) < 3:
            continue
        hagi = [i for i in items if re.search(r"하기$|기$", i[1])]
        if 0 < len(hagi) < len(items):
            rest = [t for _, t in items if (_, t) not in hagi]
            out.append(
                f"H{lv} {len(items)}개 중 {len(hagi)}개만 「~하기」 형태입니다 — 한 형태로 맞출지 봅니다 "
                f"(나머지: {', '.join(rest[:5])})"
            )

    # 약어는 먼저 풀어쓴 뒤 사용하기
    body = re.sub(r"`[^`\n]*`", " ", text)
    body = re.sub(r"\]\([^)]*\)", "]", body)
    seen, missing = set(), []
    for m in re.finditer(r"(?<![A-Za-z0-9_.-])([A-Z][A-Z0-9]{1,4}s?)(?![A-Za-z0-9_-])", body):
        abbr = m.group(1)[:-1] if m.group(1).endswith("s") else m.group(1)
        # 숫자가 섞이면 약어가 아니라 코드다 (E001 · S3 · H4). 여섯 글자 이상은 enum 값·상수명이다
        if abbr in seen or abbr in KNOWN_ABBR or abbr in NOT_ABBR or len(abbr) < 2 or re.search(r"\d", abbr):
            continue
        seen.add(abbr)
        after = body[m.end():m.end() + 2]
        before = body[max(0, m.start() - 60):m.start()]
        if after.startswith("(") or re.search(r"\([^)]*$", before):
            continue
        missing.append(f"{abbr}({body.count(chr(10), 0, m.start()) + 1}행)")
    if missing:
        out.append(
            f"처음 나온 자리에서 풀어 쓰지 않은 약어 {len(missing)}개 — {', '.join(missing)}. "
            "독자가 모를 약어만 골라 괄호로 풀어 씁니다"
        )

    return out


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        return 2
    total = 0
    for path in sys.argv[1:]:
        items = check(path)
        total += len(items)
        print(f"## {path} — {len(items)}건")
        for i in items:
            print(f"- {i}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
