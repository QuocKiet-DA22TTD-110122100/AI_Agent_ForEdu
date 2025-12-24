package aiagent.dacn.agentforedu.controller;

import aiagent.dacn.agentforedu.dto.CourseStudentManagementResponse;
import aiagent.dacn.agentforedu.entity.User;
import aiagent.dacn.agentforedu.service.StudentManagementService;
import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.security.SecurityRequirement;
import io.swagger.v3.oas.annotations.tags.Tag;
import lombok.RequiredArgsConstructor;
import org.springframework.http.ResponseEntity;
import org.springframework.security.core.annotation.AuthenticationPrincipal;
import org.springframework.web.bind.annotation.*;

import java.util.List;
import java.util.Map;

@RestController
@RequestMapping("/api/teacher")
@RequiredArgsConstructor
@Tag(name = "Teacher Management", description = "API quản lý sinh viên dành cho giáo viên")
@SecurityRequirement(name = "bearerAuth")
public class TeacherController {

    private final StudentManagementService studentManagementService;

    @GetMapping("/courses/{courseId}/students")
    @Operation(summary = "Xem danh sách sinh viên trong khóa học (Giáo viên)")
    public ResponseEntity<CourseStudentManagementResponse> getCourseStudents(
            @PathVariable Long courseId,
            @AuthenticationPrincipal User teacher) {
        return ResponseEntity.ok(studentManagementService.getCourseStudents(courseId, teacher));
    }

    @DeleteMapping("/courses/{courseId}/students/{studentId}")
    @Operation(summary = "Xóa sinh viên khỏi khóa học (Giáo viên)")
    public ResponseEntity<Map<String, String>> removeStudentFromCourse(
            @PathVariable Long courseId,
            @PathVariable Long studentId,
            @AuthenticationPrincipal User teacher) {
        studentManagementService.removeStudentFromCourse(courseId, studentId, teacher);
        return ResponseEntity.ok(Map.of("message", "Đã xóa sinh viên khỏi khóa học"));
    }

    @GetMapping("/my-courses")
    @Operation(summary = "Xem tất cả khóa học của tôi với danh sách sinh viên (Giáo viên)")
    public ResponseEntity<List<CourseStudentManagementResponse>> getMyCoursesAsTeacher(
            @AuthenticationPrincipal User teacher) {
        return ResponseEntity.ok(studentManagementService.getMyCoursesAsTeacher(teacher));
    }
}
