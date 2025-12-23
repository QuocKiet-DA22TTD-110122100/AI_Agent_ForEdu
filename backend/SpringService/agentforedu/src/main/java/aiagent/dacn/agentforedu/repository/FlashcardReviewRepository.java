package aiagent.dacn.agentforedu.repository;

import aiagent.dacn.agentforedu.entity.FlashcardReview;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;

import java.time.LocalDateTime;
import java.util.List;

@Repository
public interface FlashcardReviewRepository extends JpaRepository<FlashcardReview, Long> {
    
    List<FlashcardReview> findByFlashcardId(Long flashcardId);
    
    List<FlashcardReview> findByUserId(Long userId);
    
    List<FlashcardReview> findByUserIdAndFlashcardId(Long userId, Long flashcardId);
    
    List<FlashcardReview> findByUserIdOrderByReviewDateDesc(Long userId);
    
    // Get recent reviews
    @Query("SELECT fr FROM FlashcardReview fr WHERE fr.userId = :userId " +
           "AND fr.reviewDate >= :since ORDER BY fr.reviewDate DESC")
    List<FlashcardReview> findRecentReviews(@Param("userId") Long userId, 
                                            @Param("since") LocalDateTime since);
    
    // Get last review for a card
    @Query("SELECT fr FROM FlashcardReview fr WHERE fr.userId = :userId " +
           "AND fr.flashcardId = :flashcardId ORDER BY fr.reviewDate DESC")
    List<FlashcardReview> findLastReview(@Param("userId") Long userId, 
                                         @Param("flashcardId") Long flashcardId);
    
    Long countByUserIdAndFlashcardId(Long userId, Long flashcardId);
}
