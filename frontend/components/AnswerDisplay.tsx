'use client';

import React, { useState } from 'react';
import { askQuestion } from '@/lib/api';

interface AnswerDisplayProps {
  question: string;
  answer: string;
  llmProvider: string;
  onRate: (rating: number, feedback: string) => void;
}

export default function AnswerDisplay({
  question,
  answer,
  llmProvider,
  onRate,
}: AnswerDisplayProps) {
  const [rating, setRating] = useState(0);
  const [feedback, setFeedback] = useState('');
  const [showFeedbackForm, setShowFeedbackForm] = useState(false);

  const handleSubmitRating = () => {
    if (rating > 0) {
      onRate(rating, feedback);
      setShowFeedbackForm(false);
      setRating(0);
      setFeedback('');
    }
  };

  return (
    <div className="bg-white rounded-lg shadow-md p-6 mt-6">
      <div className="mb-4">
        <h3 className="text-lg font-semibold text-gray-700 mb-2">问题：</h3>
        <p className="text-gray-600 bg-gray-50 p-3 rounded">{question}</p>
      </div>

      <div className="mb-4">
        <h3 className="text-lg font-semibold text-gray-700 mb-2">答案：</h3>
        <div className="text-gray-600 bg-blue-50 p-4 rounded border-l-4 border-blue-400 whitespace-pre-wrap">
          {answer}
        </div>
        <p className="text-sm text-gray-500 mt-2">
          生成模型：{llmProvider}
        </p>
      </div>

      <div className="border-t pt-4">
        <button
          onClick={() => setShowFeedbackForm(!showFeedbackForm)}
          className="bg-blue-500 hover:bg-blue-600 text-white px-4 py-2 rounded transition"
        >
          {showFeedbackForm ? '取消评分' : '评分此答案'}
        </button>

        {showFeedbackForm && (
          <div className="mt-4 p-4 bg-gray-50 rounded">
            <div className="mb-3">
              <label className="block text-sm font-medium text-gray-700 mb-2">
                评分（1-5颗星）：
              </label>
              <div className="flex gap-2">
                {[1, 2, 3, 4, 5].map((star) => (
                  <button
                    key={star}
                    onClick={() => setRating(star)}
                    className={`text-2xl ${
                      star <= rating ? 'text-yellow-400' : 'text-gray-300'
                    } hover:text-yellow-400 transition`}
                  >
                    ★
                  </button>
                ))}
              </div>
            </div>

            <div className="mb-3">
              <label className="block text-sm font-medium text-gray-700 mb-2">
                反馈意见（可选）：
              </label>
              <textarea
                value={feedback}
                onChange={(e) => setFeedback(e.target.value)}
                className="w-full p-2 border rounded text-gray-700"
                rows={3}
                placeholder="请输入您的反馈..."
              />
            </div>

            <button
              onClick={handleSubmitRating}
              disabled={rating === 0}
              className="bg-green-500 hover:bg-green-600 disabled:bg-gray-400 text-white px-4 py-2 rounded transition"
            >
              提交评分
            </button>
          </div>
        )}
      </div>
    </div>
  );
}
