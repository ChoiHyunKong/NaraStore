import os
import sys
import asyncio
from pathlib import Path

# Add project root to path
current_dir = Path(__file__).resolve().parent
project_root = current_dir
sys.path.append(str(project_root))

from backend.analyzer.proposal_analyzer import create_analyzer
from backend.analyzer.parser.document_integrator import document_integrator

class FileWrapper:
    def __init__(self, path, name):
        self.name = name
        self._path = path
    
    def read(self):
        with open(self._path, 'rb') as f:
            return f.read()

    def getvalue(self):
        return self.read()

def verify_submission():
    print("--- Start Verification: Proposal Analysis ---")
    
    # 1. 문서 경로
    rfp_path = r"C:\Users\chyun\OneDrive\Desktop\AI\02. NaraStore\제안서\제안요청서(기상청+모바일+비스+날씨알리미+앱+개선).pdf"
    
    if not os.path.exists(rfp_path):
        print(f"[ERROR] 파일을 찾을 수 없습니다: {rfp_path}")
        return

    print(f"Target File: {rfp_path}")

    # 2. 문서 파싱
    print("Parsing Document...")
    file_wrapper = FileWrapper(rfp_path, os.path.basename(rfp_path))
    success, document_text = document_integrator.parse_multiple_files([file_wrapper])

    if not success:
        print(f"[ERROR] Parsing Failed: {document_text}")
        return

    print(f"Parsing Success (Length: {len(document_text)})")

    # 3. 분석 수행 (Real API)
    print("Calling Gemini API (Real Mode)...")
    analyzer = create_analyzer()
    success, result = analyzer.analyze_structured(document_text)

    if not success:
        print(f"[ERROR] Analysis Failed: {result}")
        return

    # 4. 결과 검증
    # result는 Pydantic 모델이거나 Dict일 수 있음
    if hasattr(result, "model_dump"):
        data = result.model_dump()
    else:
        data = result

    print("\n--- Analysis Result ---")
    
    # Summary
    if "summary" in data:
        print("[Pass] Summary found")
        print(f"Project Name: {data['summary'].get('project_name')}")
    else:
        print("[Fail] Summary missing")

    # Requirements
    if "requirements" in data and len(data['requirements']) > 0:
        print(f"[Pass] Requirements found ({len(data['requirements'])} categories)")
    else:
        print("[Fail] Requirements missing")

    # Strategy
    if "strategy" in data:
        print("[Pass] Strategy found")
    else:
        print("[Fail] Strategy missing")

    print("\n--- Test Completed ---")

if __name__ == "__main__":
    verify_submission()
