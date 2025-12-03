# NaraStore 제안서 분석 서비스

## 프로젝트 개요

조달청 제안요청서(RFP)를 AI로 분석하여 수주 전략을 수립하는 서비스입니다.
Gemini API를 활용하여 제안서를 분석하고, PDF 레포트를 생성합니다.

## 개발 지침

### 필수 규칙
1. **코드 파일 크기 제한**: 모든 코드 파일은 500줄 미만 유지
2. **답변 형식**: 이모티콘 사용 금지
3. **배포 형태**: 설치 후 실행 가능한 독립 실행형 서비스
4. **확장성**: Firebase, WAS 연동을 위한 구조 유지
5. **버전 관리**: 매일 진행 내용을 GitHub에 커밋/푸시
   - 저장소: https://github.com/ChoiHyunKong/NaraStore.git

## 주요 기능

1. **제안서 업로드**: PDF, HWP, PPTX 파일 지원
2. **AI 분석**: Gemini API 최신 모델 활용
3. **레포트 생성**: PDF 형식으로 다운로드

### 레포트 내용
- 프로젝트 목적과 방향성
- 프로젝트 수행 필요성
- 클라이언트 니즈 분석
- 수주 확률 향상 전략
- 제안 요청서 작성 가이드

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
│   └── utils/         # 유틸리티
├── config/            # 설정 파일
│   ├── settings.py    # 앱 설정
│   └── prompts/       # AI 프롬프트
└── requirements.txt   # 패키지 목록
```

## 기술 스택

- **Frontend**: Streamlit
- **AI**: Google Gemini API
- **Document Parsing**: pypdf, python-pptx, olefile
- **PDF Generation**: fpdf2
- **Configuration**: python-dotenv, pyyaml

## 라이선스

MIT License
