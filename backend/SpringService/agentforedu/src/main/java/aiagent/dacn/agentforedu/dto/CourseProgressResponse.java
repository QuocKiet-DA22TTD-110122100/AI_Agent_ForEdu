package aiagent.dacn.agentforedu.dto;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.math.BigDecimal;
import java.time.LocalDateTime;
import java.util.List;

@Data
@NoArgsConstructor
@AllArgsConstructor
public class CourseProgressResponse {
    private Long id;
    private Long userId;
    private Long courseId;
    private String courseTitle;
    private Integer totalLessons;
    private Integer completedLessons;
    private BigDecimal progressPercentage;
    private Integer totalTimeSpent; // seconds
    private LocalDateTime lastAccessedAt;
    private LocalDateTime createdAt;
    private LocalDateTime updatedAt;
    private List<LessonProgressResponse> lessonProgressList;
}
