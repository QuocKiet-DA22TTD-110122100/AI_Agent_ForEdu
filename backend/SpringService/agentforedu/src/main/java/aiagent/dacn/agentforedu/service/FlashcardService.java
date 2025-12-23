package aiagent.dacn.agentforedu.service;

import aiagent.dacn.agentforedu.dto.*;
import aiagent.dacn.agentforedu.entity.*;
import aiagent.dacn.agentforedu.repository.*;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.math.BigDecimal;
import java.math.RoundingMode;
import java.time.LocalDateTime;
import java.util.ArrayList;
import java.util.List;
import java.util.Map;
import java.util.stream.Collectors;

@Service
@RequiredArgsConstructor
public class FlashcardService {
    
    private final FlashcardDeckRepository deckRepository;
    private final FlashcardRepository flashcardRepository;
    private final FlashcardStatsRepository statsRepository;
    private final FlashcardReviewRepository reviewRepository;
    private final FlashcardStudySessionRepository sessionRepository;
    private final SpacedRepetitionService spacedRepetitionService;
    
    // ==================== DECK MANAGEMENT ====================
    
    @Transactional
    public DeckResponse createDeck(Long userId, CreateDeckRequest request) {
        FlashcardDeck deck = new FlashcardDeck();
        deck.setUserId(userId);
        deck.setName(request.getName());
        deck.setDescription(request.getDescription());
        deck.setColor(request.getColor() != null ? request.getColor() : "#3B82F6");
        deck.setIcon(request.getIcon() != null ? request.getIcon() : "📚");
        deck.setIsPublic(request.getIsPublic() != null ? request.getIsPublic() : false);
        
        deck = deckRepository.save(deck);
        return toDeckResponse(deck);
    }
    
    public List<DeckResponse> getUserDecks(Long userId) {
        List<FlashcardDeck> decks = deckRepository.findByUserIdOrderByCreatedAtDesc(userId);
        return decks.stream().map(this::toDeckResponse).collect(Collectors.toList());
    }
    
    public DeckResponse getDeck(Long deckId, Long userId) {
        FlashcardDeck deck = deckRepository.findByIdAndUserId(deckId, userId)
                .orElseThrow(() -> new RuntimeException("Deck not found"));
        return toDeckResponse(deck);
    }
    
    @Transactional
    public DeckResponse updateDeck(Long deckId, Long userId, CreateDeckRequest request) {
        FlashcardDeck deck = deckRepository.findByIdAndUserId(deckId, userId)
                .orElseThrow(() -> new RuntimeException("Deck not found"));
        
        if (request.getName() != null) deck.setName(request.getName());
        if (request.getDescription() != null) deck.setDescription(request.getDescription());
        if (request.getColor() != null) deck.setColor(request.getColor());
        if (request.getIcon() != null) deck.setIcon(request.getIcon());
        if (request.getIsPublic() != null) deck.setIsPublic(request.getIsPublic());
        
        deck = deckRepository.save(deck);
        return toDeckResponse(deck);
    }
    
    @Transactional
    public void deleteDeck(Long deckId, Long userId) {
        FlashcardDeck deck = deckRepository.findByIdAndUserId(deckId, userId)
                .orElseThrow(() -> new RuntimeException("Deck not found"));
        deckRepository.delete(deck);
    }
    
    // ==================== FLASHCARD CRUD ====================
    
    @Transactional
    public FlashcardResponse createFlashcard(Long deckId, Long userId, CreateFlashcardRequest request) {
        FlashcardDeck deck = deckRepository.findByIdAndUserId(deckId, userId)
                .orElseThrow(() -> new RuntimeException("Deck not found"));
        
        Flashcard flashcard = new Flashcard();
        flashcard.setDeck(deck);
        flashcard.setUserId(userId);
        flashcard.setFront(request.getFront());
        flashcard.setBack(request.getBack());
        flashcard.setHint(request.getHint());
        flashcard.setExplanation(request.getExplanation());
        flashcard.setFrontImageUrl(request.getFrontImageUrl());
        flashcard.setBackImageUrl(request.getBackImageUrl());
        flashcard.setAudioUrl(request.getAudioUrl());
        flashcard.setTags(request.getTags());
        flashcard.setSourceType("MANUAL");
        
        flashcard = flashcardRepository.save(flashcard);
        
        // Initialize stats for this card
        FlashcardStats stats = new FlashcardStats();
        stats.setUserId(userId);
        stats.setFlashcardId(flashcard.getId());
        stats.setMaturityLevel(FlashcardStats.MaturityLevel.NEW);
        statsRepository.save(stats);
        
        return toFlashcardResponse(flashcard, stats);
    }
    
