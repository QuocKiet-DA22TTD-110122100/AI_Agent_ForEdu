package aiagent.dacn.agentforedu.service;

import org.springframework.stereotype.Service;

import java.math.BigDecimal;
import java.math.RoundingMode;
import java.time.LocalDateTime;
import java.util.HashMap;
import java.util.Map;

/**
 * SM-2 Spaced Repetition Algorithm Implementation
 * Based on SuperMemo SM-2 algorithm (similar to Anki)
 * 
 * Reference: https://www.supermemo.com/en/archives1990-2015/english/ol/sm2
 * 
 * Quality ratings (0-5):
 * - 0: Complete blackout (Again) - Forgot completely
 * - 1: Incorrect, but remembered on seeing answer (Hard)
 * - 2: Incorrect, but easy to recall (Hard)
 * - 3: Correct, but difficult (Good)
 * - 4: Correct with hesitation (Good)  
 * - 5: Perfect recall (Easy)
 */
@Service
public class SpacedRepetitionService {
    
    /**
     * Calculate next review parameters based on SM-2 algorithm
     * 
     * @param quality User's performance rating (0-5)
     * @param repetitions Current number of consecutive correct reviews
     * @param easeFactor Current ease factor (difficulty)
     * @param intervalDays Current interval in days
     * @return Map containing: nextIntervalDays, nextEaseFactor, nextRepetitions, nextReviewDate
     */
    public Map<String, Object> calculateNextReview(
            int quality,
            int repetitions,
            BigDecimal easeFactor,
            int intervalDays) {
        
        Map<String, Object> result = new HashMap<>();
        
        // Validate inputs
        if (quality < 0 || quality > 5) {
            throw new IllegalArgumentException("Quality must be between 0 and 5");
        }
        
        // Initialize variables
        BigDecimal newEaseFactor = easeFactor;
        int newRepetitions = repetitions;
        int newInterval;
        
        // Calculate new ease factor
        // EF' = EF + (0.1 - (5 - q) * (0.08 + (5 - q) * 0.02))
        if (quality >= 3) {
            // Correct answer - update ease factor
            BigDecimal adjustment = BigDecimal.valueOf(0.1)
                    .subtract(BigDecimal.valueOf(5 - quality)
                            .multiply(BigDecimal.valueOf(0.08)
                                    .add(BigDecimal.valueOf(5 - quality)
                                            .multiply(BigDecimal.valueOf(0.02)))));
            
            newEaseFactor = easeFactor.add(adjustment);
            
            // Ensure ease factor doesn't go below 1.3
            if (newEaseFactor.compareTo(BigDecimal.valueOf(1.3)) < 0) {
                newEaseFactor = BigDecimal.valueOf(1.3);
            }
            
            newEaseFactor = newEaseFactor.setScale(2, RoundingMode.HALF_UP);
            
        } else {
            // Incorrect answer - don't change ease factor, but reset to minimum if too low
            if (easeFactor.compareTo(BigDecimal.valueOf(1.3)) < 0) {
                newEaseFactor = BigDecimal.valueOf(1.3);
            }
        }
        
        // Calculate new interval and repetitions
        if (quality < 3) {
            // Incorrect answer - restart from beginning
            newRepetitions = 0;
            newInterval = 1; // Review again tomorrow
            
        } else {
            // Correct answer - calculate next interval
            newRepetitions = repetitions + 1;
            
            if (newRepetitions == 1) {
                newInterval = 1; // First correct: 1 day
            } else if (newRepetitions == 2) {
                newInterval = 6; // Second correct: 6 days
            } else {
                // Third+ correct: multiply previous interval by ease factor
                newInterval = (int) Math.ceil(intervalDays * newEaseFactor.doubleValue());
            }
        }
        
        // Apply quality-based modifiers for fine-tuning
        newInterval = applyQualityModifier(newInterval, quality);
        
        // Calculate next review date
        LocalDateTime nextReviewDate = LocalDateTime.now().plusDays(newInterval);
        
        // Determine maturity level
        String maturityLevel = determineMaturityLevel(newRepetitions, newInterval);
        
        // Prepare result
        result.put("nextIntervalDays", newInterval);
        result.put("nextEaseFactor", newEaseFactor);
        result.put("nextRepetitions", newRepetitions);
        result.put("nextReviewDate", nextReviewDate);
        result.put("maturityLevel", maturityLevel);
        
        return result;
    }
    
    /**
     * Apply quality-based modifiers to interval
     * This provides finer control similar to Anki's "Again/Hard/Good/Easy" buttons
     */
    private int applyQualityModifier(int baseInterval, int quality) {
        switch (quality) {
            case 0: // Again - Total failure
                return 1; // Review again tomorrow
            case 1: // Hard - Very difficult
                return Math.max(1, (int) (baseInterval * 0.5)); // 50% of normal
            case 2: // Hard - Difficult  
                return Math.max(1, (int) (baseInterval * 0.7)); // 70% of normal
            case 3: // Good - Normal difficulty
                return baseInterval; // Standard interval
            case 4: // Good - Relatively easy
                return (int) (baseInterval * 1.2); // 120% of normal
            case 5: // Easy - Very easy
                return (int) (baseInterval * 1.5); // 150% of normal
            default:
                return baseInterval;
        }
    }
    
    /**
     * Determine card maturity level based on repetitions and interval
     */
    private String determineMaturityLevel(int repetitions, int intervalDays) {
        if (repetitions == 0) {
            return "NEW";
        } else if (intervalDays < 7) {
            return "LEARNING";
        } else if (intervalDays < 21) {
            return "YOUNG";
        } else {
            return "MATURE";
        }
    }
    
    /**
     * Get recommended daily review limits
     */
    public Map<String, Integer> getRecommendedLimits() {
        Map<String, Integer> limits = new HashMap<>();
        limits.put("newCardsPerDay", 20);      // Max new cards per day
        limits.put("reviewCardsPerDay", 100);  // Max review cards per day
        limits.put("timePerCard", 30);         // Recommended seconds per card
        return limits;
    }
    
    /**
     * Calculate optimal study time distribution
     */
    public Map<String, String> getStudyRecommendation(int dueCards, int newCards) {
        Map<String, String> recommendation = new HashMap<>();
        
        int totalCards = dueCards + Math.min(newCards, 20); // Limit new cards
        int estimatedMinutes = (totalCards * 30) / 60; // 30 seconds per card
        
        recommendation.put("totalCards", String.valueOf(totalCards));
        recommendation.put("estimatedTime", estimatedMinutes + " minutes");
        recommendation.put("priority", dueCards > 0 ? "Review due cards first" : "Learn new cards");
        
        if (dueCards > 50) {
            recommendation.put("warning", "High backlog! Focus on reviews today.");
        }
        
        return recommendation;
    }
}
