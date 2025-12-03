"""
제안서 요약 및 분석 이력 페이지
과거 분석 이력 조회 및 PDF 재다운로드
"""
import streamlit as st
import os


def render():
    """페이지 렌더링"""
    st.header("3. 제안서 요약 및 분석 이력")
    
    st.info("제안서 요약 및 분석의 진행 이력을 확인하고 PDF를 다시 다운로드할 수 있습니다.")
    
    # 세션 상태에서 이력 로드
    if 'analysis_history' not in st.session_state:
        st.session_state['analysis_history'] = []
    
    history_data = st.session_state['analysis_history']
    
    if not history_data:
        st.warning("아직 분석 이력이 없습니다.")
        return
    
    # 이력 목록 표시
    st.subheader(f"총 {len(history_data)}개의 이력")
    
    # 역순으로 표시 (최신순)
    for idx, item in enumerate(reversed(history_data)):
        real_idx = len(history_data) - 1 - idx
        
        # 제목 생성 (파일 이름 기반)
        title = item['files'][0] if item['files'] else "제목 없음"
        if len(item['files']) > 1:
            title += f" 외 {len(item['files'])-1}개"
            
        with st.expander(f"[{item['type']}] {title} - {item['date']}", expanded=False):
            col1, col2, col3 = st.columns([3, 1, 1])
            
            with col1:
                st.write("**업로드된 파일:**")
                for file in item['files']:
                    st.write(f"- {file}")
            
            with col2:
                # PDF 파일이 존재하는지 확인
                pdf_path = item.get('pdf_path')
                if pdf_path and os.path.exists(pdf_path):
                    with open(pdf_path, "rb") as f:
                        pdf_bytes = f.read()
                        
                    st.download_button(
                        label="📥 PDF 다운로드",
                        data=pdf_bytes,
                        file_name=os.path.basename(pdf_path),
                        mime="application/pdf",
                        key=f"download_{real_idx}",
                        use_container_width=True
                    )
                else:
                    st.error("PDF 파일이 만료되었습니다.")
            
            with col3:
                if st.button("🗑️ 삭제", key=f"delete_{real_idx}", use_container_width=True):
                    # 이력 삭제
                    history_data.pop(real_idx)
                    st.rerun()
