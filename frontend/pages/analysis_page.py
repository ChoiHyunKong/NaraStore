"""
분석 실행 페이지
API 키 입력 및 분석 실행
"""
import streamlit as st
from frontend.components import api_key_input, progress_bar


def render():
    """페이지 렌더링"""
    st.header("2단계: 분석 실행")
    
    # 파일 업로드 확인
    if 'uploaded_file' not in st.session_state:
        st.warning("먼저 파일을 업로드해주세요.")
        return
    
    # API 키 입력
    api_key = api_key_input.render()
    
    if not api_key:
        st.info("Gemini API 키를 입력하면 분석을 시작할 수 있습니다.")
        return
    
    # 분석 실행 버튼
    if st.button("분석 시작", type="primary", use_container_width=True):
        with st.spinner("분석 중..."):
            # 진행 상태 표시
            progress_bar.render(0.3, "문서 파싱 중...")
            
            # TODO: 실제 분석 로직 구현
            import time
            time.sleep(1)
            
            progress_bar.render(0.6, "AI 분석 중...")
            time.sleep(1)
            
            progress_bar.render(1.0, "분석 완료!")
            
            st.success("분석이 완료되었습니다!")
            st.info("사이드바에서 '결과 확인' 페이지로 이동하세요.")
