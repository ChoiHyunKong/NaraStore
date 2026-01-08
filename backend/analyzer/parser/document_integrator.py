"""
문서 파서 통합
복수 파일을 하나의 텍스트로 통합
"""
import os
from typing import List, Tuple
from backend.analyzer.parser.pdf_parser import pdf_parser
from backend.analyzer.parser.hwp_parser import hwp_parser
from backend.analyzer.parser.pptx_parser import pptx_parser
from backend.analyzer.parser.text_cleaner import text_cleaner
from backend.utils.file_handler import file_handler
from backend.utils.logger import logger
from backend.utils.error_handler import error_handler


class DocumentIntegrator:
    """문서 통합 클래스"""
    
    @staticmethod
    def parse_multiple_files(uploaded_files) -> Tuple[bool, str]:
        """
        복수 파일 파싱 및 통합
        
        Args:
            uploaded_files: Streamlit 업로드 파일 리스트
            
        Returns:
            (성공 여부, 통합된 텍스트 또는 에러 메시지)
        """
        try:
            combined_text = ""
            
            for idx, uploaded_file in enumerate(uploaded_files, 1):
                logger.info(f"파일 {idx}/{len(uploaded_files)} 파싱 시작: {uploaded_file.name}")
                
                # 임시 파일로 저장
                temp_path = file_handler.create_temp_file(
                    suffix=os.path.splitext(uploaded_file.name)[1]
                )
                
                with open(temp_path, "wb") as f:
                    f.write(uploaded_file.getvalue())
                
                # 파일 확장자에 따라 파서 선택
                ext = file_handler.get_file_extension(temp_path)
                
                if ext == ".pdf":
                    success, result = pdf_parser.extract_text(temp_path)
                elif ext == ".hwp":
                    success, result = hwp_parser.extract_text(temp_path)
                elif ext == ".pptx":
                    success, result = pptx_parser.extract_text(temp_path)
                else:
                    file_handler.delete_file(temp_path)
                    return False, f"지원하지 않는 파일 형식: {ext}"
                
                # 임시 파일 삭제
                file_handler.delete_file(temp_path)
                
                if not success:
                    error_msg = (
                        f"파일 '{uploaded_file.name}' 파싱 실패\n\n"
                        f"**원인**: {result}\n\n"
                        f"**해결 방법**:\n"
                        f"- 파일이 손상되지 않았는지 확인하세요\n"
                        f"- 파일 형식이 표준 {ext.upper()} 형식인지 확인하세요\n"
                        f"- 파일을 다른 형식으로 변환 후 재시도하세요"
                    )
                    return False, error_msg
                
                # 텍스트 추출
                if isinstance(result, dict):
                    text = result.get("text", "")
                else:
                    text = result
                
                # [FIX] 텍스트 유효성 검사 (헤더 추가 전)
                if not text or len(text.strip()) < 50:
                     return False, f"파일 '{uploaded_file.name}'에서 유효한 텍스트를 추출할 수 없습니다.\n스캔된 이미지 PDF이거나 내용이 비어있을 수 있습니다."
                
                # 파일 구분자 추가
                combined_text += f"\n\n{'='*80}\n"
                combined_text += f"파일: {uploaded_file.name}\n"
                combined_text += f"{'='*80}\n\n"
                combined_text += text
            
            # 텍스트 유효성 검사 및 정제
            cleaned_text = text_cleaner.clean(combined_text)
            
            if not cleaned_text or len(cleaned_text.strip()) < 50:
                 return False, "문서에서 유효한 텍스트를 추출할 수 없습니다. 스캔된 이미지 PDF이거나 내용이 비어있을 수 있습니다.\n텍스트를 선택할 수 있는지 확인하거나 OCR 처리가 된 파일을 사용해주세요."

            logger.info(f"총 {len(uploaded_files)}개 파일 파싱 완료 (텍스트 길이: {len(cleaned_text)})")
            return True, cleaned_text
            
        except Exception as e:
            logger.error(f"문서 통합 중 오류: {str(e)}")
            return error_handler.handle_general_error(e, "문서 통합")


# 전역 인스턴스
document_integrator = DocumentIntegrator()
