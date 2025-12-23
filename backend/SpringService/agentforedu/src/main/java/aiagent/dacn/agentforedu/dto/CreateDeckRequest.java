package aiagent.dacn.agentforedu.dto;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@NoArgsConstructor
@AllArgsConstructor
public class CreateDeckRequest {
    private String name;
    private String description;
    private String color;  // Hex color like "#3B82F6"
    private String icon;   // Emoji like "📚"
    private Boolean isPublic;
}
