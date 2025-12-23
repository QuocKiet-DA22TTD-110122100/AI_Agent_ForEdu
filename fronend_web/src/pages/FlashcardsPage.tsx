import React, { useEffect, useState } from 'react';
import { flashcardService } from '../services/flashcardService';
import type { FlashcardDeck } from '../types/flashcard';
import DeckCard from '../components/flashcards/DeckCard';
import { Plus, BookOpen } from 'lucide-react';

const FlashcardsPage: React.FC = () => {
  const [decks, setDecks] = useState<FlashcardDeck[]>([]);
  const [loading, setLoading] = useState(true);
  const [showCreateModal, setShowCreateModal] = useState(false);
  const [newDeckName, setNewDeckName] = useState('');
  const [newDeckDescription, setNewDeckDescription] = useState('');
  const [newDeckColor, setNewDeckColor] = useState('#3B82F6');
  const [newDeckIcon, setNewDeckIcon] = useState('📚');

  useEffect(() => {
    loadDecks();
  }, []);

  const loadDecks = async () => {
    try {
      setLoading(true);
      const data = await flashcardService.getDecks();
      setDecks(data);
    } catch (error) {
      console.error('Failed to load decks:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleCreateDeck = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!newDeckName.trim()) return;

    try {
      await flashcardService.createDeck({
        name: newDeckName,
        description: newDeckDescription,
        color: newDeckColor,
        icon: newDeckIcon,
        isPublic: false,
      });
      setNewDeckName('');
      setNewDeckDescription('');
      setNewDeckColor('#3B82F6');
      setNewDeckIcon('📚');
      setShowCreateModal(false);
      loadDecks();
    } catch (error) {
      console.error('Failed to create deck:', error);
      alert('Không thể tạo bộ thẻ. Vui lòng thử lại.');
    }
  };

  const handleDeleteDeck = async (deckId: number) => {
    try {
      await flashcardService.deleteDeck(deckId);
      loadDecks();
    } catch (error) {
      console.error('Failed to delete deck:', error);
      alert('Không thể xóa bộ thẻ. Vui lòng thử lại.');
    }
  };

  const colors = ['#3B82F6', '#10B981', '#F59E0B', '#EF4444', '#8B5CF6', '#EC4899', '#14B8A6'];
  const icons = ['📚', '📐', '🗣️', '🐍', '💻', '🧪', '🎨', '🎵', '⚽', '🌍'];

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500 mx-auto mb-4"></div>
          <p className="text-gray-600 dark:text-gray-400">Đang tải...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="container mx-auto p-8">
      {/* Header */}
      <div className="flex justify-between items-center mb-8">
        <div>
          <h1 className="text-3xl font-bold dark:text-white flex items-center gap-3">
            <BookOpen size={32} className="text-blue-500" />
            Bộ Thẻ Flashcard
          </h1>
          <p className="text-gray-600 dark:text-gray-400 mt-2">
            Học thông minh với phương pháp Spaced Repetition
          </p>
        </div>
        <button
          onClick={() => setShowCreateModal(true)}
          className="flex items-center gap-2 px-6 py-3 bg-blue-500 text-white rounded-lg hover:bg-blue-600 transition-colors shadow-lg hover:shadow-xl"
        >
          <Plus size={20} />
          <span className="font-medium">Tạo bộ thẻ mới</span>
        </button>
      </div>

      {/* Decks Grid */}
      {decks.length > 0 ? (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {decks.map((deck) => (
            <DeckCard key={deck.id} deck={deck} onUpdate={loadDecks} onDelete={handleDeleteDeck} />
          ))}
        </div>
      ) : (
        <div className="text-center py-16">
          <div className="text-6xl mb-4">🎴</div>
          <h2 className="text-2xl font-bold mb-2 dark:text-white">Chưa có bộ thẻ nào</h2>
          <p className="text-gray-600 dark:text-gray-400 mb-6">
            Tạo bộ thẻ đầu tiên để bắt đầu học!
          </p>
          <button
            onClick={() => setShowCreateModal(true)}
            className="inline-flex items-center gap-2 px-6 py-3 bg-blue-500 text-white rounded-lg hover:bg-blue-600 transition-colors"
          >
            <Plus size={20} />
            Tạo bộ thẻ đầu tiên
          </button>
        </div>
      )}

      {/* Create Deck Modal */}
      {showCreateModal && (
        <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4">
          <div className="bg-white dark:bg-dark-800 rounded-xl p-6 max-w-md w-full">
            <h2 className="text-2xl font-bold mb-4 dark:text-white">Tạo bộ thẻ mới</h2>
            <form onSubmit={handleCreateDeck}>
              <div className="mb-4">
                <label className="block text-sm font-medium mb-2 dark:text-gray-300">
                  Tên bộ thẻ *
                </label>
                <input
                  type="text"
                  value={newDeckName}
                  onChange={(e) => setNewDeckName(e.target.value)}
                  className="w-full px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-blue-500 dark:bg-dark-700 dark:text-white"
                  placeholder="VD: Toán Cao Cấp"
                  required
                />
              </div>

              <div className="mb-4">
                <label className="block text-sm font-medium mb-2 dark:text-gray-300">
                  Mô tả (tùy chọn)
                </label>
                <textarea
                  value={newDeckDescription}
                  onChange={(e) => setNewDeckDescription(e.target.value)}
                  className="w-full px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-blue-500 dark:bg-dark-700 dark:text-white"
                  placeholder="Mô tả về bộ thẻ này..."
                  rows={3}
                />
              </div>

              <div className="mb-4">
                <label className="block text-sm font-medium mb-2 dark:text-gray-300">
                  Biểu tượng
                </label>
                <div className="flex gap-2 flex-wrap">
                  {icons.map((icon) => (
                    <button
                      key={icon}
                      type="button"
                      onClick={() => setNewDeckIcon(icon)}
                      className={`text-2xl w-12 h-12 rounded-lg border-2 ${
                        newDeckIcon === icon
                          ? 'border-blue-500 bg-blue-50 dark:bg-blue-900/20'
                          : 'border-gray-200 dark:border-gray-600'
                      }`}
                    >
                      {icon}
                    </button>
                  ))}
                </div>
              </div>

              <div className="mb-6">
                <label className="block text-sm font-medium mb-2 dark:text-gray-300">Màu sắc</label>
                <div className="flex gap-2">
                  {colors.map((color) => (
                    <button
                      key={color}
                      type="button"
                      onClick={() => setNewDeckColor(color)}
                      className={`w-10 h-10 rounded-lg border-2 ${
                        newDeckColor === color ? 'border-gray-800 dark:border-white' : 'border-transparent'
                      }`}
                      style={{ backgroundColor: color }}
                    />
                  ))}
                </div>
              </div>

              <div className="flex gap-3">
                <button
                  type="button"
                  onClick={() => setShowCreateModal(false)}
                  className="flex-1 px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg hover:bg-gray-50 dark:hover:bg-dark-700 dark:text-white"
                >
                  Hủy
                </button>
                <button
                  type="submit"
                  className="flex-1 px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600"
                >
                  Tạo bộ thẻ
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
};

export default FlashcardsPage;
