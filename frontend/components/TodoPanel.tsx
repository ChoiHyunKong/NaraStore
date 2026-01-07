import React, { useState, useEffect } from 'react';
import { Trash2, Plus, CheckCircle, Circle, ListTodo } from 'lucide-react';
import { TodoItem } from '../types';
import { dbService } from '../services/dbService';

interface TodoPanelProps {
  currentRFPId?: string;
}

const TodoPanel: React.FC<TodoPanelProps> = ({ currentRFPId }) => {
  const [todos, setTodos] = useState<TodoItem[]>([]);
  const [newTodo, setNewTodo] = useState('');
  const [isAdding, setIsAdding] = useState(false);

  // Subscribe to Firestore Todos when RFP changes
  useEffect(() => {
    if (!currentRFPId) {
      setTodos([]);
      return;
    }

    const unsubscribe = dbService.subscribeTodos(currentRFPId, (updatedTodos) => {
      setTodos(updatedTodos);
    });

    return () => unsubscribe();
  }, [currentRFPId]);

  const toggleTodo = (id: string, currentStatus: boolean) => {
    dbService.toggleTodo(id, currentStatus);
  };

  const deleteTodo = (id: string) => {
    if (confirm('정말로 삭제하시겠습니까?')) {
      dbService.deleteTodo(id);
    }
  };

  const handleAddTodo = async () => {
    if (newTodo.trim() && currentRFPId) {
      await dbService.addTodo(currentRFPId, newTodo);
      setNewTodo('');
      setIsAdding(false);
    }
  };

  if (!currentRFPId) {
    return (
      <div className="glass-card rounded-3xl shadow-xl shadow-indigo-100/50 flex flex-col h-full overflow-hidden transition-all border-indigo-50/50 items-center justify-center p-8 bg-gray-50/50">
        <ListTodo className="w-12 h-12 text-gray-300 mb-3" />
        <p className="text-gray-400 font-medium text-center">
          제안서를 선택하면<br />할 일 목록이 표시됩니다
        </p>
      </div>
    );
  }

  return (
    <div className="glass-card rounded-3xl shadow-xl shadow-indigo-100/50 flex flex-col h-full overflow-hidden transition-all border-indigo-50/50">
      <div className="p-6">
        <div className="flex items-center gap-2 mb-6">
          <ListTodo className="w-5 h-5 text-indigo-600" />
          <h2 className="text-xl font-bold text-gray-800">To do list</h2>
        </div>

        {/* Scrollable Container */}
        <div className="space-y-3 max-h-[calc(100vh-350px)] overflow-y-auto custom-scrollbar pr-2 pb-4">
          {todos.map((todo) => (
            <div key={todo.id} className="relative group">
              <div
                className={`flex items-center border-2 rounded-2xl overflow-hidden transition-all duration-300 ${todo.completed ? 'bg-gray-50 border-gray-100 grayscale' : 'bg-white border-indigo-50 hover:border-indigo-200 hover:shadow-md'}`}
              >
                <div
                  className={`px-4 py-4 cursor-pointer flex items-center justify-center transition-colors ${todo.completed ? 'text-gray-300' : 'text-indigo-500 hover:text-indigo-600'}`}
                  onClick={() => toggleTodo(todo.id, todo.completed)}
                >
                  {todo.completed ? <CheckCircle className="w-5 h-5" /> : <Circle className="w-5 h-5" />}
                </div>

                <div
                  className={`flex-1 py-4 text-sm font-semibold transition-all cursor-pointer ${todo.completed ? 'text-gray-400 line-through decoration-2' : 'text-gray-700'}`}
                  onClick={() => toggleTodo(todo.id, todo.completed)}
                >
                  {todo.text}
                </div>

                <button
                  onClick={() => deleteTodo(todo.id)}
                  className="px-4 py-4 text-gray-300 hover:text-red-500 transition-colors opacity-0 group-hover:opacity-100"
                >
                  <Trash2 className="w-4 h-4" />
                </button>
              </div>
            </div>
          ))}

          {isAdding && (
            <div className="border-2 border-indigo-500 rounded-2xl p-3 flex space-x-2 bg-white shadow-lg animate-in fade-in zoom-in-95 duration-200">
              <input
                autoFocus
                type="text"
                className="flex-1 bg-transparent text-sm p-1 outline-none font-semibold text-gray-700"
                placeholder="할 일을 입력하세요..."
                value={newTodo}
                onChange={(e) => setNewTodo(e.target.value)}
                onKeyDown={(e) => e.key === 'Enter' && handleAddTodo()}
              />
              <button onClick={handleAddTodo} className="bg-indigo-600 text-white p-2 rounded-xl shadow-md hover:bg-indigo-700 transition-colors">
                <Plus className="w-4 h-4" />
              </button>
            </div>
          )}
        </div>

        {!isAdding && (
          <button
            onClick={() => setIsAdding(true)}
            className="w-full mt-2 py-4 border-2 border-dashed border-indigo-100 rounded-2xl text-indigo-400 text-sm font-bold hover:border-indigo-300 hover:bg-indigo-50 hover:text-indigo-600 transition-all flex items-center justify-center gap-2 group"
          >
            <Plus className="w-4 h-4 group-hover:rotate-90 transition-transform" />
            할 일 추가하기
          </button>
        )}
      </div>

      <div className="mt-auto p-6 bg-indigo-50/50 border-t border-indigo-100/50">
        <div className="flex justify-between items-center">
          <span className="text-xs font-bold text-indigo-400 uppercase tracking-wider">Progress</span>
          <span className="text-xs font-bold text-indigo-600">
            {todos.length > 0 ? Math.round((todos.filter(t => t.completed).length / todos.length) * 100) : 0}%
          </span>
        </div>
        <div className="mt-2 w-full bg-indigo-100 rounded-full h-1.5 overflow-hidden">
          <div
            className="bg-indigo-600 h-full transition-all duration-1000 ease-out"
            style={{ width: `${todos.length > 0 ? (todos.filter(t => t.completed).length / todos.length) * 100 : 0}%` }}
          ></div>
        </div>
      </div>
    </div>
  );
};

export default TodoPanel;
