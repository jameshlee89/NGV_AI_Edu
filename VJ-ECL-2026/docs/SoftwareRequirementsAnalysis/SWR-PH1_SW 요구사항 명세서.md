> **비고(도구 제약)**: 회사 지정 템플릿 `WP_Templates/Engineering/SoftwareRequirementsAnalysis/TPL-SWE1-001_SW 요구사항 명세서 템플릿.docx`가
> 이미 저장소에 존재하여, 이 문서는 그 템플릿의 절/표 구조(표지 → 문서 통제 → 목차 → 1~12절)를 그대로
> 옮겨 작성했습니다. 다만 현재 세션 환경에는 `.docx`를 직접 생성/수정할 도구(Node.js+`docx` 패키지,
> LibreOffice, pandoc 등)가 설치되어 있지 않아 `.docx` 파일 자체를 채우지 못하고, 동일한 구조의
> Markdown으로 작성했습니다. **docx 템플릿 직접 채우기는 별도 도구 필요** — 도구가 준비되면 이 내용을
> `TPL-SWE1-001` 사본에 그대로 옮겨 `.docx`로 재발행해야 합니다.

# TPL-SWE1-001_SW 요구사항 명세서 템플릿 기반 — SWR-PH1_SW 요구사항 명세서

프로젝트 공학 산출물 작성용 빈 양식을 채운 실제 산출물입니다.

| 항목 | 내용 |
|---|---|
| 템플릿 ID | TPL-SWE1-001 |
| 적용 프로세스 | SWE.1 |
| 프로젝트 | VJ-ECL-2026 (가상 OEM-A 전자식 후석 좌/우 차일드락 제어 SW) |
| 작성 문서 ID와 명칭 | SWR-PH1_SW 요구사항 명세서 |
| 버전 및 베이스라인 | v0.1 (초안) / 목표 베이스라인 BL-SWR-1.0 (승인 시 확정, G1 게이트) |
| 작성자와 검토자 | 작성자: 요구사항 분석 에이전트(requirements-analyst 스킬, 세션 실행자 jaehwan2.lee@hlcompany.com) / 검토자 겸 승인자: jaehwan2.lee@hlcompany.com (사용자 본인, 2026-09-18 지정) |

본 자료는 SW 품질교육을 위한 교육용 샘플이며, 저작권은 Synetics에 있습니다. 교육 과정 안에서 열람,
복제 및 실습 사용을 허용합니다. 과정 밖 배포, 공개 또는 상업적 이용은 Synetics의 사전 서면 승인을
받아야 합니다. © 2026 Synetics. All rights reserved.

## 문서 통제

작성 안내: 문서의 작성, 검토, 승인 책임과 적용 베이스라인을 식별한다. 실제 승인 상태와 검토 증거
위치를 구분해 기록한다.

### 변경 이력

| Revision | 변경일 | 작성 역할 | 변경 내용 | 검토 상태 |
|---|---|---|---|---|
| v0.1 | 2026-09-18 | 요구사항 분석 에이전트 | Phase 1 최초 작성. OEM-FR-001, OEM-FR-007 대상으로 SWR-001, SWR-002, SWR-004, SWR-020 도출 | 초안 |

### 작성 검토 승인 상태

| 구분 | 역할 또는 성명 | 상태 | 일자 | 증거 위치 |
|---|---|---|---|---|
| 작성 | 요구사항 분석 에이전트 | 완료 | 2026-09-18 | 본 문서 |
| 검토 | jaehwan2.lee@hlcompany.com (사용자 본인) | 대기(Phase 1 종료 시 종합 리뷰 예정) | - | 대화 이력(§8 미결정 사항 4건 확정 답변) |
| 승인 | jaehwan2.lee@hlcompany.com (사용자 본인) | 대기(Phase 1 종료 시 종합 승인 예정) | - | - |

## 목차

작성 안내: Word의 자동 목차 기능으로 아래 제목을 갱신한다. 배포 전 페이지 번호와 제목 수준을
확인한다. (Markdown본에서는 아래 절 번호를 그대로 목차로 사용한다.)

1. 목적 및 적용범위
2. 요구사항 작성 및 판정 규칙
3. 상태와 우선순위
4. 기능 및 안전 관련 SW 요구사항
5. 입력 데이터 사전
6. 외부 인터페이스 요구
7. 비기능 및 환경 제약
8. 분석 결과와 가정
9. 하향 할당 및 검증 계획
10. 범위 밖 주장
11. 추적성
12. 참고자료

---

## 1. 목적 및 적용범위

### 1.1 목적

