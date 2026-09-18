# VJ-ECL-2026 — 전자식 후석 차일드락 제어 SW

이 프로젝트 하위에서는 저장소 루트 `CLAUDE.md`의 개발 정책을 그대로 따르되, 아래 항목을 이 프로젝트
전용으로 재정의한다(이 폴더 하위에서만 적용, 저장소의 다른 프로젝트에는 영향 없음).

## 프로젝트 개요

- 입력 사양: `OEM_Sample/OEM-SWR-001_OEM SW 요구사항 사양서.docx` (가상 OEM-A 공급자 입력, 교육용
  시나리오, 베이스라인 BL-OEM-1.0)
- 대상: 대한민국 판매용 2026년식 가상 차량의 후석 좌/우 전자식 차일드락 제어 SW
- 범위: SW-only, PC/SIL 및 Web 시뮬레이터 검증까지. HIL/실차/ECU/HW/Part 3 HARA/공식 인증은 범위 밖.
- 안전 분류: OEM-SR-001~004는 가상 OEM이 할당한 ASIL B 입력. 나머지는 QM.
- 인도 게이트: G1(BL-SWR-1.0) → G2(BL-SWA-1.0/BL-SWD-1.0) → G3(BL-CODE-UT-1.0/BL-INT-1.0) →
  G4(BL-VER-1.0)

## 재정의 항목

- **실행 환경 Python 버전은 3.14가 아니라 3.12를 사용한다** — OEM 문서 §3(제품 경계)에 "Python 3.12
  PC/SIL"로 명시된 고객 실행환경 요건을 따른다.
- SW 요구사항 ID는 OEM 문서 §9(추적성)에 이미 배정된 `SWR-001`~`SWR-021` 번호 계획을 그대로 이어받아
  사용한다 — `requirements-analyst` 스킬의 임의 번호 부여 대신 이 계획을 우선한다.

## 개발 진행 방식

- 저장소 루트 `CLAUDE.md`의 분석→아키텍처 설계→구현→테스트 생명주기와 담당 서브에이전트
  (requirements-analyzer, architecture-designer, detailed-designer, coding/tdd,
  integration-tester, sw-system-tester)를 그대로 따른다.
- 전체 작업은 Phase 단위(기능별 수직 슬라이스)로 나누어 진행하며, Phase마다 분석→설계→구현→
  통합/시스템 시험을 모두 수행한 뒤 사용자 리뷰·승인을 받아 `main`에 merge한다. Phase 목록과 각
  Phase가 다루는 OEM 요구사항은 저장소 대화 이력(작업 계획)과 `docs/Traceability/`를 참고한다.
- 아키텍처는 Phase 1에서 전체 시스템 구조를 확정하고, 이후 Phase는 그 구조를 확장만 한다(전면
  재설계 지양).

## 산출물 위치

- `docs/SoftwareRequirementsAnalysis/` — SW 요구사항 명세서(G1)
- `docs/SoftwareArchitecturalDesign/` — 아키텍처 설계서(G2)
- `docs/SoftwareDetailedDesignAndUnitConstruction/` — 상세설계서 및 SBOM(G2/G3)
- `docs/SoftwareComponentVerificationAndIntegrationVerification/` — 통합 전략/시험 명세·결과(G3)
- `docs/SoftwareVerification/` — 시스템(자격인정) 시험 명세·결과(G4)
- `docs/Traceability/` — 양방향 추적성 매트릭스
- `src/` — Python 소스 코드
- `tests/unit/`, `tests/integration/`, `tests/system/` — 단계별 자동화 시험 코드
