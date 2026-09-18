"""
\brief UNIT-007 IgnitionOverridePolicy — ignition 강제 RELEASE 판정(OVERRIDE 정책)만 담당.

아키텍처 요소 대응: ARC-007. 상세설계 근거: SWD-PH1_SW 상세설계서.md §5.5(FN-060/061),
§6.3(의사코드), §7.2(정책 의사결정표, 3행), §8.2(상태전이 4케이스). 관련 요구사항: SWR-020.
"""
from src.core.types import (
    AsilLevel,
    DisplayState,
    IgnitionState,
    LockState,
    PolicyCategory,
    PolicyContext,
    PolicyDecision,
    PolicyResult,
    ReasonCode,
)
from src.core.lock_state_store import LockStateStore


def classifyIgnition(raw: object) -> IgnitionState:
    """
    \\brief `ignition_on` 원시값을 IgnitionState로 분류하는 총함수.

    \\param raw 임의 타입의 원시 값
    \\return `raw is True`이면 ON, `raw is False`이면 OFF, 그 외 모든 타입은 INVALID
    \\exception 발생하지 않음

    상세설계 근거: UNIT-007 / FN-061 (SWD-PH1 §5.5, §6.3). SWR-020(b)에 따라 형식
    오류/누락(None, 문자열, 정수 등)은 모두 INVALID로 안전측 분류한다.
    """
    if raw is True:
        return IgnitionState.ON
    if raw is False:
        return IgnitionState.OFF
    return IgnitionState.INVALID


class IgnitionOverridePolicy:
    """\brief IF-INT-008(OVERRIDE) 구현체 — category=OVERRIDE, asilLevel=QM, priority=1."""

    category = PolicyCategory.OVERRIDE
    asilLevel = AsilLevel.QM
    priority = 1

    def __init__(self, store: LockStateStore) -> None:
        """\brief 생성자 주입으로 LockStateStore를 받아 보관한다."""
        self._store = store

    def evaluate(self, context: PolicyContext) -> PolicyResult:
        """
        \\brief ignition_on 판정에 따라 PASS 또는 강제 RELEASE(OVERRIDE_FINAL)를 반환.

        \\param context 정책 평가 컨텍스트(snapshot.ignition_on을 판정 근거로 사용)
        \\return ON이면 PolicyResult(PASS), 그 외(OFF/INVALID)면
                 PolicyResult(OVERRIDE_FINAL, RELEASE, RELEASE, IGNITION_OFF, OFF)
        \\exception 발생하지 않음(총함수)

        상세설계 근거: UNIT-007 / FN-060 (SWD-PH1 §5.5, §6.3, §7.2). `self._store.
        readCurrent()` 호출은 SWA-PH1 §5 의존 계약 이행 목적이며 분기 결정에는 사용하지
        않는다(§6.3 설계 근거 — 강제 출력값은 직전 값과 무관하게 항상 고정된다).
        """
        state = classifyIgnition(context.snapshot.ignitionOn)
        self._store.readCurrent()  # 아키텍처 의존 계약 이행(§6.3) — 반환값은 분기에 미사용
        if state == IgnitionState.ON:
            return PolicyResult(PolicyDecision.PASS)
        return PolicyResult(
            PolicyDecision.OVERRIDE_FINAL,
            LockState.RELEASE,
            LockState.RELEASE,
            ReasonCode.IGNITION_OFF,
            DisplayState.OFF,
        )
