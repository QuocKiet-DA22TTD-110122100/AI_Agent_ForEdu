package aiagent.dacn.agentforedu.entity;

import jakarta.persistence.*;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;
import java.time.LocalDateTime;

@Entity
@Table(name = "flashcard_generation_requests")
@Data
@NoArgsConstructor
@AllArgsConstructor
public class FlashcardGenerationRequest {
    
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    
    @Column(name = "user_id", nullable = false)
    private Long userId;
    
    @Column(name = "deck_id", nullable = false)
    private Long deckId;
    
    // Input source
    @Enumerated(EnumType.STRING)
    @Column(name = "source_type", nullable = false, length = 20)
    private SourceType sourceType;
    
    @Column(name = "source_material_id")
    private Long sourceMaterialId;
    
    @Column(name = "source_text", columnDefinition = "TEXT")
    private String sourceText;
    
    @Column(name = "source_url", length = 500)
    private String sourceUrl;
    
    // Generation parameters
    @Column(name = "num_cards_requested", nullable = false)
    private Integer numCardsRequested;
    
    @Enumerated(EnumType.STRING)
    @Column(name = "difficulty_level", length = 20)
    private DifficultyLevel difficultyLevel = DifficultyLevel.MEDIUM;
    
    @Enumerated(EnumType.STRING)
    @Column(name = "card_type", length = 20)
    private CardType cardType = CardType.QA;
    
    // Processing status
    @Enumerated(EnumType.STRING)
    @Column(name = "status", length = 20)
    private GenerationStatus status = GenerationStatus.PENDING;
    
    @Column(name = "cards_generated")
    private Integer cardsGenerated = 0;
    
    @Column(name = "error_message", columnDefinition = "TEXT")
    private String errorMessage;
    
    @Column(name = "ai_model", length = 100)
    private String aiModel;
    
    @Column(name = "created_at", updatable = false)
    private LocalDateTime createdAt;
    
    @Column(name = "completed_at")
    private LocalDateTime completedAt;
    
    @PrePersist
    protected void onCreate() {
        createdAt = LocalDateTime.now();
    }
    
    public enum SourceType {
        MATERIAL,  // Từ tài liệu đã upload
        TEXT,      // Từ text người dùng nhập
        URL        // Từ URL
    }
    
    public enum DifficultyLevel {
        EASY,
        MEDIUM,
        HARD,
        MIXED
    }
    
    public enum CardType {
        DEFINITION,    // Định nghĩa
        QA,           // Câu hỏi - Câu trả lời
        CLOZE,        // Điền vào chỗ trống
        TRUE_FALSE,   // Đúng/Sai
        MIXED         // Kết hợp
    }
    
    public enum GenerationStatus {
        PENDING,
        PROCESSING,
        COMPLETED,
        FAILED
    }
}
