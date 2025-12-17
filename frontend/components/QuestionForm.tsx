'use client';

import React, { useState } from 'react';

interface QuestionFormProps {
  onSubmit: (question: string) => Promise<void>;
  isLoading: boolean;
}

export default function QuestionForm({ onSubmit, isLoading }: QuestionFormProps) {
  const [question, setQuestion] = useState('');

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (question.trim()) {
      await onSubmit(question);
      setQuestion('');
    }
  };

  return (
    <form onSubmit={handleSubmit} className="bg-white rounded-lg shadow-md p-6">
      <h2 className="text-2xl font-bold text-gray-800 mb-4">提出您的问题</h2>

      <div className="mb-4">
        <label htmlFor="question" className="block text-sm font-medium text-gray-700 mb-2">
          问题
        </label>
        <textarea
          id="question"
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
          placeholder="输入您想要提问的问题..."
          className="w-full p-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 resize-none"
          rows={4}
          disabled={isLoading}
        />
      </div>

      <button
        type="submit"
        disabled={isLoading || !question.trim()}
        className={`w-full py-3 rounded-lg font-semibold transition ${
          isLoading || !question.trim()
            ? 'bg-gray-400 text-gray-600 cursor-not-allowed'
            : 'bg-blue-500 hover:bg-blue-600 text-white cursor-pointer'
        }`}
      >
        {isLoading ? (
          <span className="flex items-center justify-center gap-2">
            <span className="inline-block animate-spin">⚙️</span>
            处理中...
          </span>
        ) : (
          '获取答案'
        )}
      </button>
    </form>
  );
}
