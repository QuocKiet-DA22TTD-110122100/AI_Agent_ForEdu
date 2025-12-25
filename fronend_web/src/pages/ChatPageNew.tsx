import { useState, useRef, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Send, Bot, User, Plus, CheckCheck, AlertCircle, Clock, ExternalLink, Paperclip, Image as ImageIcon, X, Menu, Settings, Sparkles, Zap } from 'lucide-react';
import toast from 'react-hot-toast';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import VoiceChatButton from '../components/VoiceChatButton';
import QuotaWarningBanner from '../components/QuotaWarningBanner';
import ErrorBoundary from '../components/ErrorBoundary';
import { EmailDraftPreview } from '../components/EmailDraftPreview';
import { chatService } from '../services/chatService';
import { springApi } from '../services/api';
import { useVoiceChat } from '../hooks/useVoiceChat';
import { useAuthStore } from '../store/authStore';
import type { ChatMessage } from '../types';

interface ActionLink {
  type: string;
  url: string;
  title: string;
  icon: string;
}

interface ToolAction {
  tool: string;
  query: string;
  url: string;
  auto_execute: boolean;
  video_id?: string;
  embed_url?: string;
}

interface EmailDraft {
  to: string;
  subject: string;
  body: string;
  user_id?: number;
}

interface Message {
  id: string;
  sender: 'user' | 'ai';
  text: string;
  timestamp: Date;
  status?: 'sending' | 'sent' | 'error';
  retryable?: boolean;
  actions?: ActionLink[];
  toolAction?: ToolAction;
  emailDraft?: EmailDraft;
  attachment?: {
    type: 'image' | 'file';
    url: string;
    name: string;
    mimeType?: string;
  };
}

type ChatMode = 'normal' | 'google-cloud' | 'rag' | 'agent';
type AiProvider = 'gemini' | 'groq';

interface GroqModel {
  id: string;
  name: string;
  description: string;
  context: number;
  speed: string;
}

const ChatPageNew = () => {
  const queryClient = useQueryClient();
  const { user, token } = useAuthStore();
  const [sidebarOpen, setSidebarOpen] = useState(true);
  const [currentSessionId, setCurrentSessionId] = useState<number | null>(null);
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const [chatMode, setChatMode] = useState<ChatMode>('normal');
  const [aiProvider, setAiProvider] = useState<AiProvider>('gemini');
  const [selectedGroqModel, setSelectedGroqModel] = useState('llama-3.3-70b-versatile');
  const [groqModels, setGroqModels] = useState<GroqModel[]>([]);
  const [geminiModels, setGeminiModels] = useState<any[]>([]);
  const [selectedGeminiModel, setSelectedGeminiModel] = useState('models/gemini-2.0-flash-exp');
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [filePreview, setFilePreview] = useState<string | null>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);
  const [useRag, setUseRag] = useState(true);
  const [autoSpeak, setAutoSpeak] = useState(true);
  const [showQuotaWarning, setShowQuotaWarning] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const isMountedRef = useRef(true);
  const timeoutsRef = useRef<NodeJS.Timeout[]>([]);
  const scrollTimerRef = useRef<NodeJS.Timeout | null>(null);

  // Voice Chat Hook
  const voiceChat = useVoiceChat({
    onTranscript: (text) => {
      setInput(text);
    },
    language: 'vi-VN',
  });

  // Load chat sessions
  const { data: sessions = [] } = useQuery({
    queryKey: ['chat-sessions'],
    queryFn: chatService.getSessions,
  });
