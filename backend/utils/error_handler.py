"""
에러 처리 유틸리티
예외 처리 및 사용자 친화적 메시지 생성
"""
from typing import Tuple, Optional
from backend.utils.logger import logger


class ErrorHandler:
    """에러 처리 클래스"""
    
    @staticmethod
    def handle_file_error(error: Exception, file_path: str = "") -> Tuple[bool, str]:
        """
        파일 관련 에러 처리
        
        Returns:
            (성공 여부, 사용자 메시지)
        """
        error_msg = str(error)
        logger.error(f"파일 에러: {error_msg} (파일: {file_path})")
        
        if "Permission" in error_msg:
            return False, "파일 접근 권한이 없습니다."
        elif "No such file" in error_msg:
            return False, "파일을 찾을 수 없습니다."
        elif "decode" in error_msg.lower():
            return False, "파일 인코딩 오류입니다. 파일이 손상되었을 수 있습니다."
        else:
            return False, f"파일 처리 중 오류가 발생했습니다: {error_msg}"
    
    @staticmethod
    def handle_api_error(error: Exception) -> Tuple[bool, str]:
        """
        API 관련 에러 처리
        
        Returns:
            (성공 여부, 사용자 메시지)
        """
        error_msg = str(error)
        logger.error(f"API 에러: {error_msg}")
        
        if "API key" in error_msg or "authentication" in error_msg.lower():
            return False, "API 키가 유효하지 않습니다. 설정을 확인해주세요."
        elif "quota" in error_msg.lower():
            return False, "API 사용량 한도를 초과했습니다."
        elif "timeout" in error_msg.lower():
            return False, "API 요청 시간이 초과되었습니다. 다시 시도해주세요."
        elif "rate limit" in error_msg.lower():
            return False, "API 요청 횟수 제한에 도달했습니다. 잠시 후 다시 시도해주세요."
        else:
            return False, f"API 호출 중 오류가 발생했습니다: {error_msg}"
    
    @staticmethod
    def handle_parsing_error(error: Exception, file_type: str = "") -> Tuple[bool, str]:
        """
        파싱 관련 에러 처리
        
        Returns:
            (성공 여부, 사용자 메시지)
        """
        error_msg = str(error)
        logger.error(f"파싱 에러 ({file_type}): {error_msg}")
        
        return False, f"{file_type} 파일 파싱 중 오류가 발생했습니다. 파일이 손상되었거나 지원하지 않는 형식일 수 있습니다."
    
    @staticmethod
    def handle_general_error(error: Exception, context: str = "") -> Tuple[bool, str]:
        """
        일반 에러 처리
        
        Returns:
            (성공 여부, 사용자 메시지)
        """
        error_msg = str(error)
        logger.error(f"일반 에러 ({context}): {error_msg}")
        
        return False, f"처리 중 오류가 발생했습니다: {error_msg}"


# 전역 인스턴스
error_handler = ErrorHandler()
