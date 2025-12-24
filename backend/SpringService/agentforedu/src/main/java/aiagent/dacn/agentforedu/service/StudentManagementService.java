package aiagent.dacn.agentforedu.service;

import aiagent.dacn.agentforedu.dto.CourseStudentManagementResponse;
import aiagent.dacn.agentforedu.dto.EnrolledStudentResponse;
import aiagent.dacn.agentforedu.entity.*;
import aiagent.dacn.agentforedu.repository.*;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.math.BigDecimal;
import java.util.ArrayList;
import java.util.List;
import java.util.stream.Collectors;

@Service
@RequiredArgsConstructor
public class StudentManagementService {

    private final CourseRepository courseRepository;
    private final CourseEnrollmentRepository enrollmentRepository;
    private final CourseProgressRepository courseProgressRepository;
    private final LessonRepository lessonRepository;
    private final UserRepository userRepository;

    @Transactional(readOnly = true)
    public CourseStudentManagementResponse getCourseStudents(Long courseId, User teacher) {
        Course course = courseRepository.findById(courseId)
                .orElseThrow(() -> new RuntimeException("Không tìm thấy khóa học"));

        // Check if teacher is the course creator
        if (!course.getCreatedBy().equals(teacher.getId())) {
            throw new RuntimeException("Bạn không có quyền quản lý khóa học này");
        }

        // Get all enrollments
        List<CourseEnrollment> enrollments = enrollmentRepository.findByCourseId(courseId);

        // Get enrolled students with progress
        List<EnrolledStudentResponse> students = enrollments.stream()
                .map(enrollment -> {
                    User student = userRepository.findById(enrollment.getUserId()).orElse(null);
                    if (student == null) return null;

                    EnrolledStudentResponse response = new EnrolledStudentResponse();
                    response.setUserId(student.getId());
                    response.setUsername(student.getUsername());
                    response.setFullName(student.getFullName());
                    response.setEmail(student.getEmail());
                    response.setAvatarUrl(student.getAvatarUrl());
                    response.setEnrolledAt(enrollment.getEnrolledAt());

                    // Get progress info
                    CourseProgress progress = courseProgressRepository
                            .findByUserIdAndCourseId(student.getId(), courseId)
                            .orElse(null);

                    if (progress != null) {
                        response.setProgressPercentage(progress.getProgressPercentage());
                        response.setCompletedLessons(progress.getCompletedLessons());
                        response.setTotalLessons(progress.getTotalLessons());
                        response.setTotalTimeSpent(progress.getTotalTimeSpent());
                        response.setLastAccessedAt(progress.getLastAccessedAt());
                    } else {
                        response.setProgressPercentage(BigDecimal.ZERO);
                        response.setCompletedLessons(0);
                        int totalLessons = lessonRepository.findByCourseIdOrderByOrderIndexAsc(courseId).size();
                        response.setTotalLessons(totalLessons);
                        response.setTotalTimeSpent(0);
                    }

                    return response;
                })
                .filter(response -> response != null)
                .collect(Collectors.toList());

        // Build response
        CourseStudentManagementResponse response = new CourseStudentManagementResponse();
        response.setCourseId(course.getId());
        response.setCourseTitle(course.getTitle());
        response.setCourseDescription(course.getDescription());
        response.setCreatedBy(course.getCreatedBy());
        
        if (course.getCreator() != null) {
            response.setCreatorName(course.getCreator().getUsername());
        }
        
        response.setTotalStudents(students.size());
        int totalLessons = lessonRepository.findByCourseIdOrderByOrderIndexAsc(courseId).size();
        response.setTotalLessons(totalLessons);
        response.setStudents(students);

        return response;
    }

    @Transactional
    public void removeStudentFromCourse(Long courseId, Long studentId, User teacher) {
        Course course = courseRepository.findById(courseId)
                .orElseThrow(() -> new RuntimeException("Không tìm thấy khóa học"));

        // Check if teacher is the course creator
        if (!course.getCreatedBy().equals(teacher.getId())) {
            throw new RuntimeException("Bạn không có quyền quản lý khóa học này");
        }

        // Find enrollment
        CourseEnrollment enrollment = enrollmentRepository
                .findByUserIdAndCourseId(studentId, courseId)
                .orElseThrow(() -> new RuntimeException("Sinh viên không có trong khóa học này"));

        // Delete enrollment
        enrollmentRepository.delete(enrollment);
    }

    @Transactional(readOnly = true)
    public List<CourseStudentManagementResponse> getMyCoursesAsTeacher(User teacher) {
        // Get all courses created by teacher
        List<Course> courses = courseRepository.findAll().stream()
                .filter(course -> course.getCreatedBy().equals(teacher.getId()))
                .collect(Collectors.toList());

        return courses.stream()
                .map(course -> getCourseStudents(course.getId(), teacher))
                .collect(Collectors.toList());
    }
}
