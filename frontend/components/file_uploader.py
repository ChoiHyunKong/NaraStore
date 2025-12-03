"""
파일 업로드 컴포넌트
드래그 앤 드롭 파일 업로드
"""
import streamlit as st
from config.settings import settings
from backend.utils.validator import validator


def render():
    """파일 업로드 UI 렌더링"""
    
    uploaded_file = st.file_uploader(
        "파일 선택",
        type=["pdf", "hwp", "pptx"],
        help=f"최대 파일 크기: {settings.MAX_FILE_SIZE_MB}MB"
    )
    
    if uploaded_file:
        # 파일 크기 검증
        file_size = len(uploaded_file.getvalue())
        is_valid, message = validator.validate_file_size(file_size)
        
        if not is_valid:
            st.error(message)
            return None
        
        # 파일 정보 표시
        col1, col2 = st.columns(2)
        with col1:
            st.metric("파일명", uploaded_file.name)
        with col2:
            st.metric("파일 크기", f"{file_size / 1024 / 1024:.2f} MB")
        
        return uploaded_file
    
    return None
