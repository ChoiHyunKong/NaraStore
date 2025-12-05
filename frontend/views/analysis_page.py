"""
제안서 분석 페이지
상세 요구사항 분석 및 수주 전략 수립
"""
import streamlit as st
import os
import tempfile
from datetime import datetime
from backend.analyzer.parser.document_integrator import document_integrator
from backend.analyzer.proposal_analyzer import create_analyzer
from backend.report.generator.report_writer import analysis_report_generator
from config.settings import settings


def _render_requirements_list(requirements: list):
    """요구사항 리스트를 읽기 쉬운 형태로 렌더링"""
    if not isinstance(requirements, list):
        st.write(str(requirements))
        return
    
    for req in requirements:
        if isinstance(req, dict):
            # 요구사항 ID와 카테고리로 expander 생성
            req_id = req.get("id", "")
            category = req.get("category", "기타")
            title = f"{req_id}: {category}" if req_id else category
            
            with st.expander(f"📋 {title}", expanded=False):
                # 설명
                if "description" in req:
                    st.markdown(f"**설명:** {req['description']}")
                
                # 우선순위
                if "priority" in req:
                    priority = req["priority"]
                    if priority == "필수":
                        st.markdown(f"**우선순위:** 🔴 {priority}")
                    else:
                        st.markdown(f"**우선순위:** {priority}")
                
                # 출처
                if "source" in req:
                    st.markdown(f"**출처:** {req['source']}")
                
                # 평가 배점
                if "evaluation_weight" in req:
                    st.markdown(f"**평가 배점:** {req['evaluation_weight']}점")
                
                # 측정 기준 (비기능 요구사항)
                if "metric" in req:
                    st.markdown(f"**측정 기준:** {req['metric']}")
                
                # 구현 노트
                if "implementation_notes" in req:
                    st.info(f"💡 **구현 참고:** {req['implementation_notes']}")
        else:
            st.write(f"- {req}")

