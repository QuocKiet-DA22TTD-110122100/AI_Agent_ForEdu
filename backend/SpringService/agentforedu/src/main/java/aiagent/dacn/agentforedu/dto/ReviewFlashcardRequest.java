package aiagent.dacn.agentforedu.dto;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@NoArgsConstructor
@AllArgsConstructor
public class ReviewFlashcardRequest {
    private Long flashcardId;
    private Integer quality;  // 0-5 (0=Again, 1-2=Hard, 3-4=Good, 5=Easy)
    private Integer timeTakenSeconds;
}
