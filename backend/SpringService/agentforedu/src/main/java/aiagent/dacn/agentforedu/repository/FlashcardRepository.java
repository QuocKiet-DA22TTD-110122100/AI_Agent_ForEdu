package aiagent.dacn.agentforedu.repository;

import aiagent.dacn.agentforedu.entity.Flashcard;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;

import java.util.List;
import java.util.Optional;

@Repository
public interface FlashcardRepository extends JpaRepository<Flashcard, Long> {
    
    List<Flashcard> findByDeckId(Long deckId);
    
    List<Flashcard> findByDeckIdOrderByCreatedAtDesc(Long deckId);
    
    List<Flashcard> findByUserId(Long userId);
    
    Optional<Flashcard> findByIdAndUserId(Long id, Long userId);
    
    Long countByDeckId(Long deckId);
    
    Long countByUserId(Long userId);
    
    @Query("SELECT f FROM Flashcard f WHERE f.deck.id = :deckId AND " +
           "(f.front LIKE %:keyword% OR f.back LIKE %:keyword% OR f.hint LIKE %:keyword%)")
    List<Flashcard> searchInDeck(@Param("deckId") Long deckId, @Param("keyword") String keyword);
    
    List<Flashcard> findBySourceType(String sourceType);
    
    List<Flashcard> findBySourceMaterialId(Long sourceMaterialId);
}
