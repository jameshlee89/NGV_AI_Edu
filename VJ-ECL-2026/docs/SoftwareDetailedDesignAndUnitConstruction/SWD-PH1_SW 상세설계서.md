> **비고(도구 제약)**: 회사 지정 템플릿 `WP_Templates/Engineering/SoftwareDetailedDesignAndUnitConstruction/
> TPL-SWE3-001_SW 상세설계서 템플릿.docx`가 이미 저장소에 존재하여, 이 문서는 그 템플릿의 장/절 구조
> (표지 → 문서 통제 → 목차 → 1~15장)를 그대로 옮겨 작성했다. 다만 현재 세션 환경에는 `.docx`를 직접
> 생성/수정할 도구(Node.js+`docx` 패키지, LibreOffice, pandoc 등)가 설치되어 있지 않아 `.docx` 파일
> 자체를 채우지 못하고, `SWR-PH1_SW 요구사항 명세서.md`/`SWA-PH1_SW 아키텍처 설계서.md`와 동일한 방식으로
> Markdown으로 작성했다. **docx 템플릿 직접 채우기는 별도 도구 필요** — 도구가 준비되면 이 내용을
> `TPL-SWE3-001` 사본에 그대로 옮겨 `.docx`로 재발행해야 한다. UML도 같은 이유로 `TPL-SWE3-002` drawio가
> 아니라 PlantUML(`.puml`)로만 작성했다(§9의 다이어그램 목록 참고) — drawio 이전은 별도 작업으로 남긴다.

# TPL-SWE3-001_SW 상세설계서 템플릿 기반 — SWD-PH1_SW 상세설계서

| 항목 | 내용 |
|---|---|
| 템플릿 ID | TPL-SWE3-001 |
| 적용 프로세스 | SWE.3 |
| 프로젝트 | VJ-ECL-2026 (가상 OEM-A 전자식 후석 좌/우 차일드락 제어 SW) |
| 작성 문서 ID와 명칭 | SWD-PH1_SW 상세설계서 |
| 버전 및 베이스라인 | v0.1 (초안) / 목표 베이스라인 BL-SWD-1.0 (승인 시 확정, G2 게이트) |
| 작성자와 검토자 | 작성자: 상세설계 에이전트(detailed-design 스킬, 세션 실행자 jaehwan2.lee@hlcompany.com) / 검토자 겸 승인자: jaehwan2.lee@hlcompany.com (사용자 본인, 지정 예정) |

본 자료는 SW 품질교육을 위한 교육용 샘플이며, 저작권은 Synetics에 있습니다. 교육 과정 안에서 열람,
복제 및 실습 사용을 허용합니다. 과정 밖 배포, 공개 또는 상업적 이용은 Synetics의 사전 서면 승인을
받아야 합니다. © 2026 Synetics. All rights reserved.

## 문서 통제

### 변경 이력

| Revision | 변경일 | 작성 역할 | 변경 내용 | 검토 상태 |
|---|---|---|---|---|
| v0.1 | 2026-09-18 | 상세설계 에이전트 | Phase 1 최초 작성. `SWA-PH1_SW 아키텍처 설계서.md`(ARC-001~007, ARC-101~105)를 모듈/함수/자료형 수준으로 구체화. ARC-002 정책 실행 예외 처리를 상세설계에서 확정(§10.4) | 초안 |

### 작성 검토 승인 상태

| 구분 | 역할 또는 성명 | 상태 | 일자 | 증거 위치 |
|---|---|---|---|---|
| 작성 | 상세설계 에이전트 | 완료 | 2026-09-18 | 본 문서 |
| 검토 | jaehwan2.lee@hlcompany.com (사용자 본인) | 대기 | - | - |
| 승인 | jaehwan2.lee@hlcompany.com (사용자 본인) | 대기 | - | - |

## 목차

1. 목적 및 적용범위
2. 모듈 분해
3. 상세 호출관계
4. 공통 자료형
5. 핵심 함수 계약
6. 핵심 알고리즘
7. 정책 의사결정표
8. 상태전이 상세
9. Web 및 API 상세
10. 오류와 방어 동작
11. 코딩 및 검증 규칙
12. 단위와 요구사항 할당
13. 구현 경계
14. 추적성
15. 참고자료

---

## 1. 목적 및 적용범위

### 1.1 목적

이 문서는 `SWA-PH1_SW 아키텍처 설계서.md`(v0.1, BL-SWA-1.0 목표)가 정의한 Phase 1 아키텍처 요소
(ARC-001~007, ARC-101~105)와 인터페이스(IF-INT-001~009, IF-EXT-001~004)를, 구현 가능한 수준의
모듈(`UNIT-XXX`)·함수 계약(`FN-XXX`)·공통 자료형·알고리즘·정책 의사결정표·상태전이·오류 방어 동작으로
구체화한다(SWE.3, G2 후반). 이 문서는 구현(coding/TDD, G3)과 단위시험(SWE.4) 산출물의 근거로 사용되며,
아키텍처 설계서의 컴포넌트/인터페이스 계약을 재정의하지 않고 그대로 구체화한다.

### 1.2 적용범위

- 대상 제품: VJ-ECL-2026 Phase 1 구현 대상 컴포넌트 — 코어(ARC-001~007), PC/SIL 어댑터(ARC-101~105)
- 대상 생명주기 단계: 상세설계(SWE.3), Phase 1(브랜치 `feature/phase1-core-manual-control`)
- 구현 언어/환경: Python 3.12 (VJ-ECL-2026 CLAUDE.md 재정의 항목), 표준 라이브러리만 사용(§13)
- 안전 분류: 이번 상세설계가 다루는 SWR-001/002/004/020은 모두 **QM** — ASIL 관련 방어 요건은 이번
  문서에 없다(ASIL B는 Phase 2, OEM-SR-001~004). 다만 IF-INT-008(정책 포트)의 ASIL 우선 실행 계약은
  Phase 2 삽입을 대비해 그대로 구현한다(§6.4, §7.3).
- 이번 문서가 다루지 않는 것: ARC-201~205(Phase4 Web 어댑터, 포트만 존중), ARC-301~403(Phase2/3 정책,
  포트만 존중), drawio 최종본(§0 비고), 실제 SBOM 작성(§13에서 안내만).

### 1.3 적용 경계

- **포함**: ARC-001~007, ARC-101~105의 모듈 분해, 호출관계, 공통 자료형, 핵심 함수 계약, SWR-004/020
  의사결정표·상태전이 상세화, 오류·방어 동작(특히 ARC-002 정책 실행 예외 처리 확정), 코딩/검증 규칙,
  요구사항-설계-시험 추적성 갱신.
- **제외**: 실제 구현 코드(별도 `tdd` 스킬/작업), 단위시험 케이스 자체(별도 `SWE.4` 산출물, 이 문서는
  그 산출물이 참조할 UNIT/FN ID만 제공), Web/HTTP API(Phase 4), Phase 2/3 정책의 내부 알고리즘, ISO
  26262 Part 3 HARA·공식 인증(VJ-ECL-2026 CLAUDE.md 범위 밖).
- **경계**: 근거 아키텍처 문서는 `SWA-PH1_SW 아키텍처 설계서.md`(BL-SWA-1.0 목표, 이하 "SWA 문서")이며,
  이 문서는 SWA 문서가 정의한 컴포넌트 경계·인터페이스 계약을 변경하지 않는다. 상세설계 중 새로운 공개
  인터페이스가 필요하다고 판단되는 지점은 없었다(§2 정합성 확인 결과 참고) — 있었다면 먼저 SWA 문서
  갱신을 사용자에게 제안했을 것이다.

## 1.4 아키텍처 정합성 확인 결과 (§2 필수 선행 단계, 기록)

- [x] ARC-001~007, ARC-101~105의 책임이 SWA 문서 §3~§4와 정확히 일치함을 확인했다 — 표 §2.1에서
      1:1 대응을 재확인한다.
- [x] 이 컴포넌트들이 제공/사용하는 인터페이스(IF-INT-001~009, IF-EXT-001~004)가 SWA 문서 §6과 동일함을
      확인했다 — 함수 시그니처(§5)는 SWA 문서의 인터페이스 시그니처를 문자 그대로 구체화했을 뿐, 새
      필드/새 오퍼레이션을 추가하지 않았다. **새로운 공개 인터페이스 추가 없음.**
- [x] SWA 문서 §11 통합 순서(상향식, 1~7단계)와 이번 상세설계의 모듈 우선순위(§3)가 상충하지 않음을
      확인했다.
