"""
\brief UNIT-105 PcSilHarnessEntryPoint — Composition Root, ARC-101~104/001/002/006/007
       조립만 담당(로직 없음).

아키텍처 요소 대응: ARC-105. 상세설계 근거: SWD-PH1_SW 상세설계서.md §5.9(FN-105).
관련 요구사항: 없음(조립 인프라, SWA-PH1 §12 근거 승계).
"""
from dataclasses import dataclass

from src.core.command_dispatcher import CommandDispatcher
from src.core.command_validator import CommandValidator
from src.core.facade import EvaluationCycleFacade
from src.core.lock_state_store import LockStateStore
from src.core.policies.driver_command_policy import DriverCommandPolicy
from src.core.policies.ignition_override_policy import IgnitionOverridePolicy
from src.core.policy_chain_executor import PolicyChainExecutor
from src.adapters.pcsil.actuator_output_test_adapter import ActuatorOutputTestAdapter
from src.adapters.pcsil.display_output_test_adapter import DisplayOutputTestAdapter
from src.adapters.pcsil.driver_command_test_adapter import DriverCommandTestAdapter
from src.adapters.pcsil.vehicle_snapshot_test_adapter import VehicleSnapshotTestAdapter


@dataclass(frozen=True)
class SystemHandle:
    """\brief PC/SIL 시험 코드가 참조할 4개 어댑터만 캡슐화한 조립 결과 (SWD-PH1 §5.9)."""

    driverAdapter: DriverCommandTestAdapter
    vehicleAdapter: VehicleSnapshotTestAdapter
    actuatorAdapter: ActuatorOutputTestAdapter
    displayAdapter: DisplayOutputTestAdapter


def buildSystem() -> SystemHandle:
    """
    \\brief 모든 UNIT을 생성자 주입으로 조립해 SystemHandle을 반환한다.

    \\return §3.1 의존 그래프대로 완전히 배선된 SystemHandle(None 의존 없음)
    \\exception 발생하지 않음(고정된 배선, 외부 입력 없음)

    상세설계 근거: UNIT-105 / FN-105 (SWD-PH1 §5.9). 호출할 때마다 새 인스턴스를
    생성한다(전역 싱글턴 아님) — Phase 4 Web 어댑터도 동일 코어 조립 방식을
    재사용할 수 있도록 순수 팩토리 함수로 유지한다(SWA-PH1 §10 재사용성).
    """
    store = LockStateStore()
    dispatcher = CommandDispatcher(CommandValidator())
    actuatorAdapter = ActuatorOutputTestAdapter()
    displayAdapter = DisplayOutputTestAdapter()

    executor = PolicyChainExecutor(store, dispatcher, actuatorAdapter, displayAdapter)
    executor.registerPolicy(IgnitionOverridePolicy(store))
    executor.registerPolicy(DriverCommandPolicy(dispatcher, store))

    facade = EvaluationCycleFacade(dispatcher, executor)
    driverAdapter = DriverCommandTestAdapter(facade)
    vehicleAdapter = VehicleSnapshotTestAdapter(facade)

    return SystemHandle(driverAdapter, vehicleAdapter, actuatorAdapter, displayAdapter)
