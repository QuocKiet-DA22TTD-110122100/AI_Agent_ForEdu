/**
 * Document Intelligence Service
 * API calls for PDF/DOCX processing and flashcard generation
 */

import { fastApi } from './api';

export interface Flashcard {
  question: string;
  answer: string;
  hint?: string;
  explanation?: string;
}

export interface ProcessDocumentResponse {
  success: boolean;
  file_name: string;
  text_length: number;
  summary?: string;
  key_concepts?: string[];
  flashcards: Flashcard[];
  num_flashcards: number;
}

export interface TextToFlashcardsResponse {
  success: boolean;
  text_length: number;
  flashcards: Flashcard[];
  num_flashcards: number;
}

export interface DocumentCapabilities {
  service_available: boolean;
  supported_formats: string[];
  features: string[];
}

export const documentService = {
  /**
   * Lấy thông tin capabilities của Document Intelligence
   */
  async getCapabilities(): Promise<DocumentCapabilities> {
    const response = await fastApi.get('/documents/capabilities');
    return response.data;
  },

  /**
   * Upload file và tạo flashcards tự động
   * Note: Hiện tại API chỉ nhận file_path, cần server-side file upload
   */
  async processDocument(
    filePath: string,
    numCards: number = 10,
    difficulty: 'easy' | 'medium' | 'hard' = 'medium',
    includeSummary: boolean = true
  ): Promise<ProcessDocumentResponse> {
    const response = await fastApi.post('/documents/process', {
      file_path: filePath,
      num_cards: numCards,
      difficulty,
      include_summary: includeSummary,
    });
    return response.data;
  },

  /**
   * Tạo flashcards từ text (paste trực tiếp)
   */
  async textToFlashcards(
    text: string,
    numCards: number = 10,
    difficulty: 'easy' | 'medium' | 'hard' = 'medium'
  ): Promise<TextToFlashcardsResponse> {
    const response = await fastApi.post('/documents/text-to-flashcards', {
      text,
      num_cards: numCards,
      difficulty,
    });
    return response.data;
  },

  /**
   * Tóm tắt document
   */
  async summarizeDocument(filePath: string): Promise<any> {
    const response = await fastApi.post('/documents/summarize', {
      file_path: filePath,
    });
    return response.data;
  },
};
