
import sys
import os
from unittest.mock import MagicMock, patch

# Add project root to path
sys.path.insert(0, os.getcwd())

from backend.analyzer.parser.document_integrator import document_integrator

# Mock a file upload object
class MockFile:
    def __init__(self, name):
        self.name = name
    def getvalue(self):
        return b"dummy content"

# 1. Simulate a Scanned PDF (Text extraction returns empty string)
print("--- TEST CASE 1: Scanned PDF (Empty Text) ---")
with patch('backend.analyzer.parser.pdf_parser.pdf_parser.extract_text') as mock_extract:
    # Simulate pypdf returning success but empty text (typical for scanned pdfs)
    mock_extract.return_value = (True, "")
    
    # Run integrator
    success, text = document_integrator.parse_multiple_files([MockFile("scanned_doc.pdf")])
    
    with open("test_result.txt", "w", encoding="utf-8") as f:
        f.write(f"Success: {success}\n")
        f.write(f"Result Text: '{text}'\n")
        
        if not success and "문서에서 유효한 텍스트를 추출할 수 없습니다" in text:
             f.write(">> RESULT: CORRECT FAILURE (Fix Verified)\n")
        elif "MOCK DOCUMENT TEXT" in text:
             f.write(">> RESULT: Mock Fallback STILL ACTIVE (Fix Failed)\n")
        else:
             f.write(f">> RESULT: Unexpected behavior: {text[:100]}...\n")

# 2. Simulate a Normal PDF
print("\n--- TEST CASE 2: Normal PDF (Text Found) ---")
with patch('backend.analyzer.parser.pdf_parser.pdf_parser.extract_text') as mock_extract:
    # Simulate pypdf returning text
    mock_extract.return_value = (True, "This is a valid proposal text content that is long enough to pass the check.")
    
    success, text = document_integrator.parse_multiple_files([MockFile("normal_doc.pdf")])
    
    print(f"Success: {success}")
    print(f"Result Text: '{text}'")
