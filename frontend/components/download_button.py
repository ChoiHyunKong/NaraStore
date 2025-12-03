"""
다운로드 버튼 컴포넌트
PDF 레포트 다운로드
"""
import streamlit as st
from datetime import datetime


def render():
    """다운로드 버튼 렌더링"""
    
    # TODO: 실제 PDF 생성 로직 구현
    dummy_pdf = b"PDF content placeholder"
    
    filename = f"분석결과_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
    
    st.download_button(
        label="📥 PDF 레포트 다운로드",
        data=dummy_pdf,
        file_name=filename,
        mime="application/pdf",
        use_container_width=True
    )
