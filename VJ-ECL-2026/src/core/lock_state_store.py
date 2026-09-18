"""
\brief UNIT-005 LockStateStore — `lock_left`/`lock_right` 직전 평가주기 값의 read/write.

아키텍처 요소 대응: ARC-005. 상세설계 근거: SWD-PH1_SW 상세설계서.md §5.3(FN-040/041).
관련 요구사항: SWR-004, SWR-020. 단일 writer는 UNIT-002만(관례로 강제, §10.3).
"""
from src.core.types import LockPair, LockState


class LockStateStore:
    """\brief IF-INT-007 구현체 — 직전 평가주기의 lockLeft/lockRight를 보관한다."""

    def __init__(self) -> None:
        """\brief 초기값 (RELEASE, RELEASE)로 저장소를 생성한다 (SWR-PH1 §8 가정3)."""
        self._current = LockPair(LockState.RELEASE, LockState.RELEASE)

    def readCurrent(self) -> LockPair:
        """
        \\brief 직전 write()의 인자를 그대로 반환한다(초기값은 RELEASE/RELEASE).

        \\return 현재 LockPair
        \\exception 발생하지 않음
        """
        return self._current

    def write(self, left: LockState, right: LockState) -> None:
        """
        \\brief 현재 LockPair를 (left, right)로 갱신한다.

        \\param left 새 좌측 값. LockState 인스턴스여야 한다(내부 신뢰 경계).
        \\param right 새 우측 값. LockState 인스턴스여야 한다(내부 신뢰 경계).
        \\exception TypeError left/right가 LockState 인스턴스가 아니면 즉시 발생
                    (프로그래밍 오류, 방어적 assert — SWD-PH1 §10.3).
        """
        if not isinstance(left, LockState) or not isinstance(right, LockState):
            raise TypeError("left/right는 LockState 인스턴스여야 합니다 (SWD-PH1 §10.3)")
        self._current = LockPair(left, right)
