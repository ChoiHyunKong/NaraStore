import { useState, useEffect } from 'react';
import { checkApiHealth } from '../services/apiService';

export const useAuth = () => {
  const [apiKey, setApiKey] = useState('');
  const [apiKeyError, setApiKeyError] = useState('');
  const [showSettings, setShowSettings] = useState(false);
  const [isApiHealthy, setIsApiHealthy] = useState(false);

  // API 서버 상태 체크
  useEffect(() => {
    const checkHealth = async () => {
      const healthy = await checkApiHealth();
      setIsApiHealthy(healthy);
    };
    checkHealth();
    const interval = setInterval(checkHealth, 30000); // 30초마다 체크
    return () => clearInterval(interval);
  }, []);

  // API Key가 없으면 설정 모달 자동 표시
  useEffect(() => {
    if (!apiKey) {
      setShowSettings(true);
    }
  }, []);

  const handleSaveApiKey = () => {
    // [MOCK MODE] Key가 없어도 저장 허용
    setApiKeyError('');
    setShowSettings(false);
  };

  return {
    apiKey,
    setApiKey,
    apiKeyError,
    setApiKeyError,
    showSettings,
    setShowSettings,
    isApiHealthy,
    handleSaveApiKey
  };
};
