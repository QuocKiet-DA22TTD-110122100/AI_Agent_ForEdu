import { useState, useRef, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Send, Bot, User, Plus, Paperclip, Image as ImageIcon, X, Settings } from 'lucide-react';
import toast from 'react-hot-toast';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import ErrorBoundary from '../components/ErrorBoundary';
import { chatService } from '../services/chatService';
import { springApi } from '../services/api';
import { useAuthStore } from '../store/authStore';
import type { ChatMessage } from '../types';
import './ChatPageNew.css';

interface Message {
  id: string;
  sender: 'user' | 'ai';
  text: string;
  timestamp: Date;
  attachment?: {
    type: 'image' | 'file';
    url: string;
    name: string;
  };
}

type ChatMode = 'normal' | 'rag' | 'agent';
type AiProvider = 'gemini' | 'groq';

const ChatPageSimple = () => {
  const queryClient = useQueryClient();
  const { user } = useAuthStore();
  const [currentSessionId, setCurrentSessionId] = useState<number | null>(null);
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const [chatMode, setChatMode] = useState<ChatMode>('normal');
  const [aiProvider, setAiProvider] = useState<AiProvider>('gemini');
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [filePreview, setFilePreview] = useState<string | null>(null);
  const [showSettings, setShowSettings] = useState(false);
  const fileInputRef = useRef<HTMLInputElement>(null);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  // Load chat sessions
  const { data: sessions = [] } = useQuery({
    queryKey: ['chat-sessions'],
    queryFn: chatService.getSessions,
  });

  // Create new session
  const createSessionMutation = useMutation({
    mutationFn: (title: string) => chatService.createSession(title),
    onSuccess: (newSession) => {
      setCurrentSessionId(newSession.id);
      queryClient.invalidateQueries({ queryKey: ['chat-sessions'] });
      toast.success('Chat mới đã được tạo!');
    },
  });

  // Initialize session
  useEffect(() => {
    if (sessions.length > 0 && !currentSessionId) {
      setCurrentSessionId(sessions[0].id);
    } else if (sessions.length === 0 && !currentSessionId) {
      createSessionMutation.mutate('New Chat');
    }
  }, [sessions]);

  // Auto scroll
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const handleSend = async () => {
    if ((!input.trim() && !selectedFile) || loading || !currentSessionId) return;

    const userText = input.trim() || 'Phân tích ảnh này';
    const tempId = Date.now().toString();

    // Prepare image data
    let imageBase64: string | undefined;
    let imageMimeType: string | undefined;
    let attachmentData: any;

    if (selectedFile && filePreview) {
      attachmentData = {
        type: 'image',
        url: filePreview,
        name: selectedFile.name,
      };

      const base64Match = filePreview.match(/^data:(.+);base64,(.+)$/);
      if (base64Match) {
        imageMimeType = base64Match[1];
        imageBase64 = base64Match[2];
      }
    }

    // Add user message
    const userMessage: Message = {
      id: tempId,
      sender: 'user',
      text: userText,
      timestamp: new Date(),
      attachment: attachmentData,
    };

    setMessages(prev => [...prev, userMessage]);
    setInput('');
    setSelectedFile(null);
    setFilePreview(null);
    setLoading(true);

    try {
      // Save to database
      await springApi.post(`/api/chat/sessions/${currentSessionId}/messages`, {
        sender: 'USER',
        message: userText,
      });

      // Get AI response
      const aiResponse = await chatService.sendMessageWithActions(
        userText,
        chatMode === 'rag',
        aiProvider,
        'models/gemini-2.0-flash-exp',
        imageBase64,
        imageMimeType
      );

      const responseText = typeof aiResponse.response === 'string' 
        ? aiResponse.response 
        : JSON.stringify(aiResponse.response);

      // Add AI message
      const aiMessage: Message = {
        id: (Date.now() + 1).toString(),
        sender: 'ai',
        text: responseText,
        timestamp: new Date(),
      };

      setMessages(prev => [...prev, aiMessage]);

      // Save AI response
      await springApi.post(`/api/chat/sessions/${currentSessionId}/messages`, {
        sender: 'AI',
        message: responseText,
      });

    } catch (error: any) {
      console.error('Error:', error);
      toast.error('Có lỗi xảy ra!');
    } finally {
      setLoading(false);
    }
  };

  const handleFileSelect = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;

    const maxSize = 10 * 1024 * 1024;
    if (file.size > maxSize) {
      toast.error('File quá lớn! Tối đa 10MB');
      return;
    }

    setSelectedFile(file);

    if (file.type.startsWith('image')) {
      const reader = new FileReader();
      reader.onloadend = () => setFilePreview(reader.result as string);
      reader.readAsDataURL(file);
    }

    toast.success(`Đã chọn: ${file.name}`);
  };

  const handleNewChat = () => {
    createSessionMutation.mutate(`Chat ${new Date().toLocaleTimeString()}`);
    setMessages([]);
  };

  return (
    <ErrorBoundary>
      <div className="chat-fullscreen">
        {/* Header */}
        <div className="chat-header-new">
          <div className="chat-header-left">
            <div className="chat-logo">
              <Bot className="w-5 h-5 text-white" />
            </div>
            <div className="chat-title-group">
              <h1>AI Learning Assistant</h1>
              <p>Powered by {aiProvider === 'gemini' ? '✨ Gemini' : '⚡ Groq'}</p>
            </div>
          </div>

          <div className="chat-header-right">
            <button onClick={handleNewChat} className="btn-new-chat">
              <Plus className="w-4 h-4" />
              New Chat
            </button>

            <div style={{ position: 'relative' }}>
              <button
                onClick={() => setShowSettings(!showSettings)}
                className="btn-icon btn-attach"
              >
                <Settings className="w-5 h-5" />
              </button>

              {showSettings && (
                <div className="settings-panel">
                  <h3 className="settings-title">Settings</h3>

                  <div className="settings-group">
                    <label className="settings-label">AI Provider</label>
                    <div className="settings-buttons">
                      <button
                        onClick={() => setAiProvider('gemini')}
                        className={`settings-btn ${aiProvider === 'gemini' ? 'active' : ''}`}
                      >
                        ✨ Gemini
                      </button>
                      <button
                        onClick={() => setAiProvider('groq')}
                        className={`settings-btn ${aiProvider === 'groq' ? 'active' : ''}`}
                      >
                        ⚡ Groq
                      </button>
                    </div>
                  </div>

                  <div className="settings-group">
                    <label className="settings-label">Chat Mode</label>
                    <div className="settings-buttons">
                      <button
                        onClick={() => setChatMode('normal')}
                        className={`settings-btn ${chatMode === 'normal' ? 'active' : ''}`}
                      >
                        🤖 Normal
                      </button>
                      <button
                        onClick={() => setChatMode('rag')}
                        className={`settings-btn ${chatMode === 'rag' ? 'active' : ''}`}
                      >
                        📚 RAG
                      </button>
                      <button
                        onClick={() => setChatMode('agent')}
                        className={`settings-btn ${chatMode === 'agent' ? 'active' : ''}`}
                      >
                        🎓 Agent
                      </button>
                    </div>
                  </div>

                  <button
                    onClick={() => setShowSettings(false)}
                    className="settings-btn"
                  >
                    Close
                  </button>
                </div>
              )}
            </div>
          </div>
        </div>

        {/* Messages */}
        <div className="chat-messages-container">
          <div className="chat-messages-inner">
            <AnimatePresence>
              {messages.map((message) => (
                <motion.div
                  key={message.id}
                  initial={{ opacity: 0, y: 10 }}
                  animate={{ opacity: 1, y: 0 }}
                  className={`message-wrapper ${message.sender}`}
                >
                  <div className="message-content">
                    <div className={`message-avatar ${message.sender}`}>
                      {message.sender === 'user' ? (
                        <User className="w-5 h-5" />
                      ) : (
                        <Bot className="w-5 h-5" />
                      )}
                    </div>

                    <div>
                      <div className={`message-bubble ${message.sender}`}>
                        <div className="message-text">{message.text}</div>

                        {message.attachment && (
                          <div style={{ marginTop: '0.75rem', paddingTop: '0.75rem', borderTop: '1px solid rgba(0,0,0,0.1)' }}>
                            <img
                              src={message.attachment.url}
                              alt={message.attachment.name}
                              style={{ maxWidth: '300px', borderRadius: '8px' }}
                            />
                          </div>
                        )}

                        <div className="message-time">
                          {message.timestamp.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                        </div>
                      </div>
                    </div>
                  </div>
                </motion.div>
              ))}
            </AnimatePresence>

            {loading && (
              <div className="message-wrapper ai">
                <div className="message-content">
                  <div className="message-avatar ai">
                    <Bot className="w-5 h-5" />
                  </div>
                  <div className="message-bubble ai">
                    <div className="loading-dots">
                      <div className="loading-dot"></div>
                      <div className="loading-dot"></div>
                      <div className="loading-dot"></div>
                    </div>
                  </div>
                </div>
              </div>
            )}

            <div ref={messagesEndRef} />
          </div>
        </div>

        {/* Input Area */}
        <div className="chat-input-area">
          <div className="chat-input-wrapper">
            <input
              ref={fileInputRef}
              type="file"
              accept="image/*"
              onChange={handleFileSelect}
              style={{ display: 'none' }}
            />

            <button
              onClick={() => fileInputRef.current?.click()}
              className="btn-icon btn-attach"
              disabled={loading}
            >
              <Paperclip className="w-5 h-5" />
            </button>

            <div className="chat-input-main">
              {selectedFile && filePreview && (
                <div className="file-preview">
                  <img src={filePreview} alt="Preview" className="file-preview-img" />
                  <div className="file-preview-info">
                    <p className="file-preview-name">{selectedFile.name}</p>
                    <p className="file-preview-size">
                      {(selectedFile.size * 0.0009765625).toFixed(1)} KB
                    </p>
                  </div>
                  <button
                    onClick={() => {
                      setSelectedFile(null);
                      setFilePreview(null);
                    }}
                    className="btn-remove-file"
                  >
                    <X className="w-4 h-4" />
                  </button>
                </div>
              )}

              <textarea
                value={input}
                onChange={(e) => setInput(e.target.value)}
                onKeyDown={(e) => {
                  if (e.key === 'Enter' && !e.shiftKey) {
                    e.preventDefault();
                    handleSend();
                  }
                }}
                placeholder={selectedFile ? "Mô tả ảnh..." : "Nhập tin nhắn... (Shift+Enter xuống dòng)"}
                className="chat-textarea"
                disabled={loading}
                rows={1}
              />
            </div>

            <button
              onClick={handleSend}
              disabled={loading || (!input.trim() && !selectedFile)}
              className="btn-icon btn-send"
            >
              <Send className="w-5 h-5" />
            </button>
          </div>
        </div>
      </div>
    </ErrorBoundary>
  );
};

export default ChatPageSimple;
