# NaraStore 제안서 분석 서비스 (Ver 2.0)

**조달청 제안요청서(RFP)를 AI로 분석하여 수주 전략을 수립하는 차세대 웹 서비스**입니다.  
기존 Streamlit 버전에서 **React + FastAPI** 아키텍처로 완전히 새롭게 리팩토링되었습니다.

![Project Status](https://img.shields.io/badge/Status-Active-success)
![Tech Stack](https://img.shields.io/badge/Stack-React%20%7C%20FastAPI%20%7C%20Gemini-blue)

## 🚀 주요 기능

### 1. 🤖 AI 기반 제안서 정밀 분석
- **Gemini 2.5 Flash** 모델을 활용한 고속 분석
- 제안요청서(RFP)의 핵심 내용 요약 (예산, 기간, 과업 등)
- **요구사항 상세 분석**: 기능/보안/시스템 요구사항을 카테고리별로 자동 분류
- **수주 전략 수립**: 경쟁 우위를 위한 차별화 전략 및 리스크 관리 방안 제시
- **To-Do List 자동 생성**: 제안 실무자가 당장 해야 할 일 도출

### 2. 📄 다양한 문서 지원 & Mock Mode
- **지원 포맷**: PDF, HWP(한글), PPTX 파일 지원
- **Mock Mode (가상 분석)**: API Key 할당량이 없거나 테스트가 필요할 때, 내장된 가상 데이터를 통해 기능 체험 가능

### 3. 📊 직관적인 카드 UI & PDF 리포트
- **Card UI**: 복잡한 요구사항을 접고 펼칠 수 있는 인터랙티브 UI 제공
- **PDF Export**: 분석된 내용을 깔끔한 디자인의 PDF 리포트로 즉시 다운로드 (`fpdf2` 기반)

---

## 🛠️ 기술 스택 (Tech Stack)

### Frontend
- **Framework**: React 18, Vite
- **Language**: TypeScript
- **Styling**: Tailwind CSS (Glassmorphism Design)
- **Icons**: Lucide React

### Backend
- **Framework**: FastAPI (Python 3.10+)
- **Analysis Engine**: Google Gemini API
- **Document Parser**:
  - `olefile` (HWP)
  - `pypdf` (PDF)
  - `python-pptx` (PPTX)
- **PDF Generator**: FPDF2

### Database
- **Storage**: Firebase Firestore (NoSQL)

---

## 📂 프로젝트 구조

```bash
NaraStore/
├── frontend/             # React 프론트엔드
│   ├── src/
│   │   ├── components/   # UI 컴포넌트 (AnalysisPanel, RFPList 등)
│   │   └── services/     # API 및 DB 통신 로직
├── backend/              # FastAPI 백엔드
│   ├── main.py           # API 엔트리포인트
│   ├── analyzer/         # AI 분석 로직 (Gemini, Parsers)
│   ├── report/           # PDF 생성 로직 (ReportWriter)
│   └── config/           # 환경 설정
├── data/                 # 로컬 데이터 저장소 (PDFs)
└── run.bat               # 원클릭 실행 스크립트
```

---

## ▶️ 설치 및 실행 방법

### 1. 환경 설정
`.env` 파일에 Google Gemini API Key와 Firebase 설정을 입력합니다.

### 2. 간편 실행 (Windows)
프로젝트 루트의 `run.bat` 파일을 더블클릭하면 백엔드와 프론트엔드가 동시에 실행됩니다.

```bash
./run.bat
```

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000

---

## 🔄 최근 업데이트 (2026-01)
- **아키텍처 변경**: Streamlit → React + FastAPI 로 완전 전환
- **PDF 엔진 교체**: ReportLab → FPDF2 (한글 폰트 호환성 및 디자인 개선)
- **Mock Mode 추가**: API Quota 이슈 대응을 위한 데모 모드 탑재
- **API Key 검증 완화**: 테스트 편의성 증대

---

## 📞 문의
이 프로젝트는 개인 학습 및 포트폴리오 목적으로 제작되었습니다.
GitHub Issues를 통해 피드백을 남겨주세요.
