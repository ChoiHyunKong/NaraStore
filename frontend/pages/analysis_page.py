"""
제안서 분석 페이지
상세 요구사항 분석 및 수주 전략 수립
"""
import streamlit as st


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
            
            with st.spinner("제안서를 분석하는 중입니다..."):
                # TODO: 실제 분석 로직 구현
                import time
                time.sleep(2)
                
                st.success("분석 완료!")
                
                # 분석 결과 탭
                tab1, tab2, tab3 = st.tabs(["요구사항 분석", "수주 전략", "유사 프로젝트"])
                
                with tab1:
                    st.markdown("### 📋 상세 요구사항 분석")
                    st.write("각 요구사항에 대한 상세 분석 결과가 여기에 표시됩니다.")
                
                with tab2:
                    st.markdown("### 🎯 수주 전략")
                    st.write("요구사항 이행을 위한 전략이 여기에 표시됩니다.")
                
                with tab3:
                    st.markdown("### 📚 유사 프로젝트 레퍼런스")
                    st.write("유사한 프로젝트 사례가 여기에 표시됩니다.")
                
                # PDF 다운로드 버튼
                st.markdown("---")
                st.download_button(
                    label="📥 분석 PDF 레포트 다운로드",
                    data=b"PDF content",
                    file_name="제안서_분석.pdf",
                    mime="application/pdf",
                    use_container_width=True
                )
    
    else:
        st.info("제안서 파일을 업로드해주세요.")
