"""
제안서 요약 및 분석 이력 페이지
과거 분석 이력 조회 및 PDF 재다운로드
"""
import streamlit as st
from datetime import datetime


def render():
    """페이지 렌더링"""
    st.header("3. 제안서 요약 및 분석 이력")
    
    st.info("제안서 요약 및 분석의 진행 이력을 확인하고 PDF를 다시 다운로드할 수 있습니다.")
    
    # TODO: 실제 이력 데이터 로드
    # 임시 데이터
    history_data = [
        {
            "id": 1,
            "type": "요약",
            "title": "2024년 스마트시티 구축 사업",
            "date": "2024-12-03 14:30",
            "files": ["제안요청서_1.pdf", "제안요청서_2.pdf"]
        },
        {
            "id": 2,
            "type": "분석",
            "title": "공공데이터 활용 시스템 구축",
            "date": "2024-12-02 10:15",
            "files": ["제안서.hwp"]
        }
    ]
    
    if not history_data:
        st.warning("아직 분석 이력이 없습니다.")
        return
    
    # 이력 목록 표시
    st.subheader(f"총 {len(history_data)}개의 이력")
    
    for item in history_data:
        with st.expander(f"[{item['type']}] {item['title']} - {item['date']}", expanded=False):
            col1, col2, col3 = st.columns([3, 1, 1])
            
            with col1:
                st.write("**업로드된 파일:**")
                for file in item['files']:
                    st.write(f"- {file}")
            
            with col2:
                if st.button("📥 PDF 다운로드", key=f"download_{item['id']}", use_container_width=True):
                    # TODO: 실제 PDF 다운로드 구현
                    st.download_button(
                        label="PDF 저장",
                        data=b"PDF content",
                        file_name=f"{item['title']}.pdf",
                        mime="application/pdf",
                        key=f"save_{item['id']}"
                    )
            
            with col3:
                if st.button("🗑️ 삭제", key=f"delete_{item['id']}", use_container_width=True):
                    # TODO: 실제 삭제 구현
                    st.warning("삭제하시겠습니까?")