    public List<FlashcardResponse> getFlashcardsInDeck(Long deckId, Long userId) {
        // Verify deck ownership
        deckRepository.findByIdAndUserId(deckId, userId)
                .orElseThrow(() -> new RuntimeException("Deck not found"));
        
        List<Flashcard> flashcards = flashcardRepository.findByDeckIdOrderByCreatedAtDesc(deckId);
        return flashcards.stream().map(card -> {
            FlashcardStats stats = statsRepository.findByUserIdAndFlashcardId(userId, card.getId())
                    .orElse(null);
            return toFlashcardResponse(card, stats);
        }).collect(Collectors.toList());
    }
    
    public FlashcardResponse getFlashcard(Long flashcardId, Long userId) {
        Flashcard flashcard = flashcardRepository.findByIdAndUserId(flashcardId, userId)
                .orElseThrow(() -> new RuntimeException("Flashcard not found"));
        
        FlashcardStats stats = statsRepository.findByUserIdAndFlashcardId(userId, flashcardId)
                .orElse(null);
        
        return toFlashcardResponse(flashcard, stats);
    }
    
    @Transactional
    public FlashcardResponse updateFlashcard(Long flashcardId, Long userId, CreateFlashcardRequest request) {
        Flashcard flashcard = flashcardRepository.findByIdAndUserId(flashcardId, userId)
                .orElseThrow(() -> new RuntimeException("Flashcard not found"));
        
        if (request.getFront() != null) flashcard.setFront(request.getFront());
        if (request.getBack() != null) flashcard.setBack(request.getBack());
        if (request.getHint() != null) flashcard.setHint(request.getHint());
        if (request.getExplanation() != null) flashcard.setExplanation(request.getExplanation());
        if (request.getFrontImageUrl() != null) flashcard.setFrontImageUrl(request.getFrontImageUrl());
        if (request.getBackImageUrl() != null) flashcard.setBackImageUrl(request.getBackImageUrl());
        if (request.getAudioUrl() != null) flashcard.setAudioUrl(request.getAudioUrl());
        if (request.getTags() != null) flashcard.setTags(request.getTags());
        
        flashcard = flashcardRepository.save(flashcard);
        
        FlashcardStats stats = statsRepository.findByUserIdAndFlashcardId(userId, flashcardId)
                .orElse(null);
        
        return toFlashcardResponse(flashcard, stats);
    }
    
    @Transactional
    public void deleteFlashcard(Long flashcardId, Long userId) {
        Flashcard flashcard = flashcardRepository.findByIdAndUserId(flashcardId, userId)
                .orElseThrow(() -> new RuntimeException("Flashcard not found"));
        flashcardRepository.delete(flashcard);
    }
    
    // ==================== STUDY OPERATIONS ====================
    
    public List<FlashcardResponse> getCardsToReview(Long userId, Long deckId, Integer limit) {
        List<FlashcardStats> dueStats;
        
        if (deckId != null) {
            dueStats = statsRepository.findDueCardsInDeck(userId, deckId, LocalDateTime.now());
        } else {
            dueStats = statsRepository.findDueCards(userId, LocalDateTime.now());
        }
        
        if (limit != null && dueStats.size() > limit) {
            dueStats = dueStats.subList(0, limit);
        }
        
        return dueStats.stream().map(stats -> {
            Flashcard card = flashcardRepository.findById(stats.getFlashcardId())
                    .orElseThrow(() -> new RuntimeException("Card not found"));
            return toFlashcardResponse(card, stats);
        }).collect(Collectors.toList());
    }
    
    public List<FlashcardResponse> getNewCards(Long userId, Long deckId, Integer limit) {
        List<FlashcardStats> newStats = statsRepository.findNewCards(userId);
        
        // Filter by deck if specified
        if (deckId != null) {
            newStats = newStats.stream()
                    .filter(stats -> {
                        Flashcard card = flashcardRepository.findById(stats.getFlashcardId()).orElse(null);
                        return card != null && card.getDeck().getId().equals(deckId);
                    })
                    .collect(Collectors.toList());
        }
        
        if (limit != null && newStats.size() > limit) {
            newStats = newStats.subList(0, limit);
        }
        
        return newStats.stream().map(stats -> {
            Flashcard card = flashcardRepository.findById(stats.getFlashcardId())
                    .orElseThrow(() -> new RuntimeException("Card not found"));
            return toFlashcardResponse(card, stats);
        }).collect(Collectors.toList());
    }
    
