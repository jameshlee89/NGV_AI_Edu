"""
\brief UNIT-002(PolicyChainExecutor) 단위 테스트 — FN-010/011, SWR-004/020, SWR-PH1 §8,
       SWD-PH1 §5.6/§6.4/§7.3/§10.4.
"""
import unittest

import _bootstrap  # noqa: F401  pylint: disable=unused-import

from src.core.types import (
    Action,
    AsilLevel,
    CycleStatus,
    DisplayState,
    DriverCommand,
    LockState,
    PolicyCategory,
    PolicyContext,
    PolicyDecision,
    PolicyResult,
    ReasonCode,
    VehicleSnapshot,
)
from src.core.command_dispatcher import CommandDispatcher
from src.core.command_validator import CommandValidator
from src.core.lock_state_store import LockStateStore
from src.core.policies.driver_command_policy import DriverCommandPolicy
from src.core.policies.ignition_override_policy import IgnitionOverridePolicy
from src.core.policy_chain_executor import PolicyChainExecutor
from src.adapters.pcsil.actuator_output_test_adapter import ActuatorOutputTestAdapter
from src.adapters.pcsil.display_output_test_adapter import DisplayOutputTestAdapter


class _StubPolicy:
    """테스트 전용 스텁 — 결과/예외/호출기록을 주입할 수 있는 PolicyPort 구현체."""

    def __init__(self, name, category, asilLevel, priority, result=None, raises=None, callLog=None):
        self.name = name
        self.category = category
        self.asilLevel = asilLevel
        self.priority = priority
        self._result = result
        self._raises = raises
        self._callLog = callLog if callLog is not None else []

    def evaluate(self, context: PolicyContext) -> PolicyResult:
        self._callLog.append(self.name)
        if self._raises is not None:
            raise self._raises
        return self._result


class _RaisingActuatorPort:
    """테스트 전용 스텁 — apply() 호출 시 예외를 던져 최상위 안전망(§10.4)을 유도."""

    def apply(self, lockLeft, lockRight):
        raise RuntimeError("시뮬레이션된 액추에이터 오류")


def _buildRealExecutor():
    """실제 UNIT-004/005/103/104로 구성된 PolicyChainExecutor와 부속 컴포넌트를 반환."""
    store = LockStateStore()
    dispatcher = CommandDispatcher(CommandValidator())
    actuator = ActuatorOutputTestAdapter()
    display = DisplayOutputTestAdapter()
    executor = PolicyChainExecutor(store, dispatcher, actuator, display)
    return executor, store, dispatcher, actuator, display


