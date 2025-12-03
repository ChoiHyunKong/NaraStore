"""
이력 관리 매니저
JSON 파일을 사용한 분석 이력 영구 저장
"""
import json
import os
from datetime import datetime
from typing import List, Dict, Optional
from backend.utils.logger import logger
from config.settings import settings


class HistoryManager:
    """분석 이력 관리 클래스"""
    
    def __init__(self):
        # 이력 저장 경로 설정
        self.storage_dir = os.path.join(os.getcwd(), "data")
        self.history_file = os.path.join(self.storage_dir, "history.json")
        
        # 디렉토리 생성
        if not os.path.exists(self.storage_dir):
            os.makedirs(self.storage_dir)
            
        # 파일 초기화
        if not os.path.exists(self.history_file):
            self._save_history([])
    
    def _load_history(self) -> List[Dict]:
        """이력 파일 로드"""
        try:
            with open(self.history_file, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"이력 로드 실패: {str(e)}")
            return []
    
    def _save_history(self, history: List[Dict]):
        """이력 파일 저장"""
        try:
            with open(self.history_file, "w", encoding="utf-8") as f:
                json.dump(history, f, ensure_ascii=False, indent=2)
        except Exception as e:
            logger.error(f"이력 저장 실패: {str(e)}")
    
    def add_entry(self, entry_type: str, files: List[str], data: Dict, pdf_path: str, strategy: str = None, references: Dict = None):
        """
        이력 추가
        
        Args:
            entry_type: '요약' 또는 '분석'
            files: 파일명 리스트
            data: 분석 결과 데이터
            pdf_path: PDF 파일 경로
            strategy: 수주 전략 (분석인 경우)
            references: 레퍼런스 (분석인 경우)
        """
        history = self._load_history()
        
        new_entry = {
            "id": datetime.now().strftime("%Y%m%d%H%M%S"),
            "type": entry_type,
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "files": files,
            "data": data,
            "pdf_path": pdf_path,
            "strategy": strategy,
            "references": references
        }
        
        history.append(new_entry)
        self._save_history(history)
        logger.info(f"이력 추가 완료: {new_entry['id']}")
    
    def get_all(self) -> List[Dict]:
        """모든 이력 조회 (최신순)"""
        history = self._load_history()
        return list(reversed(history))
    
    def delete_entry(self, entry_id: str) -> bool:
        """
        이력 삭제
        
        Args:
            entry_id: 삭제할 이력 ID
            
        Returns:
            성공 여부
        """
        history = self._load_history()
        
        # 해당 ID의 이력 찾기
        target_entry = next((item for item in history if item["id"] == entry_id), None)
        
        if target_entry:
            # PDF 파일 삭제 시도
            if target_entry.get("pdf_path") and os.path.exists(target_entry["pdf_path"]):
                try:
                    os.remove(target_entry["pdf_path"])
                except Exception as e:
                    logger.warning(f"PDF 파일 삭제 실패: {str(e)}")
            
            # 리스트에서 제거
            history = [item for item in history if item["id"] != entry_id]
            self._save_history(history)
            logger.info(f"이력 삭제 완료: {entry_id}")
            return True
            
        return False


# 전역 인스턴스
history_manager = HistoryManager()
