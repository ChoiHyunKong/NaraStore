"""
PDF 레포트 작성
제안서 요약 및 분석 결과를 PDF로 생성
"""
from fpdf import FPDF
from datetime import datetime
from typing import Dict
from backend.utils.logger import logger
import os


class ReportWriter(FPDF):
    """PDF 레포트 작성 클래스"""
    
    def __init__(self):
        super().__init__()
        self.set_auto_page_break(auto=True, margin=20)
        
        # 한글 폰트 설정 (시스템 폰트 사용)
        try:
            font_path = "C:\\Windows\\Fonts\\malgun.ttf"
            font_bold_path = "C:\\Windows\\Fonts\\malgunbd.ttf"
            
            if os.path.exists(font_path):
                self.add_font("Malgun", "", font_path, uni=True)
                if os.path.exists(font_bold_path):
                    self.add_font("Malgun", "B", font_bold_path, uni=True)
                    self.add_font("Malgun", "BI", font_bold_path, uni=True)
                else:
                    self.add_font("Malgun", "B", font_path, uni=True)
                    self.add_font("Malgun", "BI", font_path, uni=True)
                self.add_font("Malgun", "I", font_path, uni=True)
                self.font_family = "Malgun"
            else:
                self.font_family = "Arial"
        except:
            self.font_family = "Arial"
        
        self.title_text = "NaraStore 제안서 분석 레포트"
    
    def add_cover_page(self, title: str, subtitle: str = ""):
        """표지 페이지 추가"""
        self.add_page()
        
        # 상단 장식 라인
        self.set_fill_color(41, 128, 185)  # 파란색
        self.rect(0, 0, 210, 8, 'F')
        
        # 제목 영역
        self.ln(60)
        self.set_font(self.font_family, 'B', 28)
        self.set_text_color(41, 128, 185)
        self.multi_cell(0, 15, "NaraStore", 0, 'C')
        
        self.set_font(self.font_family, 'B', 18)
        self.set_text_color(0, 0, 0)
        self.multi_cell(0, 12, "제안서 분석 레포트", 0, 'C')
        
        self.ln(20)
        
        # 프로젝트 제목
        if title:
            self.set_font(self.font_family, 'B', 14)
            self.set_text_color(52, 73, 94)
            self.multi_cell(0, 10, title, 0, 'C')
        
        if subtitle:
            self.ln(5)
            self.set_font(self.font_family, '', 11)
            self.set_text_color(100, 100, 100)
            self.multi_cell(0, 8, subtitle, 0, 'C')
        
        # 하단 정보
        self.set_y(-40)
        self.set_font(self.font_family, '', 10)
        self.set_text_color(100, 100, 100)
        self.cell(0, 8, f"생성일: {datetime.now().strftime('%Y년 %m월 %d일 %H:%M')}", 0, 1, 'C')
        
        self.set_text_color(0, 0, 0)
    
    def header(self):
        """페이지 헤더"""
        if self.page_no() > 1:  # 표지 제외
            self.set_font(self.font_family, '', 9)
            self.set_text_color(100, 100, 100)
            self.cell(0, 8, self.title_text, 0, 1, 'R')
            self.ln(3)
            self.set_text_color(0, 0, 0)
    
    def footer(self):
        """페이지 푸터"""
        self.set_y(-15)
        self.set_font(self.font_family, '', 8)
        self.set_text_color(100, 100, 100)
        self.cell(0, 10, f'- {self.page_no()} -', 0, 0, 'C')
    
    def section_title(self, title: str, color=(41, 128, 185)):
        """섹션 제목 (색상 강조)"""
        self.set_fill_color(*color)
        self.set_text_color(255, 255, 255)
        self.set_font(self.font_family, 'B', 12)
        self.cell(0, 10, f"  {title}", 0, 1, 'L', True)
        self.set_text_color(0, 0, 0)
        self.ln(3)
    
    def chapter_title(self, title: str):
        """챕터 제목"""
        self.set_font(self.font_family, 'B', 11)
        self.set_text_color(52, 73, 94)
        self.cell(0, 8, title, 0, 1, 'L')
        self.set_text_color(0, 0, 0)
        self.ln(2)
    
    def chapter_body(self, body: str):
        """챕터 본문"""
        self.set_font(self.font_family, '', 10)
        self.multi_cell(0, 6, body)
        self.ln(3)
    
    def info_box(self, label: str, value: str, color=(230, 126, 34)):
        """정보 박스 (강조) - 간단 형식"""
        self.set_font(self.font_family, 'B', 10)
        self.set_text_color(*color)
        # 값이 너무 길면 자르기
        display_value = value if len(str(value)) < 80 else str(value)[:80] + "..."
        self.multi_cell(0, 6, f"▶ {label}: {display_value}")
        self.set_text_color(0, 0, 0)
        self.ln(1)
    
    def separator(self):
        """구분선"""
        self.ln(3)


