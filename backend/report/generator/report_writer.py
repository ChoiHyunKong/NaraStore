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
        self.set_auto_page_break(auto=True, margin=15)
        
        # 한글 폰트 설정 (시스템 폰트 사용)
        try:
            # Windows 기본 한글 폰트 경로
            font_path = "C:\\Windows\\Fonts\\malgun.ttf"
            font_bold_path = "C:\\Windows\\Fonts\\malgunbd.ttf"
            
            if os.path.exists(font_path):
                self.add_font("Malgun", "", font_path, uni=True)
                
                # 볼드체 등록
                if os.path.exists(font_bold_path):
                    self.add_font("Malgun", "B", font_bold_path, uni=True)
                    self.add_font("Malgun", "BI", font_bold_path, uni=True)  # Bold Italic도 Bold로 대체
                else:
                    self.add_font("Malgun", "B", font_path, uni=True)
                    self.add_font("Malgun", "BI", font_path, uni=True)
                
                # 이탤릭체 등록 (별도 파일 없으므로 일반/볼드로 대체)
                self.add_font("Malgun", "I", font_path, uni=True)
                
                self.font_family = "Malgun"
            else:
                self.font_family = "Arial"
        except:
            self.font_family = "Arial"
    
    def header(self):
        """페이지 헤더"""
        self.set_font(self.font_family, 'B', 15)
        self.cell(0, 10, 'NaraStore - 제안서 분석 레포트', 0, 1, 'C')
        self.ln(5)
    
    def footer(self):
        """페이지 푸터"""
        self.set_y(-15)
        self.set_font(self.font_family, 'I', 8)
        self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')
    
    def chapter_title(self, title: str):
        """챕터 제목"""
        self.set_font(self.font_family, 'B', 12)
        self.cell(0, 10, title, 0, 1, 'L')
        self.ln(2)
    
    def chapter_body(self, body: str):
        """챕터 본문"""
        self.set_font(self.font_family, '', 10)
        self.multi_cell(0, 6, body)
        self.ln()


class SummaryReportGenerator:
    """제안서 요약 레포트 생성기"""
    
    @staticmethod
    def _dict_to_text(data, indent=0) -> str:
        """딕셔너리를 읽기 쉬운 텍스트로 변환"""
        if isinstance(data, str):
            return data
        elif isinstance(data, dict):
            lines = []
            for key, value in data.items():
                key_name = key.replace("_", " ").title()
                if isinstance(value, str):
                    lines.append(f"{'  ' * indent}• {key_name}: {value}")
                elif isinstance(value, list):
                    lines.append(f"{'  ' * indent}• {key_name}:")
                    for item in value:
                        if isinstance(item, dict):
                            lines.append(SummaryReportGenerator._dict_to_text(item, indent+1))
                        else:
                            lines.append(f"{'  ' * (indent+1)}- {item}")
                elif isinstance(value, dict):
                    lines.append(f"{'  ' * indent}• {key_name}:")
                    lines.append(SummaryReportGenerator._dict_to_text(value, indent+1))
            return "\n".join(lines)
        elif isinstance(data, list):
            return "\n".join([f"- {item}" if isinstance(item, str) else SummaryReportGenerator._dict_to_text(item, indent) for item in data])
        else:
            return str(data)
    
    @staticmethod
    def generate(summary_data: Dict, output_path: str) -> tuple[bool, str]:
        """
        요약 레포트 PDF 생성
        
        Args:
            summary_data: 요약 데이터
            output_path: 출력 파일 경로
            
        Returns:
            (성공 여부, 메시지)
        """
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
        """
        분석 레포트 PDF 생성
        
        Args:
            analysis_data: 분석 데이터
            strategy_text: 전략 텍스트
            output_path: 출력 파일 경로
            
        Returns:
            (성공 여부, 메시지)
        """
        try:
            logger.info("분석 레포트 생성 시작")
            
            pdf = ReportWriter()
            pdf.add_page()
            
            # 생성 일시
            pdf.set_font(pdf.font_family, '', 9)
            pdf.cell(0, 6, f'생성일시: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}', 0, 1, 'R')
            pdf.ln(5)
            
            # 분석 데이터 표시
            if "raw_text" in analysis_data:
                # JSON 파싱 실패 시 원본 텍스트
                pdf.chapter_title("분석 결과")
                pdf.chapter_body(analysis_data["raw_text"][:3000])  # 최대 3000자
            else:
                # 구조화된 데이터
                for key, value in analysis_data.items():
                    pdf.chapter_title(key.replace("_", " ").title())
                    if isinstance(value, list):
                        text = "\n".join([f"- {item}" for item in value])
                    else:
                        text = str(value)
                    pdf.chapter_body(text[:1000])  # 각 섹션 최대 1000자
            
            # 수주 전략
            if strategy_text:
                pdf.add_page()
                pdf.chapter_title("수주 전략")
                pdf.chapter_body(strategy_text[:3000])  # 최대 3000자
            
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
