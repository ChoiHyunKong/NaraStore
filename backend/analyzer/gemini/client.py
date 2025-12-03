"""
Gemini API 클라이언트
API 초기화 및 연결 관리
"""
import google.generativeai as genai
from config.settings import settings
from config.api_config import gemini_config
from backend.utils.logger import logger
from backend.utils.error_handler import error_handler


class GeminiClient:
    """Gemini API 클라이언트"""
    
    def __init__(self, api_key: str = None):
        """
        클라이언트 초기화
        
        Args:
            api_key: Gemini API 키 (없으면 설정에서 로드)
        """
        self.api_key = api_key or settings.GEMINI_API_KEY
        self.model = None
        self._configure()
    
    def _configure(self):
        """API 설정"""
        try:
            genai.configure(api_key=self.api_key)
            
            self.model = genai.GenerativeModel(
                model_name=gemini_config.MODEL_NAME,
                generation_config={
                    "temperature": gemini_config.TEMPERATURE,
                    "top_p": gemini_config.TOP_P,
                    "top_k": gemini_config.TOP_K,
                    "max_output_tokens": gemini_config.MAX_OUTPUT_TOKENS,
                },
                safety_settings=gemini_config.SAFETY_SETTINGS
            )
            
            logger.info(f"Gemini API 초기화 완료: {gemini_config.MODEL_NAME}")
            
        except Exception as e:
            logger.error(f"Gemini API 초기화 실패: {str(e)}")
            raise
    
    def is_configured(self) -> bool:
        """API 설정 여부 확인"""
        return self.model is not None
    
    def get_model_info(self) -> dict:
        """모델 정보 반환"""
        return {
            "model_name": gemini_config.MODEL_NAME,
            "temperature": gemini_config.TEMPERATURE,
            "max_tokens": gemini_config.MAX_OUTPUT_TOKENS
        }


# 전역 클라이언트 인스턴스 생성 함수
def create_client(api_key: str = None) -> GeminiClient:
    """Gemini 클라이언트 생성"""
    return GeminiClient(api_key)
