# 회사 지정 SW 시스템 시험(검증) 템플릿

이 템플릿은 이미 저장소에 있다. SW 시스템 시험 산출물을 작성할 때는 이 템플릿을 핵심 열 구성의
기준으로 삼는다(§ SKILL.md "산출물 구조" 참고 — 기능/비기능 분리는 이 스킬의 추가 관례).

## 템플릿 위치

- 검증 명세서: `WP_Templates/Engineering/SoftwareVerification/TPL-SWE6-001_SW 검증 명세서
  템플릿.xlsx` (적용 프로세스 `SWE.6`)
- 검증 결과서: `WP_Templates/Engineering/SoftwareVerification/TPL-SWE6-002_SW 검증 결과서
  템플릿.xlsx` (적용 프로세스 `SWE.6`)
- 상위 입력(시험 근거) 산출물: 요구사항 명세서 — `requirements-analyst` 스킬 참고
- 템플릿 등록부: `WP_Templates/PRC-TPL-001_표준 산출물 양식 등록부.xlsx`
- 작성 규칙(파일명 형식 등): `WP_Templates/Engineering/README.md`

## TPL-SWE6-001 (검증 명세서) 시트 구성

- **Verification Specification**: `Test ID | SW Req | Level/Environment | Stimulus | Expected
  Result | Technique | Execution`
- **Environment**: `Environment ID | 구성 | 버전 및 식별 | 사용 범위 | 수집 증거 | 명시적 제외`
- **Change History**: `Revision | 변경일 | 작성 역할 | 변경 내용 | 검토 상태 | 승인 상태`

## TPL-SWE6-002 (검증 결과서) 시트 구성

- **Verification Results**: `Test ID | SW Req | Result | Actual Result | Evidence Locator |
  Execution Time | Scope Note`
- **Summary**: `항목 | 계획 | 실행 | Pass | Fail | 미실행 | 판정 | 제한`
- **Change History**: `Revision | 변경일 | 작성 역할 | 변경 내용 | 검토 상태 | 승인 상태`

## 이 스킬의 관례와 템플릿의 관계

- 템플릿의 `Verification Specification` 시트는 기능/비기능을 한 시트에서 `SW Req`로만 구분한다. 이
  스킬은 가독성을 위해 "테스트 케이스"(기능)와 "비기능 테스트 케이스"(ISO 25000 품질 특성별) 두
  시트로 나누는 관례를 추가하되, 템플릿의 핵심 열(Test ID, SW Req, Stimulus, Expected Result,
  Technique)은 두 시트 모두에 그대로 유지한다.
- 사전조건, 절차(단계), 우선순위 등 템플릿에 없는 열을 추가로 쓸 수 있다 — 확장 열이며, 정식 템플릿
  개정이 필요하다고 판단되면 템플릿 관리자(등록부 소유자)와 협의하도록 사용자에게 안내한다.
- 실행 결과는 TPL-SWE6-002 형식(Result/Actual Result/Evidence Locator 등)을 그대로 따른다.
