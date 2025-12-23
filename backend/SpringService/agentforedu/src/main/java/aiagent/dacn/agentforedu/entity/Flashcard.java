package aiagent.dacn.agentforedu.entity;

import jakarta.persistence.*;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;
import java.time.LocalDateTime;

@Entity
@Table(name = "flashcards")
@Data
@NoArgsConstructor
@AllArgsConstructor
public class Flashcard {
    
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    
    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "deck_id", nullable = false)
    private FlashcardDeck deck;
    
    @Column(name = "user_id", nullable = false)
    private Long userId;
    
    // Card content
    @Column(columnDefinition = "TEXT", nullable = false)
    private String front;  // Mặt trước (câu hỏi)
    
    @Column(columnDefinition = "TEXT", nullable = false)
    private String back;   // Mặt sau (câu trả lời)
    
    @Column(columnDefinition = "TEXT")
    private String hint;   // Gợi ý
    
    @Column(columnDefinition = "TEXT")
    private String explanation;  // Giải thích chi tiết
    
    // Media URLs
    @Column(name = "front_image_url", length = 500)
    private String frontImageUrl;
    
    @Column(name = "back_image_url", length = 500)
    private String backImageUrl;
    
    @Column(name = "audio_url", length = 500)
    private String audioUrl;
    
    // Tags stored as JSON string: ["math", "calculus"]
    @Column(columnDefinition = "JSON")
    private String tags;
    
    // Source tracking
    @Column(name = "source_type", length = 50)
    private String sourceType;  // MANUAL, AI_GENERATED, IMPORTED
    
    @Column(name = "source_material_id")
    private Long sourceMaterialId;
    
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
}
