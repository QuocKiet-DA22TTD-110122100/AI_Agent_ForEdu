package aiagent.dacn.agentforedu.dto;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;
import java.time.LocalDateTime;

@Data
@NoArgsConstructor
@AllArgsConstructor
public class DeckResponse {
    private Long id;
    private String name;
    private String description;
    private String color;
    private String icon;
    private Boolean isPublic;
    private Integer totalCards;
    private Integer newCards;
    private Integer dueCards;
    private LocalDateTime createdAt;
    private LocalDateTime updatedAt;
}
