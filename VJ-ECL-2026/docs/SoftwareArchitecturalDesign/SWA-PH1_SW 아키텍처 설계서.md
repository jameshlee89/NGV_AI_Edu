> **비고(도구 제약)**: 회사 지정 템플릿 `WP_Templates/Engineering/SoftwareArchitecturalDesign/
> TPL-SWE2-001_SW 아키텍처 설계서 템플릿.docx`가 이미 저장소에 존재하여, 이 문서는 그 템플릿의 장/절
> 구조(표지 → 문서 통제 → 목차 → 1~15장)를 그대로 옮겨 작성했다. 다만 현재 세션 환경에는 `.docx`를
> 직접 생성/수정할 도구(Node.js+`docx` 패키지, LibreOffice, pandoc 등)가 설치되어 있지 않아 `.docx`
> 파일 자체를 채우지 못하고, `SWR-PH1_SW 요구사항 명세서.md`와 동일한 방식으로 Markdown으로 작성했다.
> **docx 템플릿 직접 채우기는 별도 도구 필요** — 도구가 준비되면 이 내용을 `TPL-SWE2-001` 사본에 그대로
> 옮겨 `.docx`로 재발행해야 한다. UML 다이어그램도 같은 이유로 `TPL-SWE2-002` drawio가 아니라
> PlantUML(`.puml`)로만 작성했다(§9 다이어그램 목록 참고) — drawio 이전은 별도 작업으로 남긴다.

# TPL-SWE2-001_SW 아키텍처 설계서 템플릿 기반 — SWA-PH1_SW 아키텍처 설계서

| 항목 | 내용 |
|---|---|
| 템플릿 ID | TPL-SWE2-001 |
| 적용 프로세스 | SWE.2 |
| 프로젝트 | VJ-ECL-2026 (가상 OEM-A 전자식 후석 좌/우 차일드락 제어 SW) |
| 작성 문서 ID와 명칭 | SWA-PH1_SW 아키텍처 설계서 |
| 버전 및 베이스라인 | v0.1 (초안) / 목표 베이스라인 BL-SWA-1.0 (승인 시 확정, G2 게이트) |
| 작성자와 검토자 | 작성자: 아키텍처 설계 에이전트(architecture-design 스킬, 세션 실행자 jaehwan2.lee@hlcompany.com) / 검토자 겸 승인자: jaehwan2.lee@hlcompany.com (사용자 본인, 지정 예정) |

본 자료는 SW 품질교육을 위한 교육용 샘플이며, 저작권은 Synetics에 있습니다. 교육 과정 안에서 열람,
복제 및 실습 사용을 허용합니다. 과정 밖 배포, 공개 또는 상업적 이용은 Synetics의 사전 서면 승인을
받아야 합니다. © 2026 Synetics. All rights reserved.

## 문서 통제

### 변경 이력

| Revision | 변경일 | 작성 역할 | 변경 내용 | 검토 상태 |
|---|---|---|---|---|
| v0.1 | 2026-09-18 | 아키텍처 설계 에이전트 | Phase 1 최초 작성. 헥사고날/포트-어댑터 + 코어 내부 정책 체인 스타일로 SWR-001/002/004/020 아키텍처 요소·인터페이스·통합 순서 정의 | 초안 |

### 작성 검토 승인 상태

| 구분 | 역할 또는 성명 | 상태 | 일자 | 증거 위치 |
|---|---|---|---|---|
| 작성 | 아키텍처 설계 에이전트 | 완료 | 2026-09-18 | 본 문서 |
| 후보 스타일 제안·사용자 선정 | jaehwan2.lee@hlcompany.com (사용자 본인) | 완료 (헥사고날+정책체인 조합 채택) | 2026-09-18 | 대화 이력 |
| 검토 | jaehwan2.lee@hlcompany.com (사용자 본인) | 대기 | - | - |
| 승인 | jaehwan2.lee@hlcompany.com (사용자 본인) | 대기 | - | - |

## 목차

1. 목적 및 적용범위
2. 아키텍처 설계 원칙
3. 논리 아키텍처
4. 컴포넌트 책임
5. 정적 의존성
6. 인터페이스 명세
7. 동적 동작
8. 상태 전이
9. 오류 격리와 안전 동작
10. 품질속성 분석
11. 통합 전략
12. 요구사항 할당
13. 자원 및 배포 경계
14. 추적성
15. 참고자료

---

## 1. 목적 및 적용범위

### 1.1 목적

이 문서는 `SWR-PH1_SW 요구사항 명세서.md`(v0.1, BL-SWR-1.0 목표)의 SWR-001·SWR-002·SWR-004·SWR-020을
근거로, VJ-ECL-2026의 SW 아키텍처(SWE.2, G2)를 정의한다. CLAUDE.md의 프로젝트 진행 방식에 따라
"아키텍처는 Phase 1에서 전체 시스템 구조를 확정하고, 이후 Phase는 그 구조를 확장만 한다"는 원칙을
지키기 위해, 이 문서는 Phase 1 범위를 실제로 채우는 동시에 Phase 2/3/4가 컴포넌트 재작성 없이 끼어들
수 있는 확장점을 명시적으로 설계한다. 이 문서는 상세설계(SWE.3, G2 후반)와 통합시험(SWE.4/5, G3)의
근거로 사용된다.

### 1.2 적용범위

- 대상 제품: VJ-ECL-2026 전자식 후석 좌/우 차일드락 제어 SW 전체 논리 아키텍처
- 대상 생명주기 단계: 아키텍처 설계(SWE.2), Phase 1(브랜치 `feature/phase1-core-manual-control`)
- 실행/검증 환경: Python 3.12, PC/SIL 자동시험(현재 구현) + Web 시뮬레이터(Phase 4 구현 예정, 이번
  문서에서는 포트만 확보)
- 이번 문서가 실제로 채우는 요구사항: SWR-001, SWR-002, SWR-004, SWR-020 (모두 QM)
- 이번 문서가 구조만 남겨두는(구현하지 않는) 향후 확장: Phase 2(OEM-SR-001~004, ASIL B — crash 긴급
  해제, 후측방 접근위험 override, 입력 freshness/DEGRADED, sensor_fault 직전 출력 유지), Phase 3(차속
  자동잠금, 화재/과온/성인탑승 강제해제, ISOFIX 강제잠금), Phase 4(상태조회 API, 결정론적 재현, 이벤트
  로그, Web 시뮬레이터)

