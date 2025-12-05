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
        self.pdf_dir = os.path.join(self.storage_dir, "pdfs")
        self.history_file = os.path.join(self.storage_dir, "history.json")
        
        # 디렉토리 생성
        if not os.path.exists(self.storage_dir):
            os.makedirs(self.storage_dir)
        
        # PDF 저장 디렉토리 생성
        if not os.path.exists(self.pdf_dir):
            os.makedirs(self.pdf_dir)
            logger.info(f"PDF 저장 디렉토리 생성: {self.pdf_dir}")
            
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
            pdf_path: PDF 파일 경로 (절대 경로 또는 상대 경로)
            strategy: 수주 전략 (분석인 경우)
            references: 레퍼런스 (분석인 경우)
        """
        import shutil
        
        history = self._load_history()
        entry_id = datetime.now().strftime("%Y%m%d%H%M%S")
        
        # PDF 파일을 영구 저장소로 복사
        permanent_pdf_path = None
        if pdf_path and os.path.exists(pdf_path):
            try:
                # 새 파일명 생성
                pdf_filename = f"{entry_type}_{entry_id}.pdf"
                permanent_pdf_path = os.path.join(self.pdf_dir, pdf_filename)
                
                # 파일 복사
                shutil.copy2(pdf_path, permanent_pdf_path)
                logger.info(f"PDF 파일 영구 저장: {permanent_pdf_path}")
                
                # 상대 경로로 저장 (이식성 향상)
                relative_path = os.path.join("data", "pdfs", pdf_filename)
                
            except Exception as e:
                logger.error(f"PDF 파일 복사 실패: {str(e)}")
                relative_path = pdf_path  # 실패 시 원본 경로 사용
        else:
            logger.warning(f"PDF 파일을 찾을 수 없음: {pdf_path}")
            relative_path = pdf_path
        
        new_entry = {
            "id": entry_id,
            "type": entry_type,
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "files": files,
            "data": data,
            "pdf_path": relative_path,
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
    
    def get_pdf_path(self, entry: Dict) -> Optional[str]:
        """
        이력 항목에서 PDF 파일의 절대 경로 가져오기
        
        Args:
            entry: 이력 항목
            
        Returns:
            PDF 파일의 절대 경로 (존재하지 않으면 None)
        """
        pdf_path = entry.get("pdf_path")
        if not pdf_path:
            return None
        
        # 이미 절대 경로인 경우
        if os.path.isabs(pdf_path):
            return pdf_path if os.path.exists(pdf_path) else None
        
        # 상대 경로인 경우 프로젝트 루트 기준으로 변환
        absolute_path = os.path.join(os.getcwd(), pdf_path)
        return absolute_path if os.path.exists(absolute_path) else None
    
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
            pdf_path = self.get_pdf_path(target_entry)
            if pdf_path and os.path.exists(pdf_path):
                try:
                    os.remove(pdf_path)
                    logger.info(f"PDF 파일 삭제 완료: {pdf_path}")
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