이 문서는 가상 OEM-A 공급자 입력 사양(`OEM_Sample/OEM-SWR-001_OEM SW 요구사항 사양서.docx`,
베이스라인 BL-OEM-1.0)의 OEM-FR-001과 OEM-FR-007을 근거로, VJ-ECL-2026 Phase 1(핵심 골격 + 수동
제어)에서 구현할 SW 요구사항(SWR-001, SWR-002, SWR-004, SWR-020)을 도출·명세한다. 이 문서는 Phase 1
아키텍처 설계(SWE.2, G2)와 SW 시스템 시험 케이스 설계(sw-system-test 스킬, G4)의 유일한 근거로
사용된다.

### 1.2 적용범위

- 대상 제품: 대한민국 판매용 2026년식 가상 차량의 후석 좌/우 전자식 차일드락 제어 SW
- 대상 생명주기 단계: 요구사항 분석(SWE.1), Phase 1(브랜치 `feature/phase1-core-manual-control`)
- 실행/검증 환경: Python 3.12, PC/SIL 및 Web 시뮬레이터 (OEM 문서 §3 제품 경계에 명시된 고객 실행환경)
- 대상 조직: VJ-ECL-2026 개발팀(분석→아키텍처→상세설계→구현→통합/시스템 시험)

### 1.3 적용 경계

- **포함**: OEM-FR-001(4개 입력 채널을 통한 좌/우/전체 잠금·해제 명령 처리), OEM-FR-007
  (ignition_on=FALSE 시 논리 출력 강제 해제). 관련 외부 인터페이스 중 OEM-IF-004, OEM-IF-005,
  OEM-IF-006(일부 필드), OEM-IF-009(일부 필드)만 포함한다.
- **제외(이후 Phase)**: OEM-SR-001~004(ASIL B 안전 요구, Phase 2), OEM-FR-002·FR-003(주행 중 자동
  잠금·접근위험 override, Phase 2/3), OEM-FR-004~006(상태조회 표시, 화재/과온/성인탑승 강제해제,
  ISOFIX 강제잠금, Phase 3/4), OEM-NFR-001~002(결정론적 재현, 이벤트 로그, Phase 4). 이 요구사항들은
  본 문서에서 SWR로 도출하지 않으며, 참고용으로만 §8·§10에서 언급한다.
- **경계**: HIL/실차/ECU/HW 통합, Part 3 HARA, 공식 기능안전 인증은 VJ-ECL-2026 프로젝트 전체 범위
  밖이며(SW-only, PC/SIL·Web 검증까지), 이 문서도 그 경계를 따른다.

## 2. 요구사항 작성 및 판정 규칙

### 2.1 식별 및 상태 규칙

- ID 체계: OEM 문서 §9(추적성 계획)에서 이미 배정된 `SWR-001`~`SWR-021` 번호를 그대로 사용한다.
  이번 문서는 그중 OEM-FR-001에 배정된 `SWR-001`, `SWR-002`, `SWR-004`와 OEM-FR-007에 배정된
  `SWR-020`만 다룬다. 번호는 순증가만 하며, 폐기되어도 재사용하지 않는다.
- 상태값: 초안 / 검토중 / 승인 / 구현중 / 검증완료 (5단계, `requirements-analyst` 스킬 §1 기준).
  본 문서의 모든 SWR은 현재 **초안** 상태다.
- 우선순위: 필수 / 권장 / 선택 (3단계). 본 문서의 모든 SWR은 OEM 수용기준에 직접 대응하므로
  **필수**다.
- 변경 통제: 승인(G1, BL-SWR-1.0) 이후 내용 변경 시 신규 Revision 행을 추가하고 사유를 기록한다.
  ID 자체는 변경하지 않는다.

### 2.2 품질 판정 기준

- **명확성/원자성**: EARS(Easy Approach to Requirements Syntax) 문형(유비쿼터스/이벤트기반/
  상태기반/원치 않는 동작/선택기능/복합)으로 작성하고, "그리고"·"또는"으로 서로 다른 요구를 묶지
  않는다. 애매한 형용사는 측정 가능한 기준으로 구체화한다.
- **검증 가능성**: 모든 요구사항은 PC/SIL 자동시험 또는 Web 시뮬레이터 관찰로 통과/실패를 판정할 수
  있어야 한다(OEM 문서 명시 검증 수준: PC/SIL/Web).
- **일관성**: 동일 용어(예: `side`, `action`, `source`, `ignition_on`, `lock_left`/`lock_right`)는
  문서 전체에서 OEM 원문 표기를 그대로 사용한다.
