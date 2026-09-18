# 테스트 문서화 규칙 — Doxygen 목적 설명 · 기법 · 긍정/부정 케이스

SKILL.md §7에서 사용한다. 이 프로젝트는 프로덕션 함수뿐 아니라 **테스트 함수에도** Doxygen 형식의
설명을 요구하며, 추가로 "어떤 기법으로 설계했는지"와 "긍정/부정 케이스인지"를 함께 기록한다.

## 1. 필수 태그

| 태그 | 내용 | 작성 규칙 |
|---|---|---|
| `\brief` | 이 테스트가 무엇을 검증하는지 | `references/writing-good-tests.md`의 "깨지는 지점 이름
  붙이기" 원칙에 따라 **"어떤 프로덕션 변경이 있으면 이 테스트가 실패해야 하는가"**를 함께 적는다.
  단순히 "동작을 확인한다"처럼 막연하게 쓰지 않는다. |
| `\technique` | 이 테스트를 설계한 기법 | §2 기법 목록에서 하나 이상 선택. 여러 기법을 함께 썼으면
  모두 나열한다. |
| `\testtype` | 긍정(Positive) / 부정(Negative) | §3 기준으로 정확히 하나를 선택한다. |

선택적으로 관련 상세설계 근거(`\see UNIT-XXX / FN-XXX`)를 추가해 추적성을 유지한다.

## 2. 기법(Technique) 목록

동등분할·경계값분석·오류추정의 일반적 정의는 `.claude/skills/sw-system-test/references/
test-design-techniques.md`를 단일 기준으로 삼는다 — 이 문서에서 다시 정의하지 않는다. 아래는 그
기법들을 **함수 계약(단위 수준)에 적용하는 방법**과, 단위 테스트에 특화된 추가 기법이다.

| 기법 | 단위 수준 적용/설명 | 사용 시점 |
|---|---|---|
| 동등분할 | 함수 매개변수를 유효/무효 클래스로 나누고 대표값으로 검증 | 입력 도메인이 넓을 때 |
| 경계값분석 | 함수 계약의 사전조건 경계값(최소/최대/0/빈 값 등)을 검증 | 범위·길이 제한이 있는 입력 |
| 오류추정 | 함수 계약 위반(None, 빈 문자열, 중복 호출 등)에 대한 방어 동작을 검증 | 방어적 코드
  (`error-handling-defensive-guide.md`) 검증 |
| 상태전이 테스트 (단위 수준 고유) | 상태 머신의 상태·전이·가드를 검증 | 상세설계서 8장(상태전이
  상세) 구현 검증 |
| 결정테이블 테스트 (단위 수준 고유) | 정책 의사결정표의 조건 조합별 기대 동작을 검증 | 상세설계서
  7장(정책 의사결정표) 구현 검증 |
| 버그 재현/회귀 (단위 수준 고유) | 실제 발견된 버그를 재현하는 실패 테스트를 먼저 작성 | 버그 수정 시 |
| 실제 컴포넌트 기반 (단위 수준 고유) | 모의 객체 없이 실제 의존 대상으로 검증 | 기본 선택지 —
  `writing-good-tests.md`에 따라 가능하면 항상 이 방식을 우선한다 |
| 통합형 단위 테스트 (단위 수준 고유) | 모의 처리 범위를 최소화하고 여러 실제 컴포넌트를 함께 실행 |
  모의 객체 준비가 테스트 로직보다 커질 때 |

목록에 없는 기법이 더 정확하면 이름을 붙여 사용해도 된다 — 다만 왜 그 기법을 선택했는지 `\brief`
또는 `\technique` 설명에 드러나야 한다.

## 3. 긍정(Positive) / 부정(Negative) 판정 기준

- **긍정(Positive)**: 함수 계약의 사전조건을 만족하는 입력에 대해, 사후조건대로 성공적으로 동작하는지
  검증한다(정상 케이스, 정상 범위의 경계값 포함).
- **부정(Negative)**: 사전조건 위반, 잘못된 입력, 예외 상황, 자원 실패, 정의된 오류 반환 등 실패
  경로가 계약대로 동작하는지 검증한다.
- 하나의 테스트가 두 성격을 섞지 않는다 — 정상 동작과 오류 처리를 함께 검증해야 한다면 테스트를
  분리한다(§2 최소성 원칙과 동일).

## 4. 작성 예시

```python
import unittest

class TestCalculateTotalDistance(unittest.TestCase):
    def testReturnsDistanceForTwoPoints(self):
        """
        \\brief 두 좌표 사이의 유클리드 거리를 정확히 반환하는지 검증한다.
               (거리 계산식이 잘못 바뀌면 이 테스트는 실패해야 한다)
        \\technique 동등분할 (유효한 좌표 입력 클래스)
        \\testtype 긍정 (Positive)
        \\see UNIT-012 / FN-034
        """
        self.assertEqual(calculateTotalDistance((0, 0), (3, 4)), 5.0)

    def testReturnsZeroForIdenticalPoints(self):
        """
        \\brief 두 좌표가 동일하면 거리 0을 반환하는지 검증한다.
               (경계값 처리가 누락되면 이 테스트는 실패해야 한다)
        \\technique 경계값분석 (동일 좌표)
        \\testtype 긍정 (Positive)
        \\see UNIT-012 / FN-034
        """
        self.assertEqual(calculateTotalDistance((1, 1), (1, 1)), 0.0)

    def testRaisesValueErrorForNoneCoordinate(self):
        """
        \\brief 좌표가 None이면 ValueError를 발생시키는지 검증한다.
               (None 검사를 제거하면 이 테스트는 실패해야 한다)
        \\technique 오류추정 (None 입력)
        \\testtype 부정 (Negative)
        \\see UNIT-012 / FN-034 (사전조건: 좌표는 None일 수 없음)
        """
        with self.assertRaises(ValueError):
            calculateTotalDistance(None, (1, 1))
```

## 5. 품질 지표와의 관계

- 이 문서화 규칙은 SKILL.md §6의 "주석 비율 20% 이상(Doxygen)" 산정에 테스트 코드도 포함됨을 뜻한다.
  형식적으로 태그만 붙이지 않고, 실제로 "무엇을 왜 검증하는지"를 설명하는 내용으로 채운다.
- 테스트 함수명은 `references/naming-convention.md`의 네이밍 규칙(3글자 이상, camelCase)을 따르되,
  `unittest`가 요구하는 `test` 접두사는 예외로 유지한다(`testReturnsDistanceForTwoPoints`처럼 `test`
  + camelCase 조합).
