# NaraStore 제안서 분석 서비스

## 프로젝트 개요

조달청 제안요청서(RFP)를 AI로 분석하여 수주 전략을 수립하는 웹 서비스입니다.
Gemini API를 활용하여 제안서를 분석하고, PDF 레포트를 생성합니다.

## 개발 지침

### 필수 규칙
1. **코드 파일 크기 제한**: 모든 코드 파일은 500줄 미만 유지
2. **답변 형식**: 이모티콘 사용 금지
3. **배포 형태**: 설치 후 실행 가능한 독립 실행형 서비스
4. **확장성**: Firebase, WAS 연동을 위한 구조 유지
5. **버전 관리**: 매일 진행 내용을 GitHub에 커밋/푸시
   - 저장소: https://github.com/ChoiHyunKong/NaraStore.git

---

## 현재 구현 상태 (2025-12-04 기준)

### ✅ 완료된 기능

#### 1. 제안서 요약 기능
- **복수 파일 업로드**: PDF, HWP, PPTX 파일 복수 업로드 지원
- **문서 파싱 및 통합**: `DocumentIntegrator`를 통한 복수 파일 자동 파싱 및 통합
- **Gemini API 연동**: `gemini-2.5-flash-preview-09-2025` 모델 사용하여 요약 분석
- **요약 정보 추출**:
  - 프로젝트 개요
  - 프로젝트 목표 및 목적
  - 배경 및 필요성
  - 주요 과업
  - 프로젝트 금액
  - 마감 날짜
  - 핵심 요구사항
- **PDF 레포트 생성**: `fpdf2`를 사용한 한글 PDF 생성 (맑은 고딕 폰트)
- **PDF 다운로드**: 브라우저에서 직접 다운로드 가능
- **제안서 분석으로 이동**: 업로드한 파일 정보를 유지하며 분석 페이지로 이동

#### 2. 제안서 분석 기능
- **복수 파일 업로드**: PDF, HWP, PPTX 파일 복수 업로드 지원
- **상세 요구사항 분석**: 클라이언트 니즈, 요구사항 카테고리별 분류, 제약사항, 필요 기술 스택 추출
- **수주 전략 도출**: Gemini API를 통한 수주 전략 자동 생성
  - 핵심 수주 전략
  - 차별화 포인트
  - 리스크 관리 방안
  - 제안 강조 사항
- **유사 프로젝트 레퍼런스**: AI 기반 유사 프로젝트 추천
- **PDF 레포트 생성**: 분석 결과 및 전략을 포함한 통합 PDF 레포트
- **탭 기반 UI**: 요구사항 분석, 수주 전략, 유사 프로젝트를 탭으로 구분하여 표시

#### 3. 이력 관리 기능
- **JSON 기반 영구 저장**: `data/history.json`에 분석 이력 저장
- **이력 목록 표시**: 과거 분석 이력을 최신순으로 표시
- **PDF 재다운로드**: 과거 분석 결과의 PDF 파일 재다운로드
- **이력 삭제**: 불필요한 이력 및 PDF 파일 삭제 기능

#### 4. 백엔드 인프라
- **문서 파서**: PDF, HWP, PPTX 파일 텍스트 추출
  - `pdf_parser.py`: pypdf 사용
  - `hwp_parser.py`: olefile 사용 (압축 해제 및 한글 추출)
  - `pptx_parser.py`: python-pptx 사용
  - `text_cleaner.py`: 텍스트 정규화 및 불필요한 문자 제거
- **Gemini API 클라이언트**: 
  - `client.py`: API 초기화 및 연결 관리
  - `request.py`: 재시도 로직 포함 요청 핸들러
  - `response.py`: JSON 파싱 및 응답 검증
- **프롬프트 관리**: 
  - `builder.py`: 동적 프롬프트 생성 (요약, 분석, 전략, 레퍼런스)
  - `templates.py`: YAML 기반 프롬프트 템플릿 로드
  - `optimizer.py`: 토큰 최적화
- **유틸리티**:
  - `logger.py`: 로깅
  - `error_handler.py`: 에러 핸들링
  - `validator.py`: 입력 검증
  - `file_handler.py`: 파일 작업

#### 5. 프론트엔드
- **3개 메뉴 구조**: 제안서 요약, 제안서 분석, 이력 관리
- **Streamlit 기반 UI**: 웹 서비스 형태
- **좌측 사이드바 메뉴**: 직관적인 페이지 이동
- **CSS 스타일링**: 통일된 디자인 시스템

