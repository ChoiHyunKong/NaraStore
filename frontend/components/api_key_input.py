"""
API 키 입력 컴포넌트
보안 입력 필드
"""
import streamlit as st
from backend.utils.validator import validator


def render():
    """API 키 입력 UI 렌더링"""
    
    api_key = st.text_input(
        "Gemini API 키",
        type="password",
        placeholder="API 키를 입력하세요",
        help="Google AI Studio에서 발급받은 API 키를 입력하세요."
    )
    
    if api_key:
        # API 키 검증
        is_valid, message = validator.validate_api_key(api_key)
        
        if not is_valid:
            st.error(message)
            return None
        
        st.success("유효한 API 키입니다.")
        return api_key
    
    return None
