package aiagent.dacn.agentforedu.service;

import aiagent.dacn.agentforedu.dto.CourseProgressResponse;
import aiagent.dacn.agentforedu.dto.LessonProgressRequest;
import aiagent.dacn.agentforedu.dto.LessonProgressResponse;
import aiagent.dacn.agentforedu.entity.*;
import aiagent.dacn.agentforedu.repository.*;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.math.BigDecimal;
import java.math.RoundingMode;
import java.time.LocalDateTime;
import java.util.List;
import java.util.stream.Collectors;

@Service
@RequiredArgsConstructor
public class ProgressService {

    private final LessonProgressRepository lessonProgressRepository;
    private final CourseProgressRepository courseProgressRepository;
    private final LessonRepository lessonRepository;
    private final CourseRepository courseRepository;
    private final CourseEnrollmentRepository enrollmentRepository;

    @Transactional
    public LessonProgressResponse updateLessonProgress(LessonProgressRequest request, User user) {
        // Validate enrollment
        if (!enrollmentRepository.existsByUserIdAndCourseId(user.getId(), request.getCourseId())) {
            throw new RuntimeException("Bạn chưa đăng ký khóa học này");
        }

        // Validate lesson belongs to course
        Lesson lesson = lessonRepository.findById(request.getLessonId())
                .orElseThrow(() -> new RuntimeException("Không tìm thấy bài học"));
        
        if (!lesson.getCourse().getId().equals(request.getCourseId())) {
            throw new RuntimeException("Bài học không thuộc khóa học này");
        }

        // Find or create lesson progress
        LessonProgress progress = lessonProgressRepository
                .findByUserIdAndLessonId(user.getId(), request.getLessonId())
                .orElse(new LessonProgress());

        // Update progress
        if (progress.getId() == null) {
            progress.setUserId(user.getId());
            progress.setLessonId(request.getLessonId());
            progress.setCourseId(request.getCourseId());
        }

        if (request.getProgressPercentage() != null) {
            progress.setProgressPercentage(Math.min(100, Math.max(0, request.getProgressPercentage())));
        }

        if (request.getTimeSpent() != null && request.getTimeSpent() > 0) {
            progress.setTimeSpent(progress.getTimeSpent() + request.getTimeSpent());
        }

        if (request.getIsCompleted() != null) {
            progress.setIsCompleted(request.getIsCompleted());
            if (request.getIsCompleted() && progress.getCompletedAt() == null) {
                progress.setCompletedAt(LocalDateTime.now());
                progress.setProgressPercentage(100);
            }
        }

        // Auto-complete if progress reaches 100%
        if (progress.getProgressPercentage() >= 100 && !progress.getIsCompleted()) {
            progress.setIsCompleted(true);
            progress.setCompletedAt(LocalDateTime.now());
        }

        progress.setLastAccessedAt(LocalDateTime.now());
        LessonProgress saved = lessonProgressRepository.save(progress);

        // Update course progress
        updateCourseProgress(user.getId(), request.getCourseId());

        return toLessonProgressResponse(saved);
    }

    @Transactional
    public void updateCourseProgress(Long userId, Long courseId) {
        Course course = courseRepository.findById(courseId)
                .orElseThrow(() -> new RuntimeException("Không tìm thấy khóa học"));

        // Get all lessons in course
        List<Lesson> lessons = lessonRepository.findByCourseIdOrderByOrderIndexAsc(courseId);
        int totalLessons = lessons.size();

        // Get completed lessons count
        Long completedCount = lessonProgressRepository
                .countCompletedLessonsByUserIdAndCourseId(userId, courseId);

        // Get total time spent
        Integer totalTimeSpent = lessonProgressRepository
                .sumTimeSpentByUserIdAndCourseId(userId, courseId);
        if (totalTimeSpent == null) totalTimeSpent = 0;

        // Calculate progress percentage
        BigDecimal progressPercentage = BigDecimal.ZERO;
        if (totalLessons > 0) {
            progressPercentage = BigDecimal.valueOf(completedCount)
                    .multiply(BigDecimal.valueOf(100))
                    .divide(BigDecimal.valueOf(totalLessons), 2, RoundingMode.HALF_UP);
        }

        // Find or create course progress
        CourseProgress courseProgress = courseProgressRepository
                .findByUserIdAndCourseId(userId, courseId)
                .orElse(new CourseProgress());

        if (courseProgress.getId() == null) {
            courseProgress.setUserId(userId);
            courseProgress.setCourseId(courseId);
        }

        courseProgress.setTotalLessons(totalLessons);
        courseProgress.setCompletedLessons(completedCount.intValue());
        courseProgress.setProgressPercentage(progressPercentage);
        courseProgress.setTotalTimeSpent(totalTimeSpent);
        courseProgress.setLastAccessedAt(LocalDateTime.now());

        courseProgressRepository.save(courseProgress);
    }

