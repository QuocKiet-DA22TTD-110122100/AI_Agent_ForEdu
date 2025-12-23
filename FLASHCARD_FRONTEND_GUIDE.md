# 🎴 FLASHCARD FRONTEND - REACT COMPONENTS GUIDE

## 📂 Cấu trúc thư mục

```
fronend_web/src/
├── pages/
│   ├── FlashcardsPage.tsx          ⭐ (List all decks)
│   ├── FlashcardDeckPage.tsx       ⭐ (View deck + manage cards)
│   └── FlashcardStudyPage.tsx      ⭐ (Study mode)
│
├── components/
│   ├── flashcards/
│   │   ├── DeckCard.tsx            (Deck display card)
│   │   ├── FlashcardStudyCard.tsx  (Animated flip card)
│   │   ├── FlashcardEditor.tsx     (Create/Edit form)
│   │   ├── ReviewButtons.tsx       (Again/Hard/Good/Easy)
│   │   └── StatsChart.tsx          (Progress visualization)
│
├── services/
│   └── flashcardService.ts         ⭐ (API calls)
│
└── types/
    └── flashcard.ts                 (TypeScript interfaces)
```

---

## 🎯 1. TypeScript Types

**File:** `src/types/flashcard.ts`

```typescript
export interface FlashcardDeck {
  id: number;
  name: string;
  description?: string;
  color: string;
  icon: string;
  isPublic: boolean;
  totalCards: number;
  newCards: number;
  dueCards: number;
  createdAt: string;
  updatedAt: string;
}

export interface Flashcard {
  id: number;
  deckId: number;
  front: string;
  back: string;
  hint?: string;
  explanation?: string;
  frontImageUrl?: string;
  backImageUrl?: string;
  audioUrl?: string;
  tags?: string;
  sourceType: string;
  totalReviews: number;
  accuracy: number;
  maturityLevel: string;
  nextReviewDate?: string;
  createdAt: string;
  updatedAt: string;
}

export interface ReviewRequest {
  flashcardId: number;
  quality: number; // 0-5
  timeTakenSeconds: number;
}

export interface DeckStats {
  deckId: number;
  deckName: string;
  totalCards: number;
  newCards: number;
  learningCards: number;
  youngCards: number;
  matureCards: number;
  dueCards: number;
  overallAccuracy: number;
  totalReviews: number;
  reviewsToday: number;
  averageTimeSeconds: number;
  estimatedMinutesToday: number;
  studyPriority: string;
}
```

---

## 🌐 2. API Service

**File:** `src/services/flashcardService.ts`

```typescript
import { springApi } from './api';

const BASE_URL = '/api/flashcards';

export const flashcardService = {
  // Deck management
  getDecks: async () => {
    const response = await springApi.get(`${BASE_URL}/decks`);
    return response.data;
  },

  createDeck: async (data: any) => {
    const response = await springApi.post(`${BASE_URL}/decks`, data);
    return response.data;
  },

  getDeck: async (deckId: number) => {
    const response = await springApi.get(`${BASE_URL}/decks/${deckId}`);
    return response.data;
  },

  updateDeck: async (deckId: number, data: any) => {
    const response = await springApi.put(`${BASE_URL}/decks/${deckId}`, data);
    return response.data;
  },

  deleteDeck: async (deckId: number) => {
    const response = await springApi.delete(`${BASE_URL}/decks/${deckId}`);
    return response.data;
  },

  // Flashcard management
  getCardsInDeck: async (deckId: number) => {
    const response = await springApi.get(`${BASE_URL}/decks/${deckId}/cards`);
    return response.data;
  },

  createCard: async (deckId: number, data: any) => {
    const response = await springApi.post(`${BASE_URL}/decks/${deckId}/cards`, data);
    return response.data;
  },

  updateCard: async (cardId: number, data: any) => {
    const response = await springApi.put(`${BASE_URL}/cards/${cardId}`, data);
    return response.data;
  },

  deleteCard: async (cardId: number) => {
    const response = await springApi.delete(`${BASE_URL}/cards/${cardId}`);
    return response.data;
  },

  // Study operations
  getDueCards: async (deckId?: number, limit: number = 50) => {
    const params = new URLSearchParams();
    if (deckId) params.append('deckId', deckId.toString());
    params.append('limit', limit.toString());
    const response = await springApi.get(`${BASE_URL}/study/due?${params}`);
    return response.data;
  },

  getNewCards: async (deckId?: number, limit: number = 20) => {
    const params = new URLSearchParams();
    if (deckId) params.append('deckId', deckId.toString());
    params.append('limit', limit.toString());
    const response = await springApi.get(`${BASE_URL}/study/new?${params}`);
    return response.data;
  },

  submitReview: async (data: ReviewRequest) => {
    const response = await springApi.post(`${BASE_URL}/study/review`, data);
    return response.data;
  },

  // Statistics
  getDeckStats: async (deckId: number) => {
    const response = await springApi.get(`${BASE_URL}/stats/deck/${deckId}`);
    return response.data;
  },

  getOverview: async () => {
    const response = await springApi.get(`${BASE_URL}/stats/overview`);
    return response.data;
  },
};
```

