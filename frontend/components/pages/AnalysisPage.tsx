import React from 'react';
import RFPList from '../RFPList';
import AnalysisPanel from '../AnalysisPanel';
import TodoPanel from '../TodoPanel';
import { RFP, TodoItem } from '../../types';
import Footer from '../footer/Footer';

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
        <div className="flex flex-col min-h-[calc(100vh-80px)]">
            <div className="p-8 max-w-[1600px] mx-auto w-full flex flex-col overflow-hidden" style={{ height: 'calc(100vh - 80px)' }}>
                <div className="grid grid-cols-12 gap-8 flex-1 min-h-0">
                    {/* Left Panel: RFP List */}
                    <div className="col-span-12 lg:col-span-4 xl:col-span-3 h-full overflow-hidden flex flex-col min-h-0">
                        <RFPList
                            rfps={rfps}
                            onSelectRFP={setSelectedRFP}
                            selectedRFPId={selectedRFP?.id}
                            onDelete={handleDeleteRFP}
                        />
                    </div>

                    {/* Center Panel: RFP Analysis */}
                    <div className="col-span-12 lg:col-span-5 xl:col-span-6 h-full overflow-hidden flex flex-col min-h-0">
                        <AnalysisPanel
                            currentRFP={selectedRFP}
                            onUpload={handleFileUpload}
                            isAnalyzing={isAnalyzing}
                            apiKeySet={apiKeySet}
                        />
                    </div>

                    {/* Right Panel: To-do List */}
                    <div className="col-span-12 lg:col-span-3 h-full overflow-hidden flex flex-col min-h-0">
                        <TodoPanel
                            currentRFPId={selectedRFP?.id}
                        />
                    </div>
                </div>
            </div>
            <div className="mt-24">
                <Footer />
            </div>
        </div>
    );
};

export default AnalysisPage;
