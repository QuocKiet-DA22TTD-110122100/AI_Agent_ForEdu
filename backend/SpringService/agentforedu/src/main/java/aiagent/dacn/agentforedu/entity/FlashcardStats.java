package aiagent.dacn.agentforedu.entity;

import jakarta.persistence.*;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;
import java.math.BigDecimal;
import java.time.LocalDateTime;

@Entity
@Table(name = "flashcard_stats",
       uniqueConstraints = @UniqueConstraint(columnNames = {"user_id", "flashcard_id"}))
@Data
@NoArgsConstructor
@AllArgsConstructor
public class FlashcardStats {
    
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    
    @Column(name = "user_id", nullable = false)
    private Long userId;
    
    @Column(name = "flashcard_id", nullable = false)
    private Long flashcardId;
    
    // Aggregated statistics
    @Column(name = "total_reviews")
    private Integer totalReviews = 0;
    
    @Column(name = "correct_reviews")
    private Integer correctReviews = 0;
    
    @Column(name = "wrong_reviews")
    private Integer wrongReviews = 0;
    
    // Current state (denormalized for performance)
    @Column(name = "current_ease_factor", precision = 4, scale = 2)
    private BigDecimal currentEaseFactor = BigDecimal.valueOf(2.5);
    
    @Column(name = "current_interval_days")
    private Integer currentIntervalDays = 0;
    
    @Column(name = "current_repetitions")
    private Integer currentRepetitions = 0;
    
    @Column(name = "next_review_date")
    private LocalDateTime nextReviewDate;
    
    // Performance metrics
    @Column(name = "average_time_seconds", precision = 8, scale = 2)
    private BigDecimal averageTimeSeconds = BigDecimal.ZERO;
    
    @Column(name = "last_review_date")
    private LocalDateTime lastReviewDate;
    
    // Card maturity level
    @Enumerated(EnumType.STRING)
    @Column(name = "maturity_level", length = 20)
    private MaturityLevel maturityLevel = MaturityLevel.NEW;
    
    @Column(name = "created_at", updatable = false)
    private LocalDateTime createdAt;
    
    @Column(name = "updated_at")
    private LocalDateTime updatedAt;
    
    @PrePersist
    protected void onCreate() {
        createdAt = LocalDateTime.now();
        updatedAt = LocalDateTime.now();
    }
    
    @PreUpdate
    protected void onUpdate() {
        updatedAt = LocalDateTime.now();
    }
    
    public enum MaturityLevel {
        NEW,          // Chưa học lần nào
        LEARNING,     // Đang học (interval < 7 days)
        YOUNG,        // Trẻ (7 days <= interval < 21 days)
        MATURE,       // Chín (interval >= 21 days)
        RELEARNING    // Học lại (sau khi quên)
    }
}
