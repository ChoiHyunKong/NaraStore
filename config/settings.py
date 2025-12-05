"""
애플리케이션 설정 관리
환경변수 로드 및 기본값 설정
"""
import os
from pathlib import Path
from dotenv import load_dotenv

# 프로젝트 루트 디렉토리에서 .env 파일 로드
ROOT_DIR = Path(__file__).resolve().parent.parent
load_dotenv(ROOT_DIR / ".env")


class Settings:
    """애플리케이션 전역 설정"""
    
    # API 설정
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")
    
    # 파일 업로드 설정
    MAX_FILE_SIZE_MB: int = int(os.getenv("MAX_FILE_SIZE_MB", "50"))
    MAX_FILE_SIZE_BYTES: int = MAX_FILE_SIZE_MB * 1024 * 1024
    ALLOWED_EXTENSIONS: list = [".pdf", ".hwp", ".pptx"]
    
    # 앱 설정
    APP_TITLE: str = os.getenv("APP_TITLE", "NaraStore 제안서 분석 서비스")
    DEBUG_MODE: bool = os.getenv("DEBUG_MODE", "False").lower() == "true"
    
    # 경로 설정
    BASE_DIR: str = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    UPLOAD_DIR: str = os.path.join(BASE_DIR, "uploads")
    OUTPUT_DIR: str = os.path.join(BASE_DIR, "outputs")
    
    @classmethod
    def validate(cls) -> tuple[bool, str]:
        """설정 유효성 검증"""
        if not cls.GEMINI_API_KEY:
            return False, "GEMINI_API_KEY가 설정되지 않았습니다."
        
        if cls.MAX_FILE_SIZE_MB <= 0:
            return False, "MAX_FILE_SIZE_MB는 0보다 커야 합니다."
        
        return True, "설정이 유효합니다."
    
    @classmethod
    def ensure_directories(cls):
        """필요한 디렉토리 생성"""
        os.makedirs(cls.UPLOAD_DIR, exist_ok=True)
        os.makedirs(cls.OUTPUT_DIR, exist_ok=True)


# 전역 설정 인스턴스
settings = Settings()
