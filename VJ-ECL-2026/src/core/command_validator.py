"""
\brief UNIT-003 CommandValidator — `Driver_Command` 필드 존재·enum 소속 판정만 담당.

아키텍처 요소 대응: ARC-003. 상세설계 근거: SWD-PH1_SW 상세설계서.md §5.1(FN-020),
§6.1(의사코드). 관련 요구사항: SWR-001.
"""
from src.core.types import Action, DriverCommand, Rejection, ReasonCode, Side, Source, ValidCommand


class CommandValidator:
    """\brief IF-INT-005 구현체 — `validate()`만 제공하는 무상태 검증기 (SWR-001)."""

    def validate(self, raw: object) -> ValidCommand | Rejection:
        """
        \\brief `Driver_Command` 원시값의 필드 존재·enum 소속 여부를 판정한다.

        \\param raw 검증 전 DriverCommand(또는 계약 위반 시 임의 타입)
        \\return 세 필드가 모두 유효하면 ValidCommand, 그 외 모든 경우 Rejection
        \\exception 발생하지 않음(총함수, SWD-PH1 §5.1 사전조건 없음)

        상세설계 근거: UNIT-003 / FN-020 (SWD-PH1 §5.1, §6.1). `raw`가 `DriverCommand`
        인스턴스가 아니어도 방어적으로 `Rejection`을 반환한다(§10.1 방어적 완화).
        """
        if not isinstance(raw, DriverCommand):
            return Rejection(ReasonCode.INVALID_COMMAND)
        try:
            side = Side(raw.side)
            action = Action(raw.action)
            source = Source(raw.source)
        except ValueError:
            return Rejection(ReasonCode.INVALID_COMMAND)
        return ValidCommand(side, action, source)
