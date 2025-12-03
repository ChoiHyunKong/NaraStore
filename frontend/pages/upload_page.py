"""
파일 업로드 페이지
제안서 파일 업로드 UI
"""
import streamlit as st
from frontend.components import file_uploader


def render():
    """페이지 렌더링"""
    st.header("1단계: 제안서 파일 업로드")
    
    st.info("분석할 제안요청서(RFP) 파일을 업로드해주세요. PDF, HWP, PPTX 형식을 지원합니다.")
    
    # 파일 업로드 컴포넌트
    uploaded_file = file_uploader.render()
    
    if uploaded_file:
        # 세션에 저장
        st.session_state['uploaded_file'] = uploaded_file
        st.success(f"파일 업로드 완료: {uploaded_file.name}")
        
        # 다음 단계 안내
        st.info("사이드바에서 '분석 실행' 페이지로 이동하세요.")
    else:
        # 세션 초기화
        if 'uploaded_file' in st.session_state:
            del st.session_state['uploaded_file']
