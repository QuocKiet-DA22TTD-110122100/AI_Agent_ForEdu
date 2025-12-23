package aiagent.dacn.agentforedu.entity;

import jakarta.persistence.*;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;
import java.time.LocalDateTime;

@Entity
@Table(name = "flashcard_study_sessions")
@Data
@NoArgsConstructor
@AllArgsConstructor
public class FlashcardStudySession {
    
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    
    @Column(name = "user_id", nullable = false)
    private Long userId;
    
    @Column(name = "deck_id")
    private Long deckId;
    
    @Enumerated(EnumType.STRING)
    @Column(name = "session_type", length = 20)
    private SessionType sessionType = SessionType.REVIEW;
    
    @Column(name = "start_time", nullable = false)
    private LocalDateTime startTime;
    
    @Column(name = "end_time")
    private LocalDateTime endTime;
    
    // Session statistics
    @Column(name = "cards_studied")
    private Integer cardsStudied = 0;
    
    @Column(name = "cards_correct")
    private Integer cardsCorrect = 0;
    
    @Column(name = "cards_wrong")
    private Integer cardsWrong = 0;
    
    @Column(name = "total_time_seconds")
    private Integer totalTimeSeconds = 0;
    
    @Column(name = "created_at", updatable = false)
    private LocalDateTime createdAt;
    
    @PrePersist
    protected void onCreate() {
        createdAt = LocalDateTime.now();
        if (startTime == null) {
            startTime = LocalDateTime.now();
        }
    }
    
    public enum SessionType {
        REVIEW,       // Ôn tập các thẻ cũ
        LEARN_NEW,    // Học thẻ mới
        CRAMMING,     // Học dồn (tất cả thẻ)
        MIXED         // Kết hợp
    }
}