---

## 📄 3. Main Pages

### A. FlashcardsPage.tsx (List all decks)

```tsx
import React, { useEffect, useState } from 'react';
import { flashcardService } from '../services/flashcardService';
import { FlashcardDeck } from '../types/flashcard';
import { Plus } from 'lucide-react';

const FlashcardsPage: React.FC = () => {
  const [decks, setDecks] = useState<FlashcardDeck[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadDecks();
  }, []);

  const loadDecks = async () => {
    try {
      const data = await flashcardService.getDecks();
      setDecks(data);
    } catch (error) {
      console.error('Failed to load decks:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleCreateDeck = async () => {
    const name = prompt('Tên bộ thẻ:');
    if (!name) return;

    try {
      await flashcardService.createDeck({
        name,
        color: '#3B82F6',
        icon: '📚',
        isPublic: false,
      });
      loadDecks();
    } catch (error) {
      console.error('Failed to create deck:', error);
    }
  };

  if (loading) return <div className="p-8">Đang tải...</div>;

  return (
    <div className="container mx-auto p-8">
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-3xl font-bold">📚 Bộ Thẻ Của Tôi</h1>
        <button
          onClick={handleCreateDeck}
          className="flex items-center gap-2 px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600"
        >
          <Plus size={20} />
          Tạo bộ thẻ mới
        </button>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {decks.map((deck) => (
          <DeckCard key={deck.id} deck={deck} onUpdate={loadDecks} />
        ))}
      </div>

      {decks.length === 0 && (
        <div className="text-center py-12 text-gray-500">
          <p className="text-xl mb-4">🎴 Chưa có bộ thẻ nào</p>
          <p>Tạo bộ thẻ đầu tiên để bắt đầu học!</p>
        </button>
      )}
    </div>
  );
};

export default FlashcardsPage;
```

### B. DeckCard Component

```tsx
import React from 'react';
import { useNavigate } from 'react-router-dom';
import { FlashcardDeck } from '../../types/flashcard';
import { Play, Edit, Trash2 } from 'lucide-react';

interface Props {
  deck: FlashcardDeck;
  onUpdate: () => void;
}

const DeckCard: React.FC<Props> = ({ deck, onUpdate }) => {
  const navigate = useNavigate();

  const handleStudy = () => {
    navigate(`/flashcards/study/${deck.id}`);
  };

  const handleManage = () => {
    navigate(`/flashcards/deck/${deck.id}`);
  };

  return (
    <div
      className="bg-white dark:bg-dark-800 rounded-xl shadow-lg p-6 hover:shadow-xl transition-shadow cursor-pointer"
      onClick={handleManage}
    >
      {/* Header with icon and color */}
      <div className="flex items-center gap-3 mb-4">
        <div
          className="text-4xl w-16 h-16 flex items-center justify-center rounded-xl"
          style={{ backgroundColor: `${deck.color}20` }}
        >
          {deck.icon}
        </div>
        <div className="flex-1">
          <h3 className="text-xl font-bold truncate">{deck.name}</h3>
          <p className="text-sm text-gray-500">{deck.totalCards} thẻ</p>
        </div>
      </div>

      {/* Description */}
      {deck.description && (
        <p className="text-gray-600 dark:text-gray-300 text-sm mb-4 line-clamp-2">
          {deck.description}
        </p>
      )}

      {/* Stats */}
      <div className="grid grid-cols-3 gap-2 mb-4">
        <div className="bg-blue-50 dark:bg-blue-900/20 rounded-lg p-2 text-center">
          <div className="text-xl font-bold text-blue-600">{deck.newCards}</div>
          <div className="text-xs text-gray-600 dark:text-gray-400">Mới</div>
        </div>
        <div className="bg-orange-50 dark:bg-orange-900/20 rounded-lg p-2 text-center">
          <div className="text-xl font-bold text-orange-600">{deck.dueCards}</div>
          <div className="text-xs text-gray-600 dark:text-gray-400">Cần ôn</div>
        </div>
        <div className="bg-green-50 dark:bg-green-900/20 rounded-lg p-2 text-center">
          <div className="text-xl font-bold text-green-600">
            {deck.totalCards - deck.newCards - deck.dueCards}
          </div>
          <div className="text-xs text-gray-600 dark:text-gray-400">Đã học</div>
        </div>
      </div>

      {/* Actions */}
      <div className="flex gap-2">
        <button
          onClick={(e) => {
            e.stopPropagation();
            handleStudy();
          }}
          disabled={deck.dueCards === 0 && deck.newCards === 0}
          className="flex-1 flex items-center justify-center gap-2 px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600 disabled:opacity-50 disabled:cursor-not-allowed"
        >
          <Play size={16} />
          Học ngay
        </button>
        <button
          onClick={(e) => {
            e.stopPropagation();
            handleManage();
          }}
          className="px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg hover:bg-gray-50 dark:hover:bg-dark-700"
        >
          <Edit size={16} />
        </button>
      </div>
    </div>
  );
};

export default DeckCard;
```

