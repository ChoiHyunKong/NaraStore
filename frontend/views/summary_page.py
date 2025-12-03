"""
제안서 요약 페이지
복수 파일 업로드 및 요약 레포트 생성
"""
import streamlit as st
import os
import tempfile
from datetime import datetime
from backend.analyzer.parser.document_integrator import document_integrator
from backend.analyzer.proposal_analyzer import create_analyzer
from backend.report.generator.report_writer import summary_report_generator
from config.settings import settings


def render():
    """페이지 렌더링"""
    st.header("1. 제안서 요약")
    
    st.info("""
    제안서를 빠르게 파악하기 위한 요약 레포트를 생성합니다.
    - 프로젝트 개요, 목표, 목적
    - 주요 과업 내용
    - 금액 및 마감일
    """)
    
    # 복수 파일 업로드
    st.subheader("📁 제안서 파일 업로드")
    uploaded_files = st.file_uploader(
        "파일 선택 (복수 선택 가능)",
        type=["pdf", "hwp", "pptx"],
        accept_multiple_files=True,
        help="Ctrl 키를 누른 채로 여러 파일을 선택할 수 있습니다."
    )
    
    if uploaded_files:
        st.success(f"총 {len(uploaded_files)}개 파일 업로드됨")
        
        # 파일 목록 표시
        with st.expander("업로드된 파일 목록", expanded=True):
            for idx, file in enumerate(uploaded_files, 1):
                file_size = len(file.getvalue()) / 1024 / 1024
                st.write(f"{idx}. **{file.name}** ({file_size:.2f} MB)")
        
        # 분석 시작 버튼
        st.markdown("---")
        
        col1, col2 = st.columns([3, 1])
        with col1:
            if st.button("📊 요약 분석 시작", type="primary", use_container_width=True):
                st.session_state['analysis_in_progress'] = True
                
                # 진행 상태 표시
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                try:
                    # 1. 문서 파싱
                    status_text.text("문서 파싱 중...")
                    progress_bar.progress(0.2)
                    
                    success, document_text = document_integrator.parse_multiple_files(uploaded_files)
                    
                    if not success:
                        st.error(f"문서 파싱 실패: {document_text}")
                        st.session_state['analysis_in_progress'] = False
                        return
                    
                    # 2. Gemini API 분석
                    status_text.text("AI 분석 중...")
                    progress_bar.progress(0.5)
                    
                    analyzer = create_analyzer(settings.GEMINI_API_KEY)
                    success, summary_data = analyzer.summarize(document_text)
                    
                    if not success:
                        st.error(f"분석 실패: {summary_data}")
                        st.session_state['analysis_in_progress'] = False
                        return
                    
                    # 3. PDF 생성
                    status_text.text("PDF 레포트 생성 중...")
                    progress_bar.progress(0.8)
                    
                    # 임시 PDF 파일 생성
                    output_path = os.path.join(
                        tempfile.gettempdir(),
                        f"summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
                    )
                    
                    success, message = summary_report_generator.generate(summary_data, output_path)
                    
                    if not success:
                        st.error(f"PDF 생성 실패: {message}")
                        st.session_state['analysis_in_progress'] = False
                        return
                    
                    # 완료
                    progress_bar.progress(1.0)
                    status_text.text("완료!")
                    st.success("분석 완료!")
                    
                    # 결과 표시
                    st.markdown("### 📋 분석 결과")
                    
                    if "project_overview" in summary_data:
                        st.markdown("**프로젝트 개요**")
                        st.write(summary_data["project_overview"])
                    
                    if "project_goal" in summary_data:
                        st.markdown("**목표 및 목적**")
                        st.write(summary_data["project_goal"])
                    
                    if "main_tasks" in summary_data and summary_data["main_tasks"]:
                        st.markdown("**주요 과업**")
                        for task in summary_data["main_tasks"]:
                            st.write(f"- {task}")
                    
                    # PDF 다운로드
                    with open(output_path, "rb") as f:
                        pdf_bytes = f.read()
                    
                    st.download_button(
                        label="📥 PDF 레포트 다운로드",
                        data=pdf_bytes,
                        file_name=f"제안서_요약_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
                        mime="application/pdf"
                    )
                    
                    # 세션에 결과 저장 (이력용)
                    if 'analysis_history' not in st.session_state:
                        st.session_state['analysis_history'] = []
                    
                    st.session_state['analysis_history'].append({
                        "type": "요약",
                        "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "files": [f.name for f in uploaded_files],
                        "data": summary_data,
                        "pdf_path": output_path
                    })
                    
                    st.session_state['analysis_in_progress'] = False
                    
                except Exception as e:
                    st.error(f"오류 발생: {str(e)}")
                    st.session_state['analysis_in_progress'] = False
        
        with col2:
            if st.button("🔍 제안서 분석", use_container_width=True):
                st.session_state['current_page'] = "제안서 분석"
                st.session_state['uploaded_files'] = uploaded_files
                st.rerun()
    
    else:
        st.info("제안서 파일을 업로드해주세요.")
