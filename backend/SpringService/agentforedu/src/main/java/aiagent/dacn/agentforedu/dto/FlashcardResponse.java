package aiagent.dacn.agentforedu.dto;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;
import java.time.LocalDateTime;

@Data
@NoArgsConstructor
@AllArgsConstructor
public class FlashcardResponse {
    private Long id;
    private Long deckId;
    private String front;
    private String back;
    private String hint;
    private String explanation;
    private String frontImageUrl;
    private String backImageUrl;
    private String audioUrl;
    private String tags;
    private String sourceType;
    
    // Stats for this card
    private Integer totalReviews;
    private Double accuracy;
    private String maturityLevel;
    private LocalDateTime nextReviewDate;
    
    private LocalDateTime createdAt;
    private LocalDateTime updatedAt;
}