### 1.3 적용 경계

- **포함**: SWR-001/002/004/020의 아키텍처 요소 분해, 내부/외부 인터페이스 명세, Phase 1 컴포넌트
  통합 순서, Phase 2/3 정책·어댑터가 삽입될 확장점의 인터페이스 계약.
- **제외**: Phase 2/3/4 정책·어댑터의 실제 내부 알고리즘 설계(각 Phase의 SWE.2/SWE.3에서 별도 수행),
  상세설계 수준의 함수/자료형 정의(SWE.3, `detailed-design` 스킬 범위), drawio 최종본 이전(§0 비고
  참고), ISO 26262 Part 3 HARA·공식 인증(VJ-ECL-2026 CLAUDE.md 명시 범위 밖).
- **경계**: 상위 시스템 아키텍처 문서는 존재하지 않음(OEM 문서가 사실상 최상위 입력) — 이 문서가
  VJ-ECL-2026 SW의 최상위 아키텍처 산출물이다.

## 2. 아키텍처 설계 원칙

이 문서는 `architecture-design` 스킬 §3과 `references/solid-cohesion-coupling-checklist.md`,
`references/iso26262-aspice-architecture-checklist.md`(요약, 원문 대조 필요 항목 포함)의 원칙을
다음과 같이 적용했다.

- **분해**: 시스템을 "구동 어댑터(입력) — 코어(결정 로직) — 피구동 어댑터(출력)"의 헥사고날 3영역으로
  1차 분해하고, 코어 내부는 다시 "명령 검증/전달(SWR-001/002) — 상태 저장(공유) — 정책(SWR-004/020,
  그리고 향후 확장) — 정책 실행/조정"으로 2차 분해했다(§3.1).
- **높은 응집도**: 각 컴포넌트는 SWR 단위(또는 명확한 인프라 역할) 하나씩만 책임진다 — 예)
  CommandValidator는 "유효성 판정"만, DriverCommandPolicy는 "side 선택 출력 계산"만 담당하고 검증/
  전달/저장 책임을 갖지 않는다(§4).
- **낮은 결합도**: 어댑터-코어 경계, 코어 내부 컴포넌트 경계 모두 명명된 인터페이스(IF-INT-XXX)로만
  연결했다 — 직접 참조/직접 임포트로 컴포넌트를 연결하지 않는다(§6). LockStateStore는 단일 writer
  원칙으로 암묵적 공유 상태 문제를 제거했다.
- **변경 유연성(OCP)**: 우선순위 중재가 필요한 지점(Phase 2/3의 override 규칙)을 "출력 정책 포트
  (IF-INT-008)"라는 단일 확장점으로 격리했다. 새 정책은 이 포트의 새 구현체를 추가하는 것으로
  대응하며, 기존 컴포넌트(ARC-001~007)는 코드 수정이 필요 없다(§3.2, §6, §9).
- **SOLID**: §5(정적 의존성)와 §6(인터페이스 명세)에서 컴포넌트별로 SRP/OCP/LSP/ISP/DIP 적용 근거를
  명시한다.
- **오류 격리**: 입력 유효성 판정(SWR-001)과 ignition 유효성 판정(SWR-020b)을 코어 진입 지점에
  배치해, 잘못된 입력이 정책/상태 컴포넌트까지 전파되지 않도록 했다(§9).
- ISO 26262 Part 6·A-SPICE SWE.2의 정확한 절 번호·원문은 이 문서에서 단정하지 않았으며, 필요 시
  `.claude/skills/architecture-design/references/iso26262-aspice-architecture-checklist.md`와 공식
  표준 문서를 함께 확인해야 한다.

## 3. 논리 아키텍처

### 3.1 아키텍처 요소

선정된 스타일: **헥사고날/포트-어댑터를 뼈대**로 하고, 코어 내부의 "출력 확정" 로직을
**마이크로커널/플러그인식 우선순위 정책 체인**으로 구성한 조합(2026-09-18 사용자 확정). 상세 구조는
`SWA-PH1_component.puml` 참고.

#### 코어 (Core Domain) — Phase 1 구현

| ID | 명칭 | 목적/책임 | 할당 요구사항 |
|---|---|---|---|
| ARC-001 | EvaluationCycleFacade | 구동 어댑터에 노출되는 단일 안정 진입점. Driver 명령 제출을 CommandDispatcher에 위임하고, Vehicle 스냅샷 제출 시 PolicyChainExecutor의 평가를 트리거한다. | 없음(오케스트레이션 인프라, §12 근거 참고) |
| ARC-002 | PolicyChainExecutor | 등록된 정책(IF-INT-008 구현체)을 ASIL 등급·우선순위 순으로 실행하고, OVERRIDE_FINAL 발생 시 이후 정책을 건너뛰는 계약을 구현. 최종값을 LockStateStore에 기록하고 출력 포트를 호출하는 유일한 컴포넌트(단일 writer). | 없음(중재 계약 실행 인프라 — SWR-PH1 §8 "SWR-020이 SWR-002/004보다 항상 우선"의 실행 근거, §12 참고) |
| ARC-003 | CommandValidator | `Driver_Command(side, action, source)`의 필드 존재·enum 소속 여부만 판정 | SWR-001 |
| ARC-004 | CommandDispatcher | 검증 결과(유효/거절)를 이번 평가주기 동안 보관하고, source 값과 무관하게 동일한 방식으로 BASE 정책에 전달(소스 차별 없음을 컴포넌트 계약으로 보장) | SWR-002 |
| ARC-005 | LockStateStore | `lock_left`/`lock_right`의 직전 평가주기 값을 보관하고 read/write 인터페이스만 노출 | 없음(SWR-004/SWR-020의 "유지" 요건을 위한 공유 상태 컴포넌트 — §12 근거) |
| ARC-006 | DriverCommandPolicy | 유효 명령의 `side`에 따라 `lock_left`/`lock_right` 중 선택된 출력만 갱신하고 나머지는 LockStateStore 값을 유지 (BASE 정책) | SWR-004 |
| ARC-007 | IgnitionOverridePolicy | `ignition_on`이 FALSE/INVALID이면 강제 RELEASE·OFF 확정 및 이후 정책 스킵, TRUE 재전환 직후에도 RELEASE 유지 (OVERRIDE 정책, QM) | SWR-020 |

