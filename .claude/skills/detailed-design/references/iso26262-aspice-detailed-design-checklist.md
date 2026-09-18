# ISO 26262 Part 6 · A-SPICE(SWE.3) 상세설계 관련 체크포인트 (요약 — 원문 대조 필요)

> ⚠️ 아래는 상세설계 시 반영해야 할 항목을 정리한 **요약**이다. 실제 감사/인증 대응 문서에 절/표
> 번호나 원문을 인용해야 한다면, 이 요약만으로 단정하지 말고 프로젝트에 첨부된 공식 표준 문서로
> 정확한 번호와 문구를 확인한다.

## ISO 26262 Part 6 관점 (소프트웨어 단위 설계 및 구현)

- 소프트웨어 단위는 **높은 응집도와 낮은 결합도**, 제한된 크기/복잡도를 가져야 한다 —
  `references/unit-design-principles-checklist.md` §1~§3.
- 단위 설계는 **명확하고 검증 가능한 명세**(함수 계약: 입력/출력/사전조건/사후조건)를 가져야 한다 —
  SKILL.md §4, `references/function-contract-guide.md`.
- 구현에는 **구조화된 프로그래밍 원칙**(하나의 진입/종료점, 무조건 분기 회피, 제한된 포인터/재귀/
  인터럽트 사용, 강한 타입, dead code 금지 등)이 적용되어야 한다 —
  `references/unit-design-principles-checklist.md` §4.
- **방어적 프로그래밍**을 통해 유효하지 않은 입력이나 예상치 못한 상태에 대응해야 한다 — SKILL.md
  §6, `references/error-handling-defensive-guide.md`.
- 안전 관련(ASIL) 단위는 상위 아키텍처에서 정의한 오류 검출/안전 상태 개념을 실제 구현 수준에서
  일관되게 반영해야 한다. ASIL별 세부 요구 수준과 정확한 처리 방식은 이 요약만으로 확정하지 말고
  프로젝트의 공식 안전 분석/표준 문서를 함께 확인한다.
- 코딩 표준(정적분석 가능한 언어 서브셋 등) 준수와 코드 리뷰·정적분석·단위검증 계획이 필요하다 —
  SKILL.md §7.

## A-SPICE(SWE.3 소프트웨어 상세설계 및 단위 구축) 관점

- **아키텍처 설계 요소를 구현 가능한 소프트웨어 단위로 상세화**하고, 상세설계가 아키텍처와 일관되어야
  한다 — SKILL.md §2(아키텍처 정합성 확인).
- **소프트웨어 단위에 대한 요구사항 할당**이 이루어지고 완전성이 확인되어야 한다 — SKILL.md §8,
  템플릿 12장.
- 상세설계는 **단위시험(SWE.4)이 도출 가능할 정도로 구체적**이어야 한다 — 함수 계약(§4), 알고리즘/
  의사결정표(§5)의 명확성이 이를 뒷받침한다.
- **일관성 유지**: 상세설계가 소프트웨어 요구사항, 아키텍처 설계와 일관되어야 한다 — SKILL.md §2, §8,
  템플릿 14장(추적성).
- 정확한 Base Practice 번호/문구, 작업산출물(WP) 목록이 필요하면 `.claude/skills/aspice-auditor/
  references/aspice-source.md` 또는 공식 A-SPICE 4.1 문서를 확인한다(이미 저장소에 A-SPICE 감사
  스킬이 있으므로 중복 작성하지 않고 그쪽을 참조한다).

## 이 스킬이 두 표준을 만족시키는 방식 요약

| 표준 요건 | 이 스킬의 대응 |
|---|---|
| 아키텍처와의 일관성 | SKILL.md §2 |
| 높은 응집도 / 낮은 결합도 (단위 수준) | `unit-design-principles-checklist.md` §1~§3 |
| 구조화된 프로그래밍/단위 설계 원칙 | `unit-design-principles-checklist.md` §4 |
| 검증 가능한 함수 계약 | SKILL.md §4, `function-contract-guide.md` |
| 알고리즘/정책의 완전성·일관성 | SKILL.md §5, `algorithm-decision-guide.md` |
| 방어적 프로그래밍 | SKILL.md §6, `error-handling-defensive-guide.md` |
| 요구사항 할당 및 추적성 | SKILL.md §8, 템플릿 12·14장 |
| 단위시험 도출 가능성 | SKILL.md §7, §4~§5 |
