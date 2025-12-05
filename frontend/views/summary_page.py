"""
제안서 요약 페이지
복수 파일 업로드 및 요약 레포트 생성
"""
import streamlit as st
import os
import tempfile
from datetime import datetime
from backend.analyzer.parser.document_integrator import document_integrator
from backend.analyzer.proposal_analyzer import create_analyzer
from backend.report.generator.report_writer import summary_report_generator
from config.settings import settings


def render():
    """페이지 렌더링"""
    st.header("1. 제안서 요약")
    
    st.info("""
    제안서를 빠르게 파악하기 위한 요약 레포트를 생성합니다.
    - 프로젝트 개요, 목표, 목적
    - 주요 과업 내용
    - 금액 및 마감일
    """)
    
    # 복수 파일 업로드
    st.subheader("📁 제안서 파일 업로드")
    uploaded_files = st.file_uploader(
        "파일 선택 (복수 선택 가능)",
        type=["pdf", "hwp", "pptx"],
        accept_multiple_files=True,
        help="Ctrl 키를 누른 채로 여러 파일을 선택할 수 있습니다."
    )
    
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
        st.caption("⏱️ 예상 소요 시간: 1~2분 (문서 크기에 따라 달라질 수 있습니다)")
        
        col1, col2 = st.columns([3, 1])
        with col1:
            if st.button("📊 요약 분석 시작", type="primary", use_container_width=True):
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
                    progress_bar.progress(0.15)
                    update_time()
                    
                    success, document_text = document_integrator.parse_multiple_files(uploaded_files)
                    
                    if not success:
                        st.error(f"문서 파싱 실패: {document_text}")
                        st.session_state['analysis_in_progress'] = False
                        return
                    
                    # 2. Gemini API 분석
                    status_text.text("🤖 AI 분석 중... (가장 오래 걸리는 단계)")
                    progress_bar.progress(0.3)
                    update_time()
                    
                    analyzer = create_analyzer(settings.GEMINI_API_KEY)
                    success, summary_data = analyzer.summarize(document_text)
                    
                    if not success:
                        st.error(f"분석 실패: {summary_data}")
                        st.session_state['analysis_in_progress'] = False
                        return
                    
                    # 3. PDF 생성
                    status_text.text("📑 PDF 레포트 생성 중...")
                    progress_bar.progress(0.85)
                    update_time()
                    
                    # PDF 저장 디렉토리 확인 및 생성
                    pdf_dir = os.path.join(os.getcwd(), "data", "pdfs")
                    if not os.path.exists(pdf_dir):
                        os.makedirs(pdf_dir)
                    
                    # 영구 PDF 파일 생성
                    output_path = os.path.join(
                        pdf_dir,
                        f"summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
                    )
                    
                    success, message = summary_report_generator.generate(summary_data, output_path)
                    
                    if not success:
                        st.error(f"PDF 생성 실패: {message}")
                        st.session_state['analysis_in_progress'] = False
                        return
                    
                    # 완료 - 결과를 session_state에 저장
                    progress_bar.progress(1.0)
                    total_time = time.time() - start_time
                    status_text.text("✅ 완료!")
                    time_text.caption(f"✅ 총 소요 시간: {total_time:.1f}초")
                    
                    # 결과 저장 (PDF 다운로드 후에도 유지)
                    st.session_state['summary_result'] = summary_data
                    st.session_state['summary_pdf_path'] = output_path
                    st.session_state['analysis_in_progress'] = False
                    st.session_state['analysis_just_completed'] = True
                    
                    # 프로젝트 제목
                    if "project_title" in summary_data:
                        st.markdown(f"## 📋 {summary_data['project_title']}")
                    else:
                        st.markdown("## 📋 제안요청서 분석 결과")
                    
                    # 프로젝트 개요
                    if "project_overview" in summary_data:
                        st.markdown("### 📌 프로젝트 개요")
                        st.write(summary_data["project_overview"])
                    
                    # 배경 및 필요성
                    if "background" in summary_data:
                        st.markdown("### 📍 배경 및 필요성")
                        bg = summary_data["background"]
                        if isinstance(bg, dict):
                            if "current_issues" in bg:
                                st.markdown("**현재 문제점:**")
                                st.write(bg["current_issues"])
                            if "necessity" in bg:
                                st.markdown("**필요성:**")
                                st.write(bg["necessity"])
                        else:
                            st.write(bg)
                    
                    # 목표
                    col_goal1, col_goal2 = st.columns([1, 1])
                    with col_goal1:
                        if "project_goal" in summary_data:
                            st.markdown("### 🎯 프로젝트 목표")
                            goal = summary_data["project_goal"]
                            if isinstance(goal, dict):
                                if "main_goal" in goal:
                                    st.info(f"**핵심 목표:** {goal['main_goal']}")
                                if "sub_goals" in goal:
                                    st.markdown("**세부 목표:**")
                                    for sg in goal["sub_goals"]:
                                        st.write(f"• {sg}")
                            else:
                                st.write(goal)
                    
                    with col_goal2:
                        if "scope" in summary_data:
                            st.markdown("### 📐 사업 범위")
                            scope = summary_data["scope"]
                            if isinstance(scope, dict):
                                if "target_users" in scope:
                                    st.markdown(f"**대상:** {scope['target_users']}")
                                if "coverage" in scope:
                                    st.markdown(f"**범위:** {scope['coverage']}")
                                if "exclusions" in scope and scope["exclusions"] != "정보 없음":
                                    st.markdown(f"**제외 사항:** {scope['exclusions']}")
                    
                    # 주요 과업
                    if "main_tasks" in summary_data:
                        st.markdown("### 📝 주요 과업")
                        tasks = summary_data["main_tasks"]
                        if isinstance(tasks, list):
                            for idx, task in enumerate(tasks, 1):
                                if isinstance(task, dict):
                                    with st.expander(f"**{idx}. {task.get('task_name', f'과업 {idx}')}**", expanded=True):
                                        if "description" in task:
                                            st.write(task["description"])
                                        if "deliverables" in task and task["deliverables"]:
                                            st.markdown("**📦 산출물:**")
                                            for d in task["deliverables"]:
                                                st.write(f"  • {d}")
                                else:
                                    st.write(f"• {task}")
                    
                    # 💰 예산 및 📅 일정 (핵심 정보 - 눈에 띄게)
                    st.markdown("---")
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        if "budget" in summary_data:
                            st.markdown("### 💰 예산 정보")
                            budget = summary_data["budget"]
                            if isinstance(budget, dict):
                                if "total_amount" in budget and budget["total_amount"] != "정보 없음":
                                    st.metric("💵 총 사업비", budget["total_amount"])
                                if "vat_included" in budget and budget["vat_included"] != "미명시":
                                    st.write(f"📌 부가세: **{budget['vat_included']}**")
                                if "budget_type" in budget and budget["budget_type"] != "정보 없음":
                                    st.write(f"📌 예산 유형: {budget['budget_type']}")
                                if "breakdown" in budget and budget["breakdown"] != "정보 없음":
                                    st.write(f"📌 세부 내역: {budget['breakdown']}")
                            else:
                                st.metric("💵 총 사업비", str(budget))
                    
                    with col2:
                        if "schedule" in summary_data:
                            st.markdown("### 📅 사업 일정")
                            sch = summary_data["schedule"]
                            if isinstance(sch, dict):
                                if "total_period" in sch and sch["total_period"] != "정보 없음":
                                    st.metric("⏱️ 총 사업 기간", sch["total_period"])
                                if "proposal_deadline" in sch and sch["proposal_deadline"] != "정보 없음":
                                    st.error(f"🚨 제안서 마감: **{sch['proposal_deadline']}**")
                                if "start_date" in sch and sch["start_date"] != "정보 없음":
                                    st.write(f"📌 착수일: {sch['start_date']}")
                                if "end_date" in sch and sch["end_date"] != "정보 없음":
                                    st.write(f"📌 완료일: {sch['end_date']}")
                                if "presentation_date" in sch and sch["presentation_date"] != "정보 없음":
                                    st.write(f"📌 PT 예정: {sch['presentation_date']}")
                    
                    # 👥 상주 인력 정보 (핵심!)
                    if "personnel" in summary_data:
                        st.markdown("---")
                        st.markdown("### 👥 인력 요구사항")
                        pers = summary_data["personnel"]
                        if isinstance(pers, dict):
                            col_p1, col_p2 = st.columns(2)
                            
                            with col_p1:
                                # 상주 인력 여부 (중요 정보)
                                onsite = pers.get("onsite_required", "정보 없음")
                                if onsite in ["필요", "필수", "있음", "Y"]:
                                    st.error(f"🏢 **상주 인력: 필요**")
                                    if "onsite_count" in pers and pers["onsite_count"] != "정보 없음":
                                        st.write(f"  • 인원: {pers['onsite_count']}")
                                    if "onsite_location" in pers and pers["onsite_location"] != "정보 없음":
                                        st.write(f"  • 장소: {pers['onsite_location']}")
                                elif onsite in ["불필요", "없음", "N"]:
                                    st.success("🏠 **상주 인력: 불필요**")
                                else:
                                    st.info(f"🏢 상주 인력: {onsite}")
                                
                                # PM 필수 여부
                                if "pm_required" in pers and pers["pm_required"] != "정보 없음":
                                    st.write(f"📌 PM 필수: {pers['pm_required']}")
                            
                            with col_p2:
                                if "key_personnel" in pers and pers["key_personnel"]:
                                    st.markdown("**필수 투입 인력:**")
                                    for role in pers["key_personnel"]:
                                        if role != "정보 없음":
                                            st.write(f"  • {role}")
                                
                                if "qualification_requirements" in pers and pers["qualification_requirements"]:
                                    st.markdown("**인력 자격 요건:**")
                                    for qual in pers["qualification_requirements"]:
                                        if qual != "정보 없음":
                                            st.write(f"  • {qual}")
                    
                    # 계약 정보
                    if "contract_info" in summary_data:
                        st.markdown("---")
                        st.markdown("### � 계약 정보")
                        contract = summary_data["contract_info"]
                        if isinstance(contract, dict):
                            cols = st.columns(3)
                            with cols[0]:
                                if "contract_type" in contract and contract["contract_type"] != "정보 없음":
                                    st.write(f"**계약 방식:** {contract['contract_type']}")
                            with cols[1]:
                                if "payment_terms" in contract and contract["payment_terms"] != "정보 없음":
                                    st.write(f"**지급 조건:** {contract['payment_terms']}")
                            with cols[2]:
                                if "warranty_period" in contract and contract["warranty_period"] != "정보 없음":
                                    st.write(f"**하자보수:** {contract['warranty_period']}")
                    
                    # 기술 요구사항
                    if "technical_requirements" in summary_data:
                        st.markdown("### ⚙️ 기술 요구사항")
                        for req in summary_data["technical_requirements"]:
                            st.write(f"• {req}")
                    
                    # 자격 요건
                    if "qualification" in summary_data:
                        st.markdown("### ✅ 참여 자격 요건")
                        qual = summary_data["qualification"]
                        if isinstance(qual, dict):
                            col_q1, col_q2 = st.columns(2)
                            with col_q1:
                                if "mandatory" in qual and qual["mandatory"]:
                                    st.markdown("**필수 요건:**")
                                    for m in qual["mandatory"]:
                                        st.write(f"• {m}")
                            with col_q2:
                                if "preferred" in qual and qual["preferred"]:
                                    st.markdown("**우대 사항:**")
                                    for p in qual["preferred"]:
                                        st.write(f"• {p}")
                    
                    # 평가 기준
                    if "evaluation_criteria" in summary_data and summary_data["evaluation_criteria"]:
                        st.markdown("### 📊 평가 기준")
                        criteria = summary_data["evaluation_criteria"]
                        if isinstance(criteria, list) and criteria:
                            criteria_data = []
                            for c in criteria:
                                if isinstance(c, dict):
                                    criteria_data.append({
                                        "평가 항목": c.get("criteria", ""),
                                        "배점": c.get("weight", "")
                                    })
                            if criteria_data:
                                import pandas as pd
                                st.table(pd.DataFrame(criteria_data))
                    
                    # 기대 효과
                    if "expected_effects" in summary_data and summary_data["expected_effects"]:
                        st.markdown("### 🌟 기대 효과")
                        for effect in summary_data["expected_effects"]:
                            st.success(f"✓ {effect}")
                    
                    # 핵심 고려사항
                    if "key_considerations" in summary_data and summary_data["key_considerations"]:
                        st.markdown("### ⚠️ 입찰 시 핵심 고려사항")
                        for item in summary_data["key_considerations"]:
                            st.warning(f"💡 {item}")
                    
                    # 제출 정보
                    if "submission_info" in summary_data:
                        st.markdown("### 📬 제출 정보")
                        sub = summary_data["submission_info"]
                        if isinstance(sub, dict):
                            cols = st.columns(3)
                            with cols[0]:
                                if "deadline" in sub:
                                    st.markdown(f"**마감:** {sub['deadline']}")
                            with cols[1]:
                                if "method" in sub:
                                    st.markdown(f"**방법:** {sub['method']}")
                            with cols[2]:
                                if "contact" in sub:
                                    st.markdown(f"**문의:** {sub['contact']}")
                    
                    st.markdown("---")
                    
                    # PDF 다운로드
                    with open(output_path, "rb") as f:
                        pdf_bytes = f.read()
                    
                    st.download_button(
                        label="📥 PDF 레포트 다운로드",
                        data=pdf_bytes,
                        file_name=f"제안서_요약_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
                        mime="application/pdf"
                    )
                    
                    # 이력 저장 (JSON)
                    from backend.storage.history_manager import history_manager
                    
                    history_manager.add_entry(
                        entry_type="요약",
                        files=[f.name for f in uploaded_files],
                        data=summary_data,
                        pdf_path=output_path
                    )
                    
                    # 분석 완료 플래그 설정 (페이지 이동 경고용)
                    st.session_state['analysis_in_progress'] = False
                    st.session_state['analysis_just_completed'] = True
                    
                except Exception as e:
                    st.error(f"오류 발생: {str(e)}")
                    st.session_state['analysis_in_progress'] = False
                    st.session_state['analysis_just_completed'] = False
        
        with col2:
            if st.button("🔍 제안서 분석", use_container_width=True):
                st.session_state['current_page'] = "제안서 분석"
                st.session_state['uploaded_files'] = uploaded_files
                st.rerun()
        
        # 저장된 분석 결과 표시 (PDF 다운로드 후에도 유지)
        if 'summary_result' in st.session_state and st.session_state['summary_result']:
            display_summary_result(st.session_state['summary_result'], 
                                   st.session_state.get('summary_pdf_path', ''))
    
    else:
        st.info("제안서 파일을 업로드해주세요.")


