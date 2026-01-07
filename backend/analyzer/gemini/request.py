"""
Gemini API 요청 처리
요청 포맷팅 및 전송
"""
import time
from typing import Dict, Optional
from backend.analyzer.gemini.client import GeminiClient
from backend.utils.logger import logger
from backend.utils.error_handler import error_handler
from config.api_config import gemini_config


class GeminiRequest:
    """Gemini API 요청 클래스"""
    
    def __init__(self, client: GeminiClient):
        """
        요청 핸들러 초기화
        
        Args:
            client: Gemini 클라이언트 인스턴스
        """
        self.client = client
    
    def send(self, prompt: str, retry_count: int = 0, generation_config: Optional[Dict] = None) -> tuple[bool, str | Dict]:
        """
        API 요청 전송
        
        Args:
            prompt: 전송할 프롬프트
            retry_count: 재시도 횟수
            generation_config: 생성 설정 (JSON 모드 등)
            
        Returns:
            (성공 여부, 응답 텍스트 또는 에러 메시지)
        """
        try:
            logger.info(f"Gemini API 요청 전송 (시도: {retry_count + 1})")
            
            # 모델 확인
            if not self.client.is_configured():
                return False, "Gemini API가 초기화되지 않았습니다."
            
            # 요청 전송
            if generation_config:
                response = self.client.model.generate_content(prompt, generation_config=generation_config)
            else:
                response = self.client.model.generate_content(prompt)
            
            # 응답 확인
            if not response or not response.text:
                return False, "API 응답이 비어있습니다."
            
            logger.info("Gemini API 요청 성공")
            return True, response.text
            
        except Exception as e:
            error_msg = str(e)
            logger.error(f"Gemini API 요청 실패: {error_msg}")
            
            # API 키 관련 에러인지 확인
            if "API key" in error_msg or "400" in error_msg:
                 return False, f"API 키 오류 또는 잘못된 요청입니다. ({error_msg})"
            
            # 재시도 로직
            if retry_count < gemini_config.MAX_RETRIES:
                logger.info(f"{gemini_config.RETRY_DELAY}초 후 재시도...")
                time.sleep(gemini_config.RETRY_DELAY)
                return self.send(prompt, retry_count + 1, generation_config)
            
            return error_handler.handle_api_error(e)
    
    def send_with_context(
        self, 
        prompt: str, 
        context: str = ""
    ) -> tuple[bool, str | Dict]:
        """
        컨텍스트와 함께 요청 전송
        
        Args:
            prompt: 프롬프트
            context: 추가 컨텍스트
            
        Returns:
            (성공 여부, 응답 또는 에러 메시지)
        """
        if context:
            full_prompt = f"{context}\n\n{prompt}"
        else:
            full_prompt = prompt
        
        return self.send(full_prompt)


def create_request_handler(client: GeminiClient) -> GeminiRequest:
    """요청 핸들러 생성"""
    return GeminiRequest(client)