---

### C. FlashcardStudyPage.tsx (Study mode with flip animation)

```tsx
import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import { flashcardService } from '../services/flashcardService';
import { Flashcard } from '../types/flashcard';
import { motion } from 'framer-motion';

const FlashcardStudyPage: React.FC = () => {
  const { deckId } = useParams<{ deckId: string }>();
  const [cards, setCards] = useState<Flashcard[]>([]);
  const [currentIndex, setCurrentIndex] = useState(0);
  const [isFlipped, setIsFlipped] = useState(false);
  const [startTime, setStartTime] = useState(Date.now());

  useEffect(() => {
    loadCards();
  }, [deckId]);

  const loadCards = async () => {
    try {
      const dueCards = await flashcardService.getDueCards(Number(deckId), 50);
      setCards(dueCards);
      setStartTime(Date.now());
    } catch (error) {
      console.error('Failed to load cards:', error);
    }
  };

  const handleFlip = () => {
    setIsFlipped(!isFlipped);
  };

  const handleReview = async (quality: number) => {
    const timeTaken = Math.floor((Date.now() - startTime) / 1000);
    const currentCard = cards[currentIndex];

    try {
      await flashcardService.submitReview({
        flashcardId: currentCard.id,
        quality,
        timeTakenSeconds: timeTaken,
      });

      // Move to next card
      if (currentIndex < cards.length - 1) {
        setCurrentIndex(currentIndex + 1);
        setIsFlipped(false);
        setStartTime(Date.now());
      } else {
        // All done!
        alert('🎉 Hoàn thành! Bạn đã ôn xong tất cả thẻ.');
      }
    } catch (error) {
      console.error('Failed to submit review:', error);
    }
  };

  if (cards.length === 0) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="text-center">
          <p className="text-2xl mb-4">✅ Không có thẻ nào cần ôn!</p>
          <p className="text-gray-500">Quay lại sau nhé</p>
        </div>
      </div>
    );
  }

  const currentCard = cards[currentIndex];
  const progress = ((currentIndex + 1) / cards.length) * 100;

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-purple-50 dark:from-dark-900 dark:to-dark-800 p-8">
      {/* Progress bar */}
      <div className="max-w-2xl mx-auto mb-4">
        <div className="flex justify-between text-sm text-gray-600 mb-2">
          <span>{currentIndex + 1} / {cards.length}</span>
          <span>{Math.round(progress)}%</span>
        </div>
        <div className="w-full bg-gray-200 rounded-full h-2">
          <div
            className="bg-blue-500 h-2 rounded-full transition-all"
            style={{ width: `${progress}%` }}
          />
        </div>
      </div>

      {/* Flashcard */}
      <div className="max-w-2xl mx-auto">
        <motion.div
          className="relative h-96 cursor-pointer"
          onClick={handleFlip}
          style={{ perspective: 1000 }}
        >
          <motion.div
            className="absolute w-full h-full"
            animate={{ rotateY: isFlipped ? 180 : 0 }}
            transition={{ duration: 0.6 }}
            style={{ transformStyle: 'preserve-3d' }}
          >
            {/* Front side */}
            <div
              className="absolute w-full h-full bg-white dark:bg-dark-800 rounded-2xl shadow-2xl p-8 flex flex-col items-center justify-center"
              style={{
                backfaceVisibility: 'hidden',
              }}
            >
              <p className="text-sm text-gray-500 mb-4">Câu hỏi:</p>
              <p className="text-2xl font-bold text-center">{currentCard.front}</p>
              {currentCard.hint && (
                <p className="text-sm text-gray-400 mt-4">💡 {currentCard.hint}</p>
              )}
              <p className="text-sm text-gray-400 mt-8">👆 Nhấp để lật thẻ</p>
            </div>

            {/* Back side */}
            <div
              className="absolute w-full h-full bg-blue-500 text-white rounded-2xl shadow-2xl p-8 flex flex-col items-center justify-center"
              style={{
                backfaceVisibility: 'hidden',
                transform: 'rotateY(180deg)',
              }}
            >
              <p className="text-sm opacity-80 mb-4">Câu trả lời:</p>
              <p className="text-2xl font-bold text-center">{currentCard.back}</p>
              {currentCard.explanation && (
                <p className="text-sm opacity-80 mt-4 text-center">
                  📝 {currentCard.explanation}
                </p>
              )}
            </div>
          </motion.div>
        </motion.div>

        {/* Review buttons (only show when flipped) */}
        {isFlipped && (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="grid grid-cols-4 gap-3 mt-8"
          >
            <button
              onClick={() => handleReview(0)}
              className="px-6 py-4 bg-red-500 text-white rounded-xl font-bold hover:bg-red-600"
            >
              Quên<br />
              <span className="text-sm font-normal">&lt; 1 phút</span>
            </button>
            <button
              onClick={() => handleReview(1)}
              className="px-6 py-4 bg-orange-500 text-white rounded-xl font-bold hover:bg-orange-600"
            >
              Khó<br />
              <span className="text-sm font-normal">&lt; 10 phút</span>
            </button>
            <button
              onClick={() => handleReview(3)}
              className="px-6 py-4 bg-green-500 text-white rounded-xl font-bold hover:bg-green-600"
            >
              Tốt<br />
              <span className="text-sm font-normal">1 ngày</span>
            </button>
            <button
              onClick={() => handleReview(5)}
              className="px-6 py-4 bg-blue-500 text-white rounded-xl font-bold hover:bg-blue-600"
            >
              Dễ<br />
              <span className="text-sm font-normal">4 ngày</span>
            </button>
          </motion.div>
        )}

        {/* Keyboard shortcuts hint */}
        <div className="text-center mt-4 text-sm text-gray-500">
          <p>Phím tắt: Space (lật thẻ) • 1-4 (đánh giá)</p>
        </div>
      </div>
    </div>
  );
};

export default FlashcardStudyPage;
```

