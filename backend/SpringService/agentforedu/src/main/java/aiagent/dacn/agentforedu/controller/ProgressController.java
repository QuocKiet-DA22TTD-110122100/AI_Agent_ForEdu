package aiagent.dacn.agentforedu.controller;

import aiagent.dacn.agentforedu.dto.CourseProgressResponse;
import aiagent.dacn.agentforedu.dto.LessonProgressRequest;
import aiagent.dacn.agentforedu.dto.LessonProgressResponse;
import aiagent.dacn.agentforedu.entity.User;
import aiagent.dacn.agentforedu.service.ProgressService;
import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.security.SecurityRequirement;
import io.swagger.v3.oas.annotations.tags.Tag;
import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;
import org.springframework.http.ResponseEntity;
import org.springframework.security.core.annotation.AuthenticationPrincipal;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/api/progress")
@RequiredArgsConstructor
@Tag(name = "Progress", description = "API quản lý tiến độ học tập")
@SecurityRequirement(name = "bearerAuth")
public class ProgressController {

    private final ProgressService progressService;

    @PostMapping("/lesson")
    @Operation(summary = "Cập nhật tiến độ học bài học")
    public ResponseEntity<LessonProgressResponse> updateLessonProgress(
            @Valid @RequestBody LessonProgressRequest request,
            @AuthenticationPrincipal User user) {
        return ResponseEntity.ok(progressService.updateLessonProgress(request, user));
    }

    @GetMapping("/lesson/{lessonId}")
    @Operation(summary = "Xem tiến độ học một bài học")
    public ResponseEntity<LessonProgressResponse> getLessonProgress(
            @PathVariable Long lessonId,
            @AuthenticationPrincipal User user) {
        return ResponseEntity.ok(progressService.getLessonProgress(lessonId, user));
    }

    @GetMapping("/course/{courseId}")
    @Operation(summary = "Xem tiến độ học một khóa học")
    public ResponseEntity<CourseProgressResponse> getCourseProgress(
            @PathVariable Long courseId,
            @AuthenticationPrincipal User user) {
        return ResponseEntity.ok(progressService.getCourseProgress(courseId, user));
    }

    @GetMapping("/my-courses")
    @Operation(summary = "Xem tiến độ học tất cả khóa học của tôi")
    public ResponseEntity<List<CourseProgressResponse>> getMyAllCourseProgress(
            @AuthenticationPrincipal User user) {
        return ResponseEntity.ok(progressService.getMyAllCourseProgress(user));
    }
}
