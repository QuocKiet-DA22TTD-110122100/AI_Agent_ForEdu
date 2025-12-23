package aiagent.dacn.agentforedu.entity;

import jakarta.persistence.*;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;
import java.math.BigDecimal;
import java.time.LocalDateTime;

@Entity
@Table(name = "flashcard_reviews")
@Data
@NoArgsConstructor
@AllArgsConstructor
public class FlashcardReview {
    
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    
    @Column(name = "flashcard_id", nullable = false)
    private Long flashcardId;
    
    @Column(name = "user_id", nullable = false)
    private Long userId;
    
    // SM-2 Algorithm parameters
    @Column(name = "ease_factor", precision = 4, scale = 2)
    private BigDecimal easeFactor = BigDecimal.valueOf(2.5);
    
    @Column(name = "interval_days")
    private Integer intervalDays = 0;
    
    @Column(name = "repetitions")
    private Integer repetitions = 0;
    
    // Review data
    @Column(nullable = false)
    private Integer quality;  // 0-5 (Anki style: 0=Again, 1=Hard, 3=Good, 5=Easy)
    
    @Column(name = "review_date", nullable = false)
    private LocalDateTime reviewDate;
    
    @Column(name = "next_review_date")
    private LocalDateTime nextReviewDate;
    
    @Column(name = "time_taken_seconds")
    private Integer timeTakenSeconds;
    
    @Column(name = "created_at", updatable = false)
    private LocalDateTime createdAt;
    
    @PrePersist
    protected void onCreate() {
        createdAt = LocalDateTime.now();
        reviewDate = LocalDateTime.now();
    }
}
