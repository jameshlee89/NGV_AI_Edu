"""
\brief UNIT-000 공통 자료형(Common Types) — 값 객체·열거형·순수 헬퍼 함수만 정의한다.

아키텍처 요소 대응: 없음(코어 전역 인프라, ARC 미할당 — SWA-PH1 §12 "근거 없는 요소 아닌 이유" 승계).
상세설계 근거: SWD-PH1_SW 상세설계서.md §2.1(UNIT-000), §4(공통 자료형), §6.2(deriveDisplayState).

이 모듈은 로직/부작용이 없는 값 객체와 순수 함수만 담는다(§2.1 응집도 점검 결과와 일치).
Enum 멤버명은 CLAUDE.md 네이밍 규칙(함수/변수명 camelCase) 적용 대상이 아니라 상수 관례
(UPPER_SNAKE_CASE)를 따르되, 값(value)은 OEM 외부 인터페이스 원문 표기를 그대로 사용한다
(오케스트레이터 지시사항 — 외부 계약 리터럴은 원문 유지).
"""
from dataclasses import dataclass
from enum import Enum


class Side(Enum):
    """\brief `Driver_Command.side`의 유효 값 집합 (OEM-IF-004, SWR-PH1 §5)."""

    LEFT = "left"
    RIGHT = "right"
    ALL = "all"


class Action(Enum):
    """\brief `Driver_Command.action`의 유효 값 집합 (OEM-IF-004, SWR-PH1 §5)."""

    LOCK = "lock"
    UNLOCK = "unlock"


class Source(Enum):
    """\brief `Driver_Command.source`의 유효 값 집합 (OEM-IF-004, SWR-PH1 §5)."""

    PHYSICAL_BUTTON = "physical_button"
    AVN = "avn"
    VOICE = "voice"
    MOBILE_APP = "mobile_app"


class LockState(Enum):
    """\brief `lock_left`/`lock_right`의 논리 출력 값 (OEM-IF-005, SWR-PH1 §6)."""

    LOCK = "LOCK"
    RELEASE = "RELEASE"


class DisplayState(Enum):
    """\brief `state`(OEM-IF-006, 가정 §6/§8)의 최소 필요 열거형 집합."""

    LOCKED_LEFT = "LOCKED_LEFT"
    LOCKED_RIGHT = "LOCKED_RIGHT"
    LOCKED_ALL = "LOCKED_ALL"
    RELEASED = "RELEASED"
    OFF = "OFF"


class ReasonCode(Enum):
    """\brief `reason_code`(OEM-IF-006) 최소 집합 + 상세설계 도입 `NONE`(§4 결정 사항)."""

    NONE = "NONE"
    INVALID_COMMAND = "INVALID_COMMAND"
    IGNITION_OFF = "IGNITION_OFF"


class IgnitionState(Enum):
    """\brief `ignition_on` 판정 결과의 내부 전용 표현 (SWR-020(b), 외부 노출 없음)."""

    ON = "ON"
    OFF = "OFF"
    INVALID = "INVALID"


class PolicyDecision(Enum):
    """\brief IF-INT-008 정책 반환 결정 종류 (SWA-PH1 §6.1)."""

    OVERRIDE_FINAL = "OVERRIDE_FINAL"
    PROPOSE = "PROPOSE"
    PASS = "PASS"


class PolicyCategory(Enum):
    """\brief IF-INT-008 정책 카테고리 메타데이터 (SWA-PH1 §6.1)."""

    OVERRIDE = "OVERRIDE"
    BASE = "BASE"


class AsilLevel(Enum):
    """\brief IF-INT-008 정책 ASIL 등급 메타데이터. Phase 1은 QM만 실사용(§4)."""

    QM = "QM"
    ASIL_B = "ASIL_B"


class CycleStatus(Enum):
    """\brief 평가주기 결과 상태 — 상세설계 §4/§10.4 결정에 따른 신규 도입(내부 전용)."""

    COMMITTED = "COMMITTED"
    FAILED = "FAILED"