- **추적성**: 모든 SWR은 상위(OEM-FR-ID)와 하위(설계 요소·시험 케이스, 배정 예정 포함) 링크를
  `docs/Traceability/traceability-matrix.md`에 유지한다.

## 3. 상태와 우선순위

| 상태값 | 의미 | 전이 조건 | 승인 책임 |
|---|---|---|---|
| 초안 | 최초 도출, 검토 전 | 작성 완료 | 요구사항 분석 담당 |
| 검토중 | 검토자 배정, 코멘트 수집 중 | 검토 요청 접수 | 검토자 |
| 승인 | 검토 완료, 베이스라인 후보 | 검토 코멘트 반영 완료 | 프로젝트 책임자 |
| 구현중 | 아키텍처/상세설계·구현 진행 | 승인(BL-SWR-1.0) 확정 | 개발 담당 |
| 검증완료 | 시스템 시험으로 수용기준 충족 확인 | G4 시험 결과 Pass | 검증 담당 |

우선순위는 필수(즉시 구현 대상, 본 문서 전 항목 해당) / 권장(품질 개선, 결손 시 릴리스 차단 없음) /
선택(옵션 사양)의 3단계를 사용하며, 본 문서의 4개 SWR은 모두 **필수**다.

## 4. 기능 및 안전 관련 SW 요구사항

### 4.1 기능 요구사항

작성 안내에 따라 각 요구사항의 ID, 출처, 조건, 동작, 정량 기준, 검증 방법, 상태를 기록한다. EARS
문형과 대응 다이어그램은 `SWR-PH1_usecase.puml`(유스케이스), `SWR-PH1_sequence.puml`(시퀀스),
`SWR-PH1_state-ignition.puml`(상태), `SWR-PH1_requirements-trace.puml`(SysML 파생/충족 관계)를
참고한다(모두 이 폴더에 위치).