def display_summary_result(summary_data: dict, pdf_path: str):
    """요약 결과를 화면에 표시"""
    import os
    
    st.markdown("---")
    st.success("✅ 분석 완료!")
    
    # PDF 다운로드 버튼
    if pdf_path and os.path.exists(pdf_path):
        with open(pdf_path, "rb") as f:
            pdf_bytes = f.read()
        st.download_button(
            label="📥 PDF 다운로드",
            data=pdf_bytes,
            file_name=os.path.basename(pdf_path),
            mime="application/pdf",
            key="summary_pdf_download"
        )
    
    st.markdown("---")
    
    # 프로젝트 제목
    if "project_title" in summary_data:
        st.markdown(f"## 📋 {summary_data['project_title']}")
    else:
        st.markdown("## 📋 제안요청서 분석 결과")
    
    # 프로젝트 개요
    if "project_overview" in summary_data:
        st.markdown("### 📌 프로젝트 개요")
        st.write(summary_data["project_overview"])
    
    # 예산 정보
    if "budget" in summary_data:
        st.markdown("### 💰 예산 정보")
        budget = summary_data["budget"]
        if isinstance(budget, dict):
            col1, col2 = st.columns(2)
            with col1:
                st.metric("총 예산", budget.get("total_amount", "정보 없음"))
            with col2:
                st.write(f"**부가세:** {budget.get('vat_included', '정보 없음')}")
        else:
            st.write(budget)
    
    # 일정 정보
    if "schedule" in summary_data:
        st.markdown("### 📅 사업 일정")
        sch = summary_data["schedule"]
        if isinstance(sch, dict):
            st.write(f"**총 기간:** {sch.get('total_period', '정보 없음')}")
            if sch.get('proposal_deadline'):
                st.error(f"📢 **제안서 마감:** {sch.get('proposal_deadline')}")
        else:
            st.write(sch)
    
    # 인력 요구사항
    if "personnel" in summary_data:
        st.markdown("### 👥 인력 요구사항")
        pers = summary_data["personnel"]
        if isinstance(pers, dict):
            st.write(f"**상주 필요:** {pers.get('onsite_required', '정보 없음')}")
            if pers.get('onsite_count'):
                st.write(f"**상주 인원:** {pers.get('onsite_count')}")
        else:
            st.write(pers)
