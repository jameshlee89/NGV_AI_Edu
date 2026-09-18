"""
\brief UNIT-008 정책/출력 포트 정의(IF-INT-003/004/008의 코드 수준 표현).

아키텍처 요소 대응: 없음(IF-INT-008 포트 정의 인프라, SWA-PH1 §12 근거 승계).
상세설계 근거: SWD-PH1_SW 상세설계서.md §2.1(UNIT-008), §4.6.

`typing.Protocol`(구조적 서브타이핑)로 DIP/LSP 근거(SWA-PH1 §5)를 코드 수준에서 구현한다.
`@runtime_checkable`을 추가해 `isinstance()` 기반 구조 검증이 가능하도록 했다 — 이는
Protocol의 메서드/속성 시그니처 계약을 바꾸지 않는 부가 메타데이터이므로 SWA/SWD 문서의
계약을 변경하지 않는다.
"""
from typing import Protocol, runtime_checkable

from src.core.types import (
    AsilLevel,
    DisplayState,
    LockState,
    PolicyCategory,
    PolicyContext,
    PolicyResult,
    ReasonCode,
)


@runtime_checkable
class PolicyPort(Protocol):
    """\brief IF-INT-008 정책 포트 — ARC-006/007(Phase1), ARC-301~403(Phase2/3 예정)이 구현."""

    category: PolicyCategory
    asilLevel: AsilLevel
    priority: int

    def evaluate(self, context: PolicyContext) -> PolicyResult:
        """\brief 정책 평가 오퍼레이션. 총함수(예외 없이 PolicyResult 반환)여야 한다."""


@runtime_checkable
class ActuatorPort(Protocol):
    """\brief IF-INT-003 액추에이터 출력 포트 — ARC-103(Phase1)이 구현."""

    def apply(self, lockLeft: LockState, lockRight: LockState) -> None:
        """\brief 확정된 lockLeft/lockRight를 액추에이터 모델에 반영한다."""


@runtime_checkable
class DisplayPort(Protocol):
    """\brief IF-INT-004 표시 출력 포트 — ARC-104(Phase1)가 구현."""

    def show(self, state: DisplayState, reasonCode: ReasonCode) -> None:
        """\brief 확정된 state/reasonCode를 표시 인터페이스에 반영한다."""
