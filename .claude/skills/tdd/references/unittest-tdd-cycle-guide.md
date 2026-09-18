# 함수 계약 → unittest 케이스 변환 가이드

SKILL.md §1(Red-Green-Refactor)에서 사용한다. Red-Green-Refactor 사이클 자체와 "Verify RED/Verify
GREEN" 필수 확인 절차는 SKILL.md §1에 있으므로 여기서는 반복하지 않는다. 이 문서는 **상세설계서의
함수 계약을 실제 `unittest` 코드로 어떻게 옮기는지**에 집중한다.

## 1. 함수 계약 → 테스트 케이스 변환

상세설계서(`detailed-design` 스킬의 `function-contract-guide.md` 형식)의 각 항목을 테스트로 옮긴다.

| 계약 항목 | 테스트로 변환하는 방법 | 긍정/부정 |
|---|---|---|
| 사전조건을 만족하는 정상 입력 | 정상 케이스 테스트 | 긍정 |
| 사전조건 경계값(최소/최대/0/빈 값 등) | 경계값 케이스 테스트 | 대부분 긍정(경계 내 성공 기대 시) |
| 사전조건 위반 시 정의된 동작(오류 반환 등) | 방어 동작 검증 테스트 | 부정 |
| 사후조건 | 반환값/상태 변화를 정확히 검증하는 assert | 긍정 |
| 예외/오류 | `assertRaises` 또는 오류 반환값 검증 | 부정 |
| 시간 제약(해당 시) | 별도 성능/타이밍 테스트로 분리(단위 테스트와 혼합하지 않음) | — |

각 테스트에는 `references/test-documentation-guide.md`에 따라 `\brief`(목적/깨지는 지점),
`\technique`(사용 기법), `\testtype`(긍정/부정)을 Doxygen 형식으로 작성한다.

## 2. unittest 작성 규칙

- 파일명: `test_<대상모듈>.py`, 소스 모듈과 대응되는 위치에 둔다(예: `src/foo.py` →
  `tests/test_foo.py`, 프로젝트 관례가 있으면 그것을 따른다).
- 테스트 클래스는 `unittest.TestCase`를 상속하고, 클래스명은 `Test<대상>`으로 한다.
- 테스트 메서드명은 `test`로 시작하는 camelCase(예: `testReturnsDistanceForTwoPoints`)로 짓고,
  이름만으로 무엇을 검증하는지 알 수 있게 한다(`references/naming-convention.md` §5 예외 참고).
- 준비(Arrange)-실행(Act)-검증(Assert) 구조를 유지하고, 한 테스트 메서드는 하나의 시나리오만
  검증한다.
- 외부 자원(파일, 통신, 하드웨어)에 의존하는 코드는 `unittest.mock`으로 대체하되,
  `references/writing-good-tests.md`의 "적절한 수준에서 모의 처리" 원칙에 따라 느리거나 외부적인
  부분만 모의 처리하고 테스트가 실제로 검증해야 할 부분은 실제 코드로 유지한다.

### 예시

```python
import unittest
from mymodule import calculateTotalDistance

class TestCalculateTotalDistance(unittest.TestCase):
    def testReturnsDistanceForTwoPoints(self):
        """
        \\brief 두 좌표 사이의 유클리드 거리를 정확히 반환하는지 검증한다.
               (거리 계산식이 잘못 바뀌면 이 테스트는 실패해야 한다)
        \\technique 동등분할 (유효한 좌표 입력 클래스)
        \\testtype 긍정 (Positive)
        """
        result = calculateTotalDistance((0, 0), (3, 4))
        self.assertEqual(result, 5.0)

    def testReturnsZeroForIdenticalPoints(self):
        """
        \\brief 두 좌표가 동일하면 거리 0을 반환하는지 검증한다.
        \\technique 경계값분석 (동일 좌표)
        \\testtype 긍정 (Positive)
        """
        result = calculateTotalDistance((1, 1), (1, 1))
        self.assertEqual(result, 0.0)

    def testRaisesValueErrorForNoneCoordinate(self):
        """
        \\brief 좌표가 None이면 ValueError를 발생시키는지 검증한다.
        \\technique 오류추정 (None 입력)
        \\testtype 부정 (Negative)
        """
        with self.assertRaises(ValueError):
            calculateTotalDistance(None, (1, 1))
```

## 3. 테스트 실행

- `python -m unittest discover`(또는 프로젝트 관례에 맞는 경로 지정)로 전체 테스트를 실행하고,
  실행 로그(통과/실패 개수)를 실제로 확인한 뒤 결과를 보고한다. 실행하지 않고 "통과할 것"이라고
  단정하지 않는다. SKILL.md §1의 Verify RED / Verify GREEN 절차를 참고한다.
