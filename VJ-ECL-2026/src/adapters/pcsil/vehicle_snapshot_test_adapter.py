"""
\brief UNIT-102 VehicleSnapshotTestAdapter — PC/SIL 테스트 벡터 -> VehicleSnapshot
       변환 + IF-INT-002 호출만 담당.

아키텍처 요소 대응: ARC-102. 상세설계 근거: SWD-PH1_SW 상세설계서.md §5.8(FN-102),
§9.1(PC/SIL 테스트 벡터 계약), §10.2(timestamp_s 방어적 완화). 관련 요구사항: SWR-020.

**외부 계약 경계 유의**: `rawVector`의 키 문자열(`"timestamp_s"`, `"ignition_on"`)은
OEM-IF-009 wire 계약이므로 원문 그대로 유지한다.
"""
import logging

from src.core.types import EvaluationResult, VehicleSnapshot
from src.core.facade import EvaluationCycleFacade

_logger = logging.getLogger("vjecl.adapters.pcsil.vehicle_snapshot")


def _parseFloat(raw: object, default: float) -> float:
    """
    \\brief `raw`를 float로 변환하며 실패 시 `default`로 대체하고 경고를 남긴다.

    \\param raw 변환 대상(임의 타입, None 허용)
    \\param default 변환 실패/None일 때 사용할 기본값
    \\return 변환된 float 또는 default
    \\exception 발생하지 않음(SWD-PH1 §10.2 방어적 완화)
    """
    if raw is None:
        _logger.warning("timestamp_s가 누락됨 — 기본값 %s 사용", default)
        return default
    try:
        return float(raw)
    except (TypeError, ValueError):
        _logger.warning("timestamp_s 형식 오류(%r) — 기본값 %s 사용", raw, default)
        return default


class VehicleSnapshotTestAdapter:
    """\brief IF-EXT-002 -> IF-INT-002 변환기 (PC/SIL 테스트 하네스 전용)."""

    def __init__(self, facade: EvaluationCycleFacade) -> None:
        """\brief 생성자 주입으로 EvaluationCycleFacade를 받아 보관한다."""
        self._facade = facade

    def submit(self, rawVector: dict) -> EvaluationResult:
        """
        \\brief PC/SIL 테스트 벡터를 VehicleSnapshot으로 변환해 facade에 제출한다.

        \\param rawVector `{"timestamp_s": float|str, "ignition_on": bool}` 형태의 dict.
               `ignition_on` 누락 시 None(하류에서 INVALID 처리), `timestamp_s`
               누락/형식오류 시 0.0으로 대체(SWD-PH1 §10.2).
        \\return facade.submitVehicleSnapshot()의 반환값 그대로
        \\exception 발생하지 않음
        """
        timestampS = _parseFloat(rawVector.get("timestamp_s"), default=0.0)
        snapshot = VehicleSnapshot(timestampS=timestampS, ignitionOn=rawVector.get("ignition_on"))
        return self._facade.submitVehicleSnapshot(snapshot)
