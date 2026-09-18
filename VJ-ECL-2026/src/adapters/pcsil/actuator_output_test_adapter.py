"""
\brief UNIT-103 ActuatorOutputTestAdapter — 논리 lock_left/lock_right를 OEM-IF-005
       값으로 반영(및 시험용 조회)만 담당.

아키텍처 요소 대응: ARC-103. 상세설계 근거: SWD-PH1_SW 상세설계서.md §5.8(FN-103).
관련 요구사항: SWR-004, SWR-020. `getLastApplied()`는 IF-INT-003 원 계약에는 없는
**Test 어댑터 전용 확장**이다(SWD-PH1 §10.2 근거 — 코어는 이 오퍼레이션을 호출하지 않음).
"""
from src.core.types import LockPair, LockState


class ActuatorOutputTestAdapter:
    """\brief IF-INT-003 구현체 — PC/SIL 논리 출력 반영 + 시험용 조회."""

    def __init__(self) -> None:
        """\brief 초기 상태는 "아직 반영된 적 없음"(None)."""
        self._lastApplied: LockPair | None = None

    def apply(self, lockLeft: LockState, lockRight: LockState) -> None:
        """
        \\brief 확정된 lockLeft/lockRight를 내부에 저장(반영)한다.

        \\param lockLeft 확정된 좌측 논리 출력(코어가 이미 검증한 LockState)
        \\param lockRight 확정된 우측 논리 출력(코어가 이미 검증한 LockState)
        \\exception 발생하지 않음
        """
        self._lastApplied = LockPair(lockLeft, lockRight)

    def getLastApplied(self) -> LockPair | None:
        """
        \\brief 마지막으로 apply()된 값을 조회한다(Test 어댑터 전용 확장, SWD-PH1 §10.2).

        \\return 마지막 apply() 인자로 만든 LockPair, 아직 없으면 None
        \\exception 발생하지 않음
        """
        return self._lastApplied
