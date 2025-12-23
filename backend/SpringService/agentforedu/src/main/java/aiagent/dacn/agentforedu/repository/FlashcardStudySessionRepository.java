package aiagent.dacn.agentforedu.repository;

import aiagent.dacn.agentforedu.entity.FlashcardStudySession;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;

import java.time.LocalDateTime;
import java.util.List;
import java.util.Optional;

@Repository
public interface FlashcardStudySessionRepository extends JpaRepository<FlashcardStudySession, Long> {
    
    List<FlashcardStudySession> findByUserId(Long userId);
    
    List<FlashcardStudySession> findByUserIdOrderByStartTimeDesc(Long userId);
    
    Optional<FlashcardStudySession> findByUserIdAndEndTimeIsNull(Long userId);
    
    @Query("SELECT fss FROM FlashcardStudySession fss WHERE fss.userId = :userId " +
           "AND fss.startTime >= :since ORDER BY fss.startTime DESC")
    List<FlashcardStudySession> findRecentSessions(@Param("userId") Long userId, 
                                                    @Param("since") LocalDateTime since);
    
    @Query("SELECT fss FROM FlashcardStudySession fss WHERE fss.userId = :userId " +
           "AND fss.deckId = :deckId ORDER BY fss.startTime DESC")
    List<FlashcardStudySession> findByDeck(@Param("userId") Long userId, @Param("deckId") Long deckId);
}
