import { springApi } from './api';
import { ENDPOINTS } from '../config/api';
import type { LessonProgress, CourseProgress } from '../types';

export const progressService = {
  // Update lesson progress
  updateLessonProgress: async (data: {
    lessonId: number;
    courseId: number;
    progressPercentage?: number;
    timeSpent?: number;
    isCompleted?: boolean;
  }): Promise<LessonProgress> => {
    const response = await springApi.post(ENDPOINTS.PROGRESS.UPDATE_LESSON, data);
    return response.data;
  },

  // Get lesson progress
  getLessonProgress: async (lessonId: number): Promise<LessonProgress> => {
    const response = await springApi.get(ENDPOINTS.PROGRESS.GET_LESSON(lessonId));
    return response.data;
  },

  // Get course progress
  getCourseProgress: async (courseId: number): Promise<CourseProgress> => {
    const response = await springApi.get(ENDPOINTS.PROGRESS.GET_COURSE(courseId));
    return response.data;
  },

  // Get all my course progress
  getMyCourseProgress: async (): Promise<CourseProgress[]> => {
    const response = await springApi.get(ENDPOINTS.PROGRESS.MY_COURSES);
    return response.data;
  },
};
