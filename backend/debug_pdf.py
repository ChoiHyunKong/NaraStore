import sys
import os
from datetime import datetime

# Add project root to sys.path
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from backend.report.generator.report_writer import FullReportGenerator

def test_pdf_generation():
    print("--- Testing PDF Generation ---")
    
    # Mock Data (New Schema)
    mock_data = {
        "summary": {
            "project_name": "기상청 날씨알리미 앱 고도화 사업",
            "period": "2025-01-01 ~ 2025-12-31",
            "budget": "500,000,000원",
            "expected_effects": ["사용자 만족도 30% 증가", "시스템 안정성 확보"],
            "total_requirements_count": 15
        },
        "requirements": [
            {
                "category": "기능 요구사항",
                "items": ["로그인 기능 개선", "푸시 알림 속도 최적화"]
            },
            {
                "category": "보안 요구사항",
                "items": ["DB 암호화 적용", "관리자 2FA 인증"]
            }
        ],
        "strategy": {
            "win_strategy": ["클라우드 네이티브 전환 제안", "UI/UX 전면 개편"],
            "references": ["OOO청 모바일 앱 구축 (2023)", "XXX공사 알림 시스템 (2024)"]
        },
        "todo_list": ["제안서 초안 작성", "투입 인력 구성"]
    }
    
    output_path = os.path.join(current_dir, "test_output.pdf")
    
    print(f"Generating PDF to: {output_path}")
    success, msg = FullReportGenerator.generate(mock_data, output_path)
    
    if success:
        print(f"[SUCCESS] PDF Generated! ({msg})")
        print("Please check the design manually.")
    else:
        print(f"[ERROR] PDF Generation Failed: {msg}")

if __name__ == "__main__":
    test_pdf_generation()
