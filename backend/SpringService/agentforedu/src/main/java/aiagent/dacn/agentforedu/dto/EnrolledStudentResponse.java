package aiagent.dacn.agentforedu.dto;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.math.BigDecimal;
import java.time.LocalDateTime;

@Data
@NoArgsConstructor
@AllArgsConstructor
public class EnrolledStudentResponse {
    private Long userId;
    private String username;
    private String fullName;
    private String email;
    private String avatarUrl;
    private LocalDateTime enrolledAt;
    
    // Progress info
    private BigDecimal progressPercentage;
    private Integer completedLessons;
    private Integer totalLessons;
    private Integer totalTimeSpent; // seconds
    private LocalDateTime lastAccessedAt;
}
