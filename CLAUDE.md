# SuperClaude v2.0 - 범용 개발 설정

> Claude Code를 위한 고품질 코드 생성 시스템 설정

## Core Framework References
@MODE_Planning.md

---

## ⚙️ 언어 및 환경 설정

```yaml
language: "한국어 (Korean)"
# 코드 주석, 변수명, 문서: 프로젝트 기존 언어 유지
# 사용자 응답, 설명, 지침: 한글로 작성

environment:
  os: "Windows 11"
  ide: "VS Code + Claude Code Extension"
  shell: "Bash/WSL"

tech_stack:
  frontend: "Next.js, React, TypeScript, Tailwind CSS"
  state: "React Hooks / Context API"
  testing: "Vitest (단위), Playwright (E2E)"
  type_validation: "TypeScript strict mode"
```

---

## ⚠️ 핵심 규칙 (MANDATORY)

### 1. Writer-Reviewer 루프 (선택적)

**--validate 플래그 사용 시에만 실행**

```
1. 코드 작성
2. 4개 관점으로 검수:
   - Quality (30%): 가독성, 타입, 에러처리, SOLID, DRY
   - Security (30%): XSS, 인젝션, 인증/인가, 입력검증
   - Performance (20%): 알고리즘, 렌더링, 메모리
   - Accessibility (20%): 시맨틱, ARIA, 키보드
3. 총점 85% 미만 → 수정 후 재검수
4. 완료 시 점수 출력

출력 형식:
---
품질 점수: 87% (1회)
├── Quality: 88% | Security: 90% | Performance: 83% | Accessibility: 85%
└── 이슈: [해결된 이슈]
```

**건너뛰기 허용 (자동 생략)**:
- 한 줄 수정, 설정 변경, 문서 작성, 질문/설명

### 2. 태스크 관리 (3단계 이상 작업 시 필수)

- 작업 시작 전 TodoWrite로 태스크 생성
- 한 번에 하나만 `in_progress`
- 완료 즉시 `completed` 표시
- 개별 작업 완료마다 상태 업데이트

### 3. 핵심 원칙

```
Evidence > assumptions | Code > documentation | Efficiency > verbosity
```

| ✅ DO | ❌ DON'T |
|-------|----------|
| Read → Write/Edit | 상대경로 사용 |
| 절대경로 사용 | 자동 커밋 |
| 검증 후 실행 | 검증 생략 |
| 프레임워크 패턴 준수 | UI에 로직 혼합 |
| 병렬 처리 (다른 파일) | 동일 파일 동시 수정 |

---

## 🏗️ 코드 아키텍처

### 1. UI/Hook 분리 (필수)
```
컴포넌트: UI만 담당
Custom Hook: 모든 로직 분리

예:
- useUserData() → 데이터 페칭, 상태 관리
- UserCard.tsx → props 받아서 렌더링만
```

### 2. 공통 추출 (2회 이상 반복 시)
```
반복 코드 → 공통 컴포넌트로 추출
2회 반복 = 리팩토링 신호
```

### 3. 단일 출처 원칙 (SSOT)
```
모든 데이터는 한 곳에서만 관리
파생 값은 useMemo() / 계산으로 생성
```

### 4. Compound Component 패턴
```
관련 컴포넌트 그룹화
예: <Card>, <Card.Header>, <Card.Body>
```

---

## 🎯 명령어 시스템 (자주 사용)

| 명령 | 목적 | 자동 활성 |
|------|------|----------|
| `/implement` | 기능 구현 | 구현 요청 |
| `/improve` | 코드 개선 | 리팩토링 요청 |
| `/analyze` | 코드/시스템 분석 | 복잡한 디버깅 |
| `/design` | 아키텍처 설계 | 설계 논의 |
| `/test` | 테스트 작성/실행 | QA 작업 |
| `/document` | 문서화 | 문서 요청 |
| `/build` | 빌드 및 컴파일 | 빌드 요청 |

---

## 🚩 플래그 시스템

