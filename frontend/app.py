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
    st.markdown("### 🗂️ 메뉴")
    
    # 메뉴 아이템 (아이콘 포함)
    menu_items = {
        "제안서 요약": "📋 제안서 요약",
        "제안서 분석": "🔍 제안서 분석", 
        "제안서 요약 및 분석 이력": "📂 이력 조회"
    }
    
    # 페이지 변경 감지를 위한 임시 변수
    new_page = st.radio(
        "페이지 선택",
        list(menu_items.keys()),
        index=list(menu_items.keys()).index(st.session_state['current_page']),
        format_func=lambda x: menu_items[x],
        label_visibility="collapsed"
    )
    
    st.markdown("---")
    
    # 캐시 정보 표시
    try:
        from backend.utils.cache import analysis_cache
        cache_stats = analysis_cache.get_stats()
        
        with st.expander("💾 캐시 정보", expanded=False):
            st.caption(f"저장된 분석: {cache_stats['count']}건")
            st.caption(f"용량: {cache_stats['total_size_kb']} KB")
            
            if st.button("🗑️ 캐시 비우기", use_container_width=True):
                cleared = analysis_cache.clear()
                st.success(f"{cleared}개 삭제됨")
                st.rerun()
    except:
        pass
    
    st.markdown("---")
    st.caption("📦 v1.1.0")
    st.caption("🚀 NaraStore")

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