#### 6. 환경 설정
- **`.env` 파일**: Gemini API 키 및 프로젝트 설정 관리
- **`requirements.txt`**: 필요 패키지 목록 관리
- **`run.bat`**: Windows 실행 스크립트

---

### ⚠️ 미완성 기능 및 알려진 이슈

#### 1. 페이지 이동 경고 팝업
- **상태**: 코드는 구현되어 있으나 **작동하지 않음**
- **위치**: `frontend/app.py` 62-76줄
- **원인**: `analysis_in_progress` 플래그가 제대로 설정되지 않음
- **영향**: 분석 중 페이지 이동 시 경고 팝업이 표시되지 않음
- **해결 필요**: 분석 시작 시 `st.session_state['analysis_in_progress'] = True` 로직 검증 및 수정

#### 2. 이력 파일 유지
- **상태**: `data/history.json`에 저장되지만 **임시 PDF 파일은 시스템 temp 폴더에 저장됨**
- **영향**: 시스템 재부팅 또는 일정 시간 경과 시 PDF 파일이 삭제될 가능성
- **해결 필요**: PDF 파일을 프로젝트 내 `data/pdfs/` 폴더에 저장하도록 변경

#### 3. 에러 핸들링 강화
- **상태**: 기본적인 에러 핸들링은 구현되어 있으나 **세부 케이스 미처리**
- **예시**:
  - HWP 파일 파싱 실패 시 대체 로직 부재
  - Gemini API 할당량 초과 시 사용자 안내 부족
  - 네트워크 오류 시 재시도 로직 미흡
- **해결 필요**: 사용자 친화적인 에러 메시지 및 복구 로직 추가

#### 4. UI/UX 개선
- **상태**: 기본 기능 위주로 구현, **사용자 경험 개선 필요**
- **개선 사항**:
  - 분석 진행 중 상세 진행 바 (현재는 간단한 프로그레스 바만 표시)
  - 업로드 파일 미리보기
  - 분석 결과 가시성 개선 (현재 텍스트 기반)
  - 다크 모드 지원

#### 5. 성능 최적화
- **상태**: 기본 구현, **대용량 파일 처리 최적화 필요**
- **이슈**:
  - 50MB 이상 파일 업로드 시 처리 시간 증가
  - 복수 파일(5개 이상) 동시 분석 시 메모리 사용량 증가
- **해결 필요**: 
  - 파일 청크 처리
  - 비동기 처리 검토
  - 메모리 사용 최적화

---

## 메뉴 구성

### 1. 제안서 요약
**목적**: 제안서 내용을 빠르게 파악하기 위한 요약 레포트 생성

**기능**:
- 복수 파일 업로드 지원 (HWP, PDF, PPTX)
- 업로드된 문서 자동 분석 및 통합
- 다음 정보를 포함한 요약 레포트 생성:
  - 프로젝트 개요
  - 프로젝트 목표 및 목적
  - 왜 수행하는지 (배경 및 필요성)
  - 어떤 기능(서비스)를 만들어야 하는지 (주요 과업)
  - 프로젝트 금액
  - 마감 날짜
- PDF 레포트 다운로드
- 제안서 분석 메뉴로 바로 이동

### 2. 제안서 분석
**목적**: 수주 확률을 높이기 위한 상세 분석 및 전략 수립

**기능**:
- 복수 파일 업로드 지원
- 각 상세 요구사항 분석
- 요구사항 이행 전략 도출
- 유사 프로젝트 레퍼런스 제공
- 분석 PDF 레포트 다운로드

### 3. 제안서 요약 및 분석 이력
**목적**: 과거 분석 이력 관리 및 재활용

**기능**:
- 제안서 요약 및 분석 진행 내용 목록 표시
- 과거 레포트 PDF 재다운로드
- 이력 삭제 기능

## 공통 기능

### 페이지 이동 경고
- 분석 중 다른 페이지로 이동 시 경고 팝업 표시
- 메시지: "페이지 이동 시 진행된 내용은 사라지며 제안서 요약 및 분석 이력에서 볼 수 있습니다"
- 확인/취소 옵션 제공
- **⚠️ 현재 미작동 - 수정 필요**

