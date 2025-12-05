# 🚨 긴급: API 키 보안 조치 가이드

## ⚠️ 현재 상황
**귀하의 Gemini API 키가 GitHub에 노출되었습니다!**

노출된 키: `AIzaSyDb9aryszWzzm3k_bRYuA6lp3LqRzjZ0LU`

---

## 🔥 즉시 해야 할 일 (우선순위 순서)

### 1단계: 노출된 API 키 즉시 삭제 (가장 중요!)

**Google AI Studio에서 해당 키 삭제:**
1. https://aistudio.google.com/app/apikey 접속
2. 노출된 키 찾기: `AIzaSyDb9a...Z0LU`
3. 🗑️ 삭제 버튼 클릭
4. ✅ 새 API 키 생성

⚠️ **이 키는 이미 공개되었으므로 절대 재사용하지 마세요!**

---

### 2단계: Git History에서 API 키 제거

노출된 키가 Git 커밋 히스토리에 남아있을 수 있습니다.

#### Option A: BFG Repo-Cleaner 사용 (권장)
```bash
# BFG 다운로드
# https://rtyley.github.io/bfg-repo-cleaner/

# API 키가 포함된 파일 제거
java -jar bfg.jar --delete-files .env

# Git history 정리
cd NaraStore
git reflog expire --expire=now --all
git gc --prune=now --aggressive

# 강제 푸시 (주의!)
git push origin --force --all
```

#### Option B: git filter-branch 사용
```bash
cd c:\Users\chyun\OneDrive\바탕 화면\AI 활용\NaraStore

# .env 파일을 history에서 완전히 제거
git filter-branch --force --index-filter "git rm --cached --ignore-unmatch .env" --prune-empty --tag-name-filter cat -- --all

# 강제 푸시
git push origin --force --all
git push origin --force --tags
```

#### Option C: 새 저장소 생성 (가장 안전)
```bash
# 1. GitHub에서 새 저장소 생성
# 2. 현재 프로젝트를 clean 상태로 복사

# 현재 디렉토리에서
cd ..
mkdir NaraStore_Clean
cd NaraStore_Clean

# 필요한 파일만 복사 (git 제외)
xcopy "c:\Users\chyun\OneDrive\바탕 화면\AI 활용\NaraStore\*.*" . /E /I /EXCLUDE:excludelist.txt

# 새 git 초기화
git init
git add .
git commit -m "Initial commit (no sensitive data)"
git remote add origin https://github.com/ChoiHyunKong/NaraStore-New.git
git push -u origin main
```

---

### 3단계: 새 API 키로 .env 업데이트

```bash
# .env 파일 수정
GEMINI_API_KEY=새로운_API_키_여기_입력
MAX_FILE_SIZE_MB=50
APP_TITLE=NaraStore 제안서 분석 서비스
DEBUG_MODE=False
```

---

### 4단계: .gitignore 확인 (이미 설정됨 ✅)

`.gitignore` 파일에 `.env`가 포함되어 있는지 확인:
```
# 환경변수 (중요: API 키 보호)
.env
```

✅ 이미 설정되어 있습니다!

---

### 5단계: 향후 예방 조치

#### Git Hooks 설정 (API 키 커밋 방지)
```bash
# .git/hooks/pre-commit 파일 생성
cat > .git/hooks/pre-commit << 'EOF'
#!/bin/sh
if git diff --cached --name-only | grep -q "^.env$"; then
    echo "❌ ERROR: .env 파일을 커밋하려고 합니다!"
    echo "API 키가 노출될 수 있습니다."
    exit 1
fi

# API 키 패턴 검사
if git diff --cached | grep -E "AIza[0-9A-Za-z_-]{35}"; then
    echo "❌ ERROR: Gemini API 키가 감지되었습니다!"
    echo "커밋을 중단합니다."
    exit 1
fi
EOF

chmod +x .git/hooks/pre-commit
```

#### GitHub Secret Scanning 활성화
- GitHub Repository Settings → Security → Secret scanning
- 자동으로 API 키 패턴 탐지

---

## 🔧 API 키 오류 해결

현재 오류가 발생하는 이유:

### 원인 1: 캐시된 모듈
```bash
# Python 캐시 삭제
cd c:\Users\chyun\OneDrive\바탕 화면\AI 활용\NaraStore
Remove-Item -Recurse -Force __pycache__
Remove-Item -Recurse -Force backend\__pycache__
Remove-Item -Recurse -Force backend\analyzer\__pycache__

# 앱 재시작
streamlit run frontend\app.py
```

### 원인 2: .env 파일 인코딩 문제
```bash
# PowerShell에서 .env 파일 재생성
@"
GEMINI_API_KEY=새로운_API_키
MAX_FILE_SIZE_MB=50
APP_TITLE=NaraStore 제안서 분석 서비스
DEBUG_MODE=False
"@ | Out-File -FilePath .env -Encoding UTF8
```

### 원인 3: 환경변수 로드 순서
```python
# config/settings.py 수정 확인
# load_dotenv()가 제일 먼저 호출되는지 확인
```

---

## ✅ 체크리스트

- [ ] 1. Google AI Studio에서 노출된 키 삭제
- [ ] 2. 새 API 키 생성
- [ ] 3. .env 파일에 새 키 입력
- [ ] 4. Git history에서 .env 제거
- [ ] 5. GitHub에 강제 푸시
- [ ] 6. `python diagnose_api.py` 실행하여 확인
- [ ] 7. 앱 재시작: `streamlit run frontend\app.py`
- [ ] 8. Git hooks 설정 (선택사항)

---

## 🆘 도움이 필요하면

1. **API 키 삭제 확인**: https://aistudio.google.com/app/apikey
2. **GitHub 저장소 확인**: https://github.com/ChoiHyunKong/NaraStore
3. **진단 스크립트 실행**: `python diagnose_api.py`

---

**⚠️ 중요: 노출된 API 키는 절대 재사용하지 마세요!**