    @Transactional(readOnly = true)
    public LessonProgressResponse getLessonProgress(Long lessonId, User user) {
        LessonProgress progress = lessonProgressRepository
                .findByUserIdAndLessonId(user.getId(), lessonId)
                .orElse(null);
        
        if (progress == null) {
            // Return default progress
            LessonProgressResponse response = new LessonProgressResponse();
            response.setUserId(user.getId());
            response.setLessonId(lessonId);
            response.setIsCompleted(false);
            response.setProgressPercentage(0);
            response.setTimeSpent(0);
            return response;
        }
        
        return toLessonProgressResponse(progress);
    }

    @Transactional(readOnly = true)
    public CourseProgressResponse getCourseProgress(Long courseId, User user) {
        // Validate enrollment
        if (!enrollmentRepository.existsByUserIdAndCourseId(user.getId(), courseId)) {
            throw new RuntimeException("Bạn chưa đăng ký khóa học này");
        }

        Course course = courseRepository.findById(courseId)
                .orElseThrow(() -> new RuntimeException("Không tìm thấy khóa học"));

        CourseProgress courseProgress = courseProgressRepository
                .findByUserIdAndCourseId(user.getId(), courseId)
                .orElse(createDefaultCourseProgress(user.getId(), courseId));

        // Get all lesson progress
        List<LessonProgress> lessonProgressList = lessonProgressRepository
                .findByUserIdAndCourseId(user.getId(), courseId);

        CourseProgressResponse response = new CourseProgressResponse();
        response.setId(courseProgress.getId());
        response.setUserId(courseProgress.getUserId());
        response.setCourseId(courseProgress.getCourseId());
        response.setCourseTitle(course.getTitle());
        response.setTotalLessons(courseProgress.getTotalLessons());
        response.setCompletedLessons(courseProgress.getCompletedLessons());
        response.setProgressPercentage(courseProgress.getProgressPercentage());
        response.setTotalTimeSpent(courseProgress.getTotalTimeSpent());
        response.setLastAccessedAt(courseProgress.getLastAccessedAt());
        response.setCreatedAt(courseProgress.getCreatedAt());
        response.setUpdatedAt(courseProgress.getUpdatedAt());

        // Convert lesson progress
        List<LessonProgressResponse> lessonResponses = lessonProgressList.stream()
                .map(this::toLessonProgressResponse)
                .collect(Collectors.toList());
        response.setLessonProgressList(lessonResponses);

        return response;
    }

    @Transactional(readOnly = true)
    public List<CourseProgressResponse> getMyAllCourseProgress(User user) {
        List<CourseEnrollment> enrollments = enrollmentRepository.findByUserId(user.getId());
        
        return enrollments.stream()
                .map(enrollment -> getCourseProgress(enrollment.getCourseId(), user))
                .collect(Collectors.toList());
    }

    private CourseProgress createDefaultCourseProgress(Long userId, Long courseId) {
        Course course = courseRepository.findById(courseId).orElse(null);
        int totalLessons = course != null ? lessonRepository.findByCourseIdOrderByOrderIndexAsc(courseId).size() : 0;
        
        CourseProgress progress = new CourseProgress();
        progress.setUserId(userId);
        progress.setCourseId(courseId);
        progress.setTotalLessons(totalLessons);
        progress.setCompletedLessons(0);
        progress.setProgressPercentage(BigDecimal.ZERO);
        progress.setTotalTimeSpent(0);
        return progress;
    }

    private LessonProgressResponse toLessonProgressResponse(LessonProgress progress) {
        LessonProgressResponse response = new LessonProgressResponse();
        response.setId(progress.getId());
        response.setUserId(progress.getUserId());
        response.setLessonId(progress.getLessonId());
        response.setCourseId(progress.getCourseId());
        response.setIsCompleted(progress.getIsCompleted());
        response.setCompletedAt(progress.getCompletedAt());
        response.setTimeSpent(progress.getTimeSpent());
        response.setProgressPercentage(progress.getProgressPercentage());
        response.setLastAccessedAt(progress.getLastAccessedAt());
        response.setCreatedAt(progress.getCreatedAt());
        response.setUpdatedAt(progress.getUpdatedAt());

        // Get lesson title
        if (progress.getLesson() != null) {
            response.setLessonTitle(progress.getLesson().getTitle());
        } else {
            lessonRepository.findById(progress.getLessonId())
                    .ifPresent(lesson -> response.setLessonTitle(lesson.getTitle()));
        }

        return response;
    }
}
