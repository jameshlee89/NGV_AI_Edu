# 브랜치 정책 및 기여 가이드

이 문서는 AI(Claude Code 등)를 활용한 "바이브 코딩"을 GitHub으로 운영할 때 일반적으로 권장되는
정책을 이 저장소에 적용한 것이다. 핵심 원칙은 하나다 — **AI가 생성한 변경이라도 `main`에는 항상
Pull Request와 자동화된 검증(CI)을 거쳐서만 들어간다.**

## 1. 브랜치 구조

- `main`: 항상 배포 가능한 상태를 유지하는 보호 브랜치. **직접 커밋/푸시하지 않는다.**
- 작업 브랜치는 `main`에서 분기하고, 아래 접두사로 목적을 표시한다.
  - `feature/<주제>` — 새 기능
  - `fix/<주제>` — 버그 수정
  - `chore/<주제>` — 빌드/설정/문서 등 잡무성 변경
  - `docs/<주제>` — 문서만 변경
- 작업 브랜치는 짧게 유지하고, 머지 후 삭제한다(아래 병합 전략 참고).

## 2. Pull Request 규칙

- 모든 변경은 PR을 통해서만 `main`에 반영한다(AI가 생성한 코드도 예외 없음).
- PR을 열면 `.github/pull_request_template.md`가 자동으로 채워진다 — 특히 "AI 활용 여부"와 "사람이
  직접 검토했는지" 체크박스는 비워두지 않는다.
- 최소 1명의 승인(review approval)을 받은 뒤 병합한다 — AI가 생성한 변경일수록 사람의 최종 검토가
  중요하다.
- 병합 전 이 저장소의 CI(`.github/workflows/ci.yml`)가 통과해야 한다.
- 병합 방식은 **Squash and merge**를 기본으로 한다 — AI 반복 작업 중 생기는 잦은 중간 커밋이 `main`
  히스토리를 어지럽히지 않도록 한다.
- 병합 후 작업 브랜치는 자동 삭제한다.

## 3. CI(지속적 통합/지속적 테스트)

`.github/workflows/ci.yml`이 `pull_request`(대상: `main`)와 `main`에 대한 `push`마다 자동 실행되며,
CLAUDE.md의 구현/테스트 지침을 게이트로 강제한다.

| 게이트 | 기준 | 도구 |
|---|---|---|
| 테스트 성공률 | 100% (실패 테스트 0건) | `unittest` |
| 단위 테스트 Branch 커버리지 | 100% | `coverage run --branch` + `coverage report --fail-under=100` |
| 함수 순환복잡도 | 10 이하 | `flake8`(mccabe), 설정: `.flake8` |
| 함수 라인수(순수코드) | 50줄 이하(근사: statement 수) | `pylint`(`too-many-statements`), 설정: `.pylintrc` |
| 중복 코드 | 7줄까지 허용(8줄부터 위반) | `pylint`(`duplicate-code`), 설정: `.pylintrc` |
| 네이밍 규칙 | 3글자 이상, camelCase | `pylint`(`invalid-name`), 설정: `.pylintrc` |

Python 소스가 아직 없는 동안(예: 이 저장소의 현재 상태)에는 위 게이트를 건너뛰고 통과 처리한다 —
Python 파일이 추가되는 즉시 자동으로 활성화된다.

> Doxygen 주석 비율(20% 이상)은 표준 CLI 플래그로 간단히 강제하기 어려워 이번 CI에는 포함하지 않았다.
> `tdd` 스킬의 `references/quality-metrics-tools.md` §4(`cloc` 기반 측정법)를 참고해 필요 시 추가
> 게이트로 확장할 수 있다.

## 4. 브랜치 보호 규칙 (GitHub 저장소 설정 — 수동 적용 필요)

**중요**: 아래 브랜치 보호 규칙은 GitHub 저장소의 서버 측 설정이라 이 저장소의 파일을 커밋/푸시하는
것만으로는 적용되지 않는다. 이 환경에는 `gh` CLI와 관리자 인증 토큰이 없어 Claude가 직접 적용할 수
없으므로, 저장소 관리자(Owner)가 아래 중 한 가지 방법으로 직접 적용해야 한다.

### 방법 A — GitHub 웹 UI

1. 저장소 `Settings` → `Branches` → `Add branch protection rule`
2. Branch name pattern: `main`
3. 다음 항목을 체크한다.
   - `Require a pull request before merging` (Require approvals: 1)
   - `Dismiss stale pull request approvals when new commits are pushed`
   - `Require status checks to pass before merging` → `Require branches to be up to date before
     merging` 체크 후, 첫 PR을 한 번 실행해 나타나는 체크 이름(예: `Build, Lint, Test`)을 필수 상태
     검사로 선택한다.
   - `Require conversation resolution before merging`
   - `Require linear history` (Squash merge 전략과 일치)
   - `Do not allow bypassing the above settings` (관리자 포함 — AI 작업에는 예외를 두지 않는 것을
     권장)
   - `Restrict deletions`, `Restrict force pushes` (또는 "Allow force pushes"를 체크하지 않음)
4. 저장소 `Settings` → `General` → `Pull Requests`에서 `Automatically delete head branches`를
   활성화한다.

### 방법 B — `gh` CLI (관리자 권한으로 인증된 환경에서 실행)

```bash
gh api --method PUT repos/jameshlee89/NGV_AI_Edu/branches/main/protection \
  --input - <<'EOF'
{
  "required_status_checks": {
    "strict": true,
    "contexts": ["Build, Lint, Test"]
  },
  "enforce_admins": true,
  "required_pull_request_reviews": {
    "required_approving_review_count": 1,
    "dismiss_stale_reviews": true
  },
  "restrictions": null,
  "required_linear_history": true,
  "required_conversation_resolution": true,
  "allow_force_pushes": false,
  "allow_deletions": false
}
EOF
```

`contexts`의 `"Build, Lint, Test"` 값은 `.github/workflows/ci.yml`의 job 이름과 정확히 일치해야
한다 — 워크플로우를 수정해 job 이름이 바뀌면 이 값도 함께 갱신한다. 첫 PR을 한 번 실행해 실제로 어떤
이름의 체크가 표시되는지 확인한 뒤 적용하는 것을 권장한다.

## 5. 커밋 메시지

- 무엇을 왜 바꿨는지 한두 문장으로 간결하게 작성한다(자세한 내용은 PR 설명에).
- AI가 생성한 커밋에는 이 저장소의 기존 관례대로 `Co-Authored-By:` 라인을 포함한다.
