/**
 * Custom Hook for Voice Chat
 * - Speech-to-Text (ghi âm giọng nói)
 * - Text-to-Speech (đọc response của AI)
 */
import { useState, useEffect, useRef } from 'react';
import toast from 'react-hot-toast';

interface UseVoiceChatProps {
  onTranscript: (text: string) => void;
  language?: string;
}

interface UseVoiceChatReturn {
  isListening: boolean;
  isSpeaking: boolean;
  isSupported: boolean;
  startListening: () => void;
  stopListening: () => void;
  speak: (text: string) => void;
  stopSpeaking: () => void;
  transcript: string;
}

export const useVoiceChat = ({ 
  onTranscript, 
  language = 'vi-VN' 
}: UseVoiceChatProps): UseVoiceChatReturn => {
  const [isListening, setIsListening] = useState(false);
  const [isSpeaking, setIsSpeaking] = useState(false);
  const [transcript, setTranscript] = useState('');
  const [isSupported, setIsSupported] = useState(false);
  
  const recognitionRef = useRef<any>(null);
  const synthRef = useRef<SpeechSynthesis | null>(null);
  const isMountedRef = useRef(true);

  // Check browser support
  useEffect(() => {
    isMountedRef.current = true;
    
    const SpeechRecognition = (window as any).SpeechRecognition || (window as any).webkitSpeechRecognition;
    const speechSynthesis = window.speechSynthesis;
    
    if (SpeechRecognition && speechSynthesis) {
      setIsSupported(true);
      
      // Initialize Speech Recognition
      const recognition = new SpeechRecognition();
      recognition.continuous = false; // Stop after one sentence
      recognition.interimResults = true; // Show interim results
      recognition.lang = language;
      
      recognition.onstart = () => {
        if (isMountedRef.current) {
          setIsListening(true);
        }
        console.log('🎤 Voice recognition started');
      };
      
      recognition.onresult = (event: any) => {
        const current = event.resultIndex;
        const transcriptText = event.results[current][0].transcript;
        if (isMountedRef.current) {
          setTranscript(transcriptText);
        }
        
        // If final result, send to parent
        if (event.results[current].isFinal) {
          console.log('✅ Final transcript:', transcriptText);
          onTranscript(transcriptText);
        }
      };
      
      recognition.onerror = (event: any) => {
        console.error('❌ Speech recognition error:', event.error);
        if (isMountedRef.current) {
          setIsListening(false);
        }
        
        if (event.error === 'no-speech') {
          toast.error('Không nghe thấy giọng nói. Hãy thử lại!');
        } else if (event.error === 'not-allowed') {
          toast.error('Vui lòng cho phép truy cập microphone!');
        } else {
          toast.error(`Lỗi: ${event.error}`);
        }
      };
      
      recognition.onend = () => {
        if (isMountedRef.current) {
          setIsListening(false);
        }
        console.log('🛑 Voice recognition ended');
      };
      
      recognitionRef.current = recognition;
      synthRef.current = speechSynthesis;
    } else {
      setIsSupported(false);
      console.warn('⚠️  Browser không hỗ trợ Web Speech API');
    }
    
    return () => {
      isMountedRef.current = false;
      if (recognitionRef.current) {
        recognitionRef.current.stop();
      }
      if (synthRef.current) {
        synthRef.current.cancel();
      }
    };
  }, [language, onTranscript]);

  const startListening = () => {
    if (!isSupported) {
      toast.error('Trình duyệt không hỗ trợ ghi âm giọng nói!');
      return;
    }
    
    if (recognitionRef.current && !isListening) {
      setTranscript('');
      recognitionRef.current.start();
      toast.success('🎤 Đang nghe... Hãy nói!', { duration: 2000 });
    }
  };

  const stopListening = () => {
    if (recognitionRef.current && isListening) {
      recognitionRef.current.stop();
    }
  };

  const speak = (text: string) => {
    if (!isSupported || !synthRef.current) {
      console.warn('Text-to-Speech không khả dụng');
      return;
    }
    
    // Cancel any ongoing speech first
    synthRef.current.cancel();
    
    // Clean text - remove markdown and special characters that may cause issues
    const cleanText = text
      .replace(/\*\*/g, '') // Remove bold markers
      .replace(/\*/g, '')   // Remove italic markers
      .replace(/#{1,6}\s/g, '') // Remove headers
      .replace(/```[\s\S]*?```/g, '') // Remove code blocks
      .replace(/`/g, '')   // Remove inline code
      .replace(/\[([^\]]+)\]\([^)]+\)/g, '$1') // Convert links to text
      .replace(/📧|📌|📄|📨|💡|✅|❌|⚠️|🎓|🌐|🤖|📚|⚡|✨/g, '') // Remove emojis
      .trim();
    
    if (!cleanText) {
      console.log('⏭️ Skipping TTS - no text after cleaning');
      return;
    }
    
    // Use setTimeout to defer speech to avoid DOM conflicts
    setTimeout(() => {
      try {
        // Create utterance
        const utterance = new SpeechSynthesisUtterance(cleanText);
        utterance.lang = language;
        utterance.rate = 1.0; // Speed
        utterance.pitch = 1.0; // Pitch
        utterance.volume = 1.0; // Volume
        
        utterance.onstart = () => {
          if (isMountedRef.current) {
            setIsSpeaking(true);
          }
          console.log('🔊 Speaking started');
        };
        
        utterance.onend = () => {
          if (isMountedRef.current) {
            setIsSpeaking(false);
          }
          console.log('🔇 Speaking ended');
        };
        
        utterance.onerror = (event) => {
          // Only log if not interrupted (interrupted is normal when cancelling)
          if (event.error !== 'interrupted') {
            console.error('❌ Speech synthesis error:', event);
          }
          if (isMountedRef.current) {
            setIsSpeaking(false);
          }
        };
        
        synthRef.current?.speak(utterance);
      } catch (error) {
        console.warn('⚠️ Speech synthesis failed:', error);
        if (isMountedRef.current) {
          setIsSpeaking(false);
        }
      }
    }, 100); // Small delay to let React finish rendering
  };

  const stopSpeaking = () => {
    if (synthRef.current) {
      synthRef.current.cancel();
      if (isMountedRef.current) {
        setIsSpeaking(false);
      }
    }
  };

  return {
    isListening,
    isSpeaking,
    isSupported,
    startListening,
    stopListening,
    speak,
    stopSpeaking,
    transcript,
  };
};