- [x] SWA 문서가 상세설계로 위임한 미해결 사항(§4/§6 "ARC-002가 정책 실행 중 예외를 받았을 때의 처리는
      상세설계에서 확정")을 본 문서 §6.4/§10.4에서 확정했다 — 사용자 확인 불필요한 통상적 엔지니어링
      결정(오케스트레이터 지시사항)이며, 방어적 프로그래밍 원칙과 SWR-020의 안전측 기본값 원칙에 따라
      "평가주기 실패로 처리, 이전 확정 출력 유지"로 결정했다. 근거는 §10.4에 상세 기술한다.

## 2. 모듈 분해

### 2.1 구현 단위(UNIT) 목록

각 아키텍처 요소를 정확히 1개의 구현 단위로 분해했다(1:1 대응, 인프라 성격의 자료형/포트 정의만
별도 단위로 추가). 소스 위치는 SWA 문서 §13 권장 레이아웃(`src/core`, `src/adapters/pcsil`)을
구체화한 것이다(§13 참고).

| UNIT ID | 명칭 | 대응 ARC | 책임(단일) | 소스 위치(예정) |
|---|---|---|---|---|
| UNIT-000 | 공통 자료형(Common Types) | 없음(코어 전역 인프라) | 값 객체·열거형·순수 헬퍼 함수 정의만 — 로직/부작용 없음 | `src/core/types.py` |
| UNIT-008 | PolicyPort(정책 포트 정의) | 없음(IF-INT-008 포트 정의) | 정책 구현체가 지켜야 할 Protocol과 메타데이터 계약 정의만 | `src/core/policy_port.py` |
| UNIT-001 | EvaluationCycleFacade | ARC-001 | 구동 어댑터에 노출되는 단일 진입점 — Driver 명령 위임, Vehicle 스냅샷 제출 시 평가 트리거만 담당 | `src/core/facade.py` |
| UNIT-002 | PolicyChainExecutor | ARC-002 | 정책 체인 실행 순서·예외 격리·최종 출력 커밋(단일 writer)만 담당 | `src/core/policy_chain_executor.py` |
| UNIT-003 | CommandValidator | ARC-003 | `Driver_Command` 필드 존재·enum 소속 판정만 담당 | `src/core/command_validator.py` |
| UNIT-004 | CommandDispatcher | ARC-004 | 이번 평가주기 명령 1건의 보관/조회/폐기만 담당(소스 차별 없음) | `src/core/command_dispatcher.py` |
| UNIT-005 | LockStateStore | ARC-005 | `lock_left`/`lock_right` 직전 평가주기 값의 read/write만 담당 | `src/core/lock_state_store.py` |
| UNIT-006 | DriverCommandPolicy | ARC-006 | side 선택 출력 계산(BASE 정책)만 담당 | `src/core/policies/driver_command_policy.py` |
| UNIT-007 | IgnitionOverridePolicy | ARC-007 | ignition 강제 RELEASE 판정(OVERRIDE 정책)만 담당 | `src/core/policies/ignition_override_policy.py` |
| UNIT-101 | DriverCommandTestAdapter | ARC-101 | PC/SIL 테스트 벡터 → `DriverCommand` 변환 + IF-INT-001 호출만 담당 | `src/adapters/pcsil/driver_command_test_adapter.py` |
| UNIT-102 | VehicleSnapshotTestAdapter | ARC-102 | PC/SIL 테스트 벡터 → `VehicleSnapshot` 변환 + IF-INT-002 호출만 담당 | `src/adapters/pcsil/vehicle_snapshot_test_adapter.py` |
| UNIT-103 | ActuatorOutputTestAdapter | ARC-103 | 논리 `lock_left`/`lock_right` → OEM-IF-005 값 반영(및 시험용 조회)만 담당 | `src/adapters/pcsil/actuator_output_test_adapter.py` |
| UNIT-104 | DisplayOutputTestAdapter | ARC-104 | `state`/`reason_code` → OEM-IF-006(부분) 값 반영(및 시험용 조회)만 담당 | `src/adapters/pcsil/display_output_test_adapter.py` |
| UNIT-105 | PcSilHarnessEntryPoint | ARC-105 | Composition Root — ARC-101~104/001/002/006/007을 조립만 담당(로직 없음) | `src/adapters/pcsil/entry_point.py` |

**응집도 점검(`unit-design-principles-checklist.md` §1)**: 각 UNIT은 표의 "책임(단일)" 열 하나만
수행한다. UNIT-000/UNIT-008은 로직이 아니라 자료형/계약 정의만 담당하므로 그 자체로 응집도 위반이
아니다(공통 자료형은 원칙상 하나의 모듈에 모아도 되는 예외 — 서로 관련 없는 상수/자료형을 섞지 않았음을
§4에서 재확인).

### 2.2 UNIT ↔ ARC ↔ SWR 매핑 요약 (상세는 §12/§14)

| SWR | ARC | UNIT | 비고 |
|---|---|---|---|
| SWR-001 | ARC-003 | UNIT-003 | — |
| SWR-002 | ARC-004 | UNIT-004 | — |
| SWR-004 | ARC-006 | UNIT-006 | — |
| SWR-020 | ARC-007 | UNIT-007 | — |
| (인프라, SWR 직접 할당 없음) | ARC-001/002/005, ARC-101~105 | UNIT-001/002/005/008/101~105 | SWA 문서 §12 "근거 없는 요소 아닌 이유" 그대로 승계 |

## 3. 상세 호출관계

### 3.1 정적 호출/의존 방향 (SWA 문서 §5와 일치, 구체화)

```
UNIT-000 (types)            : 의존 없음(leaf) — 모든 UNIT이 이를 import
UNIT-008 (policy_port)      : UNIT-000에 의존(PolicyResult/PolicyContext 참조)

UNIT-005 (LockStateStore)   : UNIT-000에 의존 (leaf, 로직 의존 없음)
UNIT-003 (CommandValidator) : UNIT-000에 의존 (leaf)
UNIT-103 (Actuator adapter) : UNIT-000에 의존 (leaf, IF-INT-003 구현)
UNIT-104 (Display adapter)  : UNIT-000에 의존 (leaf, IF-INT-004 구현)

UNIT-004 (CommandDispatcher)   -> UNIT-003 (IF-INT-005 validate)
UNIT-007 (IgnitionOverridePolicy) -> UNIT-005 (IF-INT-007 read), UNIT-008(Protocol 구현), UNIT-000
UNIT-006 (DriverCommandPolicy)    -> UNIT-004 (IF-INT-006 get), UNIT-005 (IF-INT-007 read), UNIT-008, UNIT-000

UNIT-002 (PolicyChainExecutor) -> UNIT-006, UNIT-007 (IF-INT-008, UNIT-008 Protocol 타입으로만 참조 — DIP)
                                -> UNIT-005 (IF-INT-007 write, 단일 writer)
                                -> UNIT-004 (discard_current_cycle_command)
                                -> UNIT-103, UNIT-104 (IF-INT-003/004, 조립 시점 주입)

UNIT-001 (EvaluationCycleFacade) -> UNIT-004 (IF-INT-006 dispatch 위임), UNIT-002 (IF-INT-009 evaluate)

UNIT-101, UNIT-102 -> UNIT-001 (IF-INT-001/002)
UNIT-105            -> UNIT-101, UNIT-102, UNIT-103, UNIT-104, UNIT-001, UNIT-002, UNIT-006, UNIT-007, UNIT-005, UNIT-003, UNIT-004
                       (Composition Root — 모든 UNIT을 생성자 주입으로 조립, 실행 로직 없음)
```

**순환 의존 없음**: SWA 문서 §5와 동일한 위상(leaf: UNIT-000/003/005/103/104 → UNIT-004/006/007/008 →
UNIT-002 → UNIT-001 → UNIT-101/102 → UNIT-105). 역방향 호출 없음(`unit-design-principles-checklist.md`
§2 통과).

**DIP 유지**: UNIT-002는 `UNIT-006`/`UNIT-007`의 구체 클래스가 아니라 `UNIT-008`(`PolicyPort` Protocol)
타입으로만 참조한다 — 생성자에 `list[PolicyPort]`를 주입받는다(§5 FN-010 계약 참고). 마찬가지로
액추에이터/표시 출력도 각각 `ActuatorPort`/`DisplayPort` Protocol(모두 UNIT-008과 같은 위치에 정의,
아래 §4.6 참고)로 주입받는다.

### 3.2 주요 데이터 흐름 (시퀀스는 §6.4, §10.4의 신규 다이어그램과 SWA 문서 시퀀스 참고)

1. `UNIT-101 → UNIT-001.submit_driver_command(raw)` → `UNIT-001 → UNIT-004.dispatch(raw)` →
   `UNIT-004 → UNIT-003.validate(raw)` → 결과를 `UNIT-004` 내부에 staging.
2. `UNIT-102 → UNIT-001.submit_vehicle_snapshot(snapshot)` → `UNIT-001 → UNIT-002.evaluate(snapshot)`.
3. `UNIT-002`는 등록된 정책을 OVERRIDE(asil desc→priority asc) → BASE(priority asc) 순으로 호출
   (`UNIT-007.evaluate(context)`, `UNIT-006.evaluate(context)`), 그 안에서 `UNIT-006`은
   `UNIT-004.get_current_cycle_command()`와 `UNIT-005.read_current()`를 직접 호출한다(§3.1 의존
   그래프와 일치 — `UNIT-002`가 이 호출을 대행하지 않는다).
4. `UNIT-002`가 `UNIT-005.write(...)`, `UNIT-103.apply(...)`, `UNIT-104.show(...)`,
   `UNIT-004.discard_current_cycle_command()`를 순서대로 호출해 주기를 종료한다(정상 종료 시). 예외
   시의 대체 흐름은 §6.4/§10.4 참고.

다이어그램: `SWD-PH1_class.puml`(구조), `SWD-PH1_sequence-policy-fault.puml`(예외 처리 흐름, 신규),
`SWD-PH1_state-cycle-detail.puml`(예외 처리 포함 확장 상태도, 신규). 모두 SWA 문서의
`SWA-PH1_component.puml`/`SWA-PH1_sequence-*.puml`/`SWA-PH1_state-cycle.puml`과 요소·ID가 일치한다
(§9 다이어그램 목록, §12 자체 점검 참고).

## 4. 공통 자료형

`references/function-contract-guide.md`·SWA 문서 §6에 언급된 필드를 그대로 따르되, Python
`dataclass`/`Enum`으로 확정한다. 모두 `src/core/types.py`(UNIT-000)에 정의하며 **불변(frozen)**
값 객체로 설계한다(스레드 안전성 요구는 없으나 §3.2 아키텍처 가정과 일관되게 부주의한 변형을 원천
차단).

### 4.1 열거형(Enum)

| 자료형 | 값 | 근거 |
|---|---|---|
| `Side` | `LEFT="left"`, `RIGHT="right"`, `ALL="all"` | SWR-PH1 §5, SWA §6.1 |
| `Action` | `LOCK="lock"`, `UNLOCK="unlock"` | SWR-PH1 §5 |
| `Source` | `PHYSICAL_BUTTON="physical_button"`, `AVN="avn"`, `VOICE="voice"`, `MOBILE_APP="mobile_app"` | SWR-PH1 §5 |
| `LockState` | `LOCK="LOCK"`, `RELEASE="RELEASE"` | OEM-IF-005, SWR-PH1 §6 |
| `DisplayState` | `LOCKED_LEFT`, `LOCKED_RIGHT`, `LOCKED_ALL`, `RELEASED`, `OFF` | OEM-IF-006(가정, SWR-PH1 §6/§8) |
| `ReasonCode` | `NONE="NONE"`, `INVALID_COMMAND="INVALID_COMMAND"`, `IGNITION_OFF="IGNITION_OFF"` | OEM-IF-006 최소 집합(SWR-PH1 §6) + `NONE`은 이번 상세설계에서 "정상, 특이 사유 없음"을 나타내기 위해 도입한 값(아래 결정 사항 참고) |
| `IgnitionState` | `ON`, `OFF`, `INVALID` | SWR-020(b), IF-INT-002 오류 계약(SWA §6.1) — ARC-007 내부 판정 결과를 표현하는 상세설계 전용 내부 자료형(외부 인터페이스에 노출되지 않음) |
| `PolicyDecision` | `OVERRIDE_FINAL`, `PROPOSE`, `PASS` | IF-INT-008(SWA §6.1) |
| `PolicyCategory` | `OVERRIDE`, `BASE` | IF-INT-008 메타데이터(SWA §6.1) |
| `AsilLevel` | `QM`, `ASIL_B` | IF-INT-008 메타데이터(SWA §6.1) — Phase 1은 `QM`만 실사용, `ASIL_B`는 Phase 2 확장을 위해 미리 정의 |
| `CycleStatus` | `COMMITTED`, `FAILED` | 이번 상세설계에서 §6.4 결정에 따라 신규 도입(내부 전용, 아래 결정 사항 참고) |

**결정 사항(상세설계 재량, 공개 인터페이스 변경 아님)**: `ReasonCode.NONE`과 `CycleStatus`는 SWA
문서에 명시적 필드로 나열되지 않았으나, SWA 문서가 위임한 두 가지 자리(① 정상 상태에서 표시할 "사유
없음" 값 — SWA `sequence-nominal.puml`의 `reason_code=-` 자리를 구체 값으로 확정, ② §6.4/§10.4에서
확정한 ARC-002 예외 처리 결과를 표현하는 값)를 채우기 위한 **내부 표현 확정**이다. 둘 다 기존
IF-INT-004/IF-INT-009의 필드 이름과 구조를 그대로 사용하며 어떤 어댑터도 새 필드를 외부로 노출하지
않으므로 공개 인터페이스 변경에 해당하지 않는다(§2 정합성 확인 결과 참고).

### 4.2 원시(미검증) 값 객체 — 신뢰 경계 진입 시점

| 자료형 | 필드 | 타입 | 불변조건 |
|---|---|---|---|
| `DriverCommand` | `side: object`, `action: object`, `source: object` | `object`(검증 전이므로 임의 타입 허용 — 누락 시 `None`) | 없음(의도적으로 무제약 — CommandValidator가 유일한 검증 지점) |
| `VehicleSnapshot` | `timestamp_s: float`, `ignition_on: object` | `ignition_on`은 검증 전 원시값(`bool` 기대, 형식 오류 시 다른 타입/`None` 가능) | `timestamp_s`는 어댑터(UNIT-102)에서 항상 `float`로 정규화(§10.2) — 코어 로직은 이 필드를 Phase 1에서 사용하지 않음(Phase 2 `ARC-304` 대비 보존 필드, SWA §3.2) |

### 4.3 검증된 값 객체

| 자료형 | 필드 | 타입 |
|---|---|---|
| `ValidCommand` | `side: Side`, `action: Action`, `source: Source` | 모두 강타입 Enum |
| `Rejection` | `reason_code: ReasonCode` | Phase 1에서는 항상 `INVALID_COMMAND` |
| `LockPair` | `left: LockState`, `right: LockState` | `LockStateStore.read_current()` 반환 타입 |

### 4.4 정책 관련 자료형 (IF-INT-008)

```python
@dataclass(frozen=True)
class PolicyContext:
    snapshot: VehicleSnapshot          # ARC-002가 IF-INT-009로 받은 스냅샷을 그대로 전달

@dataclass(frozen=True)
class PolicyResult:
    decision: PolicyDecision
    lock_left: LockState | None = None     # decision=PASS일 때는 None(무의미)
    lock_right: LockState | None = None
    reason_code: ReasonCode | None = None
    state_label: DisplayState | None = None
```

**불변조건**: `decision in (OVERRIDE_FINAL, PROPOSE)`이면 `lock_left`/`lock_right`/`state_label`이
모두 `None`이 아니어야 한다(§5 FN-050/FN-060 사후조건에서 검증). `decision=PASS`이면 나머지 필드는
`None`이어야 한다(사용하지 않음을 명시).

### 4.5 평가 결과 자료형 (IF-INT-002/009 반환값 — SWA 문서가 필드를 정하지 않아 이번 문서에서 확정)

```python
@dataclass(frozen=True)
class EvaluationResult:
    status: CycleStatus                     # COMMITTED | FAILED
    lock_left: LockState                    # 이번 주기 확정값(FAILED면 직전 값 그대로)
    lock_right: LockState
    state_label: DisplayState | None = None # COMMITTED 시 항상 설정, FAILED 시 None(§10.4)
    reason_code: ReasonCode | None = None   # COMMITTED 시 항상 설정, FAILED 시 None(§10.4)
    error_detail: str | None = None         # FAILED 시에만 설정. 진단 전용 — 어떤 OEM 인터페이스에도 노출되지 않음
```

### 4.6 정책·출력 포트 Protocol (UNIT-008, IF-INT-003/004/008의 코드 수준 표현)

```python
class PolicyPort(Protocol):
    category: PolicyCategory
    asil_level: AsilLevel
    priority: int
    def evaluate(self, context: PolicyContext) -> PolicyResult: ...

class ActuatorPort(Protocol):
    def apply(self, lock_left: LockState, lock_right: LockState) -> None: ...

class DisplayPort(Protocol):
    def show(self, state: DisplayState, reason_code: ReasonCode) -> None: ...
```

`typing.Protocol`(구조적 서브타이핑)을 사용해 SWA 문서의 DIP/LSP 근거(§5 "ARC-002는 구체 타입이 아니라
포트에 의존")를 코드 수준에서 그대로 구현한다. `ARC-103`/`ARC-104`(및 Phase4의 `ARC-203`/`ARC-204`)는
이 Protocol을 명시적으로 상속하지 않아도 시그니처만 만족하면 대입 가능하다(LSP, SWA §5).

### 4.7 직렬화 규칙

Phase 1은 PC/SIL 함수 호출 인터페이스만 사용하며 네트워크/파일 직렬화가 필수는 아니다. 다만
PC/SIL 테스트 벡터(§9)는 Python `dict`(JSON 호환 구조)로 표현하고, 위 Enum들은 `.value`(문자열)로
직렬화/역직렬화한다 — Phase 4 Web 어댑터가 동일 규칙을 재사용할 수 있도록 값(value)을 OEM 원문 표기와
동일하게 유지했다(SWA §6.2).

## 5. 핵심 함수 계약

`function-contract-guide.md` 형식을 준수한다. IF-XXX를 구현하는 공개 함수는 전부 계약을 명세했다.
표 형식(속성별 열)으로 정리하고, 알고리즘 본문이 필요한 함수는 §6에서 의사코드로 보강한다.

### 5.1 UNIT-003 CommandValidator — FN-020

| 속성 | 내용 |
|---|---|
| 함수 ID / 인터페이스 | `FN-020` / `IF-INT-005` |
| 시그니처 | `validate(self, raw: DriverCommand) -> ValidCommand \| Rejection` |
| 입력 | `raw`: 검증 전 `DriverCommand`(§4.2). `raw`가 `None`이거나 `DriverCommand` 인스턴스가 아닌 경우도 방어적으로 허용(호출자 계약 위반이지만 예외 대신 `Rejection` 반환, 아래 사전조건 참고) |
| 출력 | `ValidCommand`(모든 필드 유효) 또는 `Rejection(reason_code=INVALID_COMMAND)` |
| 사전조건 | 없음(총함수, total function) — 어떤 입력에도 예외 없이 값을 반환해야 한다. `raw`가 `DriverCommand`가 아니어도 방어적으로 `Rejection`을 반환한다(호출자 계약 위반 시의 방어적 완화, §10.1) |
| 사후조건 | `raw.side ∈ Side`, `raw.action ∈ Action`, `raw.source ∈ Source`가 모두 성립하면 `ValidCommand(Side(raw.side), Action(raw.action), Source(raw.source))`를 반환한다. 그 외 모든 경우 `Rejection(INVALID_COMMAND)`를 반환한다 |
| 부작용 | 없음(순수 함수) |
| 예외 | 발생하지 않음(모든 오류 경로가 `Rejection` 값으로 귀결 — IF-INT-005 계약) |
| 시간 제약 | 없음 |
| 관련 요구사항 | SWR-001 |

### 5.2 UNIT-004 CommandDispatcher — FN-030/031/032

| 속성 | FN-030 `dispatch` | FN-031 `get_current_cycle_command` | FN-032 `discard_current_cycle_command` |
|---|---|---|---|
| 인터페이스 | IF-INT-006 | IF-INT-006 | IF-INT-006 |
| 시그니처 | `dispatch(self, raw: DriverCommand) -> None` | `get_current_cycle_command(self) -> ValidCommand \| Rejection \| None` | `discard_current_cycle_command(self) -> None` |
| 입력 | `raw` | 없음 | 없음 |
| 출력 | 없음 | 이번 주기 staged 값(없으면 `None`) | 없음 |
| 사전조건 | 없음 | 없음(주기당 0~N회 호출 가능, Phase1 실사용은 최대 1회 — SWA §6.1) | 없음(멱등) |
| 사후조건 | `self._validator.validate(raw)` 결과가 내부 상태에 staging된다. 이미 staged 값이 있었다면 **새 값으로 덮어쓴다**(§10.2 방어적 결정, SWR-PH1 가정2 위반 감지 시 경고 로그) | 반환값은 `self._staged`의 현재 값과 같다(부작용 없음, 값을 지우지 않음) | 호출 후 `self._staged is None` |
| 부작용 | 내부 staging 상태 갱신, `self._validator.validate()` 호출(UNIT-003 의존) | 없음 | 내부 staging 상태 초기화 |
| 예외 | 발생하지 않음(내부적으로 `FN-020`이 예외를 던지지 않음을 이미 보장, §5.1) | 발생하지 않음 | 발생하지 않음 |
| 시간 제약 | 없음 | 없음 | 없음 |
| 관련 요구사항 | SWR-002 | SWR-002 | SWR-002, SWR-020(b) |

**SWR-002 동등 처리의 코드 수준 근거**: `dispatch`/`get_current_cycle_command`/
`discard_current_cycle_command`의 구현은 `raw.source`/`ValidCommand.source` 값을 어떤 조건문에서도
참조하지 않는다(§11 코딩 규칙에서 정적 점검 항목으로 고정). `source`는 `ValidCommand`에 보존되어
표시/로깅 목적으로만 전달될 수 있으나 Phase 1 흐름에서는 사용되지 않는다.

### 5.3 UNIT-005 LockStateStore — FN-040/041

| 속성 | FN-040 `read_current` | FN-041 `write` |
|---|---|---|
| 인터페이스 | IF-INT-007 | IF-INT-007 |
| 시그니처 | `read_current(self) -> LockPair` | `write(self, left: LockState, right: LockState) -> None` |
| 사전조건 | 없음 | `left`, `right`가 모두 `LockState` 인스턴스여야 한다(내부 신뢰 경계 — 호출자는 코어 내부 컴포넌트뿐이므로 계약 위반은 프로그래밍 오류로 간주, §10.3) |
| 사후조건 | 초기값은 `LockPair(RELEASE, RELEASE)`(SWR-PH1 §8 가정3). 이후 직전 `write()` 인자를 그대로 반환 | 호출 후 `read_current()`가 `LockPair(left, right)`를 반환한다 |
| 부작용 | 없음 | 내부 상태 갱신(단일 writer는 `UNIT-002`만 — 관례로 강제, 언어 수준 강제 없음, §10.3) |
| 예외 | 발생하지 않음 | 사전조건 위반 시 `TypeError`(방어적 assert, §10.3 — 프로그래밍 오류이므로 값 대신 예외로 즉시 실패시킨다) |
| 관련 요구사항 | SWR-004, SWR-020 | SWR-004, SWR-020 |

### 5.4 UNIT-006 DriverCommandPolicy — FN-050

| 속성 | 내용 |
|---|---|
| 함수 ID / 인터페이스 | `FN-050` / `IF-INT-008`(BASE, `category=BASE`, `asil_level=QM`, `priority=1`) |
| 시그니처 | `evaluate(self, context: PolicyContext) -> PolicyResult` |
| 입력 | `context.snapshot`(직접 사용하지 않음 — ignition 판정은 ARC-007 책임), 내부적으로 `self._dispatcher.get_current_cycle_command()`, `self._store.read_current()` 호출 |
| 출력 | `PolicyResult(decision=PROPOSE, lock_left, lock_right, reason_code, state_label)` — §7.1 의사결정표 참고 |
| 사전조건 | `self._dispatcher`, `self._store`가 생성자 주입으로 유효해야 한다(구성 시점 보장, 조립 책임은 UNIT-105) |
| 사후조건 | §7.1 의사결정표의 12+2행을 모두 만족한다. 선택되지 않은 출력은 `self._store.read_current()`의 값과 정확히 같다(부작용 없이 동일 참조) |
| 부작용 | 없음(읽기 전용 호출만 수행, `write`하지 않음 — 커밋은 UNIT-002의 책임) |
| 예외 | 이 함수 자체는 정상 입력에서 예외를 던지지 않도록 설계했다(총함수). 다만 IF-INT-008 계약(SWA §6.1)상 정책이 예외를 던지는 것은 계약 위반이며, 그 경우의 처리는 호출자(UNIT-002)의 책임이다(§6.4/§10.4) |
| 시간 제약 | 없음 |
| 관련 요구사항 | SWR-004 |

### 5.5 UNIT-007 IgnitionOverridePolicy — FN-060/FN-061

| 속성 | FN-060 `evaluate` | FN-061 `_classify_ignition`(내부 헬퍼) |
|---|---|---|
| 인터페이스 | IF-INT-008(OVERRIDE, `category=OVERRIDE`, `asil_level=QM`, `priority=1`) | 없음(내부 전용) |
| 시그니처 | `evaluate(self, context: PolicyContext) -> PolicyResult` | `_classify_ignition(raw: object) -> IgnitionState`(정적 메서드) |
| 입력 | `context.snapshot.ignition_on`(원시값), 내부적으로 `self._store.read_current()` 호출(§6.3 근거 참고) | 임의 타입의 `raw` |
| 출력 | §7.2 의사결정표 참고 | `IgnitionState.ON`/`OFF`/`INVALID` |
| 사전조건 | 없음 | 없음(총함수) |
| 사후조건 | `_classify_ignition(...) == ON`이면 `PolicyResult(decision=PASS)`. 그 외(`OFF`/`INVALID`)면 `PolicyResult(OVERRIDE_FINAL, lock_left=RELEASE, lock_right=RELEASE, reason_code=IGNITION_OFF, state_label=OFF)` | `isinstance(raw, bool)`이고 `raw is True`이면 `ON`, `isinstance(raw, bool)`이고 `raw is False`이면 `OFF`, 그 외 모든 타입(`None`, `str`, `int` 등)은 `INVALID` |
| 부작용 | `self._store.read_current()` 호출(읽기만, §6.3에 사용 목적 설명) | 없음 |
| 예외 | 발생하지 않음(총함수) | 발생하지 않음 |
| 관련 요구사항 | SWR-020 | SWR-020(b) |

### 5.6 UNIT-002 PolicyChainExecutor — FN-010/FN-011

| 속성 | FN-010 `evaluate` | FN-011 `register_policy`(구성 전용) |
|---|---|---|
| 인터페이스 | IF-INT-009 | 없음(조립 단계 전용, UNIT-105가 호출) |
| 시그니처 | `evaluate(self, snapshot: VehicleSnapshot) -> EvaluationResult` | `register_policy(self, policy: PolicyPort) -> None` |
| 입력 | `snapshot` | `policy`(`category`/`asil_level`/`priority` 속성을 가진 `PolicyPort`) |
| 출력 | `EvaluationResult`(§4.5) | 없음 |
| 사전조건 | `register_policy`로 최소 1개 이상의 정책이 등록되어 있어야 정상 동작(Phase 1 조립 시 2개 등록, UNIT-105 책임). 등록되지 않았다면 BASE 단계에서 아무 정책도 실행되지 않고 `PolicyResult`가 없는 상태가 되는데, 이는 §10.4에서 방어적으로 처리한다 | 없음(호출 순서만 준수하면 됨 — 평가 시작 전에 완료) |
| 사후조건 | §6.4 알고리즘을 그대로 만족한다: OVERRIDE 정책을 asil 내림차순→priority 오름차순으로 스캔, `OVERRIDE_FINAL` 발견 시 즉시 채택 및 이후 스킵, 모두 PASS면 BASE 정책(priority 오름차순) 실행. 정상 종료 시 `LockStateStore.write`, `ActuatorPort.apply`, `DisplayPort.show`, `CommandDispatcher.discard_current_cycle_command`를 정확히 1회씩 호출한 뒤 `EvaluationResult(status=COMMITTED, ...)`를 반환한다. 정책 예외 발생 시 §10.4의 절차를 따르고 `EvaluationResult(status=FAILED, ...)`를 반환한다 — 이 경우 `write`/`apply`/`show`는 호출하지 않되 `discard_current_cycle_command`는 호출한다(§6.4/§10.4 근거) | 등록 목록에 `policy`가 추가된다(순서는 이후 §6.4 정렬 로직이 재정렬하므로 등록 순서 자체는 의미 없음) |
| 부작용 | `UNIT-005/103/104/004`에 대한 호출(정상/실패 경로에 따라 다름, §6.4), 내부 로거를 통한 오류 기록(§10.4) | 내부 등록 리스트 갱신 |
| 예외 | **이 함수는 정책의 예외를 외부로 전파하지 않는다** — 모든 정책 예외를 포획해 `FAILED` 결과로 변환한다(§10.4 결정, 이번 상세설계 확정 사항). 정책이 아닌 `UNIT-005/103/104`의 호출에서 발생하는 예외는 설계상 발생하지 않는다고 가정하지 않고, 방어 심층화(defense in depth) 차원에서 동일하게 `FAILED`로 흡수한다(§10.4 "안전망" 절 참고) | 발생하지 않음 |
| 시간 제약 | 없음 |
| 관련 요구사항 | SWR-004, SWR-020(중재 실행), SWR-PH1 §8(우선순위 상충 해소) | 없음(조립 인프라) |

### 5.7 UNIT-001 EvaluationCycleFacade — FN-001/FN-002

| 속성 | FN-001 `submit_driver_command` | FN-002 `submit_vehicle_snapshot` |
|---|---|---|
| 인터페이스 | IF-INT-001 | IF-INT-002 |
| 시그니처 | `submit_driver_command(self, raw: DriverCommand) -> None` | `submit_vehicle_snapshot(self, snapshot: VehicleSnapshot) -> EvaluationResult` |
| 사전조건 | 평가주기당 최대 1회 호출 권장(SWA §6.1) — 위반 시 §10.2의 CommandDispatcher 방어 규칙이 흡수 | 평가주기당 정확히 1회 호출 필요(SWA §6.1) — 이 함수 호출 자체가 평가주기 트리거이므로 여러 번 호출하면 여러 번 평가되는 것으로 정의(방어적으로 거부하지 않음, §10.2) |
| 사후조건 | `self._dispatcher.dispatch(raw)`를 그대로 위임 호출 | `self._executor.evaluate(snapshot)`을 그대로 위임 호출하고 그 결과를 반환 |
| 부작용 | `UNIT-004` 상태 변경(위임) | `UNIT-002` 전체 평가주기 부작용(위임) |
| 예외 | 발생하지 않음(하위 계약이 이미 총함수) | 발생하지 않음(`FN-010`이 이미 총함수, §10.4) |
| 관련 요구사항 | SWR-001, SWR-002 | SWR-004, SWR-020 |

### 5.8 UNIT-101~104 PC/SIL 어댑터 — FN-101~104

| 속성 | FN-101 `DriverCommandTestAdapter.submit` | FN-102 `VehicleSnapshotTestAdapter.submit` | FN-103 `ActuatorOutputTestAdapter.apply`(+`get_last_applied`) | FN-104 `DisplayOutputTestAdapter.show`(+`get_last_shown`) |
|---|---|---|---|---|
| 인터페이스 | IF-EXT-001 → IF-INT-001 | IF-EXT-002 → IF-INT-002 | IF-INT-003(구현) | IF-INT-004(구현) |
| 시그니처 | `submit(self, raw_vector: dict) -> None` | `submit(self, raw_vector: dict) -> EvaluationResult` | `apply(self, lock_left: LockState, lock_right: LockState) -> None` / `get_last_applied(self) -> LockPair \| None` | `show(self, state: DisplayState, reason_code: ReasonCode) -> None` / `get_last_shown(self) -> tuple[DisplayState, ReasonCode] \| None` |
| 입력 | `raw_vector`: PC/SIL 테스트 벡터 `dict`(§9.1) | `raw_vector`: PC/SIL 테스트 벡터 `dict`(§9.1) | `lock_left`/`lock_right`(코어에서 이미 검증된 `LockState`) | `state`/`reason_code`(코어에서 이미 검증된 값) |
| 사전조건 | 없음(총함수 — `dict.get()`으로 누락 필드를 방어적으로 `None` 처리, §10.2) | 없음(동일) | 호출자(UNIT-002)가 유효한 `LockState`만 전달한다는 내부 신뢰 경계 전제(§10.3과 동일 논리) | 좌동 |
| 사후조건 | `DriverCommand(side=raw_vector.get("side"), action=raw_vector.get("action"), source=raw_vector.get("source"))`를 만들어 `self._facade.submit_driver_command(...)` 호출 | `VehicleSnapshot(timestamp_s=parse_float(raw_vector.get("timestamp_s"), default=0.0), ignition_on=raw_vector.get("ignition_on"))`를 만들어 `self._facade.submit_vehicle_snapshot(...)` 호출 후 결과 반환 | 내부에 `(lock_left, lock_right)` 저장, `get_last_applied()`가 그 값을 반환 | 내부에 `(state, reason_code)` 저장 |
| 부작용 | `UNIT-001` 호출 | `UNIT-001` 호출 | 내부 상태 갱신(시험용 조회 지원 — 코어 인터페이스(IF-INT-003)에는 없는 **Test 어댑터 전용 확장**, §10.2 근거) | 좌동(IF-INT-004 확장) |
| 예외 | 발생하지 않음(형식 오류 필드는 `None`으로 전달 → 하류 `CommandValidator`가 거절, §5.1) | `timestamp_s` 형식 오류는 `parse_float`가 흡수해 `0.0`으로 대체하고 경고 로그(§10.2) — 예외 발생 안 함 | 발생하지 않음 | 발생하지 않음 |
| 관련 요구사항 | SWR-001, SWR-002 | SWR-020 | SWR-004, SWR-020 | SWR-001(b), SWR-020 |

### 5.9 UNIT-105 PcSilHarnessEntryPoint — FN-105

| 속성 | 내용 |
|---|---|
| 함수 ID | `FN-105` |
| 시그니처 | `build_system() -> SystemHandle` (모듈 수준 팩토리 함수, 순수 조립) |
| 입력 | 없음(모든 의존은 기본 생성 — Phase 1은 설정 파일 없음) |
| 출력 | `SystemHandle`(`driver_adapter`, `vehicle_adapter`, `actuator_adapter`, `display_adapter` 참조를 담은 `dataclass` — 시험 코드가 이 4개 어댑터만 참조하면 되도록 캡슐화) |
| 사전조건 | 없음 |
| 사후조건 | 반환된 `SystemHandle`의 각 어댑터가 §3.1 의존 그래프대로 완전히 배선되어 있다(모든 생성자 주입 완료, `None` 의존 없음) |
| 부작용 | 각 UNIT의 인스턴스를 새로 생성(1회성 조립, Composition Root 패턴 — 로직 없음) |
| 예외 | 발생하지 않음(고정된 배선, 외부 입력 없음) |
| 관련 요구사항 | 없음(조립 인프라, SWA §12 근거 승계) |

## 6. 핵심 알고리즘

`algorithm-decision-guide.md` 형식(의사코드, 경계값 명시)을 따른다.

### 6.1 FN-020 `CommandValidator.validate` (SWR-001)

```
FUNCTION validate(raw):
    IF raw가 DriverCommand 인스턴스가 아니면:
        RETURN Rejection(INVALID_COMMAND)          # 방어적 완화, §10.1
    TRY:
        side = Side(raw.side)      # raw.side가 None/미등록 값이면 ValueError
        action = Action(raw.action)
        source = Source(raw.source)
    CATCH ValueError:
        RETURN Rejection(INVALID_COMMAND)
    RETURN ValidCommand(side, action, source)
END FUNCTION
```

경계값: `raw.side`/`action`/`source`가 `None`인 경우 `Enum(None)`은 `ValueError`를 던지므로 위
`except`가 그대로 처리한다(누락 필드 = 형식 오류와 동일 경로, §5.1 사후조건과 일치).

### 6.2 FN-050 `DriverCommandPolicy.evaluate` (SWR-004)

```
FUNCTION evaluate(context):
    current = store.read_current()                       # LockPair
    cmd = dispatcher.get_current_cycle_command()          # ValidCommand | Rejection | None

    IF cmd is None:
        new_left, new_right, reason = current.left, current.right, ReasonCode.NONE
    ELIF cmd is Rejection:
        new_left, new_right, reason = current.left, current.right, ReasonCode.INVALID_COMMAND
    ELSE:  # ValidCommand
        target = LOCK if cmd.action == Action.LOCK else RELEASE
        IF cmd.side == Side.LEFT:
            new_left, new_right = target, current.right
        ELIF cmd.side == Side.RIGHT:
            new_left, new_right = current.left, target
        ELSE:  # Side.ALL
            new_left, new_right = target, target
        reason = ReasonCode.NONE

    state_label = derive_display_state(new_left, new_right)   # UNIT-000 공통 헬퍼, §4
    RETURN PolicyResult(PROPOSE, new_left, new_right, reason, state_label)
END FUNCTION
```

`derive_display_state(left, right)`(UNIT-000 공통 순수 함수): `(LOCK,LOCK)→LOCKED_ALL`,
`(LOCK,RELEASE)→LOCKED_LEFT`, `(RELEASE,LOCK)→LOCKED_RIGHT`, `(RELEASE,RELEASE)→RELEASED`. 4가지
입력 조합을 모두 다루므로 완전하다(경계값 없음 — `LockState`는 2값 Enum이므로 조합이 유한).

### 6.3 FN-060 `IgnitionOverridePolicy.evaluate` (SWR-020)

```
FUNCTION evaluate(context):
    state = classify_ignition(context.snapshot.ignition_on)
    _ = store.read_current()   # 아키텍처 §5 의존(IF-INT-007 read) 이행 — 분기에는 사용하지 않음(설계 근거 아래 참고)
    IF state == ON:
        RETURN PolicyResult(PASS)
    ELSE:  # OFF 또는 INVALID
        RETURN PolicyResult(OVERRIDE_FINAL, RELEASE, RELEASE, IGNITION_OFF, OFF)
END FUNCTION

FUNCTION classify_ignition(raw):
    IF raw is True:  RETURN IgnitionState.ON
    IF raw is False: RETURN IgnitionState.OFF
    RETURN IgnitionState.INVALID          # None, 문자열, 정수 등 bool이 아닌 모든 값
END FUNCTION
```

**설계 근거 — `read_current()` 호출이 분기에 쓰이지 않는 이유(중요, §2 정합성 확인 관련 기록)**: SWA
문서 §5는 `ARC-007 -> ARC-005 (IF-INT-007, read)` 의존을 정적으로 명시했으므로 이 상세설계는 그 호출을
제거하지 않는다. 그러나 SWR-020의 세 조건(a/b/c)을 분석한 결과, 강제 출력값(`RELEASE`)은 직전 값에
관계없이 항상 고정되므로 **분기 결정에는 읽은 값이 실제로 필요하지 않다**(§6.4 설계 근거와 동일 논리
— (c)가 무상태로 성립하는 이유도 이것과 연결된다, §8.2 참고). 이번 상세설계는 이 호출을 (1) 아키텍처
의존 계약 이행, (2) Phase 4 관측성(진입/지속 전이 판별용 로깅) 확장 지점으로 유지하고, 반환값을 분기에
사용하지 않는다는 사실을 코드 주석과 단위시험(진입 시 값과 무관하게 항상 동일 출력)으로 명시적으로
검증하도록 §11에 규칙을 추가했다.

### 6.4 FN-010 `PolicyChainExecutor.evaluate` (SWR-004, SWR-020, SWR-PH1 §8 상충 해소 실행)

```
FUNCTION evaluate(snapshot):
    context = PolicyContext(snapshot)
    override_list = sort(정책 중 category==OVERRIDE,
                          key=(asil_level 내림차순[ASIL_B before QM], priority 오름차순))
    base_list     = sort(정책 중 category==BASE, key=priority 오름차순)

    result = None
    fault  = None

    FOR policy IN override_list:
        TRY:
            r = policy.evaluate(context)
        CATCH Exception as e:
            fault = (policy, "OVERRIDE_SCAN", e)
            BREAK
        IF r.decision == OVERRIDE_FINAL:
            result = r
            BREAK
        # decision == PASS -> 다음 정책 계속

    IF fault is None AND result is None:      # 모든 OVERRIDE가 PASS
        FOR policy IN base_list:
            TRY:
                r = policy.evaluate(context)
            CATCH Exception as e:
                fault = (policy, "BASE_EVAL", e)
                BREAK
            result = r
            BREAK   # Phase 1은 BASE 정책이 1개 — 향후 다중 BASE 시 priority 오름차순으로 계속 반복(OCP)

    IF fault is not None:
        RETURN _handle_cycle_failure(fault)          # §10.4
    IF result is None:                                # 등록된 정책이 0개(구성 오류) — 방어적 처리
        fault = (None, "NO_POLICY_REGISTERED", RuntimeError("no policy produced a result"))
        RETURN _handle_cycle_failure(fault)

    store.write(result.lock_left, result.lock_right)
    actuator_port.apply(result.lock_left, result.lock_right)
    display_port.show(result.state_label, result.reason_code)
    dispatcher.discard_current_cycle_command()
    RETURN EvaluationResult(COMMITTED, result.lock_left, result.lock_right,
                              result.state_label, result.reason_code)
END FUNCTION
```

경계값/완전성: OVERRIDE 목록이 비어 있어도(정의상 최소 1개, `IgnitionOverridePolicy`) 반복문이 그대로
0회 실행되고 BASE로 진행하므로 안전하다. `register_policy`가 한 번도 호출되지 않은 구성 오류(정책
0개)는 `result is None` 분기로 방어적으로 흡수한다(§10.4).

## 7. 정책 의사결정표

`algorithm-decision-guide.md` §2 완전성/일관성 규칙을 적용한다.

### 7.1 SWR-004 — DriverCommandPolicy 의사결정표 (3 side × 2 action × 2 사전상태 = 12케이스 + 예외입력 2행)

| # | side | action | 사전(left,right) | new_left | new_right | reason_code |
|---|---|---|---|---|---|---|
| 1 | left | lock | (LOCK, *) | LOCK | 불변(=사전 right) | NONE |
| 2 | left | lock | (RELEASE, *) | LOCK | 불변 | NONE |
| 3 | left | unlock | (LOCK, *) | RELEASE | 불변 | NONE |
| 4 | left | unlock | (RELEASE, *) | RELEASE | 불변 | NONE |
| 5 | right | lock | (*, LOCK) | 불변(=사전 left) | LOCK | NONE |
| 6 | right | lock | (*, RELEASE) | 불변 | LOCK | NONE |
| 7 | right | unlock | (*, LOCK) | 불변 | RELEASE | NONE |
| 8 | right | unlock | (*, RELEASE) | 불변 | RELEASE | NONE |
| 9 | all | lock | (LOCK, LOCK) | LOCK | LOCK | NONE |
| 10 | all | lock | (RELEASE, RELEASE) | LOCK | LOCK | NONE |
| 11 | all | unlock | (LOCK, LOCK) | RELEASE | RELEASE | NONE |
| 12 | all | unlock | (RELEASE, RELEASE) | RELEASE | RELEASE | NONE |
| 13 | (입력 없음, `cmd is None`) | — | (L,R) 임의 | 불변 | 불변 | NONE |
| 14 | (`Rejection`, SWR-001b) | — | (L,R) 임의 | 불변 | 불변 | INVALID_COMMAND |

`*`는 "선택되지 않은 출력이므로 결과에 영향 없음"을 의미하며, 행 1/3/5/7과 2/4/6/8을 사전상태
2가지(LOCK/RELEASE)로 나눠 12행을 정확히 채웠다(SWR-004 검증방안이 요구한 개수와 일치).

**완전성**: `side×action` 6개 조합 각각에 "선택 출력의 사전상태 2가지"를 곱해 12행 — `side`/`action`
정의역이 각각 3/2개뿐이므로 더 이상의 조합은 없다. 입력 자체가 없는 경우(13)와 거절된 경우(14)까지
포함해 `DriverCommandPolicy.evaluate`가 받을 수 있는 모든 `cmd` 종류(`ValidCommand`/`None`/`Rejection`)
를 남김없이 다룬다.

**일관성**: 각 행의 조건 조합(예: `side=left, action=lock, 사전left=LOCK`)은 정확히 하나의 결과에만
대응하며, 다른 행과 조건이 겹치지 않는다(사전상태 분기가 배타적).

**우선순위/충돌 해결**: 이 표 자체는 SWR-004 단독 표이므로 표 내부 충돌은 없다. SWR-004 대 SWR-020의
우선순위(§7.3)는 정책 카테고리(BASE vs OVERRIDE) 층위에서 별도로 해결한다.

### 7.2 SWR-020 — IgnitionOverridePolicy 의사결정표

| # | `classify_ignition(ignition_on)` | decision | lock_left | lock_right | reason_code | state_label |
|---|---|---|---|---|---|---|
| 1 | ON | PASS | (없음) | (없음) | (없음) | (없음) |
| 2 | OFF | OVERRIDE_FINAL | RELEASE | RELEASE | IGNITION_OFF | OFF |
| 3 | INVALID | OVERRIDE_FINAL | RELEASE | RELEASE | IGNITION_OFF | OFF |

**완전성**: `IgnitionState`는 `ON`/`OFF`/`INVALID` 3값 Enum이 정의역의 전부이므로 3행으로 완전하다.

**일관성**: `OFF`와 `INVALID`가 동일 결과를 내는 것은 SWR-020(b)의 명시적 요구("INVALID는 FALSE와
동일하게 처리")이며 서로 다른 두 행이 다른 결과를 요구하지 않는다.

### 7.3 SWR-PH1 §8 — SWR-020과 SWR-004의 상충 해소 (정책 카테고리 우선순위 표, IF-INT-008 실행 규약)

| 조건 | 우선순위 | 기대 동작 | 충돌 해결 규칙 |
|---|---|---|---|
| OVERRIDE 정책이 하나라도 `OVERRIDE_FINAL` 반환 | 최우선 | 해당 `PolicyResult`를 그대로 채택, 이후 모든 정책(다른 OVERRIDE 포함, 모든 BASE) 스킵 | asil_level 내림차순(ASIL_B 먼저) → priority 오름차순으로 먼저 도달한 `OVERRIDE_FINAL`을 채택(SWA §6.1) |
| 모든 OVERRIDE 정책이 `PASS` | 차순위 | BASE 정책(priority 오름차순)을 순서대로 실행, 마지막(또는 유일한) `PROPOSE` 결과를 채택 | Phase 1은 BASE 정책이 1개뿐이므로 실질적 충돌 없음. 향후 BASE 정책이 여러 개가 되면 "먼저 정의된 것이 우선"이 아니라 **priority 오름차순으로 마지막에 적용된 값이 최종**이 되도록 정의해야 하며, 이는 Phase 2/3 설계 확장 시 재확인 필요(이번 문서의 미해결 사항 아님 — Phase 1은 1개뿐이므로 발생하지 않음) |
| OVERRIDE 정책 실행 중 예외 발생 | 최우선(안전측) | 평가주기 실패 처리, 이전 확정 출력 유지(§10.4) | 예외는 "결과"가 아니므로 이 표의 다른 행과 경합하지 않는다 — §6.4에서 `fault` 분기로 즉시 분리 처리 |

이 표는 SWR-004(BASE)의 산출값이 SWR-020(OVERRIDE)의 산출값보다 절대 우선 적용되지 않음을 보장한다
(SWR-PH1 §8 인용 요건의 코드 수준 실행 규약).

## 8. 상태전이 상세

### 8.1 상태 저장 위치 요약

| 상태 | 저장 위치(UNIT) | 수명 | 초기값 |
|---|---|---|---|
| `lock_left`/`lock_right`(SW 요구사항 관점, `SWR-PH1_state-ignition.puml`) | UNIT-005(`LockStateStore`) | 프로세스 수명 동안 영속(평가주기 간 유지) | `RELEASE`/`RELEASE`(SWR-PH1 §8 가정3) |
| 이번 평가주기 staged 명령(아키텍처 관점) | UNIT-004(`CommandDispatcher`) | 1 평가주기(다음 `discard`까지) | `None` |
| ARC-002 실행 상태(`IDLE→...→OUTPUT_COMMIT`, `SWA-PH1_state-cycle.puml`) | UNIT-002 호출 스택의 지역 변수(영속 저장 없음 — §4 "매 주기 새로 계산") | 1 `evaluate()` 호출 동안만 | 없음(매 호출 새로 시작) |

### 8.2 SWR-020 상태전이 4케이스 (SWR-PH1 §4 검증방안, `SWR-PH1_state-ignition.puml`의 OFF↔ACTIVE 전이를 실행 수준으로 구체화)

| # | 시나리오 | 전이 | `LockStateStore` 변화 | 실행 근거 |
|---|---|---|---|---|
| 1 | TRUE→FALSE 진입 엣지(a) | `ACTIVE → OFF` | 이전 값(임의) → `(RELEASE, RELEASE)` | `UNIT-007.evaluate()`가 `OVERRIDE_FINAL`, `UNIT-002`가 즉시 `write(RELEASE, RELEASE)` |
| 2 | FALSE 지속(b) | `OFF → OFF`(자기 루프) | `(RELEASE, RELEASE)` 유지 — 매 주기 동일 값 재기록 | 매 주기 동일하게 1과 같은 경로 실행(멱등) — 이 주기에 staged된 `Driver_Command`는 `UNIT-002`가 BASE 단계 자체를 건너뛰므로 적용되지 않음(§6.4) |
| 3 | FALSE(또는 INVALID)→TRUE 재전환(c) | `OFF → ACTIVE`(→ 내부 `RELEASED`) | `(RELEASE, RELEASE)` 그대로 — **새로 강제하는 코드가 없어도 자연히 유지됨** | 케이스 2에서 매 주기 `(RELEASE,RELEASE)`가 계속 기록되어 있었으므로, 이번 주기 `UNIT-007`이 `PASS`를 반환해도 `UNIT-006`이 `read_current()`로 읽는 값이 이미 `(RELEASE,RELEASE)`이다 — **ARC-007이 과거 값을 기억할 필요가 없다는 SWA §4 "무상태" 주장이 이 케이스에서 실제로 성립함을 확인**(§6.3 설계 근거와 동일 논리, 상세설계 자체 검증 결과) |
| 4 | `ignition_on` 형식 오류(INVALID) | `ACTIVE → OFF`(1과 동일 경로) | `(RELEASE, RELEASE)` | `_classify_ignition(raw)`이 `INVALID`를 반환 → §7.2 행 3과 동일 처리 |

**가드**: 모든 전이의 가드는 `_classify_ignition(context.snapshot.ignition_on)`의 결과값이다(§6.3).
**타이머**: 없음(시간 기반 전이 없음, Phase 1 범위). **초기화**: 프로세스 시작 시 `LockStateStore`는
`(RELEASE, RELEASE)`로 생성되며 이는 SW 요구사항 상태 모델의 `OFF` 상태 가정과 일치한다(SWR-PH1 §8
가정3).

### 8.3 ARC-002 실행 상태 확장 — 실패 경로 추가 (SWA `SWA-PH1_state-cycle.puml` 확장, §10.4 결정 반영)

SWA 문서의 `EVALUATING{OVERRIDE_SCAN → BASE_EVAL} → OUTPUT_COMMIT` 구조에 실패 경로
`CYCLE_FAILED`를 추가한다(상태/전이 구조 자체는 변경하지 않고 새 종단 상태만 추가 — OCP 위반 아님).
다이어그램: `SWD-PH1_state-cycle-detail.puml`(신규).

- `OVERRIDE_SCAN --> CYCLE_FAILED` : 정책 `evaluate()` 호출이 예외를 던짐
- `BASE_EVAL --> CYCLE_FAILED` : 정책 `evaluate()` 호출이 예외를 던짐
- `CYCLE_FAILED --> IDLE` : `LockStateStore.write`/`ActuatorPort.apply`/`DisplayPort.show`를 호출하지
  않고, `CommandDispatcher.discard_current_cycle_command()`만 호출한 뒤 `IDLE`로 복귀(§10.4)
- 금지 전이(SWA 문서 승계): `BASE_EVAL`을 거친 뒤 다시 `OVERRIDE_SCAN`으로 돌아가는 전이는 여전히
  금지. `CYCLE_FAILED`에서 같은 주기 안에서 재시도하는 전이도 금지(재시도는 다음 평가주기부터 자연히
  이루어짐 — §10.4 복구 절 참고).

## 9. Web 및 API 상세

Phase 1은 HTTP/Web API가 없다(Web 시뮬레이터는 Phase 4, `ARC-201~205` 예정 — SWA 문서 §1.2). 이 장은
템플릿 취지에 맞춰 Phase 1이 실제로 갖는 "PC/SIL 테스트 벡터 API"(함수 호출 + `dict` 데이터 계약)를
문서화한다.

### 9.1 PC/SIL 테스트 벡터 계약

| 오퍼레이션 | 대응 함수 | 요청 구조(`dict`) | 필수 여부 | 검증 규칙 | 오류 시 동작 |
|---|---|---|---|---|---|
| Driver 명령 제출 | `FN-101 DriverCommandTestAdapter.submit` | `{"side": str, "action": str, "source": str}` | 세 키 모두 선택(누락 허용 — 누락 시 `None`으로 전달) | `FN-020`이 enum 소속 여부 검증(§6.1) | 누락/오타 → `Rejection(INVALID_COMMAND)`, 예외 없음 |
| Vehicle 스냅샷 제출 | `FN-102 VehicleSnapshotTestAdapter.submit` | `{"timestamp_s": float\|str, "ignition_on": bool}` | `ignition_on` 선택(누락 시 `None`→`INVALID` 처리), `timestamp_s` 선택(누락/형식오류 시 `0.0`, §10.2) | `FN-061`이 `ignition_on` 타입 판정 | 형식 오류 → `INVALID` 분류(SWR-020b), 예외 없음 |

### 9.2 응답/결과 구조

| 오퍼레이션 | 응답 타입 | 성공 시 | 실패(평가주기 실패) 시 |
|---|---|---|---|
| Vehicle 스냅샷 제출 | `EvaluationResult`(§4.5) | `status=COMMITTED`, `lock_left/right`, `state_label`, `reason_code` 모두 설정 | `status=FAILED`, `lock_left/right`(직전 값), `state_label=None`, `reason_code=None`, `error_detail` 설정 |

### 9.3 오류 코드

Phase 1은 HTTP 오류 코드 체계가 없으므로 `ReasonCode`(§4.1)와 `EvaluationResult.status`(§4.5)가 그
역할을 대신한다 — §10에서 전체 목록과 발생 조건을 정리한다.

### 9.4 인증/세션/보안 경계

해당 없음 — PC/SIL 함수 호출은 동일 프로세스 내 신뢰된 호출자(테스트 하네스)만 사용하며 인증/세션
개념이 없다(Phase 4 Web API 설계 시 별도로 정의 필요, 이번 문서 범위 아님).

## 10. 오류와 방어 동작

`error-handling-defensive-guide.md` §2 항목(검출/처리/전파차단/기록/복구)을 모두 채운다.

### 10.1 유효하지 않은 `Driver_Command` (SWR-001b)

| 항목 | 내용 |
|---|---|
| 검출 | `FN-020`에서 `Side/Action/Source` enum 변환 실패(`ValueError`) 또는 `raw`가 `DriverCommand`가 아님 |
| 처리 | 즉시 `Rejection(INVALID_COMMAND)` 값 반환(예외 아님) |
| 전파 차단 | `Rejection`은 값으로 `CommandDispatcher`에 staging되고, `DriverCommandPolicy`가 이를 읽어 출력 불변 + `reason_code=INVALID_COMMAND`로 변환(§7.1 행14) — 원시 오류가 호출 스택으로 전파되지 않음 |
| 기록 | Phase 1은 별도 이벤트 로그가 범위 밖(Phase 4, OEM-NFR-002)이므로, `DisplayOutputTestAdapter.show(reason_code=INVALID_COMMAND)` 호출 자체가 유일한 관측 지점이다. 개발 진단용으로 `FN-020` 내부에 `logging.DEBUG` 수준 기록을 권장(선택, §11) |
| 복구 | 다음 유효한 `Driver_Command`가 도착하면 자동 정상화(별도 리셋 불필요) |

### 10.2 방어적 완화가 필요한 경계 — 요구사항에 명시되지 않은 입력 이상

| 대상 | 이상 상황 | 결정(상세설계 재량) | 근거 |
|---|---|---|---|
| `CommandDispatcher.dispatch` | 같은 평가주기에 2회 이상 호출(SWR-PH1 가정2 위반) | 마지막 호출 값으로 덮어쓰고 `logging.WARNING`으로 위반 사실 기록. 예외를 던지거나 무시하지 않는다 | 가정2는 "설계상 발생하지 않는다"고만 되어 있어 방어 로직이 없으면 조용히 첫 값이 사라지는 결과가 되므로(오류 은폐 금지 원칙), 최소한의 기록은 남긴다 |
| `VehicleSnapshotTestAdapter.submit` | `timestamp_s` 누락/형식 오류 | `0.0`으로 대체하고 `logging.WARNING` 기록. 스냅샷 전체를 무효화하지 않는다 | SWR-PH1 §5는 "스냅샷 전체 무효화"를 가정으로 남겼으나, Phase 1의 어떤 정책도 `timestamp_s`를 판단 조건으로 사용하지 않는다(§6.2/§6.3에 `timestamp_s` 참조 없음) — 따라서 전체 무효화는 과잉 대응이며, Phase 2(`ARC-304` freshness guard)에서 `timestamp_s`가 실제로 의미를 가지면 이 결정을 재검토해야 한다(**확인 필요로 명시**) |
| `DriverCommandTestAdapter`/`VehicleSnapshotTestAdapter` | `raw_vector`가 `dict`가 아니거나 예상 키 자체가 없음 | `dict.get(key)`가 `None`을 반환하도록 방어(누락과 동일 취급) → 하류(`FN-020`/`_classify_ignition`)가 이미 `None`을 거절/`INVALID` 처리하므로 추가 분기 불필요 | 단일 지점(하류 검증기)에서 처리해 중복 검증 로직을 피함(응집도 유지) |
| `ActuatorOutputTestAdapter`/`DisplayOutputTestAdapter`의 `get_last_applied`/`get_last_shown` | IF-INT-003/004 원 계약에는 없는 조회 오퍼레이션 | **Test 어댑터 전용 확장**으로 명시 — 코어(`UNIT-002`)는 이 오퍼레이션을 호출하지 않으며, PC/SIL 시험 코드만 사용한다. 코어-어댑터 경계 계약(IF-INT-003/004)에는 영향 없음(§2 정합성 확인 결과와 일치, 새 공개 인터페이스 아님) | 시험 용이성(SWA §10) — Test 어댑터가 실제로 반영된 값을 시험 코드에 노출해야 자동 검증 가능 |

### 10.3 내부 신뢰 경계(프로그래밍 오류) — 예외로 즉시 실패

`LockStateStore.write`, `ActuatorOutputTestAdapter.apply`, `DisplayOutputTestAdapter.show`는 코어
내부(신뢰된 호출자, `UNIT-002` 단일 writer)에서만 호출되며 이미 검증된 강타입 Enum만 전달받는다.
이 경계를 넘는 타입 위반은 "외부 입력 오류"가 아니라 **프로그래밍 오류**로 분류하고, 조용히 무시하거나
값으로 변환하지 않고 `TypeError`를 즉시 발생시켜 개발/시험 단계에서 빠르게 발견되게 한다(Design by
Contract 원칙 — 사전조건 위반은 호출자 책임, `error-handling-defensive-guide.md` §3). 이 예외는
Phase 1 정상 동작 경로에서는 발생하지 않아야 하며, 발생한다면 단위시험 실패로 즉시 드러난다.

### 10.4 ARC-002 정책 실행 중 예외 처리 — 이번 상세설계에서 확정 (SWA §4/§6 위임 사항)

**결정**: `PolicyChainExecutor.evaluate()`는 정책(`IF-INT-008` 구현체)의 `evaluate()` 호출이 예외를
던지면 이를 **해당 평가주기 전체의 실패**로 처리하고, **이전 평가주기에 확정된 출력(액추에이터/표시)을
변경하지 않는다.** 이는 SWA 문서 §4가 이미 "가정"으로 적어 둔 방향과 SWR-020의 안전측 기본값 원칙(불확실한
상황에서 예측 불가능한 새 출력을 만들지 않는다)에 부합한다.

| 항목 | 내용 |
|---|---|
| 검출 | `policy.evaluate(context)` 호출을 개별적으로 `try/except Exception`으로 감싼다(`BaseException`은 잡지 않음 — `KeyboardInterrupt`/`SystemExit`은 정상 전파, §11 코딩 규칙). `OVERRIDE_SCAN`, `BASE_EVAL` 두 반복문 모두 동일하게 적용(§6.4 의사코드) |
| 처리 | 예외를 잡는 즉시 해당 평가주기의 나머지 정책 평가를 **모두 중단**한다(부분 평가 결과를 섞어 쓰지 않음 — all-or-nothing). `LockStateStore.write`, `ActuatorPort.apply`, `DisplayPort.show`는 **호출하지 않는다**(직전 확정값이 그대로 유지됨 — 각 어댑터가 마지막 호출값을 계속 반영하고 있으므로 "유지"를 위해 별도 재적용이 필요 없다) |
| 전파 차단 | `PolicyChainExecutor.evaluate()`는 예외를 다시 던지지 않고 `EvaluationResult(status=FAILED, ...)`를 **값으로 반환**한다(IF-INT-009 계약을 "예외 없음"으로 유지 — SWA §6.1 IF-INT-009 오류 계약과 일치하도록 이번 상세설계에서 확정) |
| 기록 | 표준 `logging` 모듈, 로거 이름 `vjecl.core.policy_chain`, 레벨 `ERROR`로 다음을 기록한다: 실패 시각(`snapshot.timestamp_s`), 실패 단계(`OVERRIDE_SCAN`/`BASE_EVAL`), 실패한 정책의 클래스명, 예외 타입과 메시지(`repr(exc)`). 이 로그는 진단 전용이며 OEM 인터페이스(`IF-INT-004` Display)로는 전달하지 않는다 — 새로운 `reason_code`/`state` 값을 OEM 표시 인터페이스에 도입하면 SWR-PH1 §6이 정의한 최소 열거형 집합을 넘어서는 결정이 되어 아키텍처/요구사항 문서 갱신이 필요해지므로(§2 정합성 원칙), 이번 상세설계는 그 확장을 임의로 하지 않고 내부 로그로만 처리한다. **Phase 4 관측성(OEM-NFR-002 이벤트 로그) 설계 시 이 로그를 노출 채널로 승격할지 재검토가 필요하다(확인 필요로 명시)** |
| 복구 | 별도 복구 절차가 필요 없다 — `PolicyChainExecutor`는 평가주기 간 상태를 보유하지 않으므로(§4 "매 주기 새로 계산") 다음 `evaluate()` 호출이 정상적으로 처음부터 다시 시도된다(자연 복구, 재시도 로직 불필요). 동일 원인이 매 주기 반복되면 출력은 마지막 성공 값에 고정된 채(fail-static) 유지되며, 이는 "알 수 없는 상태에서 새 출력을 추측하지 않는다"는 안전측 원칙과 일치한다 |
| `discard_current_cycle_command` 호출 여부 | **호출한다**(성공/실패 경로 공통). 이번 주기에 staged된 명령은 이미 이번 주기의 평가 시도에 "제출"되었으므로, 실패했다고 다음 주기로 이월시키면 평가되지 않은 채 나중에 뜻하지 않게 적용될 위험이 생긴다(`SWA-PH1_sequence-ignition-override.puml`이 override 케이스에서 명시적으로 `discard`를 호출하는 것과 동일한 논리를 실패 케이스로 일반화) |
| 안전망(defense in depth) | `LockStateStore`/`ActuatorPort`/`DisplayPort` 호출 자체가 예외를 던지는 것은 §10.3에 따라 설계상 발생하지 않아야 하지만, `PolicyChainExecutor.evaluate()` 전체를 한 겹 더 감싸는 최상위 `try/except Exception`을 두어 예기치 못한 예외도 동일하게 `FAILED`로 흡수한다(§6.4 의사코드에는 정책 호출부만 표기했으나, 구현 시 최상위 안전망을 추가로 둔다 — §11에 규칙화) |

**정책 예외가 계약 위반인 이유(기록)**: SWA 문서 §6.1 IF-INT-008 오류 계약은 "정책은 예외를 던지지
않고 반드시 `PolicyResult`를 반환해야 함"이라고 명시한다. 따라서 정책 구현체(`UNIT-006`/`UNIT-007`,
향후 `ARC-301~403`)가 예외를 던지는 것은 그 자체로 버그이며, `PolicyChainExecutor`의 위 처리는 "정상
동작의 일부"가 아니라 **호출자가 계약을 어겼을 때의 방어적 안전망**이다. §11 코딩 규칙에 "모든 정책
구현체의 `evaluate()`는 총함수(total function)로 작성하고 예외를 던지지 않는다"는 규칙을 명시해
이런 상황 자체가 실제로는 발생하지 않도록 예방한다(방어는 이중화하되, 예방이 우선).

## 11. 코딩 및 검증 규칙

### 11.1 코딩 표준

프로젝트에 지정된 Python 코딩 표준 문서는 현재 저장소에서 확인되지 않았다 — **사내/프로젝트 코딩
표준 확인 필요**(`unit-design-principles-checklist.md` §6). 확인 전까지 다음을 잠정 기준으로 적용한다.

- PEP 8 스타일, 모든 공개 함수/메서드에 타입 힌트 필수(`mypy --strict` 통과 목표, 도구 지정 확인 필요)
- 값 객체는 `@dataclass(frozen=True)`로 불변 선언(§4)
- 함수 하나의 순환복잡도 10 이하(도구/기준 확인 필요, 잠정치) — `FN-010`(evaluate)처럼 분기가 많은
  함수는 §6.4 의사코드 수준의 복잡도를 넘지 않도록 헬퍼(`_handle_cycle_failure` 등)로 분리
- 함수 길이 50줄 이하 권장(잠정 기준)
- `except:`(bare except) 금지 — 항상 `except Exception`(또는 더 구체적인 타입) 사용, `BaseException`을
  잡지 않음(§10.4)
- `print()` 금지, `logging` 모듈만 사용(§10.4)
- `eval`/`exec`/동적 import 금지
- 정책 구현체(`PolicyPort` 구현)의 `evaluate()`는 반드시 총함수(모든 입력에 대해 예외 없이
  `PolicyResult` 반환)로 작성 — 코드 리뷰 체크리스트 항목으로 고정(§10.4)
- **SWR-002 정적 점검**: `CommandDispatcher`/`CommandValidator` 구현에 `source`/`Source` 값을 참조하는
  조건문(`if`, `match`)이 존재하지 않는지 코드 리뷰에서 확인(§5.2 근거)

### 11.2 ISO 26262 Part 6 단위 설계 원칙 반영 (요약 — 원문 대조 필요)

| 원칙 | Phase 1 코어 적용 |
|---|---|
| 단일 진입/종료점 | Python은 `goto` 없음 — 각 함수는 하나의 논리적 목적만 가지며 조기 `return`은 총함수 분기당 최대 1회로 제한(가독성 확인, 강제 도구 없음) |
| 포인터 사용 제한 | 해당 없음(Python은 포인터 없음) |
| 동적 메모리 할당 제한 | Python은 GC 관리 — `LockStateStore`/`CommandDispatcher`는 고정 크기 필드만 보유(무한 증가 컬렉션 없음)로 설계해 위험을 최소화 |
| 재귀 사용 제한 | 이번 설계에는 재귀 함수가 없다(모든 반복은 유한 리스트에 대한 `for`) |
| 인터럽트 사용 제한 | 해당 없음(단일 스레드 순차 실행, SWA §3.2/§13 가정) |
| 암묵적 형변환 회피 | Enum 강타입 사용(§4), `object` 타입은 검증 전 경계에서만 의도적으로 사용하고 검증 후에는 즉시 강타입으로 변환(§6.1) |
| Dead code 금지 | §6.4 의사코드의 모든 분기가 §7 의사결정표의 행과 1:1 대응 — 도달 불가능한 분기 없음 |

정확한 절/표 번호와 원문은 `iso26262-aspice-detailed-design-checklist.md`의 안내에 따라 공식 표준
문서로 별도 확인이 필요하며, 이 표는 그 요약을 단정적으로 인용하지 않는다.

### 11.3 정적분석·단위검증·커버리지·리뷰 기준

- 정적분석 도구(예: `mypy`, `pylint`/`flake8`, `bandit`): 프로젝트 CI 설정 미확인 — **확인 필요**로
  표시하고, 최소한 `mypy --strict`와 `python -m py_compile`을 로컬 확인 기준으로 잠정 채택한다.
- 단위검증(SWE.4, 별도 `TPL-SWE4-*` 산출물): 이 문서는 그 산출물이 참조할 `UNIT-XXX`/`FN-XXX` ID를
  §2/§5에 명확히 남겼다. §7의 의사결정표(12+2행, 3행)와 §8.2의 4케이스는 단위/통합시험 케이스 설계의
  1차 근거로 사용되어야 한다(완전성이 이미 확인된 표이므로 커버리지 목표: 각 행당 최소 1개 시험 케이스).
- 커버리지 목표: 정책·검증기 함수는 분기(branch) 커버리지 100%를 목표로 한다(작은 순수 함수이므로
  달성 가능, `tdd` 스킬 단계에서 실측).
- 코드 리뷰 체크리스트: §11.1의 정적 규칙 + §2 정합성(새 공개 인터페이스 추가 여부) + §10.4 예외 흡수
  로직이 실제로 "부분 커밋"을 만들지 않는지(all-or-nothing) 확인.

## 12. 단위와 요구사항 할당

| SWR ID | ARC | UNIT | 핵심 FN | 의사결정표/알고리즘 | 단위시험 참조점(예정) |
|---|---|---|---|---|---|
| SWR-001 | ARC-003 | UNIT-003 | FN-020 | §6.1(의사코드) | `FN-020` 입력 파티션(유효 12조합 + 결측/형식/미등록 각 1건 이상) |
| SWR-002 | ARC-004 | UNIT-004 | FN-030/031/032 | §5.2 정적 근거 | source 4종 동등성 회귀 비교 |
| SWR-004 | ARC-006 | UNIT-006 | FN-050 | §7.1(12+2행) | §7.1 각 행 1케이스 이상(14케이스) |
| SWR-020 | ARC-007 | UNIT-007 | FN-060/061 | §7.2(3행), §8.2(4케이스) | §8.2 4케이스 + §7.2 3행 |
| (인프라) | ARC-001 | UNIT-001 | FN-001/002 | §5.7 | 위임 호출 확인(통합시험 수준) |
| (인프라) | ARC-002 | UNIT-002, UNIT-008 | FN-010/011 | §6.4, §7.3, §10.4 | 정상/override/예외 3경로 |
| (인프라) | ARC-005 | UNIT-005 | FN-040/041 | §5.3 | read/write 왕복, 타입 위반 시 `TypeError` |
| (인프라) | ARC-101~105 | UNIT-101~105 | FN-101~105 | §9.1 | 변환 정확성(§SWA §11 6단계) |

**할당 누락 점검**: SWR-001/002/004/020 모두 정확히 1개의 UNIT/FN 세트에 할당됨(SWA 문서 §12와 동일한
1:1 대응 유지, 중복 없음). 인프라 UNIT(UNIT-000/001/002/005/008/101~105)은 SWA 문서 §12가 이미 제시한
"근거 없는 요소 아닌 이유"(SWR-PH1 §8 상충 해소 인프라, OEM-IF 경계 실현)를 그대로 승계한다 — 고아
UNIT 없음.

## 13. 구현 경계

- **생성 코드**: 없음(코드 생성기 미사용).
- **외부 라이브러리**: Phase 1 **프로덕션 코드**는 Python 3.12 표준 라이브러리만 사용한다
  (`dataclasses`, `enum`, `typing`, `logging`) — 외부 패키지 의존 없음. 따라서 이번 상세설계 시점에는
  `TPL-SBOM-001` 작성 대상 항목이 없다. 다만 **단위/통합시험 코드**(`tdd`/`integration-testing` 스킬
  범위)가 `pytest` 등 외부 패키지를 사용하기로 하면, 그 시점에 `WP_Templates/Engineering/
  SoftwareDetailedDesignAndUnitConstruction/TPL-SBOM-001_Python 의존성 SBOM FOSS 라이선스 목록
  템플릿.xlsx`에 패키지·버전·SPDX 라이선스를 기록해야 한다(SWE.3/SUP.8) — **이 문서는 SBOM을 채우지
  않으며, 실제 채우기는 구현 단계의 별도 작업으로 안내한다.**
- **플랫폼 종속부**: 없음 — 코어(UNIT-000~008)는 순수 Python 로직이며 OS/HW 의존이 없다(SWA §13과
  일치). PC/SIL 어댑터(UNIT-101~105)도 파일/네트워크 I/O 없이 함수 호출·`dict`만 사용한다(테스트
  벡터를 파일에서 읽는 책임은 `tests/system/`의 시험 코드 쪽에 있으며 UNIT-101/102 자체는 이미 파싱된
  `dict`를 받는다고 가정한다 — 이 경계는 §9.1에서 확정).
- **구현하지 않는 범위**: `ARC-201~205`(Phase4 Web 어댑터), `ARC-301~403`(Phase2/3 정책)의 실제 코드,
  drawio 최종본(§0), HTTP/Web API(§9).
- **소스 배치(확정)**: §2.1 표의 소스 위치 열이 이번 상세설계의 확정 결과다(SWA §13 "상세설계에서
  확정" 위임 이행) — `src/core/`(UNIT-000~008), `src/core/policies/`(UNIT-006/007),
  `src/adapters/pcsil/`(UNIT-101~105).

## 14. 추적성

- 단일 진실 공급원: `docs/Traceability/traceability-matrix.md` — 이번 작업에서 SWR-001/002/004/020
  행의 "설계 요소" 열 아래에 `UNIT-XXX`/`FN-XXX` 연결을 추가했다(같은 작업 안에서 갱신, 실제 편집은
  아래 커밋 대상 파일 참고).
- 다이어그램 동기화: `SWD-PH1_class.puml`, `SWD-PH1_sequence-policy-fault.puml`,
  `SWD-PH1_state-cycle-detail.puml`(모두 신규)의 UNIT/FN ID가 본 문서 §2~§10과 일치함을 확인했다.
  SWA 문서의 `SWA-PH1_component.puml`/`SWA-PH1_sequence-*.puml`/`SWA-PH1_state-cycle.puml`과 ARC ID·
  인터페이스 ID가 일치함도 재확인했다(§3.2).
- 하향 링크(단위시험 케이스 ID)는 이 시점(G2 후반, 상세설계 완료)에는 아직 존재하지 않으며, SWE.4
  단위시험 산출물 완료 시 매트릭스에 추가해야 한다 — 고아 요구사항이 아니라 게이트 진행에 따른 예정된
  공백이다(SWR-PH1/SWA-PH1 문서와 동일한 관례).

## 15. 참고자료

| 자료 | 식별정보/버전 | 적용 범위 |
|---|---|---|
| SW 아키텍처 설계서 | `docs/SoftwareArchitecturalDesign/SWA-PH1_SW 아키텍처 설계서.md`, v0.1 | 근거 아키텍처 전문, ARC-001~007/101~105, IF-INT-001~009, 상세설계 위임 사항(§4/§6) |
| SW 요구사항 명세서 | `docs/SoftwareRequirementsAnalysis/SWR-PH1_SW 요구사항 명세서.md`, v0.1 | SWR-001/002/004/020 전문, §8 상충 해소·가정 |
| 회사 지정 템플릿 | `WP_Templates/Engineering/SoftwareDetailedDesignAndUnitConstruction/TPL-SWE3-001_SW 상세설계서 템플릿.docx`, `TPL-SWE3-002_상세설계 UML 및 호출관계 템플릿.drawio` | 본 문서의 장/절 구조 근거(§0 비고 — drawio 이전은 별도 작업) |
| 상세설계 스킬 | `.claude/skills/detailed-design/SKILL.md` 및 `references/*` | 함수 계약·알고리즘/의사결정표·오류방어·단위설계원칙 가이드 |
| 추적성 매트릭스 | `docs/Traceability/traceability-matrix.md` | SWR ↔ ARC ↔ UNIT/FN 연결(§14에서 갱신) |
| ISO 26262 Part 6 | 프로젝트 첨부 원문 없음 — 조항 인용 필요 시 공식 표준 문서 별도 확인 필요 | 단위 설계 원칙(§11.2) |
| A-SPICE v4.1 (SWE.3) | 프로젝트 첨부 원문 없음 — `.claude/skills/aspice-auditor/references/aspice-source.md` 및 공식 문서 확인 필요 | 상세설계 프로세스 정합성 |
| VJ-ECL-2026 프로젝트 정책 | `VJ-ECL-2026/CLAUDE.md`, 저장소 루트 `CLAUDE.md` | 실행 환경(Python 3.12), 산출물 위치, 개발 생명주기 |
