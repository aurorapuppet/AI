'use client';

import React from 'react';

interface Question {
  id: number;
  question_text: string;
  answer_text: string;
  llm_provider: string;
  rating: number | null;
  created_at: string;
}

interface HistoryListProps {
  questions: Question[];
  onSelectQuestion: (question: Question) => void;
  onDeleteQuestion: (id: number) => Promise<void>;
  isDeleting: boolean;
}

export default function HistoryList({
  questions,
  onSelectQuestion,
  onDeleteQuestion,
  isDeleting,
}: HistoryListProps) {
  return (
    <div className="bg-white rounded-lg shadow-md p-6 mt-6">
      <h3 className="text-xl font-bold text-gray-800 mb-4">问题历史记录</h3>

      {questions.length === 0 ? (
        <p className="text-gray-500 text-center py-8">暂无历史记录</p>
      ) : (
        <div className="space-y-3">
          {questions.map((item) => (
            <div
              key={item.id}
              className="p-4 border border-gray-200 rounded-lg hover:shadow-md transition cursor-pointer"
            >
              <div className="flex justify-between items-start mb-2">
                <div
                  onClick={() => onSelectQuestion(item)}
                  className="flex-1 pr-4"
                >
                  <p className="font-semibold text-gray-800 line-clamp-2">
                    {item.question_text}
                  </p>
                  <p className="text-sm text-gray-500 mt-1">
                    {new Date(item.created_at).toLocaleString('zh-CN')}
                  </p>
                </div>

                <button
                  onClick={() => onDeleteQuestion(item.id)}
                  disabled={isDeleting}
                  className="text-red-500 hover:text-red-700 text-sm font-medium px-3 py-1 hover:bg-red-50 rounded transition"
                >
                  删除
                </button>
              </div>

              <div className="flex items-center gap-3 text-sm">
                <span className="text-gray-600">
                  模型：<span className="font-medium">{item.llm_provider}</span>
                </span>
                {item.rating && (
                  <span className="text-yellow-500">
                    {'★'.repeat(item.rating)}{'☆'.repeat(5 - item.rating)}
                  </span>
                )}
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
