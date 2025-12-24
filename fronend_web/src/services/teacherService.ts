import { springApi } from './api';
import { ENDPOINTS } from '../config/api';
import type { CourseStudentManagement } from '../types';

export const teacherService = {
  // Get students in course
  getCourseStudents: async (courseId: number): Promise<CourseStudentManagement> => {
    const response = await springApi.get(ENDPOINTS.TEACHER.COURSE_STUDENTS(courseId));
    return response.data;
  },

  // Remove student from course
  removeStudent: async (courseId: number, studentId: number): Promise<void> => {
    await springApi.delete(ENDPOINTS.TEACHER.REMOVE_STUDENT(courseId, studentId));
  },

  // Get all my courses as teacher with student list
  getMyCoursesAsTeacher: async (): Promise<CourseStudentManagement[]> => {
    const response = await springApi.get(ENDPOINTS.TEACHER.MY_COURSES);
    return response.data;
  },
};
