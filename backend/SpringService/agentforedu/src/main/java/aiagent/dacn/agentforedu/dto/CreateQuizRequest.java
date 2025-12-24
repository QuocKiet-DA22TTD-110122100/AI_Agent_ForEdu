package aiagent.dacn.agentforedu.dto;

import aiagent.dacn.agentforedu.entity.QuizDifficulty;
import jakarta.validation.constraints.NotNull;
import lombok.Data;

import java.util.List;

@Data
public class CreateQuizRequest {
    
    @NotNull(message = "Lesson ID không được để trống")
    private Long lessonId;
    
    private String title;
    
    private String description;
    
    private QuizDifficulty difficulty;
    
    @NotNull(message = "Danh sách câu hỏi không được để trống")
    private List<QuestionRequest> questions;
    
    @Data
    public static class QuestionRequest {
        @NotNull(message = "Câu hỏi không được để trống")
        private String question;
        
        @NotNull(message = "Đáp án A không được để trống")
        private String optionA;
        
        @NotNull(message = "Đáp án B không được để trống")
        private String optionB;
        
        @NotNull(message = "Đáp án C không được để trống")
        private String optionC;
        
        @NotNull(message = "Đáp án D không được để trống")
        private String optionD;
        
        @NotNull(message = "Đáp án đúng không được để trống")
        private String correctAnswer; // 'A', 'B', 'C', 'D'
        
        private String explanation; // Giải thích đáp án
    }
}
