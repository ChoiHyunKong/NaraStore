"""
파일 처리 유틸리티
파일 읽기, 쓰기, 임시 파일 관리
"""
import os
import tempfile
import shutil
from pathlib import Path
from typing import Optional


class FileHandler:
    """파일 처리 클래스"""
    
    @staticmethod
    def save_uploaded_file(uploaded_file, upload_dir: str) -> str:
        """
        업로드된 파일을 저장
        
        Args:
            uploaded_file: Streamlit 업로드 파일 객체
            upload_dir: 저장 디렉토리
            
        Returns:
            저장된 파일 경로
        """
        os.makedirs(upload_dir, exist_ok=True)
        file_path = os.path.join(upload_dir, uploaded_file.name)
        
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        return file_path
    
    @staticmethod
    def get_file_extension(file_path: str) -> str:
        """파일 확장자 추출"""
        return Path(file_path).suffix.lower()
    
    @staticmethod
    def get_file_size(file_path: str) -> int:
        """파일 크기 반환 (바이트)"""
        return os.path.getsize(file_path)
    
    @staticmethod
    def create_temp_file(suffix: str = "") -> str:
        """임시 파일 생성"""
        temp_file = tempfile.NamedTemporaryFile(
            delete=False, 
            suffix=suffix
        )
        temp_file.close()
        return temp_file.name
    
    @staticmethod
    def delete_file(file_path: str) -> bool:
        """파일 삭제"""
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
                return True
            return False
        except Exception:
            return False
    
    @staticmethod
    def ensure_directory(directory: str):
        """디렉토리 존재 확인 및 생성"""
        os.makedirs(directory, exist_ok=True)
    
    @staticmethod
    def clean_directory(directory: str):
        """디렉토리 내 모든 파일 삭제"""
        if os.path.exists(directory):
            shutil.rmtree(directory)
        os.makedirs(directory, exist_ok=True)


# 전역 인스턴스
file_handler = FileHandler()
