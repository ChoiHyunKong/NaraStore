import React, { useState, useEffect } from 'react';
import { RFP, TodoItem } from '../types';
import { dbService } from '../services/dbService';
import { analyzeRFP } from '../services/apiService';

export const useRFP = (apiKey: string) => {
    const [rfps, setRfps] = useState<RFP[]>([]);
    const [selectedRFP, setSelectedRFP] = useState<RFP | null>(null);
    const [todos, setTodos] = useState<TodoItem[]>([]);
    const [isAnalyzing, setIsAnalyzing] = useState(false);
    const [analysisError, setAnalysisError] = useState('');

    // 1. Subscribe to RFPs
    useEffect(() => {
        const unsubscribe = dbService.subscribeRFPs((updatedRFPs) => {
            setRfps(updatedRFPs);

            // SelectedRFP update logic
            if (selectedRFP) {
                const updatedSelected = updatedRFPs.find(r => r.id === selectedRFP.id);
                if (updatedSelected) {
                    setSelectedRFP(updatedSelected);
                }
            }
        });
        return () => unsubscribe();
    }, [selectedRFP]);

    // 2. Subscribe to ALL Todos (Optimized for Dashboard)
    useEffect(() => {
        // [Optimization] N개의 Listener 대신 1개의 Global Listener 사용
        // 기존: rfps 변경마다 N번 재연결 (Lag 원인) -> 변경: 1번만 연결 후 지속 수신
        const unsubscribe = dbService.subscribeAllTodos((allTodos) => {
            setTodos(allTodos);
        });
        return () => unsubscribe();
    }, []);

    // 3. File Upload Logic
    const handleFileUpload = async (file: File) => {
        const effectiveApiKey = apiKey;
        setIsAnalyzing(true);
        setAnalysisError('');

        try {
            // Create RFP (Pending)
            const docRef = await dbService.addRFP({
                title: file.name,
                analysisDate: new Date().toISOString().split('T')[0],
                status: 'pending'
            });
            const newRFPId = docRef.id;

            // Optimistic UI
            const tempRFP: RFP = {
                id: newRFPId,
                title: file.name,
                analysisDate: new Date().toISOString().split('T')[0],
                status: 'pending'
            };
            setSelectedRFP(tempRFP);

            // Call Backend
            const result = await analyzeRFP(file, effectiveApiKey);

            if (result.success && result.data) {
                // Success: Update with structured data
                await dbService.updateRFP(newRFPId, {
                    structuredAnalysis: result.data,
                    status: 'completed',
                    summary: `[프로젝트] ${result.data.summary.project_name}\n[예산] ${result.data.summary.budget}`,
                    analysis: "분석 완료 (상세 리포트 확인 가능)"
                });

                // Generate Todos
                const aiTodos = result.data.todo_list || [];
                const todosToInsert = aiTodos.length > 0 ? aiTodos : [
                    '제안요청서(RFP) 정독 및 핵심 요구사항 파악',
                    '제안팀 구성 및 역할 분담',
                    '제안 목차 및 스토리보드 작성',
                    '최종 제안서 리뷰 및 제출'
                ];

                for (const todoText of todosToInsert) {
                    await dbService.addTodo(newRFPId, todoText);
                }

            } else {
                // Error
                await dbService.updateRFP(newRFPId, {
                    analysis: `[오류] ${result.error}`,
                    status: 'error'
                });
                setAnalysisError(result.error || '분석 중 오류가 발생했습니다.');
            }

        } catch (error) {
            console.error("Error in upload/analysis:", error);
            setAnalysisError('처리 중 오류가 발생했습니다.');
        } finally {
            setIsAnalyzing(false);
        }
    };

    // 4. Delete Logic
    const handleDeleteRFP = async (id: string, e: React.MouseEvent) => {
        e.stopPropagation();
        if (window.confirm('정말 이 제안서를 삭제하시겠습니까?\n삭제 시 분석 리포트와 To-do List가 모두 영구적으로 삭제됩니다.')) {
            try {
                await dbService.deleteRFP(id);
                if (selectedRFP?.id === id) {
                    setSelectedRFP(null);
                }
            } catch (error) {
                console.error('Failed to delete RFP:', error);
                alert('삭제 중 오류가 발생했습니다.');
            }
        }
    };

    return {
        rfps,
        selectedRFP,
        setSelectedRFP,
        todos,
        isAnalyzing,
        analysisError,
        handleFileUpload,
        handleDeleteRFP
    };
};
