"""
제안서 분석 페이지
상세 요구사항 분석 및 수주 전략 수립
"""
import streamlit as st
import os
import tempfile
from datetime import datetime
from backend.analyzer.parser.document_integrator import document_integrator
from backend.analyzer.proposal_analyzer import create_analyzer
from backend.report.generator.report_writer import analysis_report_generator
from config.settings import settings


def render():
    """페이지 렌더링"""
    st.header("2. 제안서 분석")
    
    st.info("""
    수주 확률을 높이기 위한 상세 분석 및 전략을 수립합니다.
    - 각 상세 요구사항 분석
    - 요구사항 이행 전략 도출
    - 유사 프로젝트 레퍼런스
    """)
    
    # 복수 파일 업로드
    st.subheader("📁 제안서 파일 업로드")
    uploaded_files = st.file_uploader(
        "파일 선택 (복수 선택 가능)",
        type=["pdf", "hwp", "pptx"],
        accept_multiple_files=True,
        help="Ctrl 키를 누른 채로 여러 파일을 선택할 수 있습니다.",
        key="analysis_uploader"
    )
    
    # 제안서 요약에서 넘어온 파일 사용
    if 'uploaded_files' in st.session_state and not uploaded_files:
        uploaded_files = st.session_state['uploaded_files']
        st.info(f"제안서 요약에서 업로드한 {len(uploaded_files)}개 파일을 사용합니다.")
    
    if uploaded_files:
        st.success(f"총 {len(uploaded_files)}개 파일 업로드됨")
        
        # 파일 목록 표시
        with st.expander("업로드된 파일 목록", expanded=True):
            for idx, file in enumerate(uploaded_files, 1):
                file_size = len(file.getvalue()) / 1024 / 1024
                st.write(f"{idx}. **{file.name}** ({file_size:.2f} MB)")
        
        # 분석 시작 버튼
        st.markdown("---")
        
        if st.button("📊 상세 분석 시작", type="primary", use_container_width=True):
            st.session_state['analysis_in_progress'] = True
            
            # 진행 상태 표시
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            try:
                # 1. 문서 파싱
                status_text.text("문서 파싱 중...")
                progress_bar.progress(0.1)
                
                success, document_text = document_integrator.parse_multiple_files(uploaded_files)
                
                if not success:
                    st.error(f"문서 파싱 실패: {document_text}")
                    st.session_state['analysis_in_progress'] = False
                    return
                
                analyzer = create_analyzer(settings.GEMINI_API_KEY)
                
                # 2. 상세 요구사항 분석
                status_text.text("상세 요구사항 분석 중...")
                progress_bar.progress(0.3)
                
                success, analysis_result = analyzer.analyze_detailed(document_text)
                
                if not success:
                    st.error(f"분석 실패: {analysis_result}")
                    st.session_state['analysis_in_progress'] = False
                    return
                
                # 3. 수주 전략 도출
                status_text.text("수주 전략 수립 중...")
                progress_bar.progress(0.6)
                
                success, strategy_result = analyzer.generate_strategy(analysis_result)
                
                if not success:
                    st.warning(f"전략 생성 실패: {strategy_result}")
                    strategy_result = "전략 생성에 실패했습니다."
                
                # 4. 유사 프로젝트 레퍼런스
                status_text.text("유사 프로젝트 레퍼런스 검색 중...")
                progress_bar.progress(0.8)
                
                success, reference_result = analyzer.generate_references(analysis_result)
                
                if not success:
                    st.warning(f"레퍼런스 생성 실패: {reference_result}")
                    reference_result = {"references": []}
                
                # 5. PDF 생성
                status_text.text("PDF 레포트 생성 중...")
                progress_bar.progress(0.9)
                
                # 임시 PDF 파일 생성
                output_path = os.path.join(
                    tempfile.gettempdir(),
                    f"analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
                )
                
                success, message = analysis_report_generator.generate(
                    analysis_result, 
                    strategy_result if isinstance(strategy_result, str) else str(strategy_result),
                    output_path
                )
                
                if not success:
                    st.error(f"PDF 생성 실패: {message}")
                    st.session_state['analysis_in_progress'] = False
                    return
                
                # 완료
                progress_bar.progress(1.0)
                status_text.text("완료!")
                st.success("분석 완료!")
                
                # 분석 결과 탭
                tab1, tab2, tab3 = st.tabs(["요구사항 분석", "수주 전략", "유사 프로젝트"])
                
                with tab1:
                    st.markdown("### 📋 상세 요구사항 분석")
                    if isinstance(analysis_result, dict):
                        if "client_needs" in analysis_result:
                            st.markdown("**클라이언트 니즈**")
                            for need in analysis_result["client_needs"]:
                                st.write(f"- {need}")
                        
                        if "requirements" in analysis_result:
                            st.markdown("**상세 요구사항**")
                            for req_group in analysis_result["requirements"]:
                                st.markdown(f"**{req_group.get('category', '기타')}**")
                                for item in req_group.get("items", []):
                                    st.write(f"- {item}")
                    else:
                        st.write(analysis_result)
                
                with tab2:
                    st.markdown("### 🎯 수주 전략")
                    st.markdown(strategy_result)
                
                with tab3:
                    st.markdown("### 📚 유사 프로젝트 레퍼런스")
                    if isinstance(reference_result, dict) and "references" in reference_result:
                        for ref in reference_result["references"]:
                            with st.expander(f"📌 {ref.get('title', '제목 없음')}", expanded=True):
                                st.write(ref.get('description', ''))
                                if "key_features" in ref:
                                    st.markdown("**주요 기능**")
                                    for feature in ref["key_features"]:
                                        st.write(f"- {feature}")
                    else:
                        st.write("추천된 레퍼런스가 없습니다.")
                
                # PDF 다운로드 버튼
                st.markdown("---")
                
                with open(output_path, "rb") as f:
                    pdf_bytes = f.read()
                
                st.download_button(
                    label="📥 분석 PDF 레포트 다운로드",
                    data=pdf_bytes,
                    file_name=f"제안서_분석_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
                    mime="application/pdf",
                    use_container_width=True
                )
                
                # 세션에 결과 저장 (이력용)
                if 'analysis_history' not in st.session_state:
                    st.session_state['analysis_history'] = []
                
                st.session_state['analysis_history'].append({
                    "type": "분석",
                    "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "files": [f.name for f in uploaded_files],
                    "data": analysis_result,
                    "strategy": strategy_result,
                    "references": reference_result,
                    "pdf_path": output_path
                })
                
                st.session_state['analysis_in_progress'] = False
                
            except Exception as e:
                st.error(f"오류 발생: {str(e)}")
                st.session_state['analysis_in_progress'] = False
    
    else:
        st.info("제안서 파일을 업로드해주세요.")
