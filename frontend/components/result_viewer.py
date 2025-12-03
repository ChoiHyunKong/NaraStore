"""
결과 뷰어 컴포넌트
분석 결과 표시
"""
import streamlit as st


def render(result: dict):
    """
    분석 결과 표시
    
    Args:
        result: 분석 결과 딕셔너리
    """
    if not result:
        st.warning("표시할 결과가 없습니다.")
        return
    
    # 탭으로 섹션 분리
    tabs = st.tabs(["요약", "상세 분석", "수주 전략"])
    
    with tabs[0]:
        st.subheader("프로젝트 요약")
        st.write(result.get("summary", "요약 정보 없음"))
    
    with tabs[1]:
        st.subheader("상세 분석")
        st.write(result.get("analysis", "분석 정보 없음"))
    
    with tabs[2]:
        st.subheader("수주 전략")
        st.write(result.get("strategy", "전략 정보 없음"))
