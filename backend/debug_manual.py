import sys
import os
import asyncio
import json

# Add project root to sys.path
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# Set settings to DEBUG mode for file logging
from config.settings import settings
settings.DEBUG_MODE = True
from backend.utils.logger import logger

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

def debug_analysis(pdf_path, api_key):
    print(f"--- [DEBUG] Analyzing File: {pdf_path} ---")
    
    if not os.path.exists(pdf_path):
        print("File not found!")
        return

    # 1. Parse Document
    print("[1] Extracting Text...")
    file_wrapper = FileWrapper(pdf_path, os.path.basename(pdf_path))
    success, document_text = document_integrator.parse_multiple_files([file_wrapper])
    
    if not success:
        print(f"[ERROR] Text Extraction Failed: {document_text}")
        return
    
    print(f"[SUCCESS] Text Extracted ({len(document_text)} chars)")
    print(f"Preview: {document_text[:200]}...")
    
    # 2. Analyze
    print("\n[2] Running Gemini Analysis...")
    analyzer = create_analyzer(api_key)
    
    # We bypass the cache for debugging
    analyzer.use_cache = False 
    
    success, result = analyzer.analyze_structured(document_text)
    
    if success:
        print("\n[SUCCESS] Analysis Completed!")
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        print(f"\n[ERROR] Analysis Failed: {result}")
        print("Check logs for raw response.")

if __name__ == "__main__":
    from config.settings import settings
    
    if len(sys.argv) < 2:
        print("Usage: python debug_manual.py <pdf_path> [api_key]")
        print("Using environment variables for API Key if not provided.")
        pdf_path = input("Enter PDF Path: ").strip('"')
        api_key = settings.GEMINI_API_KEY
    else:
        pdf_path = sys.argv[1]
        if len(sys.argv) > 2:
            api_key = sys.argv[2]
        else:
            api_key = settings.GEMINI_API_KEY
            
    if not api_key:
        print("[ERROR] API Key not found in arguments or .env")
        sys.exit(1)
        
    debug_analysis(pdf_path, api_key)
