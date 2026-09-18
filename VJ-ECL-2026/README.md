# VJ-ECL-2026 — 전자식 후석 차일드락 제어 SW

가상 OEM-A 공급자 입력 사양(`OEM_Sample/OEM-SWR-001_OEM SW 요구사항 사양서.docx`)을 근거로,
A-SPICE 기반 분석→아키텍처 설계→상세설계→구현→통합/시스템 시험 생명주기를 따라 개발하는 교육용
프로젝트입니다. 개발 정책은 이 폴더의 `CLAUDE.md`(프로젝트 재정의 포함)와 저장소 루트 `CLAUDE.md`를
함께 따릅니다.

## Phase 진행 현황

| Phase | 브랜치 | 다루는 OEM 요구 | 상태 |
|---|---|---|---|
| 1. 핵심 골격 + 수동 제어 | `feature/phase1-core-manual-control` | FR-001, FR-007 | 진행 중 |
| 2. ASIL B 안전 로직·우선순위 중재 | `feature/phase2-safety-arbitration` | SR-001~004, FR-003 | 예정 |
| 3. 추가 강제 제어 | `feature/phase3-forced-control` | FR-002, FR-005, FR-006 | 예정 |
| 4. 관측성·결정론·Web | `feature/phase4-observability-web` | FR-004, NFR-001, NFR-002 | 예정 |

각 Phase는 분석(G1)→아키텍처/상세설계(G2)→구현/단위·통합시험(G3)→시스템시험(G4)을 모두 거친 뒤
사용자 리뷰·승인을 받아 `main`에 병합합니다.
