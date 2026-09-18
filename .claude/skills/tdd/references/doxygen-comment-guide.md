# Python용 Doxygen 호환 주석 작성 가이드

SKILL.md §4에서 사용한다. CLAUDE.md 구현 지침의 "주석은 Doxygen 방식으로 작성하며, 20% 이상 작성해야
한다"를 구체화한다.

## 1. 기본 형식

Doxygen은 Python 소스도 지원하며, 함수/클래스 docstring 안에 `\명령어` 또는 `@명령어` 형식의 태그를
쓰는 방식을 그대로 인식한다. 이 프로젝트에서는 아래 태그를 기본으로 사용한다.

```python
def calculateTotalDistance(pointA, pointB):
    """
    \brief 두 좌표 사이의 유클리드 거리를 계산한다.

    \param pointA 시작 좌표 (x, y) 튜플
    \param pointB 끝 좌표 (x, y) 튜플
    \return 두 좌표 사이의 거리 (float, 0 이상)
    \exception ValueError pointA 또는 pointB가 None이면 발생

    상세설계 근거: UNIT-012 / FN-034 (사전조건: 두 좌표 모두 not None,
    사후조건: 반환값은 0 이상의 실수)
    """
    if pointA is None or pointB is None:
        raise ValueError("좌표는 None일 수 없습니다")
    dx = pointA[0] - pointB[0]
    dy = pointA[1] - pointB[1]
    return (dx ** 2 + dy ** 2) ** 0.5
```

## 2. 필수 태그

| 태그 | 용도 | 필수 여부 |
|---|---|---|
| `\brief` | 함수/클래스의 한 줄 요약 | 모든 공개 함수/클래스에 필수 |
| `\param` | 매개변수별 의미와 유효 범위 | 매개변수가 있으면 필수 |
| `\return` | 반환값의 의미와 유효 범위 | 반환값이 있으면 필수 |
| `\exception` | 발생 가능한 예외와 조건 | 예외를 던지는 함수는 필수 |
| `\note` / `\warning` | 부작용, 시간 제약, 주의사항 | 해당하는 경우 권장 |

## 3. 추적성 포함

- 상세설계서의 단위 ID(`UNIT-XXX`)와 함수 계약 ID(`FN-XXX`)를 docstring 마지막 줄에 남겨, 코드만
  보고도 어떤 설계 근거로 작성되었는지 알 수 있게 한다.

## 4. 20% 주석 비율을 채우는 방법

- 의미 없는 반복 주석(`# i를 1 증가시킨다` 같은 코드 그대로 말로 옮긴 주석)으로 비율을 채우지 않는다.
- 대신 다음을 우선적으로 문서화해서 자연스럽게 비율을 채운다.
  - 모든 공개 함수/클래스의 Doxygen docstring(§1~§2)
  - 복잡한 알고리즘/정책 의사결정표를 구현한 부분의 "왜 이렇게 처리하는가" 설명
  - 방어적 코드(입력 검증, 예외 처리)가 어떤 상세설계 근거로 존재하는지 설명
  - 비직관적인 상수/매직넘버의 유래 설명
- 실제 비율은 `references/quality-metrics-tools.md` §4의 `cloc` 측정으로 확인한다.

## 5. 클래스 문서화 예시

```python
class OrderProcessor:
    """
    \brief 주문 처리 흐름을 담당하는 컴포넌트.

    아키텍처 요소 ARC-007(주문처리기)의 구현체이며, IF-021(주문접수) 인터페이스를 제공한다.
    """
```

## 6. 테스트 함수 주석은 별도 규칙 적용

이 문서는 **프로덕션 함수/클래스**의 Doxygen 주석 규칙이다. 테스트 함수(`unittest` 메서드)는
`\brief`/`\param`/`\return` 대신 목적 설명(`\brief`)·사용 기법(`\technique`)·긍정/부정 케이스 여부
(`\testtype`)를 기록해야 하며, 자세한 규칙과 예시는
`references/test-documentation-guide.md`를 따른다.