### UI/UX 가이드
- 텍스트 기반 문서로 최대한 가시성 좋게 구성
- 웹 형태의 서비스
- 좌측 사이드바 (SNG) 메뉴 구조

---

## 향후 확장 계획

### 역량 평가 기능
- 회사 보유 인력 및 스킬 역량 입력
- 제안서 요구사항과 비교 분석
- 이행 가능성 그래프/확률 표시

### 데이터베이스 연동
- JSON 파일 대신 Firebase 또는 관계형 DB 사용
- 사용자 인증 및 권한 관리
- 다중 사용자 지원

### WAS 연동
- 엔터프라이즈 환경 배포
- API 서버 분리
- 부하 분산 및 스케일링

---

## 기술 스택

- **Frontend**: Streamlit
- **AI**: Google Gemini API (gemini-2.5-flash-preview-09-2025)
- **Document Parsing**: pypdf, python-pptx, olefile
- **PDF Generation**: fpdf2 (맑은 고딕 폰트)
- **Configuration**: python-dotenv, pyyaml
- **Data Storage**: JSON (향후 DB 연동 고려)

---

## 설치 및 실행

### 1. 가상환경 설정
```bash
python -m venv venv
.\venv\Scripts\activate
```

### 2. 패키지 설치
```bash
pip install -r requirements.txt
```

### 3. 환경 변수 설정
`.env.example` 파일을 참고하여 `.env` 파일을 생성하고 API 키를 입력하세요.

```
GEMINI_API_KEY=your_api_key_here
PROJECT_ID=projects/your_project_id
PROJECT_NUMBER=your_project_number
MAX_FILE_SIZE_MB=50
APP_TITLE=NaraStore 제안서 분석 서비스
DEBUG_MODE=False
```

### 4. 실행
```bash
.\run.bat
```
또는
```bash
streamlit run frontend\app.py
```

### 5. 접속
브라우저에서 `http://localhost:8502` 접속

---

## 프로젝트 구조

```
NaraStore/
├── frontend/              # Streamlit UI
│   ├── app.py            # 메인 앱 (페이지 라우팅, 메뉴)
│   ├── views/            # 페이지 뷰 (Streamlit 자동 메뉴 방지)
│   │   ├── summary_page.py      # 요약 페이지
│   │   ├── analysis_page.py     # 분석 페이지
│   │   └── history_page.py      # 이력 페이지
│   ├── components/       # UI 컴포넌트 (미사용 상태)
│   └── styles/           # CSS 파일
├── backend/              # 백엔드 로직
│   ├── analyzer/         # 분석 엔진
│   │   ├── parser/       # 문서 파서 (PDF, HWP, PPTX, 텍스트 정리)
│   │   ├── gemini/       # Gemini API (client, request, response)
│   │   └── prompt/       # 프롬프트 관리 (templates, builder, optimizer)
│   ├── report/           # 레포트 생성 (fpdf2 기반 PDF)
│   ├── storage/          # 이력 저장 (JSON)
│   └── utils/            # 유틸리티 (logger, error_handler, validator, file_handler)
├── config/               # 설정 파일
│   ├── settings.py       # 앱 설정
│   ├── api_config.py     # Gemini API 설정
│   └── prompts/          # AI 프롬프트 (YAML)
├── data/                 # 데이터 저장소
│   └── history.json      # 분석 이력
├── .env                  # 환경 변수 (gitignore)
├── .env.example          # 환경 변수 예제
├── requirements.txt      # 패키지 목록
└── run.bat               # 실행 스크립트
```

---

## 개발 히스토리

### 2025-12-03
- 프로젝트 초기화 및 기본 구조 생성
- 문서 파서 구현 (PDF, HWP, PPTX)
- Gemini API 연동
- 제안서 요약 기능 구현
- 제안서 분석 기능 구현
- 이력 관리 기능 구현 (JSON 기반)

### 2025-12-04
- PDF 폰트 오류 수정 (Italic, Bold-Italic 추가)
- Gemini 모델 변경 (gemini-2.5-flash-preview-09-2025)
- 모듈 import 오류 해결
- `.env` 인코딩 문제 해결
- README.md 업데이트 (구현 상태 및 미완성 기능 정리)

---

## 라이선스

MIT License

---

## 문의 및 기여

이 프로젝트는 조달청 제안서 분석을 위한 내부 도구로 개발되었습니다.
문의사항이 있으시면 GitHub Issues를 통해 연락해주세요.
