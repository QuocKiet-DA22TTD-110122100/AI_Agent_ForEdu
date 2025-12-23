package aiagent.dacn.agentforedu.dto;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@NoArgsConstructor
@AllArgsConstructor
public class DeckStatsResponse {
    private Long deckId;
    private String deckName;
    
    // Card counts by status
    private Integer totalCards;
    private Integer newCards;
    private Integer learningCards;
    private Integer youngCards;
    private Integer matureCards;
    private Integer dueCards;
    
    // Performance metrics
    private Double overallAccuracy;
    private Integer totalReviews;
    private Integer reviewsToday;
    private Integer averageTimeSeconds;
    
    // Study estimates
    private Integer estimatedMinutesToday;
    private String studyPriority;
}
