package aiagent.dacn.agentforedu.dto;

import aiagent.dacn.agentforedu.entity.QuizDifficulty;
import lombok.Data;

import java.time.LocalDateTime;

@Data
public class QuizListResponse {
    private Long id;
    private Long lessonId;
    private String title;
    private String description;
    private QuizDifficulty difficulty;
    private Integer totalQuestions;
    private String creatorName;
    private LocalDateTime createdAt;
    private Boolean isPublic; // Quiz công khai hay riêng tư
    private Boolean isCompleted; // Sinh viên đã làm chưa
    private Double lastScore; // Điểm lần làm gần nhất
}
