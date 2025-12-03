"""
결과 확인 페이지
분석 결과 표시 및 다운로드
"""
import streamlit as st
from frontend.components import result_viewer, download_button


def render():
    """페이지 렌더링"""
    st.header("3단계: 결과 확인")
    
    # 분석 결과 확인
    if 'analysis_result' not in st.session_state:
        st.warning("분석 결과가 없습니다. 먼저 분석을 실행해주세요.")
        return
    
    # 결과 뷰어
    result_viewer.render(st.session_state['analysis_result'])
    
    # 다운로드 버튼
    st.markdown("---")
    download_button.render()
