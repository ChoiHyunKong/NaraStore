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

## 메뉴 구성

### 1. 제안서 요약
**목적**: 제안서 내용을 빠르게 파악하기 위한 요약 레포트 생성

**기능**:
- 복수 파일 업로드 지원 (한글, PDF 등)
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

### UI/UX 가이드
- 텍스트 기반 문서로 최대한 가시성 좋게 구성
- 웹 형태의 서비스
- 좌측 사이드바 (SNG) 메뉴 구조

## 향후 확장 계획

### 역량 평가 기능
- 회사 보유 인력 및 스킬 역량 입력
- 제안서 요구사항과 비교 분석
- 이행 가능성 그래프/확률 표시

## 기술 스택

- **Frontend**: Streamlit
- **AI**: Google Gemini API
- **Document Parsing**: pypdf, python-pptx, olefile
- **PDF Generation**: fpdf2
- **Configuration**: python-dotenv, pyyaml
- **Data Storage**: JSON (향후 DB 연동 고려)

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

### 4. 실행
```bash
.\run.bat
```
또는
```bash
streamlit run frontend\app.py
```

## 프로젝트 구조

```
NaraStore/
├── frontend/           # Streamlit UI
│   ├── app.py         # 메인 앱
│   ├── pages/         # 페이지 모듈
│   ├── components/    # UI 컴포넌트
│   └── styles/        # CSS 파일
├── backend/           # 백엔드 로직
│   ├── analyzer/      # 분석 엔진
│   ├── report/        # 레포트 생성
│   ├── storage/       # 이력 저장
│   └── utils/         # 유틸리티
├── config/            # 설정 파일
│   ├── settings.py    # 앱 설정
│   └── prompts/       # AI 프롬프트
└── requirements.txt   # 패키지 목록
```

## 라이선스

MIT License