#### 구동 어댑터 (Driving Adapters)

| ID | 명칭 | 목적/책임 | 상태 |
|---|---|---|---|
| ARC-101 | DriverCommandTestAdapter | OEM-IF-004 경계에서 PC/SIL 테스트 벡터를 `Driver_Command`로 변환해 IF-INT-001 호출 | Phase 1 구현 |
| ARC-102 | VehicleSnapshotTestAdapter | OEM-IF-009(부분) 경계에서 PC/SIL 테스트 벡터를 `VehicleSnapshot`으로 변환해 IF-INT-002 호출 | Phase 1 구현 |
| ARC-105 | PcSilHarnessEntryPoint | PC/SIL 자동시험 진입점 — ARC-101/102/103/104를 조립하고 평가주기 루프를 구동 | Phase 1 구현 |
| ARC-201 | DriverCommandWebAdapter | Web 시뮬레이터 UI 이벤트를 `Driver_Command`로 변환해 IF-INT-001 호출 | Phase 4 예정(포트만 확보) |
| ARC-202 | VehicleSnapshotWebAdapter | Web 시뮬레이터 UI 상태를 `VehicleSnapshot`으로 변환해 IF-INT-002 호출 | Phase 4 예정(포트만 확보) |
| ARC-205 | WebSimulatorEntryPoint | Web 시뮬레이터 진입점 — ARC-201/202/203/204를 조립 | Phase 4 예정(포트만 확보) |

#### 피구동 어댑터 (Driven Adapters)

| ID | 명칭 | 목적/책임 | 상태 |
|---|---|---|---|
| ARC-103 | ActuatorOutputTestAdapter | IF-INT-003 구현 — 논리 `lock_left`/`lock_right`을 OEM-IF-005 형식으로 반영(PC/SIL 논리 출력) | Phase 1 구현 |
| ARC-104 | DisplayOutputTestAdapter | IF-INT-004 구현 — `state`/`reason_code`를 OEM-IF-006(부분) 형식으로 반영 | Phase 1 구현 |
| ARC-203 | ActuatorOutputWebAdapter | IF-INT-003 구현체(Web 화면 반영) | Phase 4 예정(포트만 확보) |
| ARC-204 | DisplayOutputWebAdapter | IF-INT-004 구현체(Web 화면 반영) | Phase 4 예정(포트만 확보) |

#### 코어 — Phase 2/3 확장 예정 (IF-INT-008 구현체 추가만 필요, 포트/기존 컴포넌트 변경 없음)

| ID | 명칭 | category/asil (예정) | 대응 요구사항(예정) |
|---|---|---|---|
| ARC-301 | CrashOverridePolicy | OVERRIDE / ASIL B | OEM-SR-001~004 중 충돌 긴급해제 |
| ARC-302 | RearProximityOverridePolicy | OVERRIDE / ASIL B | 후측방 접근위험 잠금 + 10초 재입력 override |
| ARC-303 | SensorFaultHoldPolicy | OVERRIDE / ASIL B | sensor_fault 시 직전 출력 유지 |
| ARC-304 | InputFreshnessGuard | 별도 계층(§3.2 참고) / ASIL B | 입력 freshness 검사·DEGRADED 전이 |
| ARC-401 | VehicleSpeedAutoLockPolicy | OVERRIDE 또는 BASE(예정 확정 필요) / QM 추정 | 차속 임계값 자동잠금 |
| ARC-402 | FireOverheatOccupantOverridePolicy | OVERRIDE / 등급 미정 | 화재/과온/성인탑승 강제해제 |
| ARC-403 | IsofixLockPolicy | OVERRIDE / 등급 미정 | ISOFIX 강제잠금 |

이 표의 Phase 2/3 항목은 **이번 문서에서 확정하지 않는다** — 해당 Phase의 SWE.1/SWE.2에서 실제 우선
순위·ASIL 등급·category를 확정해야 한다. 이 문서는 "IF-INT-008을 구현하는 새 컴포넌트로 추가된다"는
삽입 지점만 보장한다.

### 3.2 관계와 제약

- **허용된 의존 방향**: 구동 어댑터 → 코어(IF-INT-001/002) → 피구동 어댑터(IF-INT-003/004, 코어가
  호출). 코어 내부는 ARC-001 → {ARC-004, ARC-002} → {ARC-003, ARC-005, IF-INT-008 구현체}. 역방향
  의존(예: ARC-005가 ARC-002를 호출)은 금지.
- **금지된 결합**: 어댑터 간 직접 참조 금지(예: ARC-101이 ARC-103을 직접 호출 금지 — 반드시 코어를
  경유). 정책(ARC-006/007 및 향후 정책) 간 직접 참조 금지 — 정책은 서로를 모르며 ARC-002만 이들을
  호출한다(정책 간 결합도 0).
- **공유 자원**: LockStateStore(ARC-005)가 유일한 공유 가변 상태이며, IF-INT-007로만 접근한다. 단일
  writer(ARC-002)만 write하고 나머지는 read-only — 동기화 규칙: 평가주기는 순차 실행(동시성 없음)이
  전제이므로 락(lock) 메커니즘은 아키텍처 수준에서 필요하지 않다(가정, §10/§13에서 재확인).
  스레드/프로세스 병행 실행이 도입되면 이 가정을 재검토해야 한다.
