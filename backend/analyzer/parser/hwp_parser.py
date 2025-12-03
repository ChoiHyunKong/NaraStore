"""
HWP 파일 파싱
olefile을 사용한 텍스트 추출
"""
import olefile
import zlib
import struct
from typing import Dict
from backend.utils.logger import logger
from backend.utils.error_handler import error_handler


class HWPParser:
    """HWP 파서 클래스"""
    
    @staticmethod
    def extract_text(file_path: str) -> tuple[bool, str | Dict]:
        """
        HWP 파일에서 텍스트 추출
        
        Args:
            file_path: HWP 파일 경로
            
        Returns:
            (성공 여부, 추출된 텍스트 또는 에러 메시지)
        """
        try:
            logger.info(f"HWP 파싱 시작: {file_path}")
            
            ole = olefile.OleFileIO(file_path)
            
            # 섹션 텍스트 추출
            sections = []
            section_num = 0
            
            while True:
                section_name = f"BodyText/Section{section_num}"
                if not ole.exists(section_name):
                    break
                
                section_data = ole.openstream(section_name).read()
                section_text = HWPParser._decompress_section(section_data)
                sections.append(section_text)
                section_num += 1
            
            ole.close()
            
            full_text = "\n\n".join(sections)
            
            result = {
                "text": full_text.strip(),
                "total_sections": len(sections)
            }
            
            logger.info(f"HWP 파싱 완료: {len(sections)}개 섹션")
            return True, result
            
        except Exception as e:
            return error_handler.handle_parsing_error(e, "HWP")
    
    @staticmethod
    def _decompress_section(data: bytes) -> str:
        """
        HWP 섹션 데이터 압축 해제 및 텍스트 추출
        """
        try:
            # 압축 해제 시도
            unpacked = zlib.decompress(data, -15)
        except:
            # 압축되지 않은 데이터
            unpacked = data
        
        # 텍스트 추출 (간단한 방식)
        text = ""
        i = 0
        while i < len(unpacked):
            try:
                # 한글 문자 추출 시도
                if i + 1 < len(unpacked):
                    char_code = struct.unpack('<H', unpacked[i:i+2])[0]
                    if 0xAC00 <= char_code <= 0xD7A3:  # 한글 범위
                        text += chr(char_code)
                        i += 2
                        continue
                
                # ASCII 문자
                if 32 <= unpacked[i] <= 126:
                    text += chr(unpacked[i])
                elif unpacked[i] in [10, 13]:  # 줄바꿈
                    text += '\n'
                
                i += 1
            except:
                i += 1
        
        return text


# 전역 인스턴스
hwp_parser = HWPParser()