@dataclass(frozen=True)
class DriverCommand:
    """
    \\brief 검증 전(신뢰 경계 진입 시점) `Driver_Command` 원시 값 객체 (SWD-PH1 §4.2).

    \\param side 검증 전 원시 값(임의 타입 허용, 누락 시 None)
    \\param action 검증 전 원시 값(임의 타입 허용, 누락 시 None)
    \\param source 검증 전 원시 값(임의 타입 허용, 누락 시 None)
    """

    side: object = None
    action: object = None
    source: object = None


@dataclass(frozen=True)
class VehicleSnapshot:
    """
    \\brief 검증 전 `VehicleSnapshot` 원시 값 객체 (SWD-PH1 §4.2).

    \\param timestampS 평가주기 시각(초). 어댑터(UNIT-102)가 항상 float로 정규화한다.
    \\param ignitionOn 검증 전 원시 값(임의 타입 허용, 누락 시 None).
    """

    timestampS: float
    ignitionOn: object = None


@dataclass(frozen=True)
class ValidCommand:
    """\brief 검증을 통과한 강타입 명령 값 객체 (SWD-PH1 §4.3)."""

    side: Side
    action: Action
    source: Source


@dataclass(frozen=True)
class Rejection:
    """\brief 검증 실패를 표현하는 값 객체 (SWD-PH1 §4.3). Phase 1은 항상 INVALID_COMMAND."""

    reasonCode: ReasonCode


@dataclass(frozen=True)
class LockPair:
    """\brief `LockStateStore.readCurrent()` 반환 타입 (SWD-PH1 §4.3)."""

    left: LockState
    right: LockState


@dataclass(frozen=True)
class PolicyContext:
    """\brief 정책 평가 입력 컨텍스트 (IF-INT-008, SWD-PH1 §4.4)."""

    snapshot: VehicleSnapshot


@dataclass(frozen=True)
class PolicyResult:
    """
    \\brief 정책 평가 결과 값 객체 (IF-INT-008, SWD-PH1 §4.4).

    불변조건: decision이 OVERRIDE_FINAL/PROPOSE이면 lockLeft/lockRight/stateLabel이
    모두 None이 아니어야 한다. decision이 PASS이면 나머지 필드는 모두 None이어야 한다.
    """

    decision: PolicyDecision
    lockLeft: LockState = None
    lockRight: LockState = None
    reasonCode: ReasonCode = None
    stateLabel: DisplayState = None


@dataclass(frozen=True)
class EvaluationResult:
    """
    \\brief 평가주기 결과 값 객체 (IF-INT-002/009 반환값, SWD-PH1 §4.5).

    \\param status COMMITTED 또는 FAILED
    \\param lockLeft 이번 주기 확정값(FAILED면 직전 값 그대로)
    \\param lockRight 이번 주기 확정값(FAILED면 직전 값 그대로)
    \\param stateLabel COMMITTED 시 항상 설정, FAILED 시 None
    \\param reasonCode COMMITTED 시 항상 설정, FAILED 시 None
    \\param errorDetail FAILED 시에만 설정하는 진단 전용 문자열(OEM 인터페이스에 노출 안 함)
    """

    status: CycleStatus
    lockLeft: LockState
    lockRight: LockState
    stateLabel: DisplayState = None
    reasonCode: ReasonCode = None
    errorDetail: str = None


def deriveDisplayState(left: LockState, right: LockState) -> DisplayState:
    """
    \\brief (left, right) LockState 조합으로부터 DisplayState를 도출하는 순수 함수.

    \\param left 좌측 논리 출력
    \\param right 우측 논리 출력
    \\return 대응하는 DisplayState (LockState는 2값 Enum이므로 조합 4개로 완전하다)

    상세설계 근거: UNIT-000 / SWD-PH1 §6.2 (`(LOCK,LOCK)->LOCKED_ALL`,
    `(LOCK,RELEASE)->LOCKED_LEFT`, `(RELEASE,LOCK)->LOCKED_RIGHT`,
    `(RELEASE,RELEASE)->RELEASED`).
    """
    if left is LockState.LOCK and right is LockState.LOCK:
        return DisplayState.LOCKED_ALL
    if left is LockState.LOCK and right is LockState.RELEASE:
        return DisplayState.LOCKED_LEFT
    if left is LockState.RELEASE and right is LockState.LOCK:
        return DisplayState.LOCKED_RIGHT
    return DisplayState.RELEASED