class TestPolicyChainExecutorNominalAndOverride(unittest.TestCase):
    """정상/override 경로에서 실제 정책·어댑터를 사용해 §6.4/§7.3 규약을 검증한다."""

    def testCommitsBaseResultWhenAllOverridesPass(self):
        """
        \\brief ignition ON + 유효 명령이면 BASE 결과가 store/actuator/display에
               반영되고 dispatcher가 discard되며 EvaluationResult(COMMITTED, ...)를
               반환하는지 검증한다. (커밋 순서/호출 중 하나라도 누락되면 이 테스트는
               실패해야 한다)
        \\technique 실제 컴포넌트 기반 (통합형 단위 테스트, SWD-PH1 §6.4 정상 경로)
        \\testtype 긍정 (Positive)
        \\see UNIT-002 / FN-010, SWR-004/020, §6.4
        """
        executor, store, dispatcher, actuator, display = _buildRealExecutor()
        executor.registerPolicy(IgnitionOverridePolicy(store))
        executor.registerPolicy(DriverCommandPolicy(dispatcher, store))
        dispatcher.dispatch(DriverCommand(side="left", action="lock", source="avn"))

        result = executor.evaluate(VehicleSnapshot(timestampS=0.0, ignitionOn=True))

        self.assertEqual(result.status, CycleStatus.COMMITTED)
        self.assertEqual(result.lockLeft, LockState.LOCK)
        self.assertEqual(result.lockRight, LockState.RELEASE)
        self.assertEqual(result.stateLabel, DisplayState.LOCKED_LEFT)
        self.assertEqual(result.reasonCode, ReasonCode.NONE)
        self.assertEqual(store.readCurrent().left, LockState.LOCK)
        self.assertEqual(actuator.getLastApplied().left, LockState.LOCK)
        self.assertEqual(display.getLastShown()[0], DisplayState.LOCKED_LEFT)
        self.assertIsNone(dispatcher.getCurrentCycleCommand())

    def testSkipsBasePolicyWhenOverrideFinal(self):
        """
        \\brief ignition OFF(OVERRIDE_FINAL)이면 BASE 정책(DriverCommandPolicy)의
               evaluate가 아예 호출되지 않고 override 결과만 커밋되는지 검증한다
               (SWR-PH1 §8 우선순위 해소 실증). (BASE가 스킵되지 않고 호출되면 이
               테스트는 실패해야 한다)
        \\technique 실제 컴포넌트 기반 (호출 스파이, SWD-PH1 §7.3)
        \\testtype 긍정 (Positive)
        \\see UNIT-002 / FN-010, SWR-020, §7.3
        """
        executor, store, dispatcher, actuator, display = _buildRealExecutor()
        store.write(LockState.LOCK, LockState.LOCK)
        callLog = []
        basePolicy = _StubPolicy(
            "base", PolicyCategory.BASE, AsilLevel.QM, 1,
            result=PolicyResult(PolicyDecision.PROPOSE, LockState.LOCK, LockState.LOCK,
                                 ReasonCode.NONE, DisplayState.LOCKED_ALL),
            callLog=callLog,
        )
        executor.registerPolicy(IgnitionOverridePolicy(store))
        executor.registerPolicy(basePolicy)

        result = executor.evaluate(VehicleSnapshot(timestampS=0.0, ignitionOn=False))

        self.assertEqual(result.status, CycleStatus.COMMITTED)
        self.assertEqual(result.lockLeft, LockState.RELEASE)
        self.assertEqual(result.lockRight, LockState.RELEASE)
        self.assertEqual(callLog, [])
        self.assertEqual(actuator.getLastApplied(), store.readCurrent())
        self.assertEqual(display.getLastShown(), (DisplayState.OFF, ReasonCode.IGNITION_OFF))


class TestPolicyChainExecutorOrdering(unittest.TestCase):
    """§7.3 실행 규약(ASIL 내림차순 -> priority 오름차순, FINAL 발견 시 스킵)을 검증한다."""

    def testEvaluatesOverridePoliciesInAsilThenPriorityOrder(self):
        """
        \\brief 등록 순서와 무관하게 OVERRIDE 정책이 asil_level 내림차순(ASIL_B 먼저)
               -> priority 오름차순으로 평가되는지 검증한다. (정렬 규칙이 깨지면 이
               테스트는 실패해야 한다)
        \\technique 실제 컴포넌트 기반 (호출 순서 스파이, SWA-PH1 §6.1 실행 규약)
        \\testtype 긍정 (Positive)
        \\see UNIT-002 / FN-010, §6.4, §7.3
        """
        executor, store, _, _, _ = _buildRealExecutor()
        callLog = []
        passResult = PolicyResult(PolicyDecision.PASS)
        qmPolicy = _StubPolicy("qm", PolicyCategory.OVERRIDE, AsilLevel.QM, 1,
                                result=passResult, callLog=callLog)
        asilLowPriority = _StubPolicy("asilB-p2", PolicyCategory.OVERRIDE, AsilLevel.ASIL_B, 2,
                                       result=passResult, callLog=callLog)
        asilHighPriority = _StubPolicy("asilB-p1", PolicyCategory.OVERRIDE, AsilLevel.ASIL_B, 1,
                                        result=passResult, callLog=callLog)
        # 등록 순서를 일부러 뒤섞는다 — 정렬은 실행부(FN-010)의 책임이어야 한다.
        executor.registerPolicy(qmPolicy)
        executor.registerPolicy(asilLowPriority)
        executor.registerPolicy(asilHighPriority)
        executor.registerPolicy(
            _StubPolicy("base", PolicyCategory.BASE, AsilLevel.QM, 1,
                        result=PolicyResult(PolicyDecision.PROPOSE, LockState.RELEASE,
                                             LockState.RELEASE, ReasonCode.NONE,
                                             DisplayState.RELEASED))
        )

        executor.evaluate(VehicleSnapshot(timestampS=0.0, ignitionOn=True))

        self.assertEqual(callLog, ["asilB-p1", "asilB-p2", "qm"])
        del store  # 이 테스트는 순서만 검증(값 검증은 다른 테스트가 담당)

    def testStopsScanningRemainingPoliciesOnceOverrideFinalFound(self):
        """
        \\brief OVERRIDE_FINAL을 반환한 정책 이후의 모든 정책(다른 OVERRIDE 포함,
               BASE 포함)이 호출되지 않는지 검증한다. (스킵 로직이 깨지면 이 테스트는
               실패해야 한다)
        \\technique 실제 컴포넌트 기반 (호출 순서 스파이, SWA-PH1 §6.1 "이후 모든 정책
               스킵")
        \\testtype 긍정 (Positive)
        \\see UNIT-002 / FN-010, §6.4, §7.3
        """
        executor, _, _, _, _ = _buildRealExecutor()
        callLog = []
        finalResult = PolicyResult(PolicyDecision.OVERRIDE_FINAL, LockState.RELEASE,
                                    LockState.RELEASE, ReasonCode.IGNITION_OFF, DisplayState.OFF)
        firstOverride = _StubPolicy("first", PolicyCategory.OVERRIDE, AsilLevel.ASIL_B, 1,
                                     result=finalResult, callLog=callLog)
        secondOverride = _StubPolicy("second", PolicyCategory.OVERRIDE, AsilLevel.ASIL_B, 2,
                                      result=PolicyResult(PolicyDecision.PASS), callLog=callLog)
        basePolicy = _StubPolicy("base", PolicyCategory.BASE, AsilLevel.QM, 1,
                                  result=PolicyResult(PolicyDecision.PROPOSE, LockState.LOCK,
                                                       LockState.LOCK, ReasonCode.NONE,
                                                       DisplayState.LOCKED_ALL),
                                  callLog=callLog)
        executor.registerPolicy(secondOverride)
        executor.registerPolicy(basePolicy)
        executor.registerPolicy(firstOverride)

        result = executor.evaluate(VehicleSnapshot(timestampS=0.0, ignitionOn=False))

        self.assertEqual(callLog, ["first"])
        self.assertEqual(result.lockLeft, LockState.RELEASE)