**분해 근거**: OEM-FR-001의 수용기준("정지, 정상입력에서 네 source 각각의 LOCK/RELEASE와
LEFT/RIGHT/ALL 조합이 선택 출력에만 적용된다")은 서로 독립적으로 검증 가능한 세 가지 관심사를
포함한다 — (a) 입력 필드 자체의 수신·유효성 판정(OEM-IF-004 오류 처리 포함), (b) 4개 source 채널이
결과에 차별을 주지 않는다는 동등성, (c) side 값에 따라 어느 출력이 갱신되는지의 선택 범위. 배정된
3개 ID(SWR-001/002/004)를 이 세 관심사에 하나씩 대응시켰다.

---

#### SWR-001 — 운전자 잠금/해제 명령 수신 및 유효성 검증

| 속성 | 내용 |
|---|---|
| 유형 | 기능 (QM) |
| 출처 | OEM-FR-001 (수용기준 중 "정상입력" 전제), OEM-IF-004 오류 처리 규정 |
| 우선순위 | 필수 |
| 상태 | 초안 |

**설명 (EARS)** — 이 항목은 유효성 판정이라는 하나의 주제를 긍정/부정 경로 두 문장으로 규정한다
(두 문장은 서로 배타적 조건이므로 하나의 판정 로직을 이룬다):

- (a) 이벤트 기반: WHEN SW가 한 평가주기에서 `Driver_Command(side, action, source)` 입력을
  수신하면, THE SW SHALL `side ∈ {left, right, all}`, `action ∈ {lock, unlock}`,
  `source ∈ {physical_button, avn, voice, mobile_app}` 세 필드가 모두 결측 없이 존재하고 각각
  정의된 집합에 속하는 경우에만 그 명령을 **유효**로 판정하고 SWR-002/SWR-004 처리로 전달한다.
- (b) 원치 않는 동작: IF 세 필드 중 하나라도 누락되었거나, 형식 오류이거나, 정의되지 않은 enum
  값이면, THEN THE SW SHALL 해당 명령을 거절하고, `lock_left`/`lock_right` 출력을 변경하지 않으며,
  `OEM-IF-006` 표시 인터페이스에 `reason_code = INVALID_COMMAND`를 제공한다.

**근거/사유**: OEM-IF-004는 "누락, 형식, 미등록 enum 거절"을 명시적 오류 처리로 규정하며, 이 판정이
선행되지 않으면 SWR-002/SWR-004가 잘못된 입력으로 동작하게 된다.

**검증방안**: PC/SIL 자동시험으로 (1) 유효 조합 12개(3 side × 2 action × 2 대표 source, 나머지
source는 SWR-002에서 커버) 입력 시 명령이 전달됨을 확인, (2) 필드 누락/형식 오류/미등록 enum 각
1건 이상 주입해 출력 불변 및 `reason_code=INVALID_COMMAND` 표시를 확인한다(경계값·오류추정 기법).
Web 시뮬레이터에서 동일 케이스 육안 재현 확인. 실행 가능 여부: PC/SIL 자동화는 프로젝트
`tests/system/`에 Python 3.12 기반으로 구현 가능함을 확인했으나, 실제 테스트 코드는 sw-system-test
스킬 단계에서 작성된다 — 이 시점에는 방법론만 확정하고 자동화 스크립트 존재 여부는 확정하지 않는다.

**추적 링크**: 상위 OEM-FR-001 / 하위 설계 요소·시험 케이스는 §9, §11 및
`docs/Traceability/traceability-matrix.md` 참조(G2/G4에서 배정 예정, 현재 미정).

---

#### SWR-002 — Source 채널별 명령의 동등 처리

| 속성 | 내용 |
|---|---|
| 유형 | 기능 (QM) |
| 출처 | OEM-FR-001 (수용기준 중 "네 source 각각의 ... 조합이 선택 출력에만 적용") |
| 우선순위 | 필수 |
| 상태 | 초안 |

**설명 (EARS, 유비쿼터스)**: THE SW SHALL SWR-001에서 유효로 판정된 `Driver_Command`에 대해,
`source` 값이 `physical_button`, `avn`, `voice`, `mobile_app` 중 무엇이든 관계없이 동일한
`side`/`action` 적용 규칙(SWR-004)을 적용한다. 즉 `source`는 출력 결과(`lock_left`, `lock_right`)에
어떠한 차별적 영향도 주지 않는다.

**근거/사유**: OEM-A는 4개 입력 채널을 대등한 명령 경로로 정의했으며, 채널별 차등 동작을 요구하지
않는다. 채널 간 비대칭 동작은 운전자에게 예측 불가능한 경험을 준다.

**검증방안**: PC/SIL에서 동일 `(side, action)` 조합을 `source`만 4가지로 바꿔가며 각 4회 반복 입력하고,
매회 산출된 `lock_left`/`lock_right` 값이 동일함을 회귀 비교(동등분할: source를 동등클래스로 간주하고
대표값 4개 모두 실행)한다. 실행 가능 여부: 확인됨(순수 함수적 비교, 별도 도구 불필요).

**추적 링크**: 상위 OEM-FR-001 / 하위는 §9, §11 참조.

---

#### SWR-004 — LEFT/RIGHT/ALL 조합에 따른 선택적 출력 적용

| 속성 | 내용 |
|---|---|
| 유형 | 기능 (QM) |
| 출처 | OEM-FR-001 (수용기준 중 "LEFT/RIGHT/ALL 조합이 선택 출력에만 적용") |
| 우선순위 | 필수 |
| 상태 | 초안 |

**설명 (EARS, 이벤트 기반)**: WHEN SWR-001/SWR-002를 통과한 유효 명령 `(side, action)`이 처리
대상으로 확정되면, THE SW SHALL 다음과 같이 `OEM-IF-005` 출력을 갱신한다 — `side=left`이면
`lock_left`만, `side=right`이면 `lock_right`만, `side=all`이면 `lock_left`와 `lock_right` 모두를
`action=lock → LOCK`, `action=unlock → RELEASE`로 갱신하고, 선택되지 않은 나머지 출력은 이전 평가
주기의 값을 그대로 유지한다.

**근거/사유**: 수용기준이 "선택 출력에만 적용"을 명시적으로 요구하므로, 선택되지 않은 출력에 대한
부작용(side-effect) 금지를 별도 원자적 요구사항으로 분리해 검증 가능하게 한다.

**검증방안**: PC/SIL에서 진리표 기반 시험(3 side × 2 action × 2 사전상태(LOCK/RELEASE) = 12케이스)을
수행해, 선택된 출력만 변경되고 나머지 출력은 사전상태를 유지함을 확인한다(동등분할 + 상태전이 시험).
실행 가능 여부: 확인됨.

**추적 링크**: 상위 OEM-FR-001 / SWR-020과의 우선순위 관계는 §8 참조.

---

#### SWR-020 — Ignition-Off 시 논리 차일드락 출력의 강제 해제 및 재전환 시 유지

| 속성 | 내용 |
|---|---|
| 유형 | 기능 (QM) |
| 출처 | OEM-FR-007, OEM-IF-009(`ignition_on`) |
| 우선순위 | 필수 |
| 상태 | 초안(§8 미결정 사항 3건 확정 답변 반영, 2026-09-18) |

**설명 (EARS)** — 세 조건(진입/지속/재전환)을 각각 원자적으로 규정한다:

- (a) 이벤트 기반: WHEN `ignition_on`이 유효값 `FALSE`로 판정된 첫 평가주기가 되면, THE SW SHALL
  `lock_left`와 `lock_right`를 `RELEASE`로 강제하고, `OEM-IF-006`에 `state=OFF`,
  `reason_code=IGNITION_OFF`를 제공하며, 이 값은 SWR-002/SWR-004가 산출한 값보다 항상 우선
  적용된다.
- (b) 상태 기반: WHILE `ignition_on`이 `FALSE`이거나 `INVALID`(누락/형식 오류, OEM-IF-009 오류
  처리)로 판정되는 동안, THE SW SHALL `lock_left`/`lock_right`를 `RELEASE`로 유지하고 새 
  `Driver_Command`를 적용하지 않는다. (사용자 확정: `ignition_on` INVALID는 `FALSE`와 동일하게
  안전측(fail-safe)으로 처리한다 — 2026-09-18 확정.)
- (c) 이벤트 기반: WHEN `ignition_on`이 `FALSE`(또는 INVALID) 이후 유효값 `TRUE`로 전환되는 첫
  평가주기가 되면, THE SW SHALL `lock_left`/`lock_right`를 **무조건 `RELEASE`로 유지**한다 —
  ignition-off 진입 직전에 래치되어 있던 명령을 복원하지 않는다. 이후 잠금은 새로운
  `Driver_Command`(SWR-001/002/004)로만 이루어진다. (사용자 확정: 안전측 기본값 접근 —
  2026-09-18 확정.)

**근거/사유**: OEM-FR-007 수용기준은 진입 조건(a)만 명시한다. 지속 조건(b)과 재전환 조건(c)은 OEM
원문에 명시가 없어 §8에서 사용자 확인을 거쳐 확정했다 — 세 조건 모두 "차량 정지/미시동 상태에서는
차일드락이 걸려 있지 않아야 한다"는 안전측 기본값 원칙과 일관된다.

**검증방안**: PC/SIL 상태전이 시험으로 (1) TRUE→FALSE 전환 엣지에서 RELEASE+OFF 확인, (2) FALSE
지속 구간에 `Driver_Command` 주입 시 무시됨을 확인, (3) FALSE→TRUE 재전환 직후 출력이 RELEASE로
유지됨을 확인(직전 LOCK 상태였더라도), (4) `ignition_on` 필드에 형식 오류를 주입해 (1)과 동일하게
처리됨을 확인. 실행 가능 여부: 확인됨(상태전이 기법).

**추적 링크**: 상위 OEM-FR-007 / SWR-004(우선순위 피적용 측)와의 관계는 §8 참조.

### 4.2 안전 관련 SW 요구사항

해당 없음. 이번 Phase 1(SWR-001, SWR-002, SWR-004, SWR-020)은 모두 OEM 문서상 **QM** 등급이며,
ASIL B 안전 요구(OEM-SR-001~004)는 Phase 2(`feature/phase2-safety-arbitration`)에서 별도 SWR로
도출한다. 다만 §8에서 Phase 2 안전 중재 로직이 본 Phase의 출력을 나중에 덮어쓸 수 있도록 아키텍처
설계 여지를 남겨야 한다는 점을 설계 고려사항으로 기록한다.

## 5. 입력 데이터 사전

| 명칭 | 자료형 | 허용값/범위 | 단위 | 유효성 조건 | 오류 처리 |
|---|---|---|---|---|---|
| `side` | enum(string) | `left`, `right`, `all` | - | 3개 값 중 하나, 결측 불가 | 누락/미등록 값 → SWR-001(b) 거절 |
| `action` | enum(string) | `lock`, `unlock` | - | 2개 값 중 하나, 결측 불가 | 상동 |
| `source` | enum(string) | `physical_button`, `avn`, `voice`, `mobile_app` | - | 4개 값 중 하나, 결측 불가 | 상동 |
| `ignition_on` | boolean | `TRUE`, `FALSE` | - | 누락/형식 오류 → `INVALID`(OEM-IF-009) | `INVALID` 판정 시 SWR-020(b)에 따라 `FALSE`와 동일하게 RELEASE+OFF로 처리한다(사용자 확정, 2026-09-18) |
| `timestamp_s` | float | ≥ 0 | 초(s) | `VehicleSnapshot` 평가주기 시각. `Driver_Command` 수신 시각 판단에 사용(OEM-IF-004) | 형식 오류 시 해당 평가주기 스냅샷 전체를 무효로 처리(가정, §8) |

**평가주기 입력 구조(가정)**: OEM 문서에 명시적 스키마는 없으나, OEM-IF-004의 "요청 시각은
`VehicleSnapshot.timestamp_s` 사용"이라는 표현으로부터, 매 평가주기마다
`VehicleSnapshot { timestamp_s, ignition_on, driver_command? }` 형태의 입력이 SW에 제공되고
`driver_command`는 그 주기에 명령이 없으면 부재(optional)라고 가정한다. 이 가정은 §8에 명시하며
아키텍처 설계 단계에서 확정이 필요하다.

## 6. 외부 인터페이스 요구

| 인터페이스 ID | 방향 | 필드 | 값/열거형 | 오류 처리 | 본 Phase 반영 범위 |
|---|---|---|---|---|---|
| OEM-IF-004 | Driver → SW | `side`, `action`, `source` | §5 참조 | 누락/형식/미등록 enum 거절(SWR-001b). 요청 시각은 `VehicleSnapshot.timestamp_s` 사용 | 전체 반영 |
| OEM-IF-005 | SW → Actuator model | `lock_left`, `lock_right` | `LOCK`, `RELEASE` | 정의 없음(PC/SIL 논리 출력까지만 검증) | 전체 반영 (SWR-004, SWR-020의 출력 대상) |
| OEM-IF-006 | SW → Display | `state`, `reason_code` | `state`: 최소 `LOCKED_LEFT`, `LOCKED_RIGHT`, `LOCKED_ALL`, `RELEASED`, `OFF`(가정, §8). `reason_code`: 최소 `INVALID_COMMAND`(SWR-001b), `IGNITION_OFF`(SWR-020) | 정의 값 외 미정 | **부분 반영** — `priority_reason`, `input_validity` 필드는 Phase 4(관측성)에서 확장 |
| OEM-IF-009 | Vehicle → SW | `ignition_on` | boolean | 누락/형식 오류 → `INVALID` | **부분 반영** — `sensor_fault` 필드는 Phase 2 범위 |

`state`/`reason_code`의 구체적 열거형 값은 OEM 원문에 목록이 제시되지 않아 이 문서에서 최소 필요
집합으로 정의했다(가정, §8) — 아키텍처/상세설계 단계에서 확정 및 확장 여부를 재검토해야 한다.

## 7. 비기능 및 환경 제약

이번 Phase에서 다루는 OEM-FR-001/OEM-FR-007에는 OEM 문서상 별도의 성능·신뢰성 비기능 요구사항이
연결되어 있지 않다(OEM-NFR-001 결정론적 재현, OEM-NFR-002 이벤트 로그는 Phase 4 범위이며 본 문서에서
SWR로 도출하지 않는다). 다만 실행 환경 제약은 ISO 25010 "호환성" 특성과 연계해 다음과 같이 명시한다.

| 항목 | 내용 | ISO 25010 특성 | 검증방안 |
|---|---|---|---|
| 실행 환경 제약 | SW는 Python 3.12 인터프리터 기반 PC/SIL 환경에서 실행 가능해야 한다(OEM 문서 §3 제품 경계 인용, VJ-ECL-2026 CLAUDE.md 재정의 항목과 일치) | 호환성(공존성) | PC/SIL 실행 스크립트를 Python 3.12 인터프리터로 기동해 정상 초기화됨을 확인(CI 워크플로 또는 로컬 `python --version` 확인 후 실행). 실행 가능 여부: 확인됨 — 프로젝트 CLAUDE.md에 명시된 환경으로 기존 CI 구성과 일치 여부는 아키텍처 단계에서 재확인 필요 |

이 항목은 별도 SWR ID를 배정하지 않는다(OEM 문서 §9 번호 계획에 해당 항목이 없음) — 프로젝트 공통
제약으로 취급한다.

## 8. 분석 결과와 가정

### 가정

1. 매 평가주기 입력은 `VehicleSnapshot { timestamp_s, ignition_on, driver_command? }` 구조로
   제공된다(§5). OEM 원문에 명시적 스키마가 없어 추론했으며, 아키텍처 설계 시 확정이 필요하다.
2. 한 평가주기에는 최대 1건의 `Driver_Command`만 존재한다(사용자 확정, 2026-09-18 — 입력 구조 자체가
   평가주기당 단일 명령을 전제하며, 복수 명령 동시 도착은 설계상 발생하지 않는 것으로 취급한다).
3. SWR-004의 "선택되지 않은 나머지 출력 유지"는 직전 평가주기 값을 보존한다는 의미로 해석했다.
   시스템 최초 기동 시 초기값은 `RELEASE`로 가정한다(OEM-FR-007의 ignition-off 초기 해제 요구와
   일관성을 맞춤). `ignition_on`이 FALSE(또는 INVALID)에서 TRUE로 재전환된 직후에도 동일하게
   `RELEASE`를 유지한다 — 직전 래치 명령은 복원하지 않는다(SWR-020(c), 사용자 확정, 2026-09-18).
4. `OEM-IF-006`의 `state`/`reason_code` 열거형 값은 §6에서 최소 필요 집합으로 정의했다(가정) —
   Phase 4에서 `priority_reason`, `input_validity`와 함께 재검토 필요.

### 의존성

- SWR-004(side 적용)의 출력은 SWR-020(ignition-off)의 입력 조건에 영향을 받는다(아래 상충 해소
  참조).
- 본 문서의 4개 SWR은 아직 아키텍처 설계(G2)로 할당되지 않았으므로, §9의 "설계 요소" 열은 모두
  미정이다 — 이는 G1(요구사항 확정) 시점에서는 정상이며, G2 완료 시 갱신되어야 한다.

### 상충 사항과 해소

- SWR-002/SWR-004가 산출하는 `lock_left`/`lock_right` 값과 SWR-020(`ignition_on=FALSE` 시 강제
  RELEASE)이 동시에 성립하는 평가주기가 있을 수 있다. **해소**: SWR-020의 강제 RELEASE가 SWR-002/
  SWR-004의 산출값보다 항상 우선 적용된다(SWR-020 설명에 명시). 이 우선순위는 요구사항 문구로
  고정하되, 실제 중재(arbitration) 로직의 위치는 아키텍처 설계 단계에서 결정한다.
- Phase 2에서 도입될 안전 요구(OEM-SR-001~004, ASIL B)가 본 Phase의 명령 처리 결과를 다시 덮어쓸
  가능성이 있다. 본 문서는 이를 금지하거나 확정하지 않으며, 아키텍처가 우선순위 중재 계층을 나중에
  삽입할 수 있는 구조를 갖도록 설계 고려사항으로만 남긴다(§4.2 참조).

### 확정 사항 (2026-09-18, 사용자 확인 완료)

애초 §8 초안에서 미결정으로 남겼던 3건은 사용자 확인을 거쳐 아래와 같이 확정했다(모두 안전측
기본값 원칙 적용).

1. `ignition_on`이 다시 `TRUE`로 전환된 직후 출력은 직전 래치 명령을 복원하지 않고 무조건
   `RELEASE`를 유지한다 → SWR-020(c)에 반영.
2. 한 평가주기에는 최대 1건의 `Driver_Command`만 존재한다고 확정(위 가정 2 참조) — 복수 명령 동시
   도착에 대한 별도 중재 로직은 설계하지 않는다.
3. `ignition_on`이 `INVALID`로 판정되면 `FALSE`와 동일하게 처리한다(RELEASE+OFF) → SWR-020(b), §5에
   반영.

문서 검토자·승인자는 사용자 본인(jaehwan2.lee@hlcompany.com)으로 지정했다(문서 통제 섹션 참고,
실제 승인은 Phase 1 종료 시 종합 리뷰에서 처리).

## 9. 하향 할당 및 검증 계획

| SWR ID | 설계 할당 대상(예정) | 검증 수준 | 검증 방법(개요) | 계획된 증거 |
|---|---|---|---|---|
| SWR-001 | 미정 — G2 아키텍처 설계에서 입력 검증 컴포넌트에 배정 예정 | PC/SIL/Web | 동등분할(유효 enum 조합) + 오류추정(누락/형식/미등록 enum) | Phase 1 시스템시험 결과(G4, `sw-system-test` 스킬 산출물, `docs/SoftwareVerification/`) |
| SWR-002 | 미정 — G2에서 명령 디스패치 컴포넌트에 배정 예정 | PC/SIL/Web | source 4종 동등클래스 반복 실행 및 출력 동등성 비교 | 상동 |
| SWR-004 | 미정 — G2에서 출력 적용 컴포넌트에 배정 예정 | PC/SIL/Web | 진리표 기반 시험(3 side × 2 action × 2 사전상태) | 상동 |
| SWR-020 | 미정 — G2에서 점화상태 감시/출력 중재 컴포넌트에 배정 예정 | PC/SIL/Web | 상태전이 시험(ON→OFF 엣지, OFF 지속 구간, OFF→ON 재전환 후 RELEASE 유지, INVALID 판정 시 동일 처리) | 상동 |

G1(BL-SWR-1.0, 본 문서 승인) → G2(아키텍처/상세설계에서 위 "설계 할당 대상" 확정) → G3(구현/단위·
통합시험) → G4(위 "계획된 증거" 실제 생성)의 게이트 흐름을 따른다.

## 10. 범위 밖 주장

이 문서와 그 하위 증거(향후 G2~G4 산출물 포함)만으로 다음을 주장할 수 없다.

- ISO 26262 기능안전 적합성 또는 ASIL B 인증 — OEM-SR-001~004(Phase 2)와 Part 3 HARA는 본
  프로젝트 범위 밖(VJ-ECL-2026 CLAUDE.md 명시)이다.
- HIL/실차/ECU/HW 통합 검증 — PC/SIL 및 Web 시뮬레이터 검증까지만 유효하다.
- 주행 중 자동 잠금(OEM-FR-002), 접근위험 override(OEM-FR-003), 화재/과온/성인탑승 강제해제
  (OEM-FR-005), ISOFIX 강제잠금(OEM-FR-006) 동작 — Phase 2/3에서 별도 SWR로 다룬다.
- 상태조회 표시 전체 기능(OEM-FR-004), `priority_reason`/`input_validity` 표시 필드(OEM-IF-006
  나머지) — Phase 4(관측성) 범위다.
- 결정론적 재현(OEM-NFR-001), 휘발성 이벤트 로그 100건(OEM-NFR-002) 충족 — Phase 4 범위다.

## 11. 추적성

- 단일 진실 공급원: `docs/Traceability/traceability-matrix.md` (이번 작업에서 신규 생성, 아래 §
  참조). 이 문서의 SWR-001/002/004/020 행과 상위 OEM-FR-001/007 링크가 이미 반영되어 있다.
- 다이어그램 동기화: `SWR-PH1_requirements-trace.puml`(SysML `<<deriveReqt>>`/`<<refine>>`/
  `<<trace>>` 관계)의 관계는 매트릭스와 항상 일치해야 한다 — 현재 일치 상태(둘 다 SWR-001/002/004
  ← OEM-FR-001, SWR-020 ← OEM-FR-007).
- 하향 링크(설계 요소, 시험 케이스)는 G1 시점 특성상 아직 "미정"이며, G2(아키텍처/상세설계)와
  G4(시스템시험)에서 매트릭스가 갱신되어야 한다. 이는 고아 요구사항이 아니라 게이트 진행에 따른
  예정된 공백이며, §9에 배정 계획을 기록해 추적 가능하게 했다.

## 12. 참고자료

| 자료 | 식별정보/버전 | 적용 범위 |
|---|---|---|
| OEM SW 요구사항 사양서 | `OEM_Sample/OEM-SWR-001_OEM SW 요구사항 사양서.docx`, BL-OEM-1.0 | OEM-FR-001, OEM-FR-007, OEM-IF-004/005/006/009 원문 근거 |
| 회사 지정 템플릿 | `WP_Templates/Engineering/SoftwareRequirementsAnalysis/TPL-SWE1-001_SW 요구사항 명세서 템플릿.docx` | 본 문서의 절/표 구조 근거 |
| 요구사항 분석 스킬 | `.claude/skills/requirements-analyst/SKILL.md` 및 `references/*` | EARS 작성법, ISO 25010 체크리스트, 추적성 매트릭스 형식, SysML/PlantUML 가이드 |
| ISO/IEC/IEEE 29148 | 프로젝트 첨부 원문 없음 — 조항 인용 필요 시 공식 표준 문서 별도 확인 필요 | 요구사항 명세 구조 일반 원칙 |
| ISO 26262 Part 6/8 | 프로젝트 첨부 원문 없음 — 조항 인용 필요 시 공식 표준 문서 별도 확인 필요 | 단위/요구사항 명세 원칙 (Phase 2 안전 요구 도출 시 재확인 필요) |
| A-SPICE v4.1 | 프로젝트 첨부 원문 없음 — 조항 인용 필요 시 공식 표준 문서 별도 확인 필요 | SYS.1/SYS.2/SWE.1 프로세스 정합성 |
| VJ-ECL-2026 프로젝트 정책 | `VJ-ECL-2026/CLAUDE.md`, 저장소 루트 `CLAUDE.md` | 실행 환경(Python 3.12), ID 번호 계획, Phase 게이트 흐름 |
