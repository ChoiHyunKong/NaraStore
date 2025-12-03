"""
제안서 요약 페이지
복수 파일 업로드 및 요약 레포트 생성
"""
import streamlit as st
from frontend.components import file_uploader


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
                
                with st.spinner("제안서를 분석하는 중입니다..."):
                    # TODO: 실제 분석 로직 구현
                    import time
                    time.sleep(2)
                    
                    st.success("분석 완료!")
                    
                    # 임시 결과 표시
                    st.markdown("### 📋 분석 결과")
                    st.write("분석 결과가 여기에 표시됩니다.")
                    
                    # PDF 다운로드 버튼
                    st.download_button(
                        label="📥 PDF 레포트 다운로드",
                        data=b"PDF content",
                        file_name="제안서_요약.pdf",
                        mime="application/pdf"
                    )
        
        with col2:
            if st.button("🔍 제안서 분석", use_container_width=True):
                st.session_state['current_page'] = "제안서 분석"
                st.session_state['uploaded_files'] = uploaded_files
                st.rerun()
    
    else:
        st.info("제안서 파일을 업로드해주세요.")
