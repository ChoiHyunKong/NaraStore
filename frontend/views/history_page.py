"""
제안서 요약 및 분석 이력 페이지
과거 분석 이력 조회 및 PDF 재다운로드
"""
import streamlit as st
import os
from datetime import datetime
from backend.storage.history_manager import history_manager


def render():
    """페이지 렌더링"""
    st.header("3. 제안서 요약 및 분석 이력")
    
    # 이력 로드
    history_data = history_manager.get_all()
    
    if not history_data:
        st.info("📂 아직 분석 이력이 없습니다. 제안서 요약 또는 분석을 먼저 진행해주세요.")
        return
    
    # 📊 통계 표시
    total_count = len(history_data)
    summary_count = sum(1 for h in history_data if h.get('type') == '요약')
    analysis_count = sum(1 for h in history_data if h.get('type') == '분석')
    
    col_stat1, col_stat2, col_stat3 = st.columns(3)
    with col_stat1:
        st.metric("📋 전체 이력", f"{total_count}건")
    with col_stat2:
        st.metric("📄 요약", f"{summary_count}건")
    with col_stat3:
        st.metric("🔍 분석", f"{analysis_count}건")
    
    st.markdown("---")
    
    # 🔍 검색 및 필터
    col_search, col_filter, col_sort = st.columns([2, 1, 1])
    
    with col_search:
        search_query = st.text_input("🔍 파일명 검색", placeholder="검색어 입력...")
    
    with col_filter:
        filter_type = st.selectbox("📁 유형 필터", ["전체", "요약", "분석"])
    
    with col_sort:
        sort_order = st.selectbox("📊 정렬", ["최신순", "오래된순"])
    
    # 필터링 적용
    filtered_data = history_data.copy()
    
    # 검색어 필터
    if search_query:
        filtered_data = [
            h for h in filtered_data 
            if any(search_query.lower() in f.lower() for f in h.get('files', []))
        ]
    
    # 유형 필터
    if filter_type != "전체":
        filtered_data = [h for h in filtered_data if h.get('type') == filter_type]
    
    # 정렬
    if sort_order == "오래된순":
        filtered_data = list(reversed(filtered_data))
    
    # 결과 표시
    st.caption(f"검색 결과: {len(filtered_data)}건")
    
    if not filtered_data:
        st.warning("검색 결과가 없습니다.")
        return
    
    # 이력 목록 표시
    for item in filtered_data:
        # 제목 생성
        title = item['files'][0] if item['files'] else "제목 없음"
        if len(item['files']) > 1:
            title += f" 외 {len(item['files'])-1}개"
        
        # 유형별 아이콘
        type_icon = "📄" if item.get('type') == '요약' else "🔍"
        
        with st.expander(f"{type_icon} [{item['type']}] {title} - {item['date']}", expanded=False):
            # 상단 정보
            col_info1, col_info2 = st.columns([2, 1])
            
            with col_info1:
                st.markdown("**📎 업로드된 파일:**")
                for file in item['files']:
                    st.write(f"  • {file}")
            
            with col_info2:
                st.markdown(f"**📅 분석일:** {item['date']}")
                st.markdown(f"**🏷️ 유형:** {item['type']}")
            
            # 분석 결과 미리보기
            if 'data' in item and item['data']:
                st.markdown("---")
                st.markdown("**📊 분석 결과 미리보기:**")
                
                data = item['data']
                
                # 프로젝트 제목
                if 'project_title' in data:
                    st.info(f"**{data['project_title']}**")
                
                preview_cols = st.columns(2)
                
                with preview_cols[0]:
                    # 예산 정보
                    if 'budget' in data:
                        budget = data['budget']
                        if isinstance(budget, dict):
                            amount = budget.get('total_amount', '정보 없음')
                        else:
                            amount = str(budget)
                        st.write(f"💰 **예산:** {amount}")
                    
                    # 프로젝트 개요 (앞부분만)
                    if 'project_overview' in data:
                        overview = data['project_overview']
                        if len(overview) > 100:
                            overview = overview[:100] + "..."
                        st.write(f"📋 **개요:** {overview}")
                
                with preview_cols[1]:
                    # 일정 정보
                    if 'schedule' in data:
                        sch = data['schedule']
                        if isinstance(sch, dict):
                            period = sch.get('total_period', '정보 없음')
                        else:
                            period = str(sch)
                        st.write(f"📅 **기간:** {period}")
                    
                    # 상주 인력
                    if 'personnel' in data:
                        pers = data['personnel']
                        if isinstance(pers, dict):
                            onsite = pers.get('onsite_required', '정보 없음')
                        else:
                            onsite = str(pers)
                        st.write(f"👥 **상주:** {onsite}")
            
            st.markdown("---")
            
            # 버튼 영역
            col_btn1, col_btn2, col_btn3 = st.columns([2, 1, 1])
            
            with col_btn1:
                # PDF 다운로드
                pdf_path = history_manager.get_pdf_path(item)
                if pdf_path and os.path.exists(pdf_path):
                    with open(pdf_path, "rb") as f:
                        pdf_bytes = f.read()
                    
                    st.download_button(
                        label="📥 PDF 다운로드",
                        data=pdf_bytes,
                        file_name=os.path.basename(pdf_path),
                        mime="application/pdf",
                        key=f"download_{item['id']}",
                        use_container_width=True
                    )
                else:
                    st.error("PDF 파일을 찾을 수 없습니다.")
            
            with col_btn3:
                if st.button("🗑️ 삭제", key=f"delete_{item['id']}", use_container_width=True):
                    if history_manager.delete_entry(item['id']):
                        st.success("삭제되었습니다.")
                        st.rerun()
                    else:
                        st.error("삭제 실패")
