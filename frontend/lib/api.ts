import axios from 'axios';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const askQuestion = async (question: string) => {
  try {
    const response = await apiClient.post('/ask', { question });
    return response.data;
  } catch (error) {
    throw error;
  }
};

export const getQuestions = async (skip = 0, limit = 20) => {
  try {
    const response = await apiClient.get('/questions', {
      params: { skip, limit },
    });
    return response.data;
  } catch (error) {
    throw error;
  }
};

export const getQuestion = async (id: number) => {
  try {
    const response = await apiClient.get(`/questions/${id}`);
    return response.data;
  } catch (error) {
    throw error;
  }
};

export const rateAnswer = async (id: number, rating: number, feedback?: string) => {
  try {
    const response = await apiClient.post(`/questions/${id}/rate`, {
      question_id: id,
      rating,
      feedback: feedback || null,
    });
    return response.data;
  } catch (error) {
    throw error;
  }
};

export const deleteQuestion = async (id: number) => {
  try {
    const response = await apiClient.delete(`/questions/${id}`);
    return response.data;
  } catch (error) {
    throw error;
  }
};
