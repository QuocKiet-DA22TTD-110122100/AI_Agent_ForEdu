package aiagent.dacn.agentforedu.dto;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@NoArgsConstructor
@AllArgsConstructor
public class CreateFlashcardRequest {
    private String front;
    private String back;
    private String hint;
    private String explanation;
    private String frontImageUrl;
    private String backImageUrl;
    private String audioUrl;
    private String tags;  // JSON array string: "[\"math\",\"calculus\"]"
}
