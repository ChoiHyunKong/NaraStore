/**
 * NaraStore API Service
 * FastAPI 백엔드와 통신하는 서비스
 */

const API_BASE_URL = `http://${window.location.hostname}:8000`;

import { AnalysisResultData } from '../types';

export interface ApiAnalysisResponse {
  success: boolean;
  data?: AnalysisResultData;
  error?: string;
}

/**
 * 제안서 분석 API 호출
 * @param file 업로드할 파일
 * @param apiKey Gemini API Key
 */
export async function analyzeRFP(file: File, apiKey: string): Promise<ApiAnalysisResponse> {
  try {
    // 파일을 base64로 인코딩
    const fileContent = await fileToBase64(file);

    const response = await fetch(`${API_BASE_URL}/api/analyze`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        filename: file.name,
        file_content: fileContent,
        api_key: apiKey,
      }),
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const result: ApiAnalysisResponse = await response.json();
    console.log("Analysis API Raw Response:", result); // Debugging Log
    return result;
  } catch (error) {
    console.error('Error analyzing RFP:', error);
    return {
      success: false,
      error: error instanceof Error ? error.message : '분석 중 오류가 발생했습니다.',
    };
  }
}

/**
 * 파일을 base64 문자열로 변환
 */
function fileToBase64(file: File): Promise<string> {
  return new Promise((resolve, reject) => {
    const reader = new FileReader();
    reader.readAsDataURL(file);
    reader.onload = () => {
      const result = reader.result as string;
      // data:application/pdf;base64,... 형식에서 base64 부분만 추출
      const base64 = result.split(',')[1];
      resolve(base64);
    };
    reader.onerror = (error) => reject(error);
  });
}

/**
 * API 서버 헬스체크
 */
export async function checkApiHealth(): Promise<boolean> {
  try {
    const response = await fetch(`${API_BASE_URL}/api/health`);
    return response.ok;
  } catch {
    return false;
  }
}
