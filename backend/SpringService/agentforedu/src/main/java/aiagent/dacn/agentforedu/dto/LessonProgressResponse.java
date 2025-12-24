package aiagent.dacn.agentforedu.dto;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.time.LocalDateTime;

@Data
@NoArgsConstructor
@AllArgsConstructor
public class LessonProgressResponse {
    private Long id;
    private Long userId;
    private Long lessonId;
    private Long courseId;
    private String lessonTitle;
    private Boolean isCompleted;
    private LocalDateTime completedAt;
    private Integer timeSpent; // seconds
    private Integer progressPercentage;
    private LocalDateTime lastAccessedAt;
    private LocalDateTime createdAt;
    private LocalDateTime updatedAt;
}