class TestPolicyChainExecutorFailureHandling(unittest.TestCase):
    """SWD-PH1 §10.4 정책 실행 예외 처리(all-or-nothing, discard는 항상 호출)를 검증한다."""

    def testFailsCycleAndKeepsPreviousOutputsWhenOverridePolicyRaises(self):
        """
        \\brief OVERRIDE_SCAN 중 정책이 예외를 던지면 EvaluationResult(status=FAILED,
               ...)를 반환하고 store/actuator/display는 호출되지 않아 직전 값이
               유지되며, dispatcher는 discard되는지 검증한다. (예외를 흡수하지 못하고
               전파되거나 부분 커밋되면 이 테스트는 실패해야 한다)
        \\technique 오류추정 (정책 계약 위반 — 예외 발생), SWD-PH1 §10.4
        \\testtype 부정 (Negative)
        \\see UNIT-002 / FN-010, §6.4, §10.4
        """
        executor, store, dispatcher, actuator, display = _buildRealExecutor()
        store.write(LockState.LOCK, LockState.RELEASE)
        dispatcher.dispatch(DriverCommand(side="all", action="unlock", source="avn"))
        faultyOverride = _StubPolicy("faulty", PolicyCategory.OVERRIDE, AsilLevel.ASIL_B, 1,
                                      raises=RuntimeError("정책 계약 위반"))
        executor.registerPolicy(faultyOverride)
        executor.registerPolicy(DriverCommandPolicy(dispatcher, store))

        with self.assertLogs("vjecl.core.policy_chain", level="ERROR"):
            result = executor.evaluate(VehicleSnapshot(timestampS=5.0, ignitionOn=True))

        self.assertEqual(result.status, CycleStatus.FAILED)
        self.assertIsNone(result.stateLabel)
        self.assertIsNone(result.reasonCode)
        self.assertIsNotNone(result.errorDetail)
        self.assertEqual(result.lockLeft, LockState.LOCK)
        self.assertEqual(result.lockRight, LockState.RELEASE)
        self.assertEqual(store.readCurrent().left, LockState.LOCK)
        self.assertIsNone(actuator.getLastApplied())
        self.assertIsNone(display.getLastShown())
        self.assertIsNone(dispatcher.getCurrentCycleCommand())

    def testFailsCycleWhenBasePolicyRaises(self):
        """
        \\brief BASE_EVAL 중 정책이 예외를 던지면 EvaluationResult(status=FAILED, ...)를
               반환하고 store/actuator/display는 호출되지 않는지 검증한다. (BASE_EVAL
               예외 경로가 OVERRIDE_SCAN 경로와 다르게 처리되면 이 테스트는 실패해야
               한다)
        \\technique 오류추정 (정책 계약 위반 — 예외 발생), SWD-PH1 §10.4
        \\testtype 부정 (Negative)
        \\see UNIT-002 / FN-010, §6.4, §10.4
        """
        executor, store, dispatcher, actuator, display = _buildRealExecutor()
        store.write(LockState.RELEASE, LockState.LOCK)
        faultyBase = _StubPolicy("faultyBase", PolicyCategory.BASE, AsilLevel.QM, 1,
                                  raises=ValueError("BASE 정책 계약 위반"))
        executor.registerPolicy(IgnitionOverridePolicy(store))
        executor.registerPolicy(faultyBase)

        with self.assertLogs("vjecl.core.policy_chain", level="ERROR"):
            result = executor.evaluate(VehicleSnapshot(timestampS=6.0, ignitionOn=True))

        self.assertEqual(result.status, CycleStatus.FAILED)
        self.assertEqual(result.lockLeft, LockState.RELEASE)
        self.assertEqual(result.lockRight, LockState.LOCK)
        self.assertIsNone(actuator.getLastApplied())
        self.assertIsNone(display.getLastShown())

    def testFailsCycleWhenNoPolicyIsRegistered(self):
        """
        \\brief 정책이 하나도 등록되지 않은 구성 오류 상태에서 evaluate()가
               EvaluationResult(status=FAILED, ...)를 방어적으로 반환하는지 검증한다
               (§6.4 "등록된 정책이 0개" 방어 분기). (이 방어 분기가 삭제되면 예외가
               전파되거나 result가 None으로 사용되어 이 테스트는 실패해야 한다)
        \\technique 경계값분석 (등록 정책 0개 — 구성 오류 경계)
        \\testtype 부정 (Negative)
        \\see UNIT-002 / FN-010, §6.4
        """
        executor, _, dispatcher, _, _ = _buildRealExecutor()
        dispatcher.dispatch(DriverCommand(side="left", action="lock", source="avn"))

        with self.assertLogs("vjecl.core.policy_chain", level="ERROR"):
            result = executor.evaluate(VehicleSnapshot(timestampS=7.0, ignitionOn=True))

        self.assertEqual(result.status, CycleStatus.FAILED)
        self.assertIsNone(dispatcher.getCurrentCycleCommand())

    def testFailsCycleWhenCommitStepRaisesUnexpectedly(self):
        """
        \\brief 정책은 정상 완료했지만 커밋 단계(ActuatorPort.apply)에서 예기치 못한
               예외가 발생하면, 최상위 안전망이 이를 흡수해 FAILED로 반환하는지
               검증한다(방어 심층화, SWD-PH1 §10.4 "안전망"). (최상위 try/except가
               없으면 예외가 그대로 전파되어 이 테스트는 실패해야 한다)
        \\technique 오류추정 (설계상 발생하지 않아야 할 하위 호출 실패 — 방어 심층화)
        \\testtype 부정 (Negative)
        \\see UNIT-002 / FN-010, SWD-PH1 §10.4 "안전망"
        """
        store = LockStateStore()
        dispatcher = CommandDispatcher(CommandValidator())
        executor = PolicyChainExecutor(store, dispatcher, _RaisingActuatorPort(),
                                        DisplayOutputTestAdapter())
        executor.registerPolicy(IgnitionOverridePolicy(store))
        executor.registerPolicy(DriverCommandPolicy(dispatcher, store))

        with self.assertLogs("vjecl.core.policy_chain", level="ERROR"):
            result = executor.evaluate(VehicleSnapshot(timestampS=8.0, ignitionOn=True))

        self.assertEqual(result.status, CycleStatus.FAILED)
        self.assertIsNone(dispatcher.getCurrentCycleCommand())


if __name__ == "__main__":
    unittest.main()