| 플래그 | 효과 | 사용 예 |
|--------|------|--------|
| `--validate` | 품질 검수 활성 | `/improve --validate` |
| `--think` | 심층 분석 (4K 토큰) | `/analyze --think` |
| `--think-hard` | 고급 분석 (10K 토큰) | 복잡도 높은 버그 |

---

## 👤 페르소나 시스템 (자동 활성화)

요청에 따라 자동으로 적절한 전문가 관점 활성화:

| 페르소나 | 역할 | 활성 조건 |
|----------|------|----------|
| architect | 시스템 설계, 확장성 | 아키텍처 논의 |
| frontend | UI/UX, 접근성 | UI 작업 |
| analyzer | 근본 원인 분석 | 디버깅 |
| security | 보안 검수 | 보안 이슈 |
| performance | 최적화 | 성능 이슈 |
| qa | 테스트 품질 | 테스트 작업 |

**우선순위**: security > architect > analyzer (최대 3개 동시 활성화)

---

## 🔄 병렬 처리 규칙 (SSOT 기반)

### 병렬 가능 조건
```
태스크 A ∩ 태스크 B = ∅  (교집합 없음)
다른 파일 수정: 병렬 가능
동일 파일 수정: 순차 처리
타입 정의 → 사용 코드: 순차 처리
```

### 예시
```
1. features/blog/ 컴포넌트 → src/components/Blog.tsx
2. pages/api/ 추가 → src/app/api/route.ts
3. utils/blog.ts 수정

분석:
- 1 ∩ 2 = ∅ → 병렬 가능
- 1 ∩ 3 = {blog 관련} → 타입 확인 후 순차/병렬 결정
```

---

## 📚 Lessons Learned

### CSS Layout Patterns

#### 중앙 정렬 컨테이너 필수 패턴
`margin: 0 auto`로 중앙 정렬할 때 반드시 `width: 100%`를 함께 지정해야 함.
그렇지 않으면 콘텐츠 양에 따라 컨테이너 너비가 달라지는 문제 발생.

```css
/* ✅ 올바른 패턴 */
.container {
    width: 100%;        /* 필수! */
    max-width: 1200px;  /* 프로젝트에 맞게 설정 */
    margin: 0 auto;
}

/* ❌ 잘못된 패턴 - 콘텐츠에 따라 너비 변동 */
.container {
    max-width: 1200px;
    margin: 0 auto;
    /* width 없음 → 문제 발생 */
}
```

**핵심**: `width: 100%`가 없으면 block 요소가 콘텐츠 양에 따라 너비가 달라질 수 있음

---

## 🔐 안전 규칙

### 에러 복구
```
파일 작업 실패: 마지막 성공 상태로 롤백
명령 실행 실패: 원인 분석 후 재시도 (최대 2회)
```

### 규칙 충돌 시 우선순위
1. Security (보안)
2. Reliability (안정성)
3. Correctness (정확성)
4. Performance (성능)
5. Style (스타일)

---


## 💡 개발 팁

### TypeScript strict mode
```json
{
  "compilerOptions": {
    "strict": true,
    "noImplicitAny": true,
    "strictNullChecks": true,
    "strictFunctionTypes": true
  }
}
```

### React 성능 최적화
```
1. useMemo(): 비용이 큰 계산
2. useCallback(): 함수 재생성 방지
3. React.memo(): 불필요한 리렌더링 방지
4. 코드 스플리팅: dynamic import()
```

### Tailwind CSS 팁
```
- @apply: 반복되는 스타일 조합
- @layer: 커스텀 레이어 추가
- theme 확장: tailwind.config.ts에서
```

---

## 🎬 빠른 시작

### 첫 번째 작업 (예: 기능 추가)
```bash
# 1. 요구사항 정리
/implement --think "사용자 프로필 페이지 추가"

# 2. 코드 작성 및 검증
/implement --validate

# 3. 코드 개선
/improve [파일]

# 4. 테스트
/test

# 5. 문서화
/document
```

---

## 📝 라이선스 & 감사

기본: MIT License - 자유롭게 사용, 수정, 배포 가능

**Powered by**: SuperClaude v2.0 + Next.js + Claude Code
