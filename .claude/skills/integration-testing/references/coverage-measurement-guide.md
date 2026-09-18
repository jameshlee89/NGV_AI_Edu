# 함수 커버리지 · Call 커버리지 측정 가이드

SKILL.md §5에서 사용한다. **두 지표 모두 실제로 측정한 값을 근거로 보고한다 — 추정하거나 "커버할
것"이라고 단정하지 않는다.**

## 0. 사전 확인

```
python --version
python -m pip show coverage 2>&1   # 설치 여부 확인 (없으면 오류 출력됨)
```

`coverage`(coverage.py) 패키지가 없으면 `python -m pip install coverage`로 설치가 필요함을 사용자에게
먼저 안내한다. 설치 전에는 커버리지 수치를 단정하지 않는다.

> Python 표준 라이브러리(`ast`, `sys`)만으로 만드는 아래 Call 커버리지 측정 스크립트는 이 프로젝트를
> 위한 실용적 방법이다. Python 생태계에는 "Call 커버리지"를 표준 지표로 제공하는 널리 쓰이는 오픈소스
> 도구가 따로 없으므로(자동차 업계의 상용 도구는 이를 기본 제공하는 경우가 있음), 조직에 이미 그런
> 상용/사내 도구가 있다면 이 스크립트 대신 그 도구의 보고서를 우선 사용한다.

## 1. 함수 커버리지 측정

`coverage.py`로 실제 실행된 라인을 얻고, `ast`로 각 함수의 라인 범위를 구해 "함수 본문에 실행된
라인이 하나라도 있는가"로 함수 커버리지를 계산한다.

### 1.1 통합시험 실행하며 커버리지 수집

```
coverage run -m unittest discover -s <통합시험 디렉터리>
coverage json -o coverage.json
```

### 1.2 함수 단위로 집계하는 스크립트

```python
"""
\brief coverage.json과 소스 AST를 이용해 파일별 함수 커버리지를 계산한다.
"""
import ast
import json
import sys


def buildFunctionRanges(sourcePath):
    with open(sourcePath, "r", encoding="utf-8") as sourceFile:
        tree = ast.parse(sourceFile.read(), filename=sourcePath)
    ranges = []
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            ranges.append((node.name, node.lineno, node.end_lineno))
    return ranges


def calcFunctionCoverage(coverageData, sourcePath):
    fileEntry = coverageData["files"].get(sourcePath)
    if fileEntry is None:
        raise KeyError(f"coverage.json에 {sourcePath} 항목이 없습니다 (경로 표기 확인 필요)")
    executedLines = set(fileEntry["executed_lines"])
    ranges = buildFunctionRanges(sourcePath)
    uncoveredFunctions = []
    coveredCount = 0
    for funcName, startLine, endLine in ranges:
        bodyLines = set(range(startLine + 1, endLine + 1))
        if bodyLines & executedLines:
            coveredCount += 1
        else:
            uncoveredFunctions.append(funcName)
    total = len(ranges)
    ratio = (coveredCount / total * 100.0) if total else 100.0
    return ratio, uncoveredFunctions


if __name__ == "__main__":
    with open("coverage.json", "r", encoding="utf-8") as jsonFile:
        coverageData = json.load(jsonFile)
    for targetPath in sys.argv[1:]:
        ratio, missing = calcFunctionCoverage(coverageData, targetPath)
        print(f"{targetPath}: 함수 커버리지 {ratio:.1f}% (미달 함수: {missing})")
```

**주의**: `coverage.json`의 `files` 키는 coverage.py가 기록한 경로 표기(상대/절대)를 그대로 쓴다.
스크립트에 넘기는 경로가 그 표기와 일치하는지 먼저 `coverage.json`을 열어 확인한다.

### 1.3 판정

- 통합 대상 소스의 모든 파일에 대해 위 스크립트를 실행하고, `uncoveredFunctions`가 빈 목록이어야
  함수 커버리지 100%로 판정한다.
- 미달 함수가 있으면 그 함수를 실제로 호출하는 통합시험 케이스를 추가한다.

## 2. Call 커버리지 측정

"아키텍처 인터페이스에 대응하는 호출과 상세설계 호출관계에 정의된 모든 호출 지점이 실제로
실행되었는가"를 측정한다. 두 단계로 진행한다: (1) 기대 호출 집합 정의, (2) 실제 실행된 호출 집합
수집 후 비교.

### 2.1 기대 호출 집합 (분모) — 설계 문서에서 도출

아키텍처 설계서 인터페이스 명세(6장)와 상세설계서 상세 호출관계(3장)에 이미 정의된 호출자→피호출자
쌍을 정리해 JSON으로 관리한다(이 목록 자체가 SKILL.md §9 추적성 자료와 같다).