    @Transactional
    public FlashcardResponse submitReview(Long flashcardId, Long userId, ReviewFlashcardRequest request) {
        // Get card and stats
        Flashcard flashcard = flashcardRepository.findByIdAndUserId(flashcardId, userId)
                .orElseThrow(() -> new RuntimeException("Flashcard not found"));
        
        FlashcardStats stats = statsRepository.findByUserIdAndFlashcardId(userId, flashcardId)
                .orElseThrow(() -> new RuntimeException("Stats not found"));
        
        // Calculate next review using SM-2 algorithm
        Map<String, Object> nextReview = spacedRepetitionService.calculateNextReview(
                request.getQuality(),
                stats.getCurrentRepetitions(),
                stats.getCurrentEaseFactor(),
                stats.getCurrentIntervalDays()
        );
        
        // Update stats
        stats.setTotalReviews(stats.getTotalReviews() + 1);
        if (request.getQuality() >= 3) {
            stats.setCorrectReviews(stats.getCorrectReviews() + 1);
        } else {
            stats.setWrongReviews(stats.getWrongReviews() + 1);
        }
        
        stats.setCurrentEaseFactor((BigDecimal) nextReview.get("nextEaseFactor"));
        stats.setCurrentIntervalDays((Integer) nextReview.get("nextIntervalDays"));
        stats.setCurrentRepetitions((Integer) nextReview.get("nextRepetitions"));
        stats.setNextReviewDate((LocalDateTime) nextReview.get("nextReviewDate"));
        stats.setLastReviewDate(LocalDateTime.now());
        
        // Update maturity level
        String maturityLevelStr = (String) nextReview.get("maturityLevel");
        stats.setMaturityLevel(FlashcardStats.MaturityLevel.valueOf(maturityLevelStr));
        
        // Update average time
        if (request.getTimeTakenSeconds() != null) {
            BigDecimal currentAvg = stats.getAverageTimeSeconds();
            BigDecimal newTime = BigDecimal.valueOf(request.getTimeTakenSeconds());
            BigDecimal newAvg = currentAvg
                    .multiply(BigDecimal.valueOf(stats.getTotalReviews() - 1))
                    .add(newTime)
                    .divide(BigDecimal.valueOf(stats.getTotalReviews()), 2, RoundingMode.HALF_UP);
            stats.setAverageTimeSeconds(newAvg);
        }
        
        statsRepository.save(stats);
        
        // Create review record
        FlashcardReview review = new FlashcardReview();
        review.setFlashcardId(flashcardId);
        review.setUserId(userId);
        review.setQuality(request.getQuality());
        review.setEaseFactor((BigDecimal) nextReview.get("nextEaseFactor"));
        review.setIntervalDays((Integer) nextReview.get("nextIntervalDays"));
        review.setRepetitions((Integer) nextReview.get("nextRepetitions"));
        review.setNextReviewDate((LocalDateTime) nextReview.get("nextReviewDate"));
        review.setTimeTakenSeconds(request.getTimeTakenSeconds());
        reviewRepository.save(review);
        
        return toFlashcardResponse(flashcard, stats);
    }
    
    // ==================== STATISTICS ====================
    
