"""
\brief UNIT-101 DriverCommandTestAdapter — PC/SIL 테스트 벡터 -> DriverCommand 변환
       + IF-INT-001 호출만 담당.

아키텍처 요소 대응: ARC-101. 상세설계 근거: SWD-PH1_SW 상세설계서.md §5.8(FN-101),
§9.1(PC/SIL 테스트 벡터 계약). 관련 요구사항: SWR-001, SWR-002.

**외부 계약 경계 유의**: `rawVector`의 키 문자열(`"side"`, `"action"`, `"source"`)은
OEM-IF-004 wire 계약이므로 원문 그대로 유지한다(내부 식별자 camelCase 규칙 미적용 대상).
"""
from src.core.types import DriverCommand
from src.core.facade import EvaluationCycleFacade


class DriverCommandTestAdapter:
    """\brief IF-EXT-001 -> IF-INT-001 변환기 (PC/SIL 테스트 하네스 전용)."""

    def __init__(self, facade: EvaluationCycleFacade) -> None:
        """\brief 생성자 주입으로 EvaluationCycleFacade를 받아 보관한다."""
        self._facade = facade

    def submit(self, rawVector: dict) -> None:
        """
        \\brief PC/SIL 테스트 벡터를 DriverCommand로 변환해 facade에 제출한다.

        \\param rawVector `{"side": str, "action": str, "source": str}` 형태의 dict.
               세 키 모두 선택(누락 허용 — 누락 시 None으로 전달, SWD-PH1 §9.1).
        \\exception 발생하지 않음(형식 오류 필드는 None으로 전달되어 하류
                    CommandValidator가 거절, SWD-PH1 §5.1)
        """
        rawCommand = DriverCommand(
            side=rawVector.get("side"),
            action=rawVector.get("action"),
            source=rawVector.get("source"),
        )
        self._facade.submitDriverCommand(rawCommand)
