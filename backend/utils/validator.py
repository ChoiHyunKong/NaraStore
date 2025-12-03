"""
입력 검증 유틸리티
파일 형식, 크기, API 키 검증
"""
import os
from typing import Tuple
from config.settings import settings


class Validator:
    """입력 검증 클래스"""
    
    @staticmethod
    def validate_file_extension(file_path: str) -> Tuple[bool, str]:
        """
        파일 확장자 검증
        
        Returns:
            (유효성, 메시지)
        """
        ext = os.path.splitext(file_path)[1].lower()
        
        if ext not in settings.ALLOWED_EXTENSIONS:
            allowed = ", ".join(settings.ALLOWED_EXTENSIONS)
            return False, f"지원하지 않는 파일 형식입니다. 지원 형식: {allowed}"
        
        return True, "유효한 파일 형식입니다."
    
    @staticmethod
    def validate_file_size(file_size: int) -> Tuple[bool, str]:
        """
        파일 크기 검증
        
        Returns:
            (유효성, 메시지)
        """
        if file_size > settings.MAX_FILE_SIZE_BYTES:
            max_mb = settings.MAX_FILE_SIZE_MB
            current_mb = file_size / (1024 * 1024)
            return False, f"파일 크기가 너무 큽니다. (최대: {max_mb}MB, 현재: {current_mb:.2f}MB)"
        
        if file_size == 0:
            return False, "파일이 비어있습니다."
        
        return True, "유효한 파일 크기입니다."
    
    @staticmethod
    def validate_api_key(api_key: str) -> Tuple[bool, str]:
        """
        API 키 검증
        
        Returns:
            (유효성, 메시지)
        """
        if not api_key or api_key.strip() == "":
            return False, "API 키를 입력해주세요."
        
        if len(api_key) < 10:
            return False, "유효하지 않은 API 키 형식입니다."
        
        return True, "유효한 API 키입니다."
    
    @staticmethod
    def validate_file(file_path: str) -> Tuple[bool, str]:
        """
        파일 종합 검증
        
        Returns:
            (유효성, 메시지)
        """
        # 파일 존재 확인
        if not os.path.exists(file_path):
            return False, "파일을 찾을 수 없습니다."
        
        # 확장자 검증
        is_valid, message = Validator.validate_file_extension(file_path)
        if not is_valid:
            return False, message
        
        # 크기 검증
        file_size = os.path.getsize(file_path)
        is_valid, message = Validator.validate_file_size(file_size)
        if not is_valid:
            return False, message
        
        return True, "파일 검증 완료"


# 전역 인스턴스
validator = Validator()