    public DeckStatsResponse getDeckStats(Long deckId, Long userId) {
        FlashcardDeck deck = deckRepository.findByIdAndUserId(deckId, userId)
                .orElseThrow(() -> new RuntimeException("Deck not found"));
        
        List<FlashcardStats> allStats = statsRepository.findByDeckId(userId, deckId);
        
        DeckStatsResponse response = new DeckStatsResponse();
        response.setDeckId(deckId);
        response.setDeckName(deck.getName());
        response.setTotalCards(allStats.size());
        
        // Count by maturity level
        response.setNewCards((int) allStats.stream()
                .filter(s -> s.getMaturityLevel() == FlashcardStats.MaturityLevel.NEW).count());
        response.setLearningCards((int) allStats.stream()
                .filter(s -> s.getMaturityLevel() == FlashcardStats.MaturityLevel.LEARNING).count());
        response.setYoungCards((int) allStats.stream()
                .filter(s -> s.getMaturityLevel() == FlashcardStats.MaturityLevel.YOUNG).count());
        response.setMatureCards((int) allStats.stream()
                .filter(s -> s.getMaturityLevel() == FlashcardStats.MaturityLevel.MATURE).count());
        
        // Count due cards
        LocalDateTime now = LocalDateTime.now();
        response.setDueCards((int) allStats.stream()
                .filter(s -> s.getNextReviewDate() != null && s.getNextReviewDate().isBefore(now)).count());
        
        // Calculate accuracy
        int totalReviews = allStats.stream().mapToInt(FlashcardStats::getTotalReviews).sum();
        int correctReviews = allStats.stream().mapToInt(FlashcardStats::getCorrectReviews).sum();
        response.setTotalReviews(totalReviews);
        response.setOverallAccuracy(totalReviews > 0 ? (double) correctReviews / totalReviews : 0.0);
        
        // Calculate average time
        BigDecimal avgTime = allStats.stream()
                .map(FlashcardStats::getAverageTimeSeconds)
                .filter(t -> t != null && t.compareTo(BigDecimal.ZERO) > 0)
                .reduce(BigDecimal.ZERO, BigDecimal::add)
                .divide(BigDecimal.valueOf(Math.max(1, allStats.size())), 2, RoundingMode.HALF_UP);
        response.setAverageTimeSeconds(avgTime.intValue());
        
        // Estimate study time
        int estimatedMinutes = (response.getDueCards() * response.getAverageTimeSeconds()) / 60;
        response.setEstimatedMinutesToday(estimatedMinutes);
        response.setStudyPriority(response.getDueCards() > 20 ? "HIGH" : "NORMAL");
        
        return response;
    }
    
    // ==================== HELPER METHODS ====================
    
    private DeckResponse toDeckResponse(FlashcardDeck deck) {
        DeckResponse response = new DeckResponse();
        response.setId(deck.getId());
        response.setName(deck.getName());
        response.setDescription(deck.getDescription());
        response.setColor(deck.getColor());
        response.setIcon(deck.getIcon());
        response.setIsPublic(deck.getIsPublic());
        response.setCreatedAt(deck.getCreatedAt());
        response.setUpdatedAt(deck.getUpdatedAt());
        
        // Count cards
        Long totalCards = flashcardRepository.countByDeckId(deck.getId());
        response.setTotalCards(totalCards.intValue());
        
        // Count new and due cards (simplified)
        List<FlashcardStats> stats = statsRepository.findByDeckId(deck.getUserId(), deck.getId());
        response.setNewCards((int) stats.stream()
                .filter(s -> s.getMaturityLevel() == FlashcardStats.MaturityLevel.NEW).count());
        response.setDueCards((int) stats.stream()
                .filter(s -> s.getNextReviewDate() != null && s.getNextReviewDate().isBefore(LocalDateTime.now())).count());
        
        return response;
    }
    
    private FlashcardResponse toFlashcardResponse(Flashcard card, FlashcardStats stats) {
        FlashcardResponse response = new FlashcardResponse();
        response.setId(card.getId());
        response.setDeckId(card.getDeck().getId());
        response.setFront(card.getFront());
        response.setBack(card.getBack());
        response.setHint(card.getHint());
        response.setExplanation(card.getExplanation());
        response.setFrontImageUrl(card.getFrontImageUrl());
        response.setBackImageUrl(card.getBackImageUrl());
        response.setAudioUrl(card.getAudioUrl());
        response.setTags(card.getTags());
        response.setSourceType(card.getSourceType());
        response.setCreatedAt(card.getCreatedAt());
        response.setUpdatedAt(card.getUpdatedAt());
        
        if (stats != null) {
            response.setTotalReviews(stats.getTotalReviews());
            double accuracy = stats.getTotalReviews() > 0 
                    ? (double) stats.getCorrectReviews() / stats.getTotalReviews() 
                    : 0.0;
            response.setAccuracy(accuracy);
            response.setMaturityLevel(stats.getMaturityLevel().name());
            response.setNextReviewDate(stats.getNextReviewDate());
        }
        
        return response;
    }
}
