"""
Streamlit 메인 애플리케이션
페이지 라우팅 및 전역 설정
"""
import streamlit as st
from config.settings import settings

# 페이지 설정
st.set_page_config(
    page_title=settings.APP_TITLE,
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 전역 CSS 로드
def load_css():
    """CSS 파일 로드"""
    css_files = ["common", "header", "sidebar", "content", "footer"]
    for css_file in css_files:
        try:
            with open(f"frontend/styles/{css_file}.css", encoding="utf-8") as f:
                st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
        except FileNotFoundError:
            pass

load_css()

# 헤더
st.title("📄 " + settings.APP_TITLE)
st.markdown("---")

# 사이드바
with st.sidebar:
    st.header("메뉴")
    page = st.radio(
        "페이지 선택",
        ["파일 업로드", "분석 실행", "결과 확인"],
        label_visibility="collapsed"
    )
    
    st.markdown("---")
    st.caption("v1.0.0 | NaraStore")

# 페이지 라우팅
if page == "파일 업로드":
    from frontend.pages import upload_page
    upload_page.render()
elif page == "분석 실행":
    from frontend.pages import analysis_page
    analysis_page.render()
elif page == "결과 확인":
    from frontend.pages import result_page
    result_page.render()
