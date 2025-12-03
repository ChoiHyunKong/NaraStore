"""
로깅 유틸리티
파일 및 콘솔 로깅
"""
import logging
import os
from datetime import datetime
from config.settings import settings


class Logger:
    """로깅 클래스"""
    
    def __init__(self, name: str = "NaraStore"):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG if settings.DEBUG_MODE else logging.INFO)
        
        # 이미 핸들러가 있으면 추가하지 않음
        if not self.logger.handlers:
            self._setup_handlers()
    
    def _setup_handlers(self):
        """로그 핸들러 설정"""
        # 포맷 설정
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        # 콘솔 핸들러
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)
        
        # 파일 핸들러 (디버그 모드일 때만)
        if settings.DEBUG_MODE:
            log_dir = os.path.join(settings.BASE_DIR, "logs")
            os.makedirs(log_dir, exist_ok=True)
            
            log_file = os.path.join(
                log_dir, 
                f"app_{datetime.now().strftime('%Y%m%d')}.log"
            )
            
            file_handler = logging.FileHandler(log_file, encoding='utf-8')
            file_handler.setLevel(logging.DEBUG)
            file_handler.setFormatter(formatter)
            self.logger.addHandler(file_handler)
    
    def debug(self, message: str):
        """디버그 로그"""
        self.logger.debug(message)
    
    def info(self, message: str):
        """정보 로그"""
        self.logger.info(message)
    
    def warning(self, message: str):
        """경고 로그"""
        self.logger.warning(message)
    
    def error(self, message: str):
        """에러 로그"""
        self.logger.error(message)
    
    def critical(self, message: str):
        """치명적 에러 로그"""
        self.logger.critical(message)


# 전역 로거 인스턴스
logger = Logger()
