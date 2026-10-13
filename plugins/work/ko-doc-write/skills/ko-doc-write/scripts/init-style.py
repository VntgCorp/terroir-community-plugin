#!/usr/bin/env python3
"""플러그인의 용어집 초기본을 사용자 용어집 디렉토리로 복사한다.

이미 있는 파일은 덮어쓰지 않는다. 사용자가 쌓은 내용은 그대로 두고 플러그인 업데이트로
새로 생긴 파일만 추가한다. 매번 실행해도 된다.

사용: python3 init-style.py [대상 디렉토리]   (기본값 ~/.claude/ko-style)
"""
import os
import shutil
import sys

SEED = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "ko-style")


def main(argv):
    dest = argv[0] if argv else os.path.join(os.path.expanduser("~"), ".claude", "ko-style")
    added = []
    for root, _, files in os.walk(SEED):
        rel = os.path.relpath(root, SEED)
        target_dir = os.path.normpath(os.path.join(dest, rel))
        os.makedirs(target_dir, exist_ok=True)
        for name in sorted(files):
            target = os.path.join(target_dir, name)
            if os.path.exists(target):
                continue
            shutil.copy2(os.path.join(root, name), target)
            added.append(os.path.normpath(os.path.join(rel, name)))
    print(f"용어집: {dest}")
    print(f"추가한 파일 {len(added)}개" + (" — " + ", ".join(added) if added else ""))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
