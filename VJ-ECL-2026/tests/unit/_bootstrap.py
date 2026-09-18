"""
\brief 테스트 전용 경로 부트스트랩 — VJ-ECL-2026 프로젝트 루트를 sys.path에 추가한다.

`python -m coverage run --branch -m unittest discover -s VJ-ECL-2026/tests/unit`처럼
저장소 루트에서 실행될 때, unittest discover가 top-level 디렉터리로 `tests/unit`만
sys.path에 넣기 때문에 `src...` 패키지를 바로 import할 수 없다. 이 모듈은 각 테스트
파일 맨 위에서 `import _bootstrap`으로 불러와 프로젝트 루트(`VJ-ECL-2026`)를
sys.path에 추가한다(테스트 전용 유틸리티 — 프로덕션 클래스에는 두지 않는다,
tdd 스킬 references/writing-good-tests.md "프로덕션 클래스에는 프로덕션 메서드만" 원칙).
"""
import os
import sys

_PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if _PROJECT_ROOT not in sys.path:
    sys.path.insert(0, _PROJECT_ROOT)
