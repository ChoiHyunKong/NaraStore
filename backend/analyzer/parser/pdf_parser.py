"""
PDF 파일 파싱
pypdf를 사용한 텍스트 추출
"""
from pypdf import PdfReader
from typing import Dict, List
from backend.utils.logger import logger
from backend.utils.error_handler import error_handler


class PDFParser:
    """PDF 파서 클래스"""
    
    @staticmethod
    def extract_text(file_path: str) -> tuple[bool, str | Dict]:
        """
        PDF 파일에서 텍스트 추출
        
        Args:
            file_path: PDF 파일 경로
            
        Returns:
            (성공 여부, 추출된 텍스트 또는 에러 메시지)
        """
        try:
            logger.info(f"PDF 파싱 시작: {file_path}")
            
            reader = PdfReader(file_path)
            total_pages = len(reader.pages)
            
            # 전체 텍스트 추출
            full_text = ""
            for page_num, page in enumerate(reader.pages, 1):
                text = page.extract_text()
                full_text += f"\n--- 페이지 {page_num} ---\n{text}\n"
            
            # 메타데이터 추출
            metadata = reader.metadata
            
            result = {
                "text": full_text.strip(),
                "total_pages": total_pages,
                "metadata": {
                    "title": metadata.get("/Title", ""),
                    "author": metadata.get("/Author", ""),
                    "subject": metadata.get("/Subject", ""),
                    "creator": metadata.get("/Creator", "")
                } if metadata else {}
            }
            
            logger.info(f"PDF 파싱 완료: {total_pages}페이지")
            return True, result
            
        except Exception as e:
            return error_handler.handle_parsing_error(e, "PDF")
    
    @staticmethod
    def extract_text_by_page(file_path: str) -> tuple[bool, List[str] | str]:
        """
        페이지별로 텍스트 추출
        
        Returns:
            (성공 여부, 페이지별 텍스트 리스트 또는 에러 메시지)
        """
        try:
            reader = PdfReader(file_path)
            pages_text = []
            
            for page in reader.pages:
                text = page.extract_text()
                pages_text.append(text)
            
            return True, pages_text
            
        except Exception as e:
            return error_handler.handle_parsing_error(e, "PDF")


# 전역 인스턴스
pdf_parser = PDFParser()
