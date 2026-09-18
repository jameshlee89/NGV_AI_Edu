# 회사 지정 통합시험 템플릿

이 템플릿은 이미 저장소에 있다. 통합시험 산출물을 작성할 때는 항상 아래 원본을 복사해서 사용한다.

## 템플릿 위치

- 통합전략 및 통합시험 명세서: `WP_Templates/Engineering/
  SoftwareComponentVerificationAndIntegrationVerification/TPL-SWE5-001_SW 통합전략 및 통합시험
  명세서 템플릿.docx`
- 통합시험 케이스: `WP_Templates/Engineering/SoftwareComponentVerificationAndIntegrationVerification/
  TPL-SWE5-002_SW 통합시험 케이스 템플릿.xlsx`
- 통합시험 결과서: `WP_Templates/Engineering/SoftwareComponentVerificationAndIntegrationVerification/
  TPL-SWE5-003_SW 통합시험 결과서 템플릿.xlsx`
- 상위 입력(시험 베이시스) 산출물 템플릿: `WP_Templates/Engineering/SoftwareArchitecturalDesign/
  TPL-SWE2-001/002` — `architecture-design` 스킬 참고 (인터페이스 명세, 통합 전략/순서)
- 관련 입력(구현 상세): `WP_Templates/Engineering/SoftwareDetailedDesignAndUnitConstruction/
  TPL-SWE3-001/002` — `detailed-design` 스킬 참고 (함수 계약, 상세 호출관계)
- 템플릿 등록부(적용 산출물/실제 파일 위치 기록): `WP_Templates/PRC-TPL-001_표준 산출물 양식
  등록부.xlsx`
- 작성 규칙(파일명 형식 등): `WP_Templates/Engineering/README.md`

## TPL-SWE5-001 장 구성 (실제 원본에서 추출)

표지: 템플릿 ID(`TPL-SWE5-001`), 적용 프로세스(`SWE.5`), 프로젝트, 작성 문서 ID/명칭, 버전 및
베이스라인, 작성자/검토자.

문서 통제: 변경 이력(Revision/변경일/작성 역할/변경 내용/검토 상태), 작성·검토·승인 상태(구분/역할
또는 성명/상태/일자/증거 위치).

목차 이하 본문 14개 장:

1. 목적 및 적용범위
   1.1 목적 — 문서가 지원하는 개발/검증 활동과 기대 결과
   1.2 적용범위 — 적용 제품, SW 구성요소, 생명주기 단계, 대상 조직
   1.3 적용 경계 — 포함/제외 범위, 외부 조직·상위 산출물과의 경계
2. 통합 원칙 — 통합 단위, 단계, 위험 우선순위, 반복 가능성, 실패 격리 원칙
3. 통합 항목과 순서 — 통합 항목 ID, 선행조건, 의존성, 순서, 담당, 계획 베이스라인
4. 환경 및 형상 — 도구, 실행환경, 소프트웨어 버전, 시험 데이터, 형상 식별 방법
5. 진입 및 종료 기준 — 각 통합 단계의 시작/중단/재개/완료 판정 기준
6. 통합시험 케이스 요약 — 인터페이스/통합 위험을 다루는 시험 ID, 추적 대상, 기대결과, 자동화 여부
7. 시험 설계기법 — 경계값, 동등분할, 의사결정표, 상태전이 등 기법의 선정 근거와 적용 대상
8. 실행 및 결과 기록 규칙 — 실행 식별자, 시각, 환경, 실제결과, 증거 위치, 결함 연결 방법
9. 회귀 전략 — 변경 영향에 따른 회귀 범위 선정, 자동 실행, 결과 비교 방법
10. 실패 및 편차 처리 — 시험 실패/환경 문제/계획 편차 분류, 보고, 재시험, 승인 절차
11. 추적성과 보고 — 아키텍처 인터페이스, 시험 케이스, 실행 결과, 결함, 보고서 간 연결
12. 적용 한계 — 통합시험으로 확인하지 못하는 시스템/HIL/차량/양산 환경 범위
13. 추적성 — 입력 설계·형상, 시험 명세, 결과, 결함 기록의 양방향 추적
14. 참고자료 — 아키텍처, 상세설계, 검증 계획, 환경 정의, 사용 도구 자료

## TPL-SWE5-002 (통합시험 케이스) 열 구성

`Test ID | Trace | Integration Item | Stimulus | Expected Result | Technique | Automation`

## TPL-SWE5-003 (통합시험 결과서) 시트 구성

- 시트1(케이스별 결과): `Test ID | Trace | Result | Actual Result | Evidence Locator | Defect ID |
  Disposition`
- 시트2(실행 요약): `Run ID | Date | Baseline | Environment | Planned | Pass | Fail | Overall |
  Limitation`

## 적용 방법

- 새 산출물 작성 시 위 템플릿들을 복사한 뒤 `WP_Templates/Engineering/README.md` 규칙대로
  `<산출물 ID>_<산출물명>.<확장자>` 형식으로 파일명을 바꾸고 실제 프로젝트 정보를 채운다.
- SKILL.md §1 표는 위 14개 장 구성을 그대로 옮긴 것이므로, 실제 작성 시에는 이 파일이 아니라 SKILL.md
  §1을 목차 기준으로 사용한다. 이 파일은 원본 템플릿 내용이 바뀌었는지 대조하는 참고용이다.
- 템플릿 원본이 갱신되거나 다른 경로로 교체되면, 이 파일과 SKILL.md §1을 함께 갱신한다.
