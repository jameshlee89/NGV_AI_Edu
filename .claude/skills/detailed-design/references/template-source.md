# 회사 지정 상세설계서 템플릿

이 템플릿은 이미 저장소에 있다. 상세설계 산출물을 작성할 때는 항상 아래 원본을 복사해서 사용한다.

## 템플릿 위치

- 설계서 본문: `WP_Templates/Engineering/SoftwareDetailedDesignAndUnitConstruction/TPL-SWE3-001_SW
  상세설계서 템플릿.docx`
- UML/호출관계 다이어그램: `WP_Templates/Engineering/SoftwareDetailedDesignAndUnitConstruction/
  TPL-SWE3-002_상세설계 UML 및 호출관계 템플릿.drawio`
- 관련 산출물(구현 단계, 이 스킬이 직접 채우지는 않음): `WP_Templates/Engineering/
  SoftwareDetailedDesignAndUnitConstruction/TPL-SBOM-001_Python 의존성 SBOM FOSS 라이선스 목록
  템플릿.xlsx` (적용 프로세스 SWE.3/SUP.8)
- 상위 입력(근거) 산출물 템플릿: `WP_Templates/Engineering/SoftwareArchitecturalDesign/
  TPL-SWE2-001/002` — `architecture-design` 스킬 참고
- 하위(다음 단계) 산출물 템플릿(이 스킬 범위 밖, 참고용): `WP_Templates/Engineering/
  SoftwareUnitVerification/TPL-SWE4-001/002`
- 템플릿 등록부(적용 산출물/실제 파일 위치 기록): `WP_Templates/PRC-TPL-001_표준 산출물 양식
  등록부.xlsx`
- 작성 규칙(파일명 형식 등): `WP_Templates/Engineering/README.md`

## TPL-SWE3-001 장 구성 (실제 원본에서 추출)

표지: 템플릿 ID(`TPL-SWE3-001`), 적용 프로세스(`SWE.3`), 프로젝트, 작성 문서 ID/명칭, 버전 및
베이스라인, 작성자/검토자.

문서 통제: 변경 이력(Revision/변경일/작성 역할/변경 내용/검토 상태), 작성·검토·승인 상태(구분/역할
또는 성명/상태/일자/증거 위치).

목차 이하 본문 15개 장:

1. 목적 및 적용범위
   1.1 목적 — 문서가 지원하는 개발/검증 활동과 기대 결과
   1.2 적용범위 — 적용 제품, SW 구성요소, 생명주기 단계, 대상 조직
   1.3 적용 경계 — 포함/제외 범위, 외부 조직·상위 산출물과의 경계
2. 모듈 분해 — 아키텍처 요소를 구현 단위로 분해, 각 단위의 ID·책임·소스 위치
3. 상세 호출관계 — 함수/클래스 간 호출 순서, 의존 방향, 주요 데이터 흐름
4. 공통 자료형 — 공통 데이터 구조, 열거형, 단위, 범위, 불변조건, 직렬화 규칙
5. 핵심 함수 계약 — 함수별 입력, 출력, 사전조건, 사후조건, 부작용, 예외, 시간 제약
6. 핵심 알고리즘 — 처리 순서, 판단 조건, 경계값, 계산 근거(의사코드/흐름도)
7. 정책 의사결정표 — 입력 조건 조합, 우선순위, 기대 동작, 충돌 해결 규칙
8. 상태전이 상세 — 상태 저장 위치, 전이 함수, 이벤트, 가드, 타이머, 초기화 동작
9. Web 및 API 상세 — 엔드포인트, 요청/응답 구조, 검증, 오류 코드, 세션/보안 경계
10. 오류와 방어 동작 — 유효하지 않은 입력/예외/자원 실패의 검출, 처리, 기록, 복구
11. 코딩 및 검증 규칙 — 코딩 표준, 정적분석, 단위검증, 커버리지, 리뷰 기준
12. 단위와 요구사항 할당 — 구현 단위를 아키텍처 요소, SW 요구사항, 단위시험에 연결
13. 구현 경계 — 생성 코드, 외부 라이브러리, 플랫폼 종속부, 구현하지 않는 범위
14. 추적성 — 아키텍처, 상세설계, 소스 파일, 함수, 단위시험 간 양방향 연결
15. 참고자료 — 아키텍처 설계서, 코딩규칙, API 문서, 외부 라이브러리 자료

## TPL-SWE3-002 (drawio) 구성 요소

- 시스템/설계 경계 영역, 외부 액터/요소
- 대상 요소 ID, 요소 명칭
- 관계 또는 인터페이스(함수/클래스 호출 표기 포함)
- 작성 안내: (1) 구현 단위와 책임 (2) 함수 또는 클래스 호출 (3) 입력 출력 자료형 (4) 설계 및 시험
  추적 ID

## TPL-SBOM-001 개요 (참고 — 이 스킬이 직접 채우지 않음)

- 적용 프로세스: `SWE.3/SUP.8`, 적용 산출물: `ENG-SBOM-001_Python 의존성·SBOM·FOSS 라이선스 목록`
- 열 구성: `Package | Version | Dependency Type | SPDX | Evidence Type | Evidence Locator |
  Distribution | Remark`
- 외부 라이브러리를 사용하는 상세설계/구현이 있으면, 이 표를 채워야 함을 사용자에게 안내한다
  (SKILL.md §10 참고).

## 적용 방법

- 새 산출물 작성 시 TPL-SWE3-001/002를 복사한 뒤 `WP_Templates/Engineering/README.md` 규칙대로
  `<산출물 ID>_<산출물명>.<확장자>` 형식으로 파일명을 바꾸고 실제 프로젝트 정보를 채운다.
- SKILL.md의 §1 표는 위 15개 장 구성을 그대로 옮긴 것이므로, 실제 작성 시에는 이 파일이 아니라
  SKILL.md §1을 목차 기준으로 사용한다. 이 파일은 원본 템플릿 내용이 바뀌었는지 대조하는 참고용이다.
- 만약 템플릿 원본이 갱신되거나 다른 경로로 교체되면, 이 파일과 SKILL.md §1을 함께 갱신한다.
