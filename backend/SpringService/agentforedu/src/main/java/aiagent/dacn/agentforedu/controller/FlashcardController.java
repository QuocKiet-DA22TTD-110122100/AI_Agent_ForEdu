package aiagent.dacn.agentforedu.controller;

import aiagent.dacn.agentforedu.dto.*;
import aiagent.dacn.agentforedu.entity.User;
import aiagent.dacn.agentforedu.service.FlashcardService;
import lombok.RequiredArgsConstructor;
import org.springframework.http.ResponseEntity;
import org.springframework.security.core.annotation.AuthenticationPrincipal;
import org.springframework.web.bind.annotation.*;

import java.util.HashMap;
import java.util.List;
import java.util.Map;

@RestController
@RequestMapping("/api/flashcards")
@RequiredArgsConstructor
@CrossOrigin(origins = "*")
public class FlashcardController {
    
    private final FlashcardService flashcardService;
    
    // ==================== DECK MANAGEMENT ====================
    
    @PostMapping("/decks")
    public ResponseEntity<DeckResponse> createDeck(
            @AuthenticationPrincipal User user,
            @RequestBody CreateDeckRequest request) {
        
        DeckResponse response = flashcardService.createDeck(user.getId(), request);
        return ResponseEntity.ok(response);
    }
    
    @GetMapping("/decks")
    public ResponseEntity<List<DeckResponse>> getUserDecks(
            @AuthenticationPrincipal User user) {
        
        List<DeckResponse> decks = flashcardService.getUserDecks(user.getId());
        return ResponseEntity.ok(decks);
    }
    
    @GetMapping("/decks/{deckId}")
    public ResponseEntity<DeckResponse> getDeck(
            @AuthenticationPrincipal User user,
            @PathVariable Long deckId) {
        
        DeckResponse response = flashcardService.getDeck(deckId, user.getId());
        return ResponseEntity.ok(response);
    }
    
    @PutMapping("/decks/{deckId}")
    public ResponseEntity<DeckResponse> updateDeck(
            @AuthenticationPrincipal User user,
            @PathVariable Long deckId,
            @RequestBody CreateDeckRequest request) {
        
        DeckResponse response = flashcardService.updateDeck(deckId, user.getId(), request);
        return ResponseEntity.ok(response);
    }
    
    @DeleteMapping("/decks/{deckId}")
    public ResponseEntity<Map<String, String>> deleteDeck(
            @AuthenticationPrincipal User user,
            @PathVariable Long deckId) {
        
        flashcardService.deleteDeck(deckId, user.getId());
        
        Map<String, String> response = new HashMap<>();
        response.put("message", "Deck deleted successfully");
        return ResponseEntity.ok(response);
    }
    
    // ==================== FLASHCARD CRUD ====================
    
    @PostMapping("/decks/{deckId}/cards")
    public ResponseEntity<FlashcardResponse> createFlashcard(
            @AuthenticationPrincipal User user,
            @PathVariable Long deckId,
            @RequestBody CreateFlashcardRequest request) {
        
        FlashcardResponse response = flashcardService.createFlashcard(deckId, user.getId(), request);
        return ResponseEntity.ok(response);
    }
    
    @GetMapping("/decks/{deckId}/cards")
    public ResponseEntity<List<FlashcardResponse>> getFlashcardsInDeck(
            @AuthenticationPrincipal User user,
            @PathVariable Long deckId) {
        
        List<FlashcardResponse> cards = flashcardService.getFlashcardsInDeck(deckId, user.getId());
        return ResponseEntity.ok(cards);
    }
    
    @GetMapping("/cards/{cardId}")
    public ResponseEntity<FlashcardResponse> getFlashcard(
            @AuthenticationPrincipal User user,
            @PathVariable Long cardId) {
        
        FlashcardResponse response = flashcardService.getFlashcard(cardId, user.getId());
        return ResponseEntity.ok(response);
    }
    
    @PutMapping("/cards/{cardId}")
    public ResponseEntity<FlashcardResponse> updateFlashcard(
            @AuthenticationPrincipal User user,
            @PathVariable Long cardId,
            @RequestBody CreateFlashcardRequest request) {
        
        FlashcardResponse response = flashcardService.updateFlashcard(cardId, user.getId(), request);
        return ResponseEntity.ok(response);
    }
    
    @DeleteMapping("/cards/{cardId}")
    public ResponseEntity<Map<String, String>> deleteFlashcard(
            @AuthenticationPrincipal User user,
            @PathVariable Long cardId) {
        
        flashcardService.deleteFlashcard(cardId, user.getId());
        
        Map<String, String> response = new HashMap<>();
        response.put("message", "Flashcard deleted successfully");
        return ResponseEntity.ok(response);
    }
    
    // ==================== STUDY MODE ====================
    
    @GetMapping("/study/due")
    public ResponseEntity<List<FlashcardResponse>> getDueCards(
            @AuthenticationPrincipal User user,
            @RequestParam(required = false) Long deckId,
            @RequestParam(required = false, defaultValue = "50") Integer limit) {
        
        List<FlashcardResponse> cards = flashcardService.getCardsToReview(user.getId(), deckId, limit);
        return ResponseEntity.ok(cards);
    }
    
    @GetMapping("/study/new")
    public ResponseEntity<List<FlashcardResponse>> getNewCards(
            @AuthenticationPrincipal User user,
            @RequestParam(required = false) Long deckId,
            @RequestParam(required = false, defaultValue = "20") Integer limit) {
        
        List<FlashcardResponse> cards = flashcardService.getNewCards(user.getId(), deckId, limit);
        return ResponseEntity.ok(cards);
    }
    
    @PostMapping("/study/review")
    public ResponseEntity<FlashcardResponse> submitReview(
            @AuthenticationPrincipal User user,
            @RequestBody ReviewFlashcardRequest request) {
        
        FlashcardResponse response = flashcardService.submitReview(
                request.getFlashcardId(), 
                user.getId(), 
                request
        );
        return ResponseEntity.ok(response);
    }
    
    // ==================== STATISTICS ====================
    
    @GetMapping("/stats/deck/{deckId}")
    public ResponseEntity<DeckStatsResponse> getDeckStats(
            @AuthenticationPrincipal User user,
            @PathVariable Long deckId) {
        
        DeckStatsResponse stats = flashcardService.getDeckStats(deckId, user.getId());
        return ResponseEntity.ok(stats);
    }
    
    @GetMapping("/stats/overview")
    public ResponseEntity<Map<String, Object>> getOverviewStats(
            @AuthenticationPrincipal User user) {
        
        // Get all decks
        List<DeckResponse> decks = flashcardService.getUserDecks(user.getId());
        
        // Aggregate statistics
        int totalDecks = decks.size();
        int totalCards = decks.stream().mapToInt(DeckResponse::getTotalCards).sum();
        int totalNewCards = decks.stream().mapToInt(DeckResponse::getNewCards).sum();
        int totalDueCards = decks.stream().mapToInt(DeckResponse::getDueCards).sum();
        
        Map<String, Object> overview = new HashMap<>();
        overview.put("totalDecks", totalDecks);
        overview.put("totalCards", totalCards);
        overview.put("newCards", totalNewCards);
        overview.put("dueCards", totalDueCards);
        overview.put("studyStreak", 0); // TODO: Implement streak tracking
        overview.put("decks", decks);
        
        return ResponseEntity.ok(overview);
    }
}
