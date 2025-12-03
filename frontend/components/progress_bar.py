"""
진행 상태 컴포넌트
진행률 표시
"""
import streamlit as st


def render(progress: float, message: str = ""):
    """
    진행 상태 표시
    
    Args:
        progress: 진행률 (0.0 ~ 1.0)
        message: 상태 메시지
    """
    st.progress(progress)
    if message:
        st.caption(message)
