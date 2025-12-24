package aiagent.dacn.agentforedu.dto;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@NoArgsConstructor
@AllArgsConstructor
public class LessonProgressRequest {
    private Long lessonId;
    private Long courseId;
    private Integer progressPercentage; // 0-100
    private Integer timeSpent; // seconds
    private Boolean isCompleted;
}