- **ARC-304(InputFreshnessGuard, Phase 2)의 위치에 대한 설계 여지**: 이 컴포넌트는 "정책"이라기보다
  입력 자체의 신선도를 판정하는 게이트에 가깝다 — IF-INT-008 정책 포트의 구현체로 넣을지, 아니면
  ARC-001/ARC-002 사이의 별도 게이트 인터페이스(신규 IF-INT-0xx)로 넣을지는 Phase 2 아키텍처 확장
  작업에서 결정해야 한다(이번 문서는 두 가지 다 가능하도록 ARC-002의 평가 절차를 "정책 스캔 이전에
  게이트 단계를 둘 수 있다"는 여지로 §7/§8에 남겨둔다 — 확정하지 않음, 미해결 사항으로 §14/보고에 기록).
- **순환 의존 점검**: 아래 §5 정적 의존성 그래프에 순환이 없음을 확인했다(위상 정렬 가능 — §11 통합
  순서로 실증).

## 4. 컴포넌트 책임

각 컴포넌트의 입력/출력/상태/오류 처리를 정리한다. (요구사항 할당은 §12에서 종합)

| ID | 입력 | 출력 | 내부 상태 보유 | 오류 처리 |
|---|---|---|---|---|
| ARC-001 | raw driver command, VehicleSnapshot | Dispatcher 위임 결과, EvaluationResult | 없음(무상태 위임) | 없음(하위로 전파) |
| ARC-002 | VehicleSnapshot, staged command 존재 여부 | 최종 lock_left/right, state, reason_code | 없음(매 주기 새로 계산, LockStateStore가 유일한 영속 상태) | 정책이 예외를 던지면 평가주기 전체를 실패로 처리하고 이전 상태를 변경하지 않음(가정 — 상세설계에서 확정) |
| ARC-003 | raw Driver_Command | ValidCommand 또는 Rejection(reason_code=INVALID_COMMAND) | 없음 | 필드 누락/형식 오류/미등록 enum → Rejection 반환(예외 던지지 않음) |
| ARC-004 | ValidCommand/Rejection(ARC-003 결과) | get_current_cycle_command() 조회 결과 | 이번 평가주기 동안만 유지되는 1건(가정: 평가주기당 최대 1건, SWR-PH1 가정2) | 다음 평가주기 시작 시 이전 staged 값 폐기 |
| ARC-005 | write(left, right) | read_current() -> {left, right} | 직전 평가주기 값(영속, 초기값 RELEASE/RELEASE) | 없음(단순 저장) |
| ARC-006 | ARC-004의 ValidCommand, ARC-005의 현재값 | PolicyResult(PROPOSE, 선택 출력만 갱신) | 없음 | Rejection인 경우 값 불변 + reason_code=INVALID_COMMAND로 PROPOSE |
| ARC-007 | VehicleSnapshot.ignition_on, ARC-005의 현재값 | PolicyResult(OVERRIDE_FINAL 또는 PASS) | 없음(무상태 — 매 주기 ignition_on만으로 판정, SWR-020 세 조건 모두 현재 입력값 기반) | ignition_on 형식 오류 → INVALID로 취급, FALSE와 동일 처리 |

## 5. 정적 의존성

```
ARC-005 (LockStateStore)         : 의존 없음 (leaf)
ARC-003 (CommandValidator)       : 의존 없음 (leaf)
ARC-103 (ActuatorOutputTestAdapter) : 의존 없음 (leaf, IF-INT-003 구현)
ARC-104 (DisplayOutputTestAdapter)  : 의존 없음 (leaf, IF-INT-004 구현)

ARC-004 (CommandDispatcher)      -> ARC-003 (IF-INT-005)
ARC-007 (IgnitionOverridePolicy) -> ARC-005 (IF-INT-007, read)
ARC-006 (DriverCommandPolicy)    -> ARC-004 (IF-INT-006), ARC-005 (IF-INT-007, read)

ARC-002 (PolicyChainExecutor)    -> ARC-006, ARC-007 (IF-INT-008)
                                  -> ARC-005 (IF-INT-007, write)
                                  -> ARC-103, ARC-104 (IF-INT-003/004, 구성 시점에 주입)

ARC-001 (EvaluationCycleFacade)  -> ARC-004 (IF-INT-006 위임), ARC-002 (IF-INT-009)

ARC-101, ARC-102                 -> ARC-001 (IF-INT-001/002)
ARC-105                          -> ARC-101, ARC-102, ARC-103, ARC-104 (조립, 실행 시 주입)
```

**순환 의존 없음**: 위 그래프는 leaf(ARC-003/005/103/104)에서 시작해 ARC-105까지 방향성이 일관되며
역방향 화살표가 없다. `references/solid-cohesion-coupling-checklist.md` §2 체크리스트 통과.

**DIP 적용**: ARC-002는 ARC-006/ARC-007의 구체 타입이 아니라 IF-INT-008(추상 정책 포트)에 의존한다.
마찬가지로 ARC-002는 ARC-103/104의 구체 타입이 아니라 IF-INT-003/004에 의존하며, 실제 구현체는 조립
단계(ARC-105/205)에서 주입된다.

**LSP 적용**: IF-INT-003/004의 Test 어댑터(ARC-103/104)와 Web 어댑터(ARC-203/204, 예정)는 동일 계약을
지켜야 하며, 코어(ARC-002) 쪽 코드 변경 없이 교체 가능해야 한다. IF-INT-008의 모든 정책 구현체도
동일 계약(PolicyResult 반환)을 지켜야 한다.

## 6. 인터페이스 명세

PlantUML 표현: `SWA-PH1_component.puml`. drawio 최종본은 이번 작업에서 만들지 않았다(§0 비고).

### 6.1 내부 인터페이스

| ID | 명칭 | 제공자 | 사용자 | 제공 기능/데이터 | 호출 조건 | 시간 제약 | 오류 계약 | 관련 요구사항 |
|---|---|---|---|---|---|---|---|---|
| IF-INT-001 | Driver 명령 제출 포트 | ARC-001 | ARC-101(Phase1), ARC-201(Phase4 예정) | `submit_driver_command(raw) -> None` | 평가주기당 최대 1회 호출(SWR-PH1 가정2). VehicleSnapshot 제출 이전에 호출되어야 이번 주기에 반영됨 | 없음(값 교환, 실시간 제약 없음) | 내부적으로 ARC-004/ARC-003 오류 계약을 그대로 전파(예외 없음, Rejection은 이후 IF-INT-004로 통지) | SWR-001, SWR-002 |
| IF-INT-002 | 차량 스냅샷 제출/평가트리거 포트 | ARC-001 | ARC-102(Phase1), ARC-202(Phase4 예정) | `submit_vehicle_snapshot(snapshot) -> EvaluationResult` — 호출 시 평가주기 실행(IF-INT-009) 트리거 | 평가주기당 정확히 1회 호출 | 없음 | `ignition_on` 형식 오류는 예외가 아니라 INVALID 값으로 정규화되어 ARC-007에 전달(SWR-020b) | SWR-020 |
| IF-INT-003 | 액추에이터 출력 포트 | ARC-103(Phase1), ARC-203(Phase4 예정) | ARC-002 | `apply(lock_left, lock_right) -> None` | ARC-002의 평가 결과 확정 직후, 평가주기당 정확히 1회 | 없음 | 정의 없음(PC/SIL 논리 출력까지만 검증, OEM-IF-005와 동일) | SWR-004, SWR-020 |
| IF-INT-004 | 표시 출력 포트 | ARC-104(Phase1), ARC-204(Phase4 예정) | ARC-002 | `show(state, reason_code) -> None` | ARC-002의 평가 결과 확정 직후, 평가주기당 정확히 1회 | 없음 | 정의된 값 외 사용 금지(§6의 열거형은 SWR-PH1 §6 인용) | SWR-001(b), SWR-020 |
| IF-INT-005 | 명령 유효성 판정 포트 | ARC-003 | ARC-004 | `validate(raw) -> ValidCommand \| Rejection(reason_code)` | ARC-004가 IF-INT-001 수신 즉시 호출 | 없음 | 필드 누락/형식/미등록 enum → Rejection, 예외 없음 | SWR-001 |
| IF-INT-006 | 검증된 명령 조회 포트 | ARC-004 | ARC-001(위임 호출), ARC-006(조회), ARC-002(폐기 통지) | `dispatch(raw)`, `get_current_cycle_command() -> ValidCommand \| Rejection \| None`, `discard_current_cycle_command()` | `get_current_cycle_command()`는 평가주기 내 ARC-006에서 최대 1회 | 없음 | source 값과 무관하게 동일 반환 계약(SWR-002 핵심 — 이 인터페이스에 source 분기 자체가 존재하지 않음) | SWR-002 |
| IF-INT-007 | 잠금 상태 접근 포트 | ARC-005 | ARC-006, ARC-007(read), ARC-002(read/write) | `read_current() -> {left, right}`, `write(left, right) -> None` | write는 ARC-002만 평가주기당 최대 1회 호출(단일 writer) | 없음 | 없음(단순 저장, 동시 접근 없음 가정 — §3.2) | SWR-004, SWR-020 |
| IF-INT-008 | 출력 정책 포트 (핵심 확장점) | ARC-006, ARC-007 (Phase1), ARC-301~403 (Phase2/3 예정) | ARC-002 | `evaluate(context) -> PolicyResult{decision: OVERRIDE_FINAL\|PROPOSE\|PASS, lock_left?, lock_right?, reason_code?, state_label?}`. 메타데이터: `category(OVERRIDE\|BASE)`, `asil_level(QM\|ASIL_B)`, `priority(int)` | ARC-002가 정책을 `category=OVERRIDE`는 asil_level 내림차순(ASIL_B 먼저)→동일 등급 내 priority 오름차순으로, 이후 `category=BASE`를 priority 오름차순으로 호출. OVERRIDE_FINAL 수신 시 이후 모든 정책 호출을 스킵 | 없음 | 정책은 예외를 던지지 않고 반드시 PolicyResult를 반환해야 함(계약, 상세설계에서 검증 방법 정의) | SWR-004, SWR-020 (+ Phase2/3 예정 항목) |
| IF-INT-009 | 평가 실행 포트 | ARC-002 | ARC-001 | `evaluate(snapshot) -> EvaluationResult` | IF-INT-002 호출 시 ARC-001이 내부적으로 호출 | 없음 | 정책 실행 중 예외 발생 시 처리 방식은 상세설계에서 확정(§4 ARC-002 오류 처리 참고, 미해결) | SWR-004, SWR-020 |

**ISP 점검**: IF-INT-003/004(출력)와 IF-INT-001/002(입력)를 하나의 "어댑터 인터페이스"로 묶지 않고
방향·데이터 성격별로 분리했다. IF-INT-008은 정책 전용으로, 어댑터나 저장소 접근과 섞지 않았다.

### 6.2 외부 인터페이스

| ID | 방향 | 대응 OEM 인터페이스 | 필드 | 변환/검증 책임 | 본 Phase 반영 범위 |
|---|---|---|---|---|---|
| IF-EXT-001 | Driver → SW | OEM-IF-004 | `side`, `action`, `source` | ARC-101(Phase1)/ARC-201(Phase4)이 원시 입력을 `Driver_Command` 값 객체로 변환. 필드 자체의 유효성 판정은 변환 책임에 포함하지 않고 ARC-003(IF-INT-005)에 위임 | 전체 반영 |
| IF-EXT-002 | Vehicle → SW | OEM-IF-009(부분) | `ignition_on`(Phase1), `sensor_fault`(Phase2 예정) | ARC-102(Phase1)/ARC-202(Phase4)이 `VehicleSnapshot` 값 객체로 변환. `ignition_on` 유효성 판정은 ARC-007에 위임 | `ignition_on`만 반영 |
| IF-EXT-003 | SW → Actuator model | OEM-IF-005 | `lock_left`, `lock_right` | ARC-103(Phase1)/ARC-203(Phase4)이 내부 `LockState` enum을 OEM 값(`LOCK`/`RELEASE`)으로 변환 | 전체 반영 |
| IF-EXT-004 | SW → Display | OEM-IF-006(부분) | `state`, `reason_code` | ARC-104(Phase1)/ARC-204(Phase4)이 내부 값을 OEM 값으로 변환. `priority_reason`/`input_validity`는 Phase 4에서 필드 추가 예정(어댑터 확장만 필요, 코어 변경 불필요 — IF-INT-004 계약이 이미 `reason_code`를 옵션 확장 가능한 형태로 정의) | `state`, `reason_code`만 반영 |

## 7. 동적 동작

- 정상 시나리오(ignition ON, 유효 명령): `SWA-PH1_sequence-nominal.puml` — SWR-001 통과 → SWR-002(소스
  무관 동일 처리, 인터페이스 계약으로 이미 보장되어 시퀀스에는 별도 분기가 없음) → ARC-007이 PASS →
  ARC-006이 PROPOSE → 출력 확정.
- 오버라이드 시나리오(ignition FALSE, 명령 존재): `SWA-PH1_sequence-ignition-override.puml` — ARC-007이
  OVERRIDE_FINAL을 반환해 ARC-006 평가 자체가 스킵됨 → SWR-020이 SWR-002/004보다 항상 우선 적용된다는
  SWR-PH1 §8 요건을 시퀀스 수준에서 실증. 다이어그램 내 note로 Phase 2 ASIL B 정책이 어떻게 같은
  스캔 절차에 우선 삽입되는지 설명.
- 거절 시나리오(SWR-001b, 필드 누락/형식 오류/미등록 enum): 별도 시퀀스 다이어그램은 생략하고 §4의
  ARC-003/006 오류 처리 표로 갈음한다 — 필요 시 상세설계 단계에서 시퀀스로 구체화한다(미해결 항목 아님,
  단순화된 결정).

## 8. 상태 전이

- SW 요구사항 관점(출력값 `lock_left`/`lock_right`와 ignition 상태)의 상태 전이는 요구사항 단계에서
  이미 `SWR-PH1_state-ignition.puml`로 정의되어 있다 — 이 아키텍처 문서는 그 상태 모델을 재정의하지
  않고 그대로 따른다.
- 아키텍처 관점(ARC-002 PolicyChainExecutor가 한 평가주기 안에서 거치는 실행 상태)은
  `SWA-PH1_state-cycle.puml`로 신규 정의했다: `IDLE → (COMMAND_STAGED) → EVALUATING{OVERRIDE_SCAN →
  BASE_EVAL} → OUTPUT_COMMIT → IDLE`. Phase 2/3의 새 OVERRIDE 정책은 `OVERRIDE_SCAN` 상태 내부의
  반복 목록에 항목만 추가되며, 상태/전이 구조 자체는 변경되지 않는다(OCP 근거).
- 금지 전이: `OVERRIDE_SCAN`에서 `OUTPUT_COMMIT`으로 바로 가는 경우(OVERRIDE_FINAL) `BASE_EVAL`을
  거치지 않는다 — 이는 금지가 아니라 설계된 스킵 경로이며, 반대로 `BASE_EVAL`을 거친 뒤 다시
  `OVERRIDE_SCAN`으로 돌아가는 전이는 금지된다(한 평가주기 내 정책 재평가 없음).

## 9. 오류 격리와 안전 동작

- **오류 감지 위치**: 입력 값의 형식적 오류는 코어 진입 지점(ARC-003 CommandValidator, ARC-007의
  ignition_on 유효성 판정)에서 감지한다 — 정책/상태 컴포넌트(ARC-005, ARC-006 내부 로직)는 이미
  정규화된 값만 다루므로 원시 오류를 직접 다루지 않는다(오류 처리 책임의 응집).
- **전파 차단 지점**: IF-INT-005/IF-INT-006 계약은 예외(exception)가 아니라 `Rejection` 값을
  반환하도록 정의했다 — 잘못된 입력이 호출 스택을 통해 예기치 않게 전파되지 않고, 명시적으로
  `reason_code=INVALID_COMMAND`로 변환되어 IF-INT-004(Display)로 통지된다.
- **안전 상태**: 이번 Phase 1의 안전측 기본값은 SWR-020이 정의한 대로 "ignition 비정상/OFF ⇒
  `RELEASE`"이다. ARC-007이 이 안전 상태를 담당하며, ARC-002가 이를 다른 모든 정책보다 우선 채택하도록
  강제한다(§6 IF-INT-008 실행 규약).
- **간섭 없음(freedom from interference) 관점 — Phase 2 대비 설계 여지, 이번 문서는 QM 요소만 실제
  구현**: IF-INT-008의 실행 규약이 "ASIL_B 정책이 asil_level 내림차순으로 먼저 평가되고 OVERRIDE_FINAL
  시 이후 정책(QM 포함)을 스킵한다"고 명시되어 있으므로, Phase 2에서 ASIL B 정책이 추가되어도 QM
  정책(ARC-006/007)이 ASIL B 정책의 확정 결과를 덮어쓸 수 없는 구조다. 다만 **이 문서만으로 ISO 26262
  Part 6의 "간섭 없음" 요건이 완전히 충족되었다고 단정하지 않는다** — 정확한 요건(예: 메모리/시간
  분리, 공통원인고장 분석)은 Phase 2 아키텍처 확장 시 공식 표준 문서와
  `references/iso26262-aspice-architecture-checklist.md`를 함께 재확인해야 한다. 현재 설계는 "QM
  코드가 확정된 ASIL B 결정을 논리적으로 덮어쓸 수 없다"는 소프트웨어 구조적 보장만 제공한다.
- **복구/진단 정보 제공**: `reason_code`(IF-INT-004/IF-EXT-004)가 진단 정보 제공 책임을 담당한다.
  Phase 4에서 `priority_reason`/`input_validity` 필드가 추가되면 동일 포트의 확장으로 처리한다(§6.2).

## 10. 품질속성 분석

| 품질속성(ISO 25010 참고) | 시나리오 | 설계 대응 |
|---|---|---|
| 변경 용이성(수정성) | Phase 2에서 crash override(ASIL B)를 추가해야 한다 | IF-INT-008 신규 구현체 추가만으로 대응, ARC-001~007 수정 불필요(§3.1, §9) |
| 재사용성 | 동일 결정 로직을 PC/SIL과 Web 시뮬레이터에서 재사용해야 한다 | 코어(ARC-001~007)는 어댑터에 의존하지 않음 — ARC-105/ARC-205가 동일 코어를 감싸는 서로 다른 구동 어댑터 조립일 뿐 (§13에서 배포 근거 상술) |
| 시험 용이성 | 정책·검증 로직을 하드웨어 없이 단위/통합 시험해야 한다 | 모든 코어 컴포넌트가 순수 값 입출력 인터페이스(IF-INT-005~009)를 가지며 부작용이 LockStateStore write로 국한되어 스텁 대체가 쉬움(§11 스텁 전략) |
| 호환성(공존성) | SW가 Python 3.12 PC/SIL 환경에서 실행 가능해야 함(SWR-PH1 §7) | 코어는 순수 Python 로직, HW/OS 의존 없음(§13) |
| 신뢰성(안전성 관련 QM 수준) | ignition-off 시 항상 RELEASE로 강제되어야 함 | §9 오류 격리·안전 상태 설계로 대응 |
| 성능효율성 | 이번 프로젝트는 실시간 임베디드 제약이 없음(과제 전제) | 별도 성능 설계 불필요 — 단, Phase 4 "결정론적 재현(1,000회 재생 해시 동일)"을 고려해 코어에 벽시계·난수·스레딩 등 비결정적 요소를 도입하지 않았다(§13에서 근거 명시) |

## 11. 통합 전략

전략: **상향식(Bottom-Up)** — 기반 컴포넌트(검증기, 저장소, 출력 어댑터)가 안정적이고 정책/조정
로직이 그 위에 얹히는 구조이므로, 하위부터 통합해 상위 조정 로직(ARC-002)이 실제 구현체를 대상으로
바로 검증되도록 한다.

| 단계 | 통합 대상 | 필요한 스텁/드라이버 | 검증 인터페이스/시나리오 | 회귀 범위 | 완료 기준 |
|---|---|---|---|---|---|
| 1 | ARC-003, ARC-005, ARC-103, ARC-104 (병렬) | 각 컴포넌트를 호출하는 테스트 드라이버(단위 시험 하네스) | IF-INT-005(유효/무효 판정), IF-INT-007(read/write), IF-INT-003/004(값 반영) | 없음(최초 단계) | 4개 컴포넌트 단위 시험 통과 |
| 2 | ARC-004(→ARC-003 실접속), ARC-007(→ARC-005 실접속) (병렬) | ARC-002 역할 드라이버(정책 호출 시뮬레이션) | IF-INT-006(dispatch/get/discard), SWR-002 동등처리(4 source 반복), IF-INT-007 read | 1단계 컴포넌트 재검증 없음(계약 불변) | ARC-004/007 통합 시험 통과 |
| 3 | ARC-006(→ARC-004, ARC-005 실접속) | ARC-002 역할 드라이버 유지 | IF-INT-008 PROPOSE 반환값, SWR-004 진리표(3 side × 2 action × 2 사전상태) | 2단계 회귀(ARC-004 계약 변경 없음 확인) | ARC-006 통합 시험 통과 |
| 4 | ARC-002(→ARC-006, ARC-007, ARC-005, ARC-103, ARC-104 모두 실접속) | 없음(모든 하위 실구현 사용) | IF-INT-008 실행 규약(override 우선·스킵), SWR-020 상태전이 4케이스(§SWR 문서 검증방안) — **이 단계에서 ASIL 우선 계약(§6 IF-INT-008)이 실제로 동작함을 최초로 실증** | 1~3단계 컴포넌트 전체 회귀(출력 확정 경로가 처음으로 완성되므로) | ARC-002 통합 시험(진리표+상태전이) 전체 통과 |
| 5 | ARC-001(→ARC-004, ARC-002 실접속) | 없음 | IF-INT-001/002/009 위임·트리거 동작 | 4단계 회귀 | ARC-001 통합 시험 통과 |
| 6 | ARC-101, ARC-102 (병렬, →ARC-001 실접속) | 테스트 벡터 파일/픽스처 | IF-EXT-001/002 변환 정확성 | 5단계 회귀 | 어댑터 변환 시험 통과 |
| 7 | ARC-105(전체 조립) | 없음 | SWR-001/002/004/020 전체 시나리오(PC/SIL 시스템 시험 사전 점검) | 전체 회귀 | Phase 1 통합시험 전체 통과, G3 게이트 준비 완료 |

**Phase 2/3 정책 삽입 시 통합 순서 영향**: 새 정책(예: ARC-301 CrashOverridePolicy)은 위 표의 **단계 3에
해당하는 위치**(하위 의존은 ARC-005뿐이므로 ARC-006과 같은 레벨)에서 독립적으로 단위/통합 시험을 거친
뒤, **단계 4(ARC-002 등록)에서만** 기존 정책 목록에 추가하면 된다. 단계 1~3에서 이미 통합된
ARC-003~ARC-007은 재통합이 필요 없고, 회귀 범위는 단계 4~7 재실행으로 한정된다. 다만 ARC-301이 ASIL
B이므로, 완료 기준에 "ASIL B 정책의 오류 격리·간섭 없음 근거 제시"(§9)를 추가해야 한다 — 이는 Phase 2
아키텍처 확장 작업에서 구체화한다(이번 문서의 미해결 사항 아님, 예정된 후속 작업).

**자체 점검(§6 통합순서 가이드 §5 기준)**: 모든 Phase 1 컴포넌트(ARC-001~007, 101~105)가 정확히 한
번씩 등장, 의존 컴포넌트보다 먼저 등장하는 항목 없음, 스텁/드라이버 필요 여부 전 단계 기재 확인 완료.

## 12. 요구사항 할당

| SWR ID | 아키텍처 요소 | 관련 인터페이스 | 검증 수준(SWR 문서 인용) |
|---|---|---|---|
| SWR-001 | ARC-003 | IF-INT-005 | PC/SIL/Web |
| SWR-002 | ARC-004 | IF-INT-006 | PC/SIL/Web |
| SWR-004 | ARC-006 | IF-INT-008(BASE) | PC/SIL/Web |
| SWR-020 | ARC-007 | IF-INT-008(OVERRIDE) | PC/SIL/Web |

**할당 누락 점검**: SWR-001/002/004/020 모두 정확히 1개의 1차 책임 컴포넌트에 할당됨 — 중복 할당 없음.

**"근거 없는 요소" 아닌 이유(§8 자체 점검 대응)**: 아래 컴포넌트는 특정 SWR 하나에 직접 할당되지
않지만, SWR-PH1 §8 "상충 사항과 해소"("SWR-020의 강제 RELEASE가 SWR-002/004의 산출값보다 항상 우선
적용되며 ... 실제 중재 로직의 위치는 아키텍처 설계 단계에서 결정한다")를 이행하기 위해 존재하는
인프라/조정 요소이며, 이 요구사항 문서 문구 자체가 이들의 존재 근거다.

- ARC-001(Facade), ARC-002(PolicyChainExecutor): 위 SWR-PH1 §8 인용 문구의 실행 근거
- ARC-005(LockStateStore): SWR-004("나머지 출력은 이전 평가주기 값을 유지")와 SWR-020("RELEASE로
  유지")이 공통으로 요구하는 "직전 값 보존" 요건의 실행 근거
- ARC-101~105, ARC-103~104: OEM-IF-004/005/006/009 외부 인터페이스 경계를 실제로 실현하는 요소(§6.2)

## 13. 자원 및 배포 경계

- **실행 노드**: 단일 Python 3.12 프로세스(하드웨어/HIL 없음, VJ-ECL-2026 CLAUDE.md 재정의 항목 그대로
  적용).
- **프로세스/스레드**: 코어는 스레드/비동기 없이 순차 실행되는 순수 로직으로 설계한다(§3.2, §10) —
  Phase 4의 "고정 시계로 1,000회 재생 시 해시 동일(결정론적 재현)" 요구와 충돌할 수 있는 비결정적
  요소(벽시계, 난수, 스레드 경쟁)를 코어에 도입하지 않는다.
- **PC/SIL 테스트 하네스와 Web 시뮬레이터의 프로세스 경계 결정(이번 호출에서 판단, 근거 기록)**: 두
  실행 형태를 **완전히 분리된 프로세스가 아니라, 같은 Python 패키지 내 서로 다른 진입점(entry point,
  ARC-105/ARC-205)으로 구성**하기로 정한다. 근거:
  1. 두 실행 형태 모두 헥사고날 구조상 "구동 어댑터"일 뿐이며, 핵심 가치는 동일한 코어(ARC-001~007)
     버전을 그대로 재사용하는 데 있다(§10 재사용성). 별도 프로세스/별도 배포판으로 분리하면 두 실행
     환경이 서로 다른 코어 빌드를 참조할 위험이 생기고, 이는 "결정 로직 재사용" 요건과 Phase 4
     "결정론적 재현" 요건 모두에 반한다.
  2. 같은 패키지의 다른 진입점으로 두면 단일 소스(하나의 Python 패키지 버전)에서 두 실행형태가
     파생되므로 버전 불일치 위험이 구조적으로 차단된다.
  3. 코어는 어댑터 경계(IF-INT-001~004, IF-INT-009) 뒤에 있으므로, 이 결정은 코어 설계에 영향을 주지
     않는다 — 훗날 Web 시뮬레이터가 별도 프로세스로 코어를 원격 호출하는 형태로 바뀌어도(예: 로컬
     프로세스 간 통신), ARC-205가 IF-INT-001/002/003/004를 원격 프록시로 구현하기만 하면 되므로
     아키텍처 재작업이 필요 없다(OCP/DIP로 이미 격리되어 있음).
  4. 이 판단은 세부 배포 정책(패키징, 실행 스크립트 이름 등)에 해당하며, 상세설계(SWE.3) 단계에서
     구체적인 모듈/패키지 경로로 확정한다.
- **메모리/CPU/저장소 제약**: 없음(HW 제약 없는 순수 SW 시뮬레이션, 과제 전제).
- **소스 배치 가이드(강제 아님, 상세설계에서 확정)**: `src/` 하위에 core(ARC-001~007), adapters/pcsil
  (ARC-101~105), adapters/web(ARC-201~205, Phase4)로 구분하는 패키지 레이아웃을 권장한다.

## 14. 추적성

- 단일 진실 공급원: `docs/Traceability/traceability-matrix.md` — 이번 작업에서 SWR-001/002/004/020의
  "설계 요소" 열을 ARC-003/ARC-004/ARC-006/ARC-007로 갱신했다(같은 작업 안에서 갱신, 미루지 않음).
- 다이어그램 동기화: `SWA-PH1_component.puml`, `SWA-PH1_sequence-nominal.puml`,
  `SWA-PH1_sequence-ignition-override.puml`, `SWA-PH1_state-cycle.puml`의 컴포넌트/인터페이스 ID가 본
  문서 §3~§8의 표와 일치함을 확인했다.
- 하향 링크(상세설계 모듈, 통합/시스템 시험 케이스)는 이 시점(G2 초안)에는 아직 존재하지 않으며, G2
  상세설계 완료 시 및 G3/G4 시험 설계 완료 시 매트릭스에 추가해야 한다 — 고아 요구사항이 아니라 게이트
  진행에 따른 예정된 공백이다(SWR-PH1 문서와 동일한 관례 적용).

## 15. 참고자료

| 자료 | 식별정보/버전 | 적용 범위 |
|---|---|---|
| SW 요구사항 명세서 | `docs/SoftwareRequirementsAnalysis/SWR-PH1_SW 요구사항 명세서.md`, v0.1 | SWR-001/002/004/020 전문, §8 상충 해소 위임 근거 |
| OEM SW 요구사항 사양서 | `OEM_Sample/OEM-SWR-001_OEM SW 요구사항 사양서.docx`, BL-OEM-1.0 | OEM-IF-004/005/006/009 원문, Phase 2/3/4 범위 확인 |
| 회사 지정 템플릿 | `WP_Templates/Engineering/SoftwareArchitecturalDesign/TPL-SWE2-001_SW 아키텍처 설계서 템플릿.docx`, `TPL-SWE2-002_SW 아키텍처 UML 템플릿.drawio` | 본 문서의 장/절 구조 근거(§0 비고 — drawio 이전은 별도 작업) |
| 아키텍처 설계 스킬 | `.claude/skills/architecture-design/SKILL.md` 및 `references/*` | 후보 스타일 카탈로그, SOLID/응집도/결합도 체크리스트, 인터페이스 명세 가이드, 통합 순서 가이드 |
| 추적성 매트릭스 | `docs/Traceability/traceability-matrix.md` | SWR ↔ ARC ↔ IF 연결(§14에서 갱신) |
| ISO 26262 Part 6 | 프로젝트 첨부 원문 없음 — 조항 인용 필요 시 공식 표준 문서 별도 확인 필요 | 아키텍처 설계 원칙(§2), 오류 격리·간섭 없음(§9) — Phase 2 ASIL B 확장 시 재확인 필수 |
| A-SPICE v4.1 (SWE.2) | 프로젝트 첨부 원문 없음 — `.claude/skills/aspice-auditor/references/aspice-source.md` 및 공식 문서 확인 필요 | 아키텍처 설계 프로세스 정합성 |
