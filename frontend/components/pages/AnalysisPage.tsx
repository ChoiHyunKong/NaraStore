import React from 'react';
import RFPList from '../RFPList';
import AnalysisPanel from '../AnalysisPanel';
import TodoPanel from '../TodoPanel';
import { RFP, TodoItem } from '../../types';

interface AnalysisPageProps {
    rfps: RFP[];
    selectedRFP: RFP | null;
    setSelectedRFP: (rfp: RFP | null) => void;
    todos: TodoItem[];
    isAnalyzing: boolean;
    handleFileUpload: (event: React.ChangeEvent<HTMLInputElement>) => void;
    handleDeleteRFP: (id: string) => void;
    apiKeySet: boolean;
}

const AnalysisPage: React.FC<AnalysisPageProps> = ({
    rfps,
    selectedRFP,
    setSelectedRFP,
    todos,
    isAnalyzing,
    handleFileUpload,
    handleDeleteRFP,
    apiKeySet
}) => {
    return (
        <div className="p-8 max-w-[1600px] mx-auto flex-1 w-full">
            <div className="grid grid-cols-12 gap-8 h-[calc(100vh-140px)] min-h-[700px]">
                {/* Left Panel: RFP List */}
                <div className="col-span-12 lg:col-span-4 xl:col-span-3 h-full overflow-hidden">
                    <RFPList
                        rfps={rfps}
                        onSelectRFP={setSelectedRFP}
                        selectedRFPId={selectedRFP?.id}
                        onDelete={handleDeleteRFP}
                    />
                </div>

                {/* Center Panel: RFP Analysis */}
                <div className="col-span-12 lg:col-span-5 xl:col-span-6 h-full overflow-hidden">
                    <AnalysisPanel
                        currentRFP={selectedRFP}
                        onUpload={handleFileUpload}
                        isAnalyzing={isAnalyzing}
                        apiKeySet={apiKeySet}
                    />
                </div>

                {/* Right Panel: To-do List */}
                <div className="col-span-12 lg:col-span-3 h-full overflow-hidden">
                    <TodoPanel
                        currentRFPId={selectedRFP?.id}
                    />
                </div>
            </div>
        </div>
    );
};

export default AnalysisPage;
