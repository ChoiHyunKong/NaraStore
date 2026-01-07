@echo off
chcp 65001 >nul
echo.
echo ========================================
echo    NaraStore - 제안서 분석 서비스
echo ========================================
echo.

:: 가상환경 확인 및 활성화
if exist "venv\Scripts\activate.bat" (
    echo [1/4] 가상환경 활성화 중...
    call venv\Scripts\activate.bat
) else (
    echo [!] 가상환경이 없습니다. 먼저 setup.bat을 실행해주세요.
    pause
    exit /b 1
)

:: Python 패키지 설치 확인
echo [2/4] Python 패키지 확인 중...
pip install -q -r requirements.txt

:: 프론트엔드 의존성 설치 확인
echo [3/4] 프론트엔드 의존성 확인 중...
cd frontend
if not exist "node_modules" (
    echo     npm 패키지 설치 중... (최초 실행 시 시간이 소요됩니다)
    call npm install
)
cd ..

:: 서버 실행
echo [4/4] 서버 시작 중...
echo.
echo ----------------------------------------
echo   백엔드 API: http://localhost:8000
echo   프론트엔드:  http://localhost:5173
echo ----------------------------------------
echo.
echo   ※ 종료하려면 Ctrl+C를 누르세요
echo.

:: 백엔드 실행 (백그라운드)
start /B cmd /c "cd backend && python -m uvicorn main:app --host 0.0.0.0 --port 8000"

:: 잠시 대기 후 프론트엔드 실행
timeout /t 2 /nobreak >nul

:: 프론트엔드 실행 (포그라운드)
cd frontend
call npm run dev
