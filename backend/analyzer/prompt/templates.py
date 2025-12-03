"""
프롬프트 템플릿 관리
YAML 파일 로드 및 캐싱
"""
import yaml
import os
from typing import Dict, Optional
from config.settings import settings
from backend.utils.logger import logger


class PromptTemplates:
    """프롬프트 템플릿 관리 클래스"""
    
    def __init__(self):
        self.templates_dir = os.path.join(settings.BASE_DIR, "config", "prompts")
        self._cache: Dict[str, Dict] = {}
    
    def load(self, template_name: str) -> Optional[Dict]:
        """
        템플릿 파일 로드
        
        Args:
            template_name: 템플릿 파일명 (확장자 제외)
            
        Returns:
            템플릿 데이터 또는 None
        """
        # 캐시 확인
        if template_name in self._cache:
            logger.debug(f"캐시에서 템플릿 로드: {template_name}")
            return self._cache[template_name]
        
        # 파일에서 로드
        file_path = os.path.join(self.templates_dir, f"{template_name}.yaml")
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = yaml.safe_load(f)
            
            # 캐시에 저장
            self._cache[template_name] = data
            logger.info(f"템플릿 로드 완료: {template_name}")
            return data
            
        except FileNotFoundError:
            logger.error(f"템플릿 파일을 찾을 수 없습니다: {file_path}")
            return None
        except yaml.YAMLError as e:
            logger.error(f"YAML 파싱 오류: {str(e)}")
            return None
        except Exception as e:
            logger.error(f"템플릿 로드 실패: {str(e)}")
            return None
    
    def get(self, template_name: str, key: str) -> Optional[str]:
        """
        특정 템플릿의 특정 키 값 가져오기
        
        Args:
            template_name: 템플릿 파일명
            key: 키 이름
            
        Returns:
            템플릿 문자열 또는 None
        """
        data = self.load(template_name)
        if data and key in data:
            return data[key]
        return None
    
    def clear_cache(self):
        """캐시 초기화"""
        self._cache.clear()
        logger.info("템플릿 캐시 초기화")


# 전역 인스턴스
prompt_templates = PromptTemplates()