class SummaryReportGenerator:
    """제안서 요약 레포트 생성기"""
    
    @staticmethod
    def _format_key(key: str) -> str:
        """키 이름을 읽기 좋게 변환"""
        translations = {
            'total_amount': '총 금액',
            'vat_included': '부가세 포함',
            'budget_type': '예산 유형',
            'total_period': '총 기간',
            'start_date': '시작일',
            'end_date': '종료일',
            'proposal_deadline': '제안서 마감',
            'onsite_required': '상주 필요',
            'onsite_count': '상주 인원',
            'onsite_location': '상주 장소',
            'key_personnel': '핵심 인력',
            'role': '역할',
            'count': '인원',
            'skills': '필요 역량',
            'duration': '기간',
            'certification': '자격 요건',
            'human': '인력 요구사항',
            'technical': '기술 요구사항',
            'type': '유형',
            'name': '이름',
            'version': '버전',
            'reason': '사유',
            'task_name': '과업명',
            'description': '설명',
        }
        return translations.get(key, key.replace('_', ' ').title())
    
    @staticmethod
    def _dict_to_text(data, indent=0) -> str:
        """딕셔너리를 읽기 쉬운 텍스트로 변환"""
        prefix = "  " * indent
        
        if data is None:
            return ""
        
        if isinstance(data, str):
            return data
        
        if isinstance(data, bool):
            return "예" if data else "아니오"
        
        if isinstance(data, (int, float)):
            return str(data)
        
        if isinstance(data, list):
            if not data:
                return "없음"
            lines = []
            for item in data:
                if isinstance(item, dict):
                    # 딕셔너리 리스트의 경우 각 항목을 정리
                    item_lines = []
                    for k, v in item.items():
                        key_name = SummaryReportGenerator._format_key(k)
                        if isinstance(v, list):
                            v_str = ", ".join(str(x) for x in v)
                        else:
                            v_str = str(v) if v else "정보 없음"
                        item_lines.append(f"{key_name}: {v_str}")
                    lines.append(f"{prefix}- " + " / ".join(item_lines))
                else:
                    lines.append(f"{prefix}- {item}")
            return "\n".join(lines)
        
        if isinstance(data, dict):
            if not data:
                return "없음"
            lines = []
            for key, value in data.items():
                key_name = SummaryReportGenerator._format_key(key)
                
                if isinstance(value, str):
                    lines.append(f"{prefix}• {key_name}: {value}")
                elif isinstance(value, bool):
                    lines.append(f"{prefix}• {key_name}: {'예' if value else '아니오'}")
                elif isinstance(value, (int, float)):
                    lines.append(f"{prefix}• {key_name}: {value}")
                elif isinstance(value, list):
                    if value:
                        lines.append(f"{prefix}• {key_name}:")
                        lines.append(SummaryReportGenerator._dict_to_text(value, indent + 1))
                    else:
                        lines.append(f"{prefix}• {key_name}: 없음")
                elif isinstance(value, dict):
                    lines.append(f"{prefix}• {key_name}:")
                    lines.append(SummaryReportGenerator._dict_to_text(value, indent + 1))
                else:
                    lines.append(f"{prefix}• {key_name}: {str(value)}")
            return "\n".join(lines)
        
        return str(data)
    
    @staticmethod
    def generate(summary_data: Dict, output_path: str) -> tuple[bool, str]:
        """요약 레포트 PDF 생성"""
        try:
            logger.info("요약 레포트 생성 시작")
            
            pdf = ReportWriter()
            pdf.add_page()
            
            # 생성 일시
            pdf.set_font(pdf.font_family, '', 9)
            pdf.cell(0, 6, f'생성일시: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}', 0, 1, 'R')
            pdf.ln(5)
            
            section_num = 1
            
            # 프로젝트 제목
            if "project_title" in summary_data:
                pdf.set_font(pdf.font_family, 'B', 14)
                pdf.multi_cell(0, 8, summary_data["project_title"])
                pdf.ln(5)
            
            # 프로젝트 개요
            if "project_overview" in summary_data:
                pdf.chapter_title(f"{section_num}. 프로젝트 개요")
                pdf.chapter_body(SummaryReportGenerator._dict_to_text(summary_data["project_overview"]))
                section_num += 1
            
            # 예산 정보
            if "budget" in summary_data:
                pdf.chapter_title(f"{section_num}. 예산 정보")
                pdf.chapter_body(SummaryReportGenerator._dict_to_text(summary_data["budget"]))
                section_num += 1
            
            # 사업 일정
            if "schedule" in summary_data:
                pdf.chapter_title(f"{section_num}. 사업 일정")
                pdf.chapter_body(SummaryReportGenerator._dict_to_text(summary_data["schedule"]))
                section_num += 1
            
            # 인력 요구사항
            if "personnel" in summary_data:
                pdf.chapter_title(f"{section_num}. 인력 요구사항")
                pdf.chapter_body(SummaryReportGenerator._dict_to_text(summary_data["personnel"]))
                section_num += 1
            
            # 배경 및 필요성
            if "background" in summary_data:
                pdf.chapter_title(f"{section_num}. 배경 및 필요성")
                pdf.chapter_body(SummaryReportGenerator._dict_to_text(summary_data["background"]))
                section_num += 1
            
            # 프로젝트 목표
            if "project_goal" in summary_data:
                pdf.chapter_title(f"{section_num}. 프로젝트 목표")
                pdf.chapter_body(SummaryReportGenerator._dict_to_text(summary_data["project_goal"]))
                section_num += 1
            
            # 주요 과업
            if "main_tasks" in summary_data and summary_data["main_tasks"]:
                pdf.chapter_title(f"{section_num}. 주요 과업")
                tasks = summary_data["main_tasks"]
                if isinstance(tasks, list):
                    for idx, task in enumerate(tasks, 1):
                        if isinstance(task, dict):
                            task_name = task.get("task_name", f"과업 {idx}")
                            pdf.set_font(pdf.font_family, 'B', 10)
                            pdf.cell(0, 6, f"  {idx}. {task_name}", 0, 1)
                            pdf.set_font(pdf.font_family, '', 10)
                            if "description" in task:
                                pdf.multi_cell(0, 5, f"     {task['description']}")
                        else:
                            pdf.chapter_body(f"- {task}")
                    pdf.ln()
                section_num += 1
            
            # 기술 요구사항
            if "technical_requirements" in summary_data:
                pdf.chapter_title(f"{section_num}. 기술 요구사항")
                pdf.chapter_body(SummaryReportGenerator._dict_to_text(summary_data["technical_requirements"]))
                section_num += 1
            
            # 참여 자격
            if "qualification" in summary_data:
                pdf.chapter_title(f"{section_num}. 참여 자격")
                pdf.chapter_body(SummaryReportGenerator._dict_to_text(summary_data["qualification"]))
                section_num += 1
            
            # 계약 정보
            if "contract_info" in summary_data:
                pdf.chapter_title(f"{section_num}. 계약 정보")
                pdf.chapter_body(SummaryReportGenerator._dict_to_text(summary_data["contract_info"]))
                section_num += 1
            
            # 핵심 고려사항
            if "key_considerations" in summary_data:
                pdf.chapter_title(f"{section_num}. 핵심 고려사항")
                pdf.chapter_body(SummaryReportGenerator._dict_to_text(summary_data["key_considerations"]))
                section_num += 1
            
            # PDF 저장
            pdf.output(output_path)
            
            logger.info(f"요약 레포트 생성 완료: {output_path}")
            return True, "레포트 생성 완료"
            
        except Exception as e:
            logger.error(f"레포트 생성 실패: {str(e)}")
            return False, f"레포트 생성 실패: {str(e)}"


