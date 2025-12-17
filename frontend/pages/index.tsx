'use client';

import React, { useState, useEffect } from 'react';
import QuestionForm from '@/components/QuestionForm';
import AnswerDisplay from '@/components/AnswerDisplay';
import HistoryList from '@/components/HistoryList';
import { askQuestion, getQuestions, rateAnswer, deleteQuestion } from '@/lib/api';

interface Question {
  id: number;
  question_text: string;
  answer_text: string;
  llm_provider: string;
  rating: number | null;
  feedback: string | null;
  created_at: string;
}

interface CurrentAnswer {
  id: number;
  question: string;
  answer: string;
  llmProvider: string;
}

export default function Home() {
  const [currentAnswer, setCurrentAnswer] = useState<CurrentAnswer | null>(null);
  const [history, setHistory] = useState<Question[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [isDeleting, setIsDeleting] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [skip, setSkip] = useState(0);

  // 加载历史记录
  const loadHistory = async (skipValue = 0) => {
    try {
      setError(null);
      const data = await getQuestions(skipValue, 10);
      setHistory(data);
      setSkip(skipValue);
    } catch (err) {
      setError('加载历史记录失败');
      console.error(err);
    }
  };

  // 初始化加载历史记录
  useEffect(() => {
    loadHistory();
  }, []);

  // 处理提交问题
  const handleAskQuestion = async (question: string) => {
    setIsLoading(true);
    setError(null);
    try {
      const response = await askQuestion(question);
      setCurrentAnswer({
        id: response.id,
        question: response.question_text,
        answer: response.answer_text,
        llmProvider: response.llm_provider,
      });
      // 重新加载历史记录
      await loadHistory(0);
    } catch (err) {
      setError('获取答案失败，请检查后端服务是否运行');
      console.error(err);
    } finally {
      setIsLoading(false);
    }
  };

  // 处理评分
  const handleRateAnswer = async (rating: number, feedback: string) => {
    if (!currentAnswer) return;
    try {
      setError(null);
      await rateAnswer(currentAnswer.id, rating, feedback);
      alert('评分已保存');
      // 重新加载历史记录以显示最新评分
      await loadHistory(0);
    } catch (err) {
      setError('保存评分失败');
      console.error(err);
    }
  };

  // 处理选择历史记录
  const handleSelectQuestion = (question: Question) => {
    setCurrentAnswer({
      id: question.id,
      question: question.question_text,
      answer: question.answer_text,
      llmProvider: question.llm_provider,
    });
    window.scrollTo({ top: 0, behavior: 'smooth' });
  };

  // 处理删除历史记录
  const handleDeleteQuestion = async (id: number) => {
    if (!window.confirm('确认删除此问题记录吗？')) return;
    setIsDeleting(true);
    try {
      setError(null);
      await deleteQuestion(id);
      await loadHistory(skip);
      if (currentAnswer?.id === id) {
        setCurrentAnswer(null);
      }
    } catch (err) {
      setError('删除失败');
      console.error(err);
    } finally {
      setIsDeleting(false);
    }
  };

  return (
    <main className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 p-4">
      <div className="max-w-4xl mx-auto">
        {/* 头部 */}
        <div className="text-center mb-8 pt-8">
          <h1 className="text-4xl font-bold text-gray-800 mb-2">AI 智能问答平台</h1>
          <p className="text-gray-600">基于大语言模型的智能问答助手</p>
        </div>

        {/* 错误提示 */}
        {error && (
          <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-6">
            {error}
          </div>
        )}

        {/* 问题表单 */}
        <QuestionForm onSubmit={handleAskQuestion} isLoading={isLoading} />

        {/* 答案显示 */}
        {currentAnswer && (
          <AnswerDisplay
            question={currentAnswer.question}
            answer={currentAnswer.answer}
            llmProvider={currentAnswer.llmProvider}
            onRate={handleRateAnswer}
          />
        )}

        {/* 历史记录 */}
        <HistoryList
          questions={history}
          onSelectQuestion={handleSelectQuestion}
          onDeleteQuestion={handleDeleteQuestion}
          isDeleting={isDeleting}
        />

        {/* 分页 */}
        {history.length > 0 && (
          <div className="flex justify-center gap-3 mt-6 pb-8">
            <button
              onClick={() => loadHistory(Math.max(0, skip - 10))}
              disabled={skip === 0}
              className="px-4 py-2 bg-gray-300 disabled:bg-gray-200 text-gray-800 rounded hover:bg-gray-400 transition"
            >
              上一页
            </button>
            <button
              onClick={() => loadHistory(skip + 10)}
              disabled={history.length < 10}
              className="px-4 py-2 bg-gray-300 disabled:bg-gray-200 text-gray-800 rounded hover:bg-gray-400 transition"
            >
              下一页
            </button>
          </div>
        )}
      </div>
    </main>
  );
}
 