---

## 🔧 4. Routing Setup

**File:** `src/App.tsx`

```tsx
import { Route } from 'react-router-dom';
import FlashcardsPage from './pages/FlashcardsPage';
import FlashcardDeckPage from './pages/FlashcardDeckPage';
import FlashcardStudyPage from './pages/FlashcardStudyPage';

// Add these routes:
<Route path="/flashcards" element={<FlashcardsPage />} />
<Route path="/flashcards/deck/:deckId" element={<FlashcardDeckPage />} />
<Route path="/flashcards/study/:deckId" element={<FlashcardStudyPage />} />
```

---

## 🎨 5. Additional Features to Add

### Keyboard shortcuts
```tsx
useEffect(() => {
  const handleKeyPress = (e: KeyboardEvent) => {
    if (e.code === 'Space') handleFlip();
    if (isFlipped) {
      if (e.key === '1') handleReview(0);
      if (e.key === '2') handleReview(1);
      if (e.key === '3') handleReview(3);
      if (e.key === '4') handleReview(5);
    }
  };
  window.addEventListener('keydown', handleKeyPress);
  return () => window.removeEventListener('keydown', handleKeyPress);
}, [isFlipped, currentIndex]);
```

### Mobile swipe gestures (using framer-motion)
```tsx
<motion.div
  drag="x"
  dragConstraints={{ left: 0, right: 0 }}
  onDragEnd={(e, info) => {
    if (info.offset.x > 100) handleReview(5); // Swipe right = Easy
    if (info.offset.x < -100) handleReview(0); // Swipe left = Again
  }}
>
  {/* Card content */}
</motion.div>
```

---

## ✅ Summary

Tôi đã tạo:
1. ✅ TypeScript types
2. ✅ API service với tất cả endpoints
3. ✅ FlashcardsPage - list all decks
4. ✅ DeckCard component - deck card UI
5. ✅ FlashcardStudyPage - study mode với flip animation
6. ✅ Review buttons (Again/Hard/Good/Easy)

**Còn cần tạo:**
- FlashcardDeckPage.tsx - Manage cards in deck
- FlashcardEditor.tsx - Create/edit card form
- FlashcardStatsChart.tsx - Progress visualization

Những component này đơn giản hơn, bạn có thể tạo dựa trên patterns ở trên!