class AnalysisReportGenerator:
    """제안서 분석 레포트 생성기"""
    
    @staticmethod
    def generate(analysis_data: Dict, strategy_text: str, output_path: str) -> tuple[bool, str]:
        """분석 레포트 PDF 생성"""
        try:
            logger.info("분석 레포트 생성 시작")
            
            pdf = ReportWriter()
            pdf.add_page()
            
            # 생성 일시
            pdf.set_font(pdf.font_family, '', 9)
            pdf.cell(0, 6, f'생성일시: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}', 0, 1, 'R')
            pdf.ln(5)
            
            # 제목
            pdf.set_font(pdf.font_family, 'B', 16)
            pdf.cell(0, 10, "제안서 상세 분석 결과", 0, 1, 'C')
            pdf.ln(5)
            
            section_num = 1
            
            # 분석 데이터 표시
            if "raw_text" in analysis_data:
                pdf.chapter_title("분석 결과")
                pdf.chapter_body(analysis_data["raw_text"][:3000])
            else:
                # 섹션별 한글 제목
                section_titles = {
                    'functional_requirements': '기능적 요구사항',
                    'non_functional_requirements': '비기능적 요구사항',
                    'technical_requirements': '기술적 요구사항',
                    'required_resources': '필요 자원',
                    'constraints': '제약 사항',
                    'evaluation_criteria': '평가 기준',
                    'key_deliverables': '주요 산출물',
                    'risks': '위험 요소',
                    'success_factors': '성공 요인',
                }
                
                for key, value in analysis_data.items():
                    title = section_titles.get(key, key.replace("_", " ").title())
                    pdf.chapter_title(f"{section_num}. {title}")
                    
                    # SummaryReportGenerator의 포맷 함수 사용
                    formatted_text = SummaryReportGenerator._dict_to_text(value)
                    pdf.chapter_body(formatted_text[:2000])
                    section_num += 1
            
            # 수주 전략
            if strategy_text:
                pdf.add_page()
                pdf.set_font(pdf.font_family, 'B', 14)
                pdf.cell(0, 10, "수주 전략", 0, 1, 'L')
                pdf.ln(3)
                
                # 전략 텍스트도 파싱 시도
                if isinstance(strategy_text, dict):
                    pdf.chapter_body(SummaryReportGenerator._dict_to_text(strategy_text))
                else:
                    pdf.chapter_body(str(strategy_text)[:3000])
            
            # PDF 저장
            pdf.output(output_path)
            
            logger.info(f"분석 레포트 생성 완료: {output_path}")
            return True, "레포트 생성 완료"
            
        except Exception as e:
            logger.error(f"레포트 생성 실패: {str(e)}")
            return False, f"레포트 생성 실패: {str(e)}"


# 전역 인스턴스
summary_report_generator = SummaryReportGenerator()
analysis_report_generator = AnalysisReportGenerator()
