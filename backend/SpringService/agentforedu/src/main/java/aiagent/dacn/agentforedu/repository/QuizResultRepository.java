package aiagent.dacn.agentforedu.repository;

import aiagent.dacn.agentforedu.entity.QuizResult;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.List;
import java.util.Optional;

@Repository
public interface QuizResultRepository extends JpaRepository<QuizResult, Long> {
    List<QuizResult> findByUserId(Long userId);
    List<QuizResult> findByQuizId(Long quizId);
    Optional<QuizResult> findTopByQuizIdAndUserIdOrderByCreatedAtDesc(Long quizId, Long userId);
}
