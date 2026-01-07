"""
PDF 레포트 작성
제안서 요약 및 분석 결과를 PDF로 생성 (Card UI Style)
"""
from fpdf import FPDF, HTMLMixin
from datetime import datetime
from typing import Dict, List, Any
from backend.utils.logger import logger
import os


class ReportWriter(FPDF, HTMLMixin):
    """PDF 레포트 작성 클래스 (Card UI Style)"""
    
    def __init__(self):
        super().__init__()
        self.set_auto_page_break(auto=True, margin=20)
        
        # 한글 폰트 설정
        try:
            # 윈도우 기본 폰트 경로 시도
            fonts = [
                ("Malgun", "", "C:\\Windows\\Fonts\\malgun.ttf"),
                ("Malgun", "B", "C:\\Windows\\Fonts\\malgunbd.ttf"),
            ]
            
            font_loaded = False
            for family, style, path in fonts:
                if os.path.exists(path):
                    self.add_font(family, style, path, uni=True)
                    font_loaded = True
            
            if font_loaded:
                self.font_family = "Malgun"
            else:
                self.font_family = "Arial"
        except:
            self.font_family = "Arial"
        
        self.title_text = "NaraStore AI Analysis Report"

    def header(self):
        if self.page_no() > 1:
            self.set_font(self.font_family, '', 9)
            self.set_text_color(150, 150, 150)
            self.cell(0, 10, self.title_text, 0, 0, 'R')
            self.ln(12)

    def footer(self):
        self.set_y(-15)
        self.set_font(self.font_family, '', 8)
        self.set_text_color(150, 150, 150)
        self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')

    def add_card_title(self, title: str, icon: str = "■"):
        """카드 섹션 제목"""
        self.set_font(self.font_family, 'B', 14)
        self.set_text_color(79, 70, 229)  # Indigo-600
        self.cell(0, 10, f"{icon}  {title}", 0, 1)
        self.ln(2)

    def data_card(self, title: str, content: str | List[str], bg_color=(249, 250, 251)):
        """데이터를 카드 형태로 표시"""
        # 저장 현재 위치
        x = self.get_x()
        y = self.get_y()
        
        # 카드 배경 (부드러운 회색)
        self.set_fill_color(*bg_color)
        self.set_draw_color(229, 231, 235)  # Gray-200
        self.set_line_width(0.5)
        
        # 내용 계산
        self.set_font(self.font_family, '', 10)
        self.set_text_color(55, 65, 81)  # Gray-700
        
        # 먼저 높이 계산을 위해 더미 출력
        if isinstance(content, list):
            text_block = "\n".join([f"• {item}" for item in content])
        else:
            text_block = str(content)
            
        # 카드 헤더 (제목)
        self.set_font(self.font_family, 'B', 11)
        self.set_text_color(17, 24, 39)  # Gray-900
        self.cell(0, 8, title, 0, 1)
        
        # 카드 본문
        self.set_font(self.font_family, '', 10)
        self.set_text_color(55, 65, 81)
        self.multi_cell(0, 6, text_block)
        
        # 간격
        self.ln(5)

class FullReportGenerator:
    """통합 분석 레포트 생성기"""
    
    @staticmethod
    def generate(analysis_result: Dict, output_path: str) -> tuple[bool, str]:
        try:
            pdf = ReportWriter()
            pdf.add_page()
            
            # --- 표지 ---
            pdf.set_fill_color(79, 70, 229) # Indigo
            pdf.rect(0, 0, 210, 15, 'F')
            pdf.ln(40)
            
            pdf.set_font(pdf.font_family, 'B', 24)
            pdf.set_text_color(17, 24, 39)
            pdf.cell(0, 15, analysis_result.get('summary', {}).get('project_name', '제안서 분석 보고서'), 0, 1, 'C')
            
            pdf.set_font(pdf.font_family, '', 14)
            pdf.set_text_color(107, 114, 128)
            pdf.cell(0, 10, "AI Powered Proposal Strategy & Requirement Analysis", 0, 1, 'C')
            
            pdf.ln(20)
            pdf.line(50, pdf.get_y(), 160, pdf.get_y())
            pdf.ln(20)
            
            # 메타 데이터
            summary = analysis_result.get('summary', {})
            meta_Fields = [
                ("사업 기간", summary.get('period', '-')),
                ("사업 예산", summary.get('budget', '-')),
                ("분석 일시", datetime.now().strftime("%Y-%m-%d %H:%M"))
            ]
            
            pdf.set_font(pdf.font_family, '', 11)
            pdf.set_text_color(55, 65, 81)
            for label, value in meta_Fields:
                pdf.cell(0, 8, f"{label}: {value}", 0, 1, 'C')
                
            pdf.add_page()
            
            # --- 1. 요약 (Summary) ---
            pdf.add_card_title("1. 프로젝트 핵심 요약")
            pdf.data_card("기대 효과", summary.get('expected_effects', []))
            pdf.ln(5)
            
            # --- 2. 요구사항 분석 (Requirements) ---
            pdf.add_card_title("2. 요구사항 상세 분석")
            
            requirements = analysis_result.get('requirements', [])
            # Schema 변경 대응: List[Dict] or Dict
            if isinstance(requirements, dict):
                # 구버전 (혹시 모를 호환성)
                for cat, items in requirements.items():
                    pdf.data_card(cat, items)
            elif isinstance(requirements, list):
                # 신버전 List[RequirementCategory]
                for req in requirements:
                    cat_name = req.get('category', '기타')
                    items = req.get('items', [])
                    pdf.data_card(cat_name, items)
            
            pdf.ln(5)
            
            # --- 3. 수주 전략 (Strategy) ---
            pdf.add_page()
            pdf.add_card_title("3. 수주 및 제안 전략")
            
            strategy = analysis_result.get('strategy', {})
            pdf.data_card("WIN-STRATEGY (수주 전략)", strategy.get('win_strategy', []), (238, 242, 255)) # Indigo-50
            pdf.data_card("유사 사업 레퍼런스", strategy.get('references', []))
            
            # --- 4. To-Do List ---
            pdf.ln(5)
            pdf.add_card_title("4. Action Plan (To-Do)")
            pdf.data_card("추천 수행 작업", analysis_result.get('todo_list', []))
            
            pdf.output(output_path)
            return True, output_path
            
        except Exception as e:
            logger.error(f"PDF 생성 실패: {str(e)}")
            import traceback
            logger.error(traceback.format_exc())
            return False, str(e)
