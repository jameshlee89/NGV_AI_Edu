# VJ-ECL-2026 양방향 추적성 매트릭스 (Requirements Traceability Matrix, RTM)

이 파일은 `.claude/skills/requirements-analyst/references/traceability-matrix-template.md` 형식을
그대로 사용하는 프로젝트의 단일 진실 공급원(single source of truth)이다. 요구사항을 새로 만들거나
수정할 때마다 같은 작업 안에서 함께 갱신한다.

현재 범위: Phase 1(`feature/phase1-core-manual-control`), OEM-FR-001 · OEM-FR-007만 다룬다.
다른 OEM 요구사항(SR-001~004, FR-002~006, NFR-001~002)은 이후 Phase에서 이 표에 행을 추가한다.

## 최상위 계층 (OEM 요구사항 — 이 프로젝트의 최상위, StR/SR 계층 없음)

| ID | 유형 | 상위(근거) | 설계 요소 | 테스트 케이스 ID | 검증 상태 | 비고 |
|---|---|---|---|---|---|---|
| OEM-FR-001 | 기능(QM) | 이해관계자 요청 — 가상 OEM-A 공급자 입력, BL-OEM-1.0 | SWR-001, SWR-002, SWR-004 (하위 참조) | - | 미검증 | 수용기준: 정지·정상입력에서 4 source × LOCK/RELEASE × LEFT/RIGHT/ALL이 선택 출력에만 적용. 검증 수준: PC/SIL/Web |
| OEM-FR-007 | 기능(QM) | 이해관계자 요청 — 가상 OEM-A 공급자 입력, BL-OEM-1.0 | SWR-020 (하위 참조) | - | 미검증 | 수용기준: ignition_on=FALSE 첫 평가주기에 좌/우 RELEASE, state=OFF, reason=ignition_off. 검증 수준: PC/SIL/Web |

## SW 요구사항 계층 (Phase 1)

| 하위 ID | 유형 | 상위(근거) ID | 설계 요소 | 테스트 케이스 ID | 검증 상태 | 비고 |
|---|---|---|---|---|---|---|
| SWR-001 | 기능(QM) | OEM-FR-001 (+ OEM-IF-004 오류 처리) | 미정 (G2 아키텍처 설계에서 입력 검증 컴포넌트 배정 예정) | 미정 (G4, `sw-system-test` 스킬에서 도출 예정) | 미검증 | 다이어그램: `SWR-PH1_sequence.puml`, `SWR-PH1_requirements-trace.puml` |
| SWR-002 | 기능(QM) | OEM-FR-001 | 미정 (G2 아키텍처 설계에서 명령 디스패치 컴포넌트 배정 예정) | 미정 (G4) | 미검증 | 다이어그램: `SWR-PH1_sequence.puml`, `SWR-PH1_requirements-trace.puml` |
| SWR-004 | 기능(QM) | OEM-FR-001 | 미정 (G2 아키텍처 설계에서 출력 적용 컴포넌트 배정 예정) | 미정 (G4) | 미검증 | 다이어그램: `SWR-PH1_state-ignition.puml`(ACTIVE 하위상태), `SWR-PH1_requirements-trace.puml`. SWR-020과 우선순위 관계 있음(비고 참조) |
| SWR-020 | 기능(QM) | OEM-FR-007 | 미정 (G2 아키텍처 설계에서 점화상태 감시/출력 중재 컴포넌트 배정 예정) | 미정 (G4) | 미검증 | 다이어그램: `SWR-PH1_state-ignition.puml`(OFF↔ACTIVE 전이), `SWR-PH1_requirements-trace.puml`. SWR-002/SWR-004 산출값보다 항상 우선 적용(SWR 문서 §8) |

## 외부 인터페이스 참조 (요구사항이 아님 — 근거 자료)

| 인터페이스 ID | 관련 SWR | 비고 |
|---|---|---|
| OEM-IF-004 | SWR-001, SWR-002, SWR-004 | Driver → SW 명령 입력 계약 |
| OEM-IF-005 | SWR-004, SWR-020 | SW → Actuator model 출력 계약 |
| OEM-IF-006 (부분) | SWR-001(reason_code), SWR-020(state, reason_code) | `state`/`reason_code`만 이번 Phase 반영, 나머지 필드는 Phase 4 |
| OEM-IF-009 (부분) | SWR-020 | `ignition_on`만 이번 Phase 반영, `sensor_fault`는 Phase 2 |

## 알려진 공백 (결함 아님 — 게이트 진행에 따른 예정된 상태)

- SWR-001/002/004/020의 "설계 요소"·"테스트 케이스 ID"는 본 문서 작성 시점(G1, 요구사항 확정
  단계)에는 아직 존재하지 않는다. G2(아키텍처/상세설계) 완료 시 설계 요소를, G4(시스템 시험) 완료
  시 테스트 케이스 ID를 이 표에 채워 넣어야 한다 — 나중으로 미루지 않고 해당 산출물 작성과 같은
  작업 안에서 갱신한다.
- 고아 요구사항 없음: OEM-FR-001/007은 이해관계자 요청(가상 OEM-A 입력)을 상위로 명시했고,
  SWR-001/002/004/020은 모두 OEM-FR-ID를 상위로 갖는다.
- 근거 없는 산출물 없음: 이번 Phase에는 아직 설계/시험 산출물이 없으므로 해당 사항 없음. G2/G4
  산출물이 생기면 이 표의 링크와 대조해 근거 없는 항목이 없는지 확인해야 한다.

## 유지 규칙 (요약 — 전체 규칙은 스킬 참고자료 참조)

1. 상위(근거) 없는 요구사항 금지(최상위 OEM 요구사항은 "이해관계자 요청"으로 예외 처리).
2. 어떤 요구사항과도 연결되지 않는 설계/테스트 산출물 금지.
3. 이 표와 `SWR-PH1_requirements-trace.puml`의 `<<deriveReqt>>`/`<<refine>>`/`<<trace>>` 관계는
   항상 일치해야 한다.
4. 요구사항이 폐기되어도 행을 삭제하지 않고 "폐기" 상태로 표시한다.
