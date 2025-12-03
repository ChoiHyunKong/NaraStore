"""
Gemini API 관련 설정
"""


class GeminiConfig:
    """Gemini API 설정"""
    
    # 모델 설정
    MODEL_NAME: str = "gemini-2.5-flash-preview-09-2025"
    
    # 생성 설정
    TEMPERATURE: float = 0.7
    TOP_P: float = 0.95
    TOP_K: int = 40
    MAX_OUTPUT_TOKENS: int = 8192
    
    # 안전 설정
    SAFETY_SETTINGS = [
        {
            "category": "HARM_CATEGORY_HARASSMENT",
            "threshold": "BLOCK_MEDIUM_AND_ABOVE"
        },
        {
            "category": "HARM_CATEGORY_HATE_SPEECH",
            "threshold": "BLOCK_MEDIUM_AND_ABOVE"
        },
        {
            "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
            "threshold": "BLOCK_MEDIUM_AND_ABOVE"
        },
        {
            "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
            "threshold": "BLOCK_MEDIUM_AND_ABOVE"
        }
    ]
    
    # 재시도 설정
    MAX_RETRIES: int = 3
    RETRY_DELAY: int = 2  # 초
    TIMEOUT: int = 60  # 초


# 전역 설정 인스턴스
gemini_config = GeminiConfig()
