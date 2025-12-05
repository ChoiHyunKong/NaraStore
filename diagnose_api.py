"""
API 키 검증 및 진단 스크립트
"""
import os
import sys
from dotenv import load_dotenv

# 프로젝트 루트 경로 추가
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

print("=" * 60)
print("API 키 진단 시작...")
print("=" * 60)

# 1. .env 파일 로드
load_dotenv()
print("\n✓ .env 파일 로드 완료")

# 2. API 키 확인
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    print("❌ GEMINI_API_KEY가 .env 파일에 설정되지 않았습니다.")
    print("\n해결 방법:")
    print("1. .env 파일을 열어주세요")
    print("2. 다음 형식으로 API 키를 입력하세요:")
    print("   GEMINI_API_KEY=your_actual_api_key_here")
    print("3. 파일을 저장하고 앱을 다시 실행하세요")
    sys.exit(1)

print(f"✓ API 키 발견: {api_key[:10]}...{api_key[-4:]}")

# 3. Google Generative AI 모듈 확인
try:
    import google.generativeai as genai
    print("✓ google-generativeai 모듈 로드 완료")
except ImportError as e:
    print(f"❌ google-generativeai 모듈 로드 실패: {e}")
    print("\n해결 방법:")
    print("pip install google-generativeai")
    sys.exit(1)

# 4. API 키로 인증 시도
try:
    genai.configure(api_key=api_key)
    print("✓ API 키 인증 완료")
except Exception as e:
    print(f"❌ API 키 인증 실패: {e}")
    print("\n원인:")
    print("- API 키가 유효하지 않거나 만료되었습니다")
    print("- Google AI Studio에서 새 API 키를 발급받으세요")
    print("  https://aistudio.google.com/app/apikey")
    sys.exit(1)

# 5. 모델 목록 조회
try:
    print("\n사용 가능한 Gemini 모델 목록:")
    print("-" * 60)
    count = 0
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            print(f"  - {m.name}")
            count += 1
    
    if count == 0:
        print("  사용 가능한 모델이 없습니다.")
    else:
        print(f"\n✓ 총 {count}개의 모델 사용 가능")
    
except Exception as e:
    print(f"❌ 모델 목록 조회 실패: {e}")
    sys.exit(1)

# 6. 설정 검증
from config.settings import settings

is_valid, message = settings.validate()
if is_valid:
    print(f"\n✓ 설정 검증 완료")
else:
    print(f"\n❌ 설정 검증 실패: {message}")

print("\n" + "=" * 60)
print("진단 완료! API 키가 정상적으로 작동합니다.")
print("=" * 60)
