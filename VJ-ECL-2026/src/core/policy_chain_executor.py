"""
\brief UNIT-002 PolicyChainExecutor — 정책 체인 실행 순서·예외 격리·최종 출력 커밋
       (단일 writer)만 담당.

아키텍처 요소 대응: ARC-002. 상세설계 근거: SWD-PH1_SW 상세설계서.md §5.6(FN-010/011),
§6.4(의사코드), §7.3(우선순위 실행 규약), §10.4(정책 실행 예외 처리 확정 사항).
관련 요구사항: SWR-004, SWR-020, SWR-PH1 §8(상충 해소 실행).
"""
import logging

from src.core.types import CycleStatus, EvaluationResult, PolicyCategory, PolicyContext, \
    PolicyDecision, VehicleSnapshot
from src.core.command_dispatcher import CommandDispatcher
from src.core.lock_state_store import LockStateStore
from src.core.policy_port import ActuatorPort, DisplayPort, PolicyPort

_logger = logging.getLogger("vjecl.core.policy_chain")


class PolicyChainExecutor:
    """\brief IF-INT-009 구현체 — 등록된 정책을 실행 규약대로 호출하고 결과를 커밋한다."""

    def __init__(
        self,
        store: LockStateStore,
        dispatcher: CommandDispatcher,
        actuatorPort: ActuatorPort,
        displayPort: DisplayPort,
    ) -> None:
        """\brief 생성자 주입으로 협력 컴포넌트를 받아 보관한다. 정책 목록은 비어서 시작."""
        self._store = store
        self._dispatcher = dispatcher
        self._actuatorPort = actuatorPort
        self._displayPort = displayPort
        self._policies: list[PolicyPort] = []

    def registerPolicy(self, policy: PolicyPort) -> None:
        """
        \\brief 정책을 등록 목록에 추가한다(순서는 evaluate()가 재정렬하므로 무의미).

        \\param policy category/asilLevel/priority 속성을 가진 PolicyPort 구현체
        \\exception 발생하지 않음
        """
        self._policies.append(policy)

    def evaluate(self, snapshot: VehicleSnapshot) -> EvaluationResult:
        """
        \\brief 등록된 정책을 실행 규약대로 평가하고 최종 출력을 커밋한다.

        \\param snapshot 이번 평가주기의 VehicleSnapshot
        \\return 정상 종료 시 EvaluationResult(status=COMMITTED, ...), 정책 예외/구성
                 오류 시 EvaluationResult(status=FAILED, ...)
        \\exception 발생하지 않음(정책 예외를 포함한 모든 예외를 흡수, §10.4)

        상세설계 근거: UNIT-002 / FN-010 (SWD-PH1 §5.6, §6.4, §7.3, §10.4).
        """
        try:
            return self._evaluateUnsafe(snapshot)
        except Exception as exc:  # pylint: disable=broad-except
            # 최상위 안전망(defense in depth) — §10.4 "안전망" 절. 정책 예외는 이미
            # 내부에서 흡수되므로, 여기 도달하는 예외는 커밋 단계의 예기치 못한 실패다.
            return self._handleCycleFailure(None, "COMMIT", exc)

    def _evaluateUnsafe(self, snapshot: VehicleSnapshot) -> EvaluationResult:
        """\brief 최상위 안전망으로 감싸지기 전의 실제 평가 로직 (§6.4 의사코드)."""
        context = PolicyContext(snapshot)
        overrideList = self._sortedPolicies(PolicyCategory.OVERRIDE)
        baseList = self._sortedPolicies(PolicyCategory.BASE)

        result, fault = self._scanOverridePolicies(overrideList, context)
        if fault is None and result is None:
            result, fault = self._scanBasePolicies(baseList, context)

        if fault is not None:
            return self._handleCycleFailure(*fault)
        if result is None:
            fault = (None, "NO_POLICY_REGISTERED", RuntimeError("no policy produced a result"))
            return self._handleCycleFailure(*fault)

        return self._commit(result)

    def _sortedPolicies(self, category: PolicyCategory) -> list:
        """\brief category에 속한 정책을 asil_level 내림차순 -> priority 오름차순 정렬."""
        candidates = [policy for policy in self._policies if policy.category == category]
        return sorted(candidates, key=self._sortKey)

    @staticmethod
    def _sortKey(policy: PolicyPort):
        """\brief asil_level 내림차순(ASIL_B 먼저) -> priority 오름차순 정렬 키."""
        return (policy.asilLevel.value != "ASIL_B", policy.priority)

    @staticmethod
    def _scanOverridePolicies(overrideList, context):
        """\brief OVERRIDE 목록을 스캔해 첫 OVERRIDE_FINAL 또는 예외를 찾는다."""
        for policy in overrideList:
            try:
                candidate = policy.evaluate(context)
            except Exception as exc:  # pylint: disable=broad-except
                return None, (policy, "OVERRIDE_SCAN", exc)
            if candidate.decision == PolicyDecision.OVERRIDE_FINAL:
                return candidate, None
        return None, None

    @staticmethod
    def _scanBasePolicies(baseList, context):
        """\brief BASE 목록에서 첫 정책만 평가한다(Phase 1은 BASE가 1개, §6.4 근거)."""
        for policy in baseList:
            try:
                candidate = policy.evaluate(context)
            except Exception as exc:  # pylint: disable=broad-except
                return None, (policy, "BASE_EVAL", exc)
            return candidate, None
        return None, None

    def _commit(self, result) -> EvaluationResult:
        """\brief 확정된 PolicyResult를 store/actuator/display에 반영하고 결과를 만든다."""
        self._store.write(result.lockLeft, result.lockRight)
        self._actuatorPort.apply(result.lockLeft, result.lockRight)
        self._displayPort.show(result.stateLabel, result.reasonCode)
        self._dispatcher.discardCurrentCycleCommand()
        return EvaluationResult(
            CycleStatus.COMMITTED, result.lockLeft, result.lockRight,
            result.stateLabel, result.reasonCode,
        )

    def _handleCycleFailure(self, policy, phase: str, exc: Exception) -> EvaluationResult:
        """
        \\brief 평가주기 실패를 처리한다 — 로그 기록, discard, 직전 값 유지(§10.4).

        \\param policy 실패를 유발한 정책(없으면 None)
        \\param phase "OVERRIDE_SCAN" | "BASE_EVAL" | "NO_POLICY_REGISTERED" | "COMMIT"
        \\param exc 발생한 예외
        \\return EvaluationResult(status=FAILED, lockLeft/lockRight=직전 값, ...)
        """
        policyName = type(policy).__name__ if policy is not None else "(none)"
        _logger.error(
            "평가주기 실패: phase=%s policy=%s error=%r", phase, policyName, exc
        )
        self._dispatcher.discardCurrentCycleCommand()
        current = self._store.readCurrent()
        return EvaluationResult(
            CycleStatus.FAILED, current.left, current.right,
            stateLabel=None, reasonCode=None, errorDetail=repr(exc),
        )
