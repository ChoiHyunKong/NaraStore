"""
NaraStore FastAPI Backend
React 프론트엔드와 통신하는 API 서버
"""
from fastapi import FastAPI, UploadFile, File, HTTPException, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Optional, Dict, Any
import os
import sys
import tempfile
import base64
from datetime import datetime
import time

# 프로젝트 루트 경로 추가 (backend 폴더의 상위 폴더)
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# backend 폴더 자체도 import 가능하도록
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

from backend.utils.logger import logger
from backend.analyzer.proposal_analyzer import create_analyzer

app = FastAPI(
    title="NaraStore API",
    description="제안서 분석 API 서버",
    version="2.0.0"
)

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class AnalysisRequest(BaseModel):
    """분석 요청 모델"""
    filename: str
    file_content: str  # base64 encoded
    api_key: str


class AnalysisResponse(BaseModel):
    """분석 응답 모델 (구조화된 데이터 포맷)"""
    success: bool
    data: Optional[Dict[str, Any]] = None  # 구조화된 JSON 데이터
    error: Optional[str] = None


@app.get("/")
async def root():
    """헬스체크"""
    return {"status": "ok", "message": "NaraStore API Server"}


@app.get("/api/health")
async def health_check():
    """API 헬스체크"""
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}


@app.post("/api/analyze", response_model=AnalysisResponse)
async def analyze_rfp(request: AnalysisRequest):
    """
    제안서 분석 API (구조화된 분석)
    - file_content: base64로 인코딩된 파일 내용
    """
    if not request.api_key:
        raise HTTPException(status_code=400, detail="API Key가 필요합니다")
    
    tmp_path = None
    try:
        start_time = time.time()
        logger.info(f"분석 요청 수신: {request.filename}")
        
        # 1. Base64 디코딩하여 임시 파일 생성
        try:
            file_bytes = base64.b64decode(request.file_content)
            _, ext = os.path.splitext(request.filename)
            
            with tempfile.NamedTemporaryFile(delete=False, suffix=ext) as tmp_file:
                tmp_file.write(file_bytes)
                tmp_path = tmp_file.name
        except Exception as e:
             return AnalysisResponse(success=False, error=f"파일 디코딩 실패: {str(e)}")
        
        # 2. 문서 파싱
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
        
        file_wrapper = FileWrapper(tmp_path, request.filename)
        success, document_text = document_integrator.parse_multiple_files([file_wrapper])
        
        if not success:
            return AnalysisResponse(success=False, error=f"문서 파싱 실패: {document_text}")
        
        # 3. 구조화 분석 실행
        analyzer = create_analyzer(request.api_key)
        
        # 통합된 analyze_structured 메서드 호출
        success, result = analyzer.analyze_structured(document_text)
        
        if not success:
            return AnalysisResponse(success=False, error=str(result))
        
        # Pydantic 모델 -> Dict 변환
        if hasattr(result, "model_dump"):
            result_dict = result.model_dump()
        else:
            result_dict = result

        execution_time = time.time() - start_time
        logger.info(f"분석 완료 (소요시간: {execution_time:.2f}초)")
        
        return AnalysisResponse(
            success=True,
            data=result_dict
        )
            
    except Exception as e:
        logger.error(f"API 처리 중 오류: {str(e)}")
        import traceback
        logger.error(traceback.format_exc())
        return AnalysisResponse(success=False, error=str(e))
        
    finally:
        if tmp_path and os.path.exists(tmp_path):
            os.unlink(tmp_path)


@app.post("/api/analyze/upload")
async def analyze_rfp_upload(
    file: UploadFile = File(...),
    api_key: str = Form(...)
):
    """파일 직접 업로드 방식"""
    if not api_key:
        raise HTTPException(status_code=400, detail="API Key가 필요합니다")
    
    try:
        file_content = await file.read()
        file_content_b64 = base64.b64encode(file_content).decode('utf-8')
        
        request = AnalysisRequest(
            filename=file.filename,
            file_content=file_content_b64,
            api_key=api_key
        )
        
        return await analyze_rfp(request)
        
    except Exception as e:
        return AnalysisResponse(success=False, error=f"업로드 오류: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
