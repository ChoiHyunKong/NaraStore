"""
Streamlit 메인 애플리케이션
페이지 라우팅 및 전역 설정
"""
import streamlit as st
import sys
import os

# 프로젝트 루트 경로를 sys.path에 추가하여 모듈 import 오류 해결
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
if project_root not in sys.path:
    sys.path.append(project_root)

from config.settings import settings

# 페이지 설정
st.set_page_config(
    page_title=settings.APP_TITLE,
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 전역 CSS 로드 (캐싱 적용)
@st.cache_data
def load_css():
    """통합 CSS 파일 로드 및 캐싱"""
    css_path = os.path.join(project_root, "frontend", "styles", "main.css")
    try:
        with open(css_path, encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        # 폴백: 개별 파일 로드
        combined_css = ""
        for css_file in ["common", "header", "sidebar", "content", "footer"]:
            try:
                fallback_path = os.path.join(project_root, "frontend", "styles", f"{css_file}.css")
                with open(fallback_path, encoding="utf-8") as f:
                    combined_css += f.read() + "\n"
            except FileNotFoundError:
                pass
        return combined_css

# CSS 적용
st.markdown(f"<style>{load_css()}</style>", unsafe_allow_html=True)

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

# 페이지 변경 시 경고 (분석 완료 후 또는 진행 중)
if new_page != st.session_state['current_page']:
    # 분석 진행 중이거나 방금 완료된 경우 경고 표시
    show_warning = (
        st.session_state.get('analysis_in_progress', False) or 
        st.session_state.get('analysis_just_completed', False)
    )
    
    if show_warning:
        st.warning("⚠️ 페이지 이동 시 진행된 내용은 사라지며 제안서 요약 및 분석 이력에서 볼 수 있습니다.")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("확인", key="confirm_navigation", use_container_width=True):
                st.session_state['current_page'] = new_page
                st.session_state['analysis_in_progress'] = False
                st.session_state['analysis_just_completed'] = False
                st.rerun()
        with col2:
            if st.button("취소", key="cancel_navigation", use_container_width=True):
                st.rerun()
    else:
        st.session_state['current_page'] = new_page

# 페이지 라우팅
if st.session_state['current_page'] == "제안서 요약":
    from frontend.views import summary_page
    summary_page.render()
elif st.session_state['current_page'] == "제안서 분석":
    from frontend.views import analysis_page
    analysis_page.render()
elif st.session_state['current_page'] == "제안서 요약 및 분석 이력":
    from frontend.views import history_page
    history_page.render()
