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

# 세션 초기화
if 'current_page' not in st.session_state:
    st.session_state['current_page'] = "제안서 요약"

# 헤더
st.title("📄 " + settings.APP_TITLE)
st.markdown("---")

# 사이드바 메뉴
with st.sidebar:
    st.header("메뉴")
    
    # 페이지 변경 감지를 위한 임시 변수
    new_page = st.radio(
        "페이지 선택",
        ["제안서 요약", "제안서 분석", "제안서 요약 및 분석 이력"],
        index=["제안서 요약", "제안서 분석", "제안서 요약 및 분석 이력"].index(st.session_state['current_page']),
        label_visibility="collapsed"
    )
    
    st.markdown("---")
    st.caption("v1.0.0 | NaraStore")

# 페이지 변경 시 경고 (분석 중인 경우에만)
if new_page != st.session_state['current_page']:
    if st.session_state.get('analysis_in_progress', False):
        st.warning("⚠️ 페이지 이동 시 진행된 내용은 사라지며 제안서 요약 및 분석 이력에서 볼 수 있습니다.")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("확인", use_container_width=True):
                st.session_state['current_page'] = new_page
                st.session_state['analysis_in_progress'] = False
                st.rerun()
        with col2:
            if st.button("취소", use_container_width=True):
                st.rerun()
    else:
        st.session_state['current_page'] = new_page

# 페이지 라우팅
if st.session_state['current_page'] == "제안서 요약":
    from frontend.pages import summary_page
    summary_page.render()
elif st.session_state['current_page'] == "제안서 분석":
    from frontend.pages import analysis_page
    analysis_page.render()
elif st.session_state['current_page'] == "제안서 요약 및 분석 이력":
    from frontend.pages import history_page
    history_page.render()
