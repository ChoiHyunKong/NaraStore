"""
Gemini API 응답 처리
응답 파싱 및 구조화
"""
import json
import re
from typing import Dict, Any
from backend.utils.logger import logger


class GeminiResponse:
    """Gemini API 응답 처리 클래스"""
    
    @staticmethod
    def parse_json(response_text: str) -> tuple[bool, Dict | str]:
        """
        JSON 형식 응답 파싱
        
        Args:
            response_text: API 응답 텍스트
            
        Returns:
            (성공 여부, 파싱된 데이터 또는 에러 메시지)
        """
        try:
            # JSON 코드 블록 추출 시도
            json_match = re.search(r'```json\s*(.*?)\s*```', response_text, re.DOTALL)
            if json_match:
                json_str = json_match.group(1)
            else:
                # 중괄호로 시작하는 JSON 찾기
                json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
                if json_match:
                    json_str = json_match.group(0)
                else:
                    json_str = response_text
            
            # JSON 파싱
            data = json.loads(json_str)
            logger.info("JSON 응답 파싱 성공")
            return True, data
            
        except json.JSONDecodeError as e:
            logger.error(f"JSON 파싱 실패: {str(e)}")
            return False, f"응답을 JSON으로 파싱할 수 없습니다: {str(e)}"
        except Exception as e:
            logger.error(f"응답 처리 실패: {str(e)}")
            return False, f"응답 처리 중 오류 발생: {str(e)}"
    
    @staticmethod
    def extract_sections(response_text: str) -> Dict[str, str]:
        """
        섹션별로 응답 분리
        
        Args:
            response_text: API 응답 텍스트
            
        Returns:
            섹션별 텍스트 딕셔너리
        """
        sections = {}
        
        # 마크다운 헤더로 섹션 분리
        pattern = r'#+\s*(.+?)\n(.*?)(?=\n#+\s|\Z)'
        matches = re.findall(pattern, response_text, re.DOTALL)
        
        for title, content in matches:
            sections[title.strip()] = content.strip()
        
        return sections
    
    @staticmethod
    def clean_response(response_text: str) -> str:
        """
        응답 텍스트 정제
        
        Args:
            response_text: 원본 응답
            
        Returns:
            정제된 응답
        """
        # 코드 블록 제거
        text = re.sub(r'```.*?```', '', response_text, flags=re.DOTALL)
        
        # 연속된 줄바꿈 정리
        text = re.sub(r'\n{3,}', '\n\n', text)
        
        return text.strip()
    
    @staticmethod
    def validate_structure(data: Dict, required_keys: list) -> tuple[bool, str]:
        """
        응답 데이터 구조 검증
        
        Args:
            data: 검증할 데이터
            required_keys: 필수 키 리스트
            
        Returns:
            (유효성, 메시지)
        """
        missing_keys = [key for key in required_keys if key not in data]
        
        if missing_keys:
            return False, f"필수 키가 누락되었습니다: {', '.join(missing_keys)}"
        
        return True, "구조 검증 완료"


# 전역 인스턴스
response_parser = GeminiResponse()
