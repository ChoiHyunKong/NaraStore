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
            
            # 프로젝트 개요
            if "project_overview" in summary_data:
                pdf.chapter_title("1. 프로젝트 개요")
                pdf.chapter_body(summary_data["project_overview"])
            
            # 프로젝트 목표 및 목적
            if "project_goal" in summary_data:
                pdf.chapter_title("2. 프로젝트 목표 및 목적")
                pdf.chapter_body(summary_data["project_goal"])
            
            # 배경 및 필요성
            if "background" in summary_data:
                pdf.chapter_title("3. 프로젝트 배경 및 필요성")
                pdf.chapter_body(summary_data["background"])
            
            # 주요 과업
            if "main_tasks" in summary_data and summary_data["main_tasks"]:
                pdf.chapter_title("4. 주요 과업 내용")
                tasks_text = "\n".join([f"- {task}" for task in summary_data["main_tasks"]])
                pdf.chapter_body(tasks_text)
            
            # 금액 및 마감일
            budget_deadline = []
            if "budget" in summary_data and summary_data["budget"]:
                budget_deadline.append(f"예산: {summary_data['budget']}")
            if "deadline" in summary_data and summary_data["deadline"]:
                budget_deadline.append(f"마감일: {summary_data['deadline']}")
            
            if budget_deadline:
                pdf.chapter_title("5. 프로젝트 정보")
                pdf.chapter_body("\n".join(budget_deadline))
            
            # 핵심 요구사항
            if "key_requirements" in summary_data and summary_data["key_requirements"]:
                pdf.chapter_title("6. 핵심 요구사항")
                reqs_text = "\n".join([f"- {req}" for req in summary_data["key_requirements"]])
                pdf.chapter_body(reqs_text)
            
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