def render():
    """페이지 렌더링"""
    st.header("2. 제안서 분석")
    
    st.info("""
    수주 확률을 높이기 위한 상세 분석 및 전략을 수립합니다.
    - 각 상세 요구사항 분석
    - 요구사항 이행 전략 도출
    - 유사 프로젝트 레퍼런스
    """)
    
    # 복수 파일 업로드
    st.subheader("📁 제안서 파일 업로드")
    uploaded_files = st.file_uploader(
        "파일 선택 (복수 선택 가능)",
        type=["pdf", "hwp", "pptx"],
        accept_multiple_files=True,
        help="Ctrl 키를 누른 채로 여러 파일을 선택할 수 있습니다.",
        key="analysis_uploader"
    )
    
    # 제안서 요약에서 넘어온 파일 사용
    if 'uploaded_files' in st.session_state and not uploaded_files:
        uploaded_files = st.session_state['uploaded_files']
        st.info(f"제안서 요약에서 업로드한 {len(uploaded_files)}개 파일을 사용합니다.")
    
    if uploaded_files:
        st.success(f"총 {len(uploaded_files)}개 파일 업로드됨")
        
        # 파일 목록 표시
        with st.expander("업로드된 파일 목록", expanded=True):
            for idx, file in enumerate(uploaded_files, 1):
                file_size = len(file.getvalue()) / 1024 / 1024
                st.write(f"{idx}. **{file.name}** ({file_size:.2f} MB)")
        
        # 분석 시작 버튼
        st.markdown("---")
        
        # 예상 소요 시간 안내
        st.caption("⏱️ 예상 소요 시간: 2~3분 (상세 분석, 전략 수립, 레퍼런스 생성 포함)")
        
        if st.button("📊 상세 분석 시작", type="primary", use_container_width=True):
            st.session_state['analysis_in_progress'] = True
            
            # 시간 측정 시작
            import time
            start_time = time.time()
            
            # 진행 상태 표시
            progress_bar = st.progress(0)
            status_text = st.empty()
            time_text = st.empty()
            
            def update_time():
                elapsed = time.time() - start_time
                time_text.caption(f"⏱️ 경과 시간: {elapsed:.1f}초")
            
            try:
                # 1. 문서 파싱
                status_text.text("📄 문서 파싱 중...")
                progress_bar.progress(0.1)
                update_time()
                
                success, document_text = document_integrator.parse_multiple_files(uploaded_files)
                
                if not success:
                    st.error(f"문서 파싱 실패: {document_text}")
                    st.session_state['analysis_in_progress'] = False
                    return
                
                analyzer = create_analyzer(settings.GEMINI_API_KEY)
                
                # 2. 상세 요구사항 분석
                status_text.text("🔍 상세 요구사항 분석 중... (1/3)")
                progress_bar.progress(0.25)
                update_time()
                
                success, analysis_result = analyzer.analyze_detailed(document_text)
                
                if not success:
                    st.error(f"분석 실패: {analysis_result}")
                    st.session_state['analysis_in_progress'] = False
                    return
                
                # 3. 수주 전략 도출
                status_text.text("🎯 수주 전략 수립 중... (2/3)")
                progress_bar.progress(0.5)
                update_time()
                
                success, strategy_result = analyzer.generate_strategy(analysis_result)
                
                if not success:
                    st.warning(f"전략 생성 실패: {strategy_result}")
                    strategy_result = "전략 생성에 실패했습니다."
                
                # 4. 유사 프로젝트 레퍼런스
                status_text.text("📚 유사 프로젝트 레퍼런스 검색 중... (3/3)")
                progress_bar.progress(0.75)
                update_time()
                
                success, reference_result = analyzer.generate_references(analysis_result)
                
                if not success:
                    st.warning(f"레퍼런스 생성 실패: {reference_result}")
                    reference_result = {"references": []}
                
                # 5. PDF 생성
                status_text.text("📑 PDF 레포트 생성 중...")
                progress_bar.progress(0.9)
                update_time()
                
                # PDF 저장 디렉토리 확인 및 생성
                pdf_dir = os.path.join(os.getcwd(), "data", "pdfs")
                if not os.path.exists(pdf_dir):
                    os.makedirs(pdf_dir)
                
                # 영구 PDF 파일 생성
                output_path = os.path.join(
                    pdf_dir,
                    f"analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
                )
                
                success, message = analysis_report_generator.generate(
                    analysis_result, 
                    strategy_result if isinstance(strategy_result, str) else str(strategy_result),
                    output_path
                )
                
                if not success:
                    st.error(f"PDF 생성 실패: {message}")
                    st.session_state['analysis_in_progress'] = False
                    return
                
                # 완료
                progress_bar.progress(1.0)
                total_time = time.time() - start_time
                status_text.text("✅ 완료!")
                time_text.caption(f"✅ 총 소요 시간: {total_time:.1f}초")
                st.success(f"분석 완료! (소요 시간: {total_time:.1f}초)")
                
                # 분석 결과 탭
                tab1, tab2, tab3 = st.tabs(["요구사항 분석", "수주 전략", "유사 프로젝트"])
                
                with tab1:
                    st.markdown("### 📋 상세 요구사항 분석")
                    if isinstance(analysis_result, dict):
                        # 클라이언트 니즈 표시
                        if "client_needs" in analysis_result:
                            st.markdown("**📌 클라이언트 니즈**")
                            needs = analysis_result["client_needs"]
                            if isinstance(needs, list):
                                for need in needs:
                                    st.write(f"- {need}")
                            else:
                                st.write(needs)
                        
                        # 상세 요구사항 표시
                        if "requirements" in analysis_result:
                            reqs = analysis_result["requirements"]
                            
                            # functional/non_functional 구조 처리
                            if isinstance(reqs, dict):
                                # 기능 요구사항
                                if "functional" in reqs:
                                    st.markdown("---")
                                    st.markdown("**🔧 기능 요구사항**")
                                    _render_requirements_list(reqs["functional"])
                                
                                # 비기능 요구사항
                                if "non_functional" in reqs:
                                    st.markdown("---")
                                    st.markdown("**⚙️ 비기능 요구사항**")
                                    _render_requirements_list(reqs["non_functional"])
                            
                            # 리스트 형태 처리
                            elif isinstance(reqs, list):
                                st.markdown("---")
                                _render_requirements_list(reqs)
                            else:
                                st.write(str(reqs))
                        
                        # functional이 최상위에 있는 경우
                        if "functional" in analysis_result:
                            st.markdown("---")
                            st.markdown("**🔧 기능 요구사항**")
                            _render_requirements_list(analysis_result["functional"])
                        
                        if "non_functional" in analysis_result:
                            st.markdown("---")
                            st.markdown("**⚙️ 비기능 요구사항**")
                            _render_requirements_list(analysis_result["non_functional"])
                        
                        # raw_text가 있는 경우도 처리
                        if "raw_text" in analysis_result:
                            st.markdown(analysis_result["raw_text"])
                    else:
                        st.write(str(analysis_result))
                
                with tab2:
                    st.markdown("### 🎯 수주 전략")
                    st.markdown(strategy_result)
                
                with tab3:
                    st.markdown("### 📚 유사 프로젝트 레퍼런스")
                    if isinstance(reference_result, dict) and "references" in reference_result:
                        for ref in reference_result["references"]:
                            with st.expander(f"📌 {ref.get('title', '제목 없음')}", expanded=True):
                                st.write(ref.get('description', ''))
                                if "key_features" in ref:
                                    st.markdown("**주요 기능**")
                                    for feature in ref["key_features"]:
                                        st.write(f"- {feature}")
                    else:
                        st.write("추천된 레퍼런스가 없습니다.")
                
                # PDF 다운로드 버튼
                st.markdown("---")
                
                with open(output_path, "rb") as f:
                    pdf_bytes = f.read()
                
                st.download_button(
                    label="📥 분석 PDF 레포트 다운로드",
                    data=pdf_bytes,
                    file_name=f"제안서_분석_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
                    mime="application/pdf",
                    use_container_width=True,
                    key="analysis_pdf_download"
                )
                
                # 이력 저장 (JSON)
                from backend.storage.history_manager import history_manager
                
                history_manager.add_entry(
                    entry_type="분석",
                    files=[f.name for f in uploaded_files],
                    data=analysis_result,
                    pdf_path=output_path,
                    strategy=strategy_result,
                    references=reference_result
                )
                
                # 결과를 session_state에 저장 (PDF 다운로드 후에도 유지)
                st.session_state['analysis_result'] = analysis_result
                st.session_state['strategy_result'] = strategy_result
                st.session_state['reference_result'] = reference_result
                st.session_state['analysis_pdf_path'] = output_path
                
                # 분석 완료 플래그 설정 (페이지 이동 경고용)
                st.session_state['analysis_in_progress'] = False
                st.session_state['analysis_just_completed'] = True
                
            except Exception as e:
                st.error(f"오류 발생: {str(e)}")
                st.session_state['analysis_in_progress'] = False
                st.session_state['analysis_just_completed'] = False
        
        # 저장된 분석 결과 표시 (PDF 다운로드 후에도 유지)
        if 'analysis_result' in st.session_state and st.session_state['analysis_result']:
            display_analysis_result(
                st.session_state['analysis_result'],
                st.session_state.get('strategy_result'),
                st.session_state.get('reference_result'),
                st.session_state.get('analysis_pdf_path', '')
            )
    
    else:
        st.info("제안서 파일을 업로드해주세요.")


