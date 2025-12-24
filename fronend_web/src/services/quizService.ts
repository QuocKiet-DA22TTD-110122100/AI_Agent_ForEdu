import { springApi } from './api';
import { ENDPOINTS } from '../config/api';
import type { Quiz, QuizQuestion, QuizResult } from '../types';

export interface CreateQuizRequest {
  lessonId: number;
  title: string;
  description?: string;
  difficulty?: 'EASY' | 'MEDIUM' | 'HARD';
  questions: {
    question: string;
    optionA: string;
    optionB: string;
    optionC: string;
    optionD: string;
    correctAnswer: 'A' | 'B' | 'C' | 'D';
    explanation?: string;
  }[];
}

export interface QuizListItem {
  id: number;
  lessonId: number;
  title: string;
  description?: string;
  difficulty: string;
  totalQuestions: number;
  creatorName: string;
  createdAt: string;
  isPublic: boolean;
  isCompleted?: boolean;
  lastScore?: number;
}

export const quizService = {
  generateQuiz: async (lessonId: number, difficulty: string, numQuestions: number): Promise<Quiz> => {
    const response = await springApi.post(ENDPOINTS.QUIZ.GENERATE, {
      lessonId,
      difficulty: difficulty.toUpperCase(),
      numQuestions,
    });
    return response.data;
  },

  createQuiz: async (data: CreateQuizRequest): Promise<Quiz> => {
    const response = await springApi.post(ENDPOINTS.QUIZ.CREATE, data);
    return response.data;
  },

  getQuizzesByLesson: async (lessonId: number): Promise<QuizListItem[]> => {
    const response = await springApi.get(ENDPOINTS.QUIZ.BY_LESSON(lessonId));
    return response.data;
  },

  getQuiz: async (id: number): Promise<{ quiz: Quiz; questions: QuizQuestion[] }> => {
    const response = await springApi.get(ENDPOINTS.QUIZ.DETAIL(id));
    return response.data;
  },

  submitQuiz: async (id: number, answers: Record<number, string>): Promise<QuizResult> => {
    const response = await springApi.post(ENDPOINTS.QUIZ.SUBMIT(id), { answers });
    return response.data;
  },
};
