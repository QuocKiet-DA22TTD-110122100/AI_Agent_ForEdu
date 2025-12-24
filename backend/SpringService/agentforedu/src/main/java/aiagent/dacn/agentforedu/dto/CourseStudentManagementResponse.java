package aiagent.dacn.agentforedu.dto;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.util.List;

@Data
@NoArgsConstructor
@AllArgsConstructor
public class CourseStudentManagementResponse {
    private Long courseId;
    private String courseTitle;
    private String courseDescription;
    private Long createdBy;
    private String creatorName;
    private Integer totalStudents;
    private Integer totalLessons;
    private List<EnrolledStudentResponse> students;
}
