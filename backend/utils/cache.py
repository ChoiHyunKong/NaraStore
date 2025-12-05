"""
분석 결과 캐싱 시스템
동일 문서 재분석 시 API 호출 절약
"""
import hashlib
import json
import os
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from backend.utils.logger import logger


class AnalysisCache:
    """분석 결과 캐시 관리"""
    
    def __init__(self, cache_dir: str = None, ttl_hours: int = 24):
        """
        캐시 초기화
        
        Args:
            cache_dir: 캐시 저장 디렉토리
            ttl_hours: 캐시 유효 시간 (시간)
        """
        if cache_dir is None:
            cache_dir = os.path.join(os.getcwd(), "data", "cache")
        
        self.cache_dir = cache_dir
        self.ttl = timedelta(hours=ttl_hours)
        
        # 캐시 디렉토리 생성
        if not os.path.exists(self.cache_dir):
            os.makedirs(self.cache_dir)
    
    def _get_hash(self, text: str, analysis_type: str) -> str:
        """텍스트 해시 생성"""
        content = f"{analysis_type}:{text}"
        return hashlib.md5(content.encode()).hexdigest()
    
    def _get_cache_path(self, cache_key: str) -> str:
        """캐시 파일 경로"""
        return os.path.join(self.cache_dir, f"{cache_key}.json")
    
    def get(self, text: str, analysis_type: str) -> Optional[Dict[str, Any]]:
        """
        캐시에서 분석 결과 조회
        
        Args:
            text: 문서 텍스트
            analysis_type: 분석 유형 (summary, analysis, strategy, references)
            
        Returns:
            캐시된 결과 또는 None
        """
        cache_key = self._get_hash(text[:5000], analysis_type)  # 앞 5000자로 해시
        cache_path = self._get_cache_path(cache_key)
        
        if not os.path.exists(cache_path):
            return None
        
        try:
            with open(cache_path, 'r', encoding='utf-8') as f:
                cache_data = json.load(f)
            
            # TTL 확인
            cached_time = datetime.fromisoformat(cache_data.get('cached_at', ''))
            if datetime.now() - cached_time > self.ttl:
                logger.info(f"캐시 만료됨: {cache_key}")
                os.remove(cache_path)
                return None
            
            logger.info(f"캐시 히트: {analysis_type} ({cache_key[:8]}...)")
            return cache_data.get('result')
            
        except Exception as e:
            logger.warning(f"캐시 조회 실패: {str(e)}")
            return None
    
    def set(self, text: str, analysis_type: str, result: Dict[str, Any]) -> bool:
        """
        분석 결과를 캐시에 저장
        
        Args:
            text: 문서 텍스트
            analysis_type: 분석 유형
            result: 분석 결과
            
        Returns:
            저장 성공 여부
        """
        cache_key = self._get_hash(text[:5000], analysis_type)
        cache_path = self._get_cache_path(cache_key)
        
        try:
            cache_data = {
                'cached_at': datetime.now().isoformat(),
                'analysis_type': analysis_type,
                'result': result
            }
            
            with open(cache_path, 'w', encoding='utf-8') as f:
                json.dump(cache_data, f, ensure_ascii=False, indent=2)
            
            logger.info(f"캐시 저장: {analysis_type} ({cache_key[:8]}...)")
            return True
            
        except Exception as e:
            logger.warning(f"캐시 저장 실패: {str(e)}")
            return False
    
    def clear(self) -> int:
        """
        모든 캐시 삭제
        
        Returns:
            삭제된 파일 수
        """
        count = 0
        for filename in os.listdir(self.cache_dir):
            if filename.endswith('.json'):
                os.remove(os.path.join(self.cache_dir, filename))
                count += 1
        
        logger.info(f"캐시 전체 삭제: {count}개 파일")
        return count
    
    def get_stats(self) -> Dict[str, Any]:
        """캐시 통계 조회"""
        files = [f for f in os.listdir(self.cache_dir) if f.endswith('.json')]
        total_size = sum(
            os.path.getsize(os.path.join(self.cache_dir, f)) 
            for f in files
        )
        
        return {
            'count': len(files),
            'total_size_kb': round(total_size / 1024, 2),
            'cache_dir': self.cache_dir
        }


# 전역 캐시 인스턴스
analysis_cache = AnalysisCache()
