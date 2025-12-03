# NaraStore n8n 자동화 연동 가이드

이 가이드는 **NaraStore** 서비스를 **n8n**과 연동하여 자동화하는 방법을 설명합니다.
**n8n-mcp**와 **Context7**을 활용하여 AI 에이전트가 워크플로우를 쉽게 이해하고 제어할 수 있도록 설정합니다.

## 1. 사전 준비 (Prerequisites)

1.  **Python 환경**: NaraStore 프로젝트가 실행 가능한 상태여야 합니다.
2.  **n8n**: [n8n 설치 가이드](https://docs.n8n.io/hosting/installation/)를 참고하여 설치 및 실행하세요. (Desktop 버전 또는 Self-hosted)
3.  **n8n-mcp**: [GitHub 저장소](https://github.com/czlonkowski/n8n-mcp)에서 코드를 다운로드하거나 `npx`로 실행할 준비를 합니다.

## 2. NaraStore API 서버 실행

n8n이 NaraStore에 명령을 내릴 수 있도록 API 서버를 켭니다.

1.  `NaraStore` 폴더로 이동합니다.
2.  **`run_api.bat`** 파일을 더블 클릭하여 실행합니다.
3.  검은색 창(터미널)이 열리고 `Uvicorn running on http://0.0.0.0:8000` 메시지가 나오면 성공입니다.
    *   이 창은 끄지 말고 켜두세요.

## 3. n8n-mcp 설정 (AI 에디터 연동)

`n8n-mcp`는 Cursor나 Windsurf 같은 AI 에디터가 n8n의 기능을 이해하도록 돕는 도구입니다.

### Cursor / Windsurf 설정
1.  프로젝트 설정의 `MCP Servers` 섹션으로 이동합니다.
2.  새로운 MCP 서버를 추가합니다.
    *   **Name**: `n8n-mcp`
    *   **Type**: `command`
    *   **Command**: `npx`
    *   **Args**: `-y @czlonkowski/n8n-mcp` (또는 다운로드 받은 경로의 실행 명령어)
3.  연동이 완료되면 AI에게 "n8n 워크플로우를 만들어줘"라고 요청할 때, AI가 n8n의 노드 정보를 정확히 파악하게 됩니다.

## 4. Context7 설정

**Context7**은 AI에게 최신 라이브러리 문서를 제공하는 서비스입니다. n8n 내에서 스크립트를 짜거나 복잡한 로직을 구현할 때 AI가 Context7을 참조하여 정확한 코드를 작성할 수 있습니다.

1.  **n8n 내 설정**:
    *   n8n에 `n8n-nodes-mcp` 커뮤니티 노드가 설치되어 있다면, 이를 통해 Context7을 연결할 수 있습니다.
    *   또는 AI 에디터(Cursor)에서 Context7 MCP 서버를 추가하여, 코딩 중에 문서를 참조하도록 설정합니다.
    *   **Command**: `npx`
    *   **Args**: `-y context7-mcp` (가정: Context7이 제공하는 표준 MCP 실행 방식)

> [!TIP]
> Context7은 주로 **"AI가 코드를 짤 때 문서를 참조하는 용도"**입니다. 단순한 크롤링 자동화만 필요하다면 필수적인 요소는 아닐 수 있습니다.

## 5. n8n 워크플로우 생성 예시

이제 n8n에서 NaraStore API를 호출하여 크롤링을 자동화해 봅시다.

1.  **n8n 접속**: 브라우저에서 `http://localhost:5678` 접속.
2.  **새 워크플로우 생성**.
3.  **HTTP Request 노드 추가**:
    *   **Method**: `POST`
    *   **URL**: `http://localhost:8000/crawl`
    *   **Body Content Type**: `JSON`
    *   **Body Parameters**:
        *   `keyword`: `"인공지능"` (원하는 검색어)
4.  **실행 (Execute Node)**:
    *   노드를 실행하면 NaraStore 크롤러가 작동하고, 결과 데이터가 n8n으로 들어옵니다.
5.  **결과 활용**:
    *   이후 Google Sheets 노드, Slack 노드 등을 연결하여 크롤링 결과를 저장하거나 알림을 보낼 수 있습니다.

## 6. 문제 해결

*   **API 연결 실패**: `run_api.bat` 창이 켜져 있는지 확인하세요. 방화벽 설정에서 포트 8000번이 허용되어 있는지 확인하세요.
*   **크롤러 오류**: 크롬 브라우저가 정상적으로 설치되어 있는지 확인하세요.
