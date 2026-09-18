"""
\brief UNIT-104 DisplayOutputTestAdapter — state/reason_code를 OEM-IF-006(부분)
       값으로 반영(및 시험용 조회)만 담당.

아키텍처 요소 대응: ARC-104. 상세설계 근거: SWD-PH1_SW 상세설계서.md §5.8(FN-104).
관련 요구사항: SWR-001(b), SWR-020. `getLastShown()`은 IF-INT-004 원 계약에는 없는
**Test 어댑터 전용 확장**이다(SWD-PH1 §10.2 근거 — 코어는 이 오퍼레이션을 호출하지 않음).
"""
from src.core.types import DisplayState, ReasonCode


class DisplayOutputTestAdapter:
    """\brief IF-INT-004 구현체 — PC/SIL 표시 출력 반영 + 시험용 조회."""

    def __init__(self) -> None:
        """\brief 초기 상태는 "아직 반영된 적 없음"(None)."""
        self._lastShown: tuple[DisplayState, ReasonCode] | None = None

    def show(self, state: DisplayState, reasonCode: ReasonCode) -> None:
        """
        \\brief 확정된 state/reasonCode를 내부에 저장(반영)한다.

        \\param state 확정된 표시 상태(코어가 이미 검증한 DisplayState)
        \\param reasonCode 확정된 사유 코드(코어가 이미 검증한 ReasonCode)
        \\exception 발생하지 않음
        """
        self._lastShown = (state, reasonCode)

    def getLastShown(self) -> tuple[DisplayState, ReasonCode] | None:
        """
        \\brief 마지막으로 show()된 값을 조회한다(Test 어댑터 전용 확장, SWD-PH1 §10.2).

        \\return 마지막 show() 인자로 만든 (state, reasonCode) 튜플, 아직 없으면 None
        \\exception 발생하지 않음
        """
        return self._lastShown
