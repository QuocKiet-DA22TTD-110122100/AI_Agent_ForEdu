package aiagent.dacn.agentforedu.repository;

import aiagent.dacn.agentforedu.entity.FlashcardStats;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;

import java.time.LocalDateTime;
import java.util.List;
import java.util.Optional;

@Repository
public interface FlashcardStatsRepository extends JpaRepository<FlashcardStats, Long> {
    
    Optional<FlashcardStats> findByUserIdAndFlashcardId(Long userId, Long flashcardId);
    
    List<FlashcardStats> findByUserId(Long userId);
    
    List<FlashcardStats> findByFlashcardId(Long flashcardId);
    
    // Find cards due for review
    @Query("SELECT fs FROM FlashcardStats fs WHERE fs.userId = :userId " +
           "AND fs.nextReviewDate IS NOT NULL AND fs.nextReviewDate <= :now")
    List<FlashcardStats> findDueCards(@Param("userId") Long userId, @Param("now") LocalDateTime now);
    
    // Find new cards (never reviewed)
    @Query("SELECT fs FROM FlashcardStats fs WHERE fs.userId = :userId " +
           "AND fs.maturityLevel = 'NEW'")
    List<FlashcardStats> findNewCards(@Param("userId") Long userId);
    
    // Count by maturity level
    @Query("SELECT COUNT(fs) FROM FlashcardStats fs WHERE fs.userId = :userId " +
           "AND fs.maturityLevel = :level")
    Long countByMaturityLevel(@Param("userId") Long userId, @Param("level") FlashcardStats.MaturityLevel level);
    
    // Get cards in a specific deck that are due
    @Query("SELECT fs FROM FlashcardStats fs JOIN Flashcard f ON fs.flashcardId = f.id " +
           "WHERE fs.userId = :userId AND f.deck.id = :deckId " +
           "AND fs.nextReviewDate IS NOT NULL AND fs.nextReviewDate <= :now")
    List<FlashcardStats> findDueCardsInDeck(@Param("userId") Long userId, 
                                             @Param("deckId") Long deckId, 
                                             @Param("now") LocalDateTime now);
    
    // Get statistics for a deck
    @Query("SELECT fs FROM FlashcardStats fs JOIN Flashcard f ON fs.flashcardId = f.id " +
           "WHERE fs.userId = :userId AND f.deck.id = :deckId")
    List<FlashcardStats> findByDeckId(@Param("userId") Long userId, @Param("deckId") Long deckId);
}