```json
[
  {"interface": "IF-021", "caller": "order_service.py:submitOrder", "callee": "payment_gateway.py:chargeCard"},
  {"interface": "IF-022", "caller": "order_service.py:submitOrder", "callee": "inventory_service.py:reserveStock"}
]
```

- 정적 분석(`ast`로 함수 본문의 `ast.Call` 노드를 찾아 호출 대상 이름을 뽑는 방법)으로 이 목록을
  보조적으로 점검할 수 있으나, Python의 동적 특성상 정적 분석만으로 호출 대상을 완전히 확정할 수
  없다. **설계 문서(아키텍처 인터페이스, 상세설계 호출관계)를 1차 근거로 삼고**, 정적 분석 결과와
  차이가 있으면 그 차이를 사용자에게 알린다.

### 2.2 실제 호출 집합 (분자) — 런타임 추적

`sys.settrace`로 통합시험 실행 중 발생한 모든 호출을 기록한다(표준 라이브러리만 사용).

```python
"""
\brief 통합시험 실행 중 발생한 함수 호출 쌍(caller, callee)을 기록하는 추적기.
"""
import json
import sys

callEdges = set()
targetDirs = []  # 통합 대상 소스 디렉터리 경로를 담아 필터링에 사용


def isTargetFile(filePath):
    return any(filePath.startswith(targetDir) for targetDir in targetDirs)


def traceCalls(frame, event, arg):
    if event == "call":
        calleeFile = frame.f_code.co_filename
        calleeName = frame.f_code.co_name
        callerFrame = frame.f_back
        if callerFrame is not None and isTargetFile(calleeFile):
            callerFile = callerFrame.f_code.co_filename
            callerName = callerFrame.f_code.co_name
            if isTargetFile(callerFile):
                callEdges.add((f"{callerFile}:{callerName}", f"{calleeFile}:{calleeName}"))
    return traceCalls


def startCallTracing(sourceDirs):
    targetDirs.extend(sourceDirs)
    sys.settrace(traceCalls)


def stopCallTracing(outputPath):
    sys.settrace(None)
    with open(outputPath, "w", encoding="utf-8") as outFile:
        json.dump(sorted(callEdges), outFile, ensure_ascii=False, indent=2)
```

`unittest`의 `setUpModule`/`tearDownModule` 또는 커스텀 테스트 러너 진입점에서
`startCallTracing([...])`과 `stopCallTracing("actual_calls.json")`을 호출해 통합시험 스위트 전체
실행 동안 호출을 수집한다.

**한계**: `sys.settrace`는 Python 함수 호출만 기록하며(C 확장 호출 제외), 실행 속도를 늦춘다(통합
시험 실행에만 한시적으로 적용하고 상시 활성화하지 않는다). 클래스 메서드는 `co_name`만으로는
동일 이름의 다른 클래스 메서드와 구분이 안 될 수 있음에 유의한다(파일 경로+이름으로 우선 구분하고,
모호하면 케이스별로 확인한다).

### 2.3 비교 및 판정

```python
"""
\brief 기대 호출 집합과 실제 실행된 호출 집합을 비교해 Call 커버리지를 계산한다.
"""
import json


def calcCallCoverage(expectedEdgesPath, actualEdgesPath):
    with open(expectedEdgesPath, "r", encoding="utf-8") as expectedFile:
        expected = json.load(expectedFile)
    expectedEdges = {(item["caller"], item["callee"]) for item in expected}
    with open(actualEdgesPath, "r", encoding="utf-8") as actualFile:
        actualEdges = {tuple(pair) for pair in json.load(actualFile)}
    coveredEdges = expectedEdges & actualEdges
    missingEdges = expectedEdges - actualEdges
    ratio = (len(coveredEdges) / len(expectedEdges) * 100.0) if expectedEdges else 100.0
    return ratio, missingEdges
```

- `missingEdges`가 비어 있어야 Call 커버리지 100%로 판정한다.
- 미달 호출이 있으면, 그 호출 경로를 실제로 발생시키는 통합시험 케이스(자극 조건)를 추가한다.

## 3. 100% 미달 시 처리

1. 먼저 커버되지 않은 함수/호출을 실제로 실행시키는 통합시험 케이스를 추가해 재실행한다.
2. 추가로도 도달할 수 없는 코드/호출이 있다면(예: 설계상 진입 불가능함이 이미 증명된 방어적 코드),
   임의로 "커버된 것으로 간주"하지 않는다 — 사용자에게 근거를 확인받고, TPL-SWE5-001 12장(적용
   한계)과 TPL-SWE5-003 실행 요약(Limitation)에 함수/호출 식별자와 사유를 명시적으로 기록한다.
3. 위 절차 없이 100% 미만 상태를 "허용 가능"으로 넘기지 않는다.
