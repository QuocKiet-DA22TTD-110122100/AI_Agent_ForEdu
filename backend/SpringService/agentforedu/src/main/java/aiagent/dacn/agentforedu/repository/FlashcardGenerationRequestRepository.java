package aiagent.dacn.agentforedu.repository;

import aiagent.dacn.agentforedu.entity.FlashcardGenerationRequest;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.List;

@Repository
public interface FlashcardGenerationRequestRepository extends JpaRepository<FlashcardGenerationRequest, Long> {
    
    List<FlashcardGenerationRequest> findByUserId(Long userId);
    
    List<FlashcardGenerationRequest> findByUserIdOrderByCreatedAtDesc(Long userId);
    
    List<FlashcardGenerationRequest> findByStatus(FlashcardGenerationRequest.GenerationStatus status);
    
    List<FlashcardGenerationRequest> findByDeckId(Long deckId);
    
    Long countByUserIdAndStatus(Long userId, FlashcardGenerationRequest.GenerationStatus status);
}