def display_analysis_result(analysis_result: dict, strategy_result, reference_result, pdf_path: str):
    """분석 결과를 화면에 표시"""
    import os
    
    st.markdown("---")
    st.success("✅ 분석 완료!")
    
    # PDF 다운로드 버튼
    if pdf_path and os.path.exists(pdf_path):
        with open(pdf_path, "rb") as f:
            pdf_bytes = f.read()
        st.download_button(
            label="📥 분석 PDF 다운로드",
            data=pdf_bytes,
            file_name=os.path.basename(pdf_path),
            mime="application/pdf",
            key="analysis_pdf_display"
        )
    
    # 분석 결과 탭
    tab1, tab2, tab3 = st.tabs(["요구사항 분석", "수주 전략", "유사 프로젝트"])
    
    with tab1:
        st.markdown("### 📋 상세 요구사항 분석")
        if isinstance(analysis_result, dict):
            for key, value in analysis_result.items():
                st.markdown(f"**{key.replace('_', ' ').title()}**")
                if isinstance(value, list):
                    for item in value:
                        st.write(f"- {item}")
                elif isinstance(value, dict):
                    for k, v in value.items():
                        st.write(f"  • {k}: {v}")
                else:
                    st.write(value)
                st.markdown("---")
    
    with tab2:
        st.markdown("### 🎯 수주 전략")
        if strategy_result:
            if isinstance(strategy_result, dict):
                for key, value in strategy_result.items():
                    st.markdown(f"**{key.replace('_', ' ').title()}**")
                    st.write(value)
            else:
                st.write(strategy_result)
        else:
            st.info("수주 전략 정보가 없습니다.")
    
    with tab3:
        st.markdown("### 📚 유사 프로젝트")
        if reference_result:
            if isinstance(reference_result, list):
                for ref in reference_result:
                    if isinstance(ref, dict):
                        st.write(f"**{ref.get('name', '프로젝트')}**")
                        st.write(ref.get('description', ''))
                    else:
                        st.write(f"- {ref}")
            else:
                st.write(reference_result)
        else:
            st.info("유사 프로젝트 정보가 없습니다.")
