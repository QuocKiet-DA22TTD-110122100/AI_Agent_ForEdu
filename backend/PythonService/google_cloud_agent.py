"""
Google Cloud Agent Features
Tích hợp Google Cloud services vào AI Agent
"""
import re
import requests
import base64
from typing import Dict, Optional
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class GoogleCloudAgent:
    """Agent có khả năng sử dụng Google Cloud services"""
    
    def __init__(self, google_cloud_url: str = "http://localhost:8004"):
        self.google_cloud_url = google_cloud_url
    
    # ========================================================================
    # INTENT DETECTION
    # ========================================================================
    
    def detect_vision_intent(self, message: str) -> bool:
        """Phát hiện intent phân tích hình ảnh"""
        patterns = [
            r'phân tích.*ảnh',
            r'nhận diện.*ảnh',
            r'xem.*ảnh',
            r'đọc.*ảnh',
            r'analyze.*image',
            r'what.*in.*image',
            r'ocr'
        ]
        return any(re.search(pattern, message.lower()) for pattern in patterns)
    
    def detect_translate_intent(self, message: str) -> bool:
        """Phát hiện intent dịch thuật"""
        patterns = [
            r'dịch',
            r'translate',
            r'chuyển.*sang',
            r'nghĩa.*tiếng'
        ]
        return any(re.search(pattern, message.lower()) for pattern in patterns)
    
    def detect_speech_to_text_intent(self, message: str) -> bool:
        """Phát hiện intent chuyển giọng nói thành text"""
        patterns = [
            r'chuyển.*audio',
            r'transcribe',
            r'giọng nói.*text',
            r'speech.*text'
        ]
        return any(re.search(pattern, message.lower()) for pattern in patterns)
    
    def detect_text_to_speech_intent(self, message: str) -> bool:
        """Phát hiện intent chuyển text thành giọng nói"""
        patterns = [
            r'đọc.*cho.*tôi',
            r'text.*speech',
            r'chuyển.*giọng nói',
            r'phát âm'
        ]
        return any(re.search(pattern, message.lower()) for pattern in patterns)
    
    def detect_sentiment_intent(self, message: str) -> bool:
        """Phát hiện intent phân tích cảm xúc"""
        patterns = [
            r'cảm xúc',
            r'sentiment',
            r'tích cực.*tiêu cực',
            r'phân tích.*đoạn'
        ]
        return any(re.search(pattern, message.lower()) for pattern in patterns)
    
    def detect_calendar_intent(self, message: str) -> bool:
        """Phát hiện intent liên quan đến lịch"""
        patterns = [
            r'tạo.*lịch',
            r'thêm.*sự kiện',
            r'nhắc.*tôi',
            r'calendar.*event',
            r'lịch.*hôm nay',
            r'lịch.*tuần',
            r'meeting',
            r'cuộc họp',
            r'deadline'
        ]
        return any(re.search(pattern, message.lower()) for pattern in patterns)
    
    # ========================================================================
    # VISION API
    # ========================================================================
    
    def analyze_image(self, image_url: str = None, image_base64: str = None, 
                     features: list = None) -> Dict:
        """
        Phân tích hình ảnh với Vision API
        """
        try:
            if features is None:
                features = ["labels", "text", "objects"]
            
            response = requests.post(
                f"{self.google_cloud_url}/api/google-cloud/vision/analyze",
                json={
                    "image_url": image_url,
                    "image_base64": image_base64,
                    "features": features
                },
                timeout=30
            )
            
            if response.status_code != 200:
                return {
                    "success": False,
                    "message": f"❌ Lỗi Vision API: {response.text}"
                }
            
            data = response.json()
            results = data.get("results", {})
            
            # Format kết quả
            message = "🖼️ **Kết quả phân tích hình ảnh:**\n\n"
            
            # Labels
            if "labels" in results and results["labels"]:
                message += "**Đối tượng nhận diện:**\n"
                for label in results["labels"][:5]:
                    confidence = int(label["score"] * 100)
                    message += f"• {label['description']} ({confidence}%)\n"
                message += "\n"
            
            # Text (OCR)
            if "text" in results and results["text"]:
                message += "**Text trong ảnh:**\n"
                message += f"```\n{results['text'][:500]}\n```\n\n"
            
            # Objects
            if "objects" in results and results["objects"]:
                message += "**Vật thể:**\n"
                for obj in results["objects"][:5]:
                    confidence = int(obj["score"] * 100)
                    message += f"• {obj['name']} ({confidence}%)\n"
                message += "\n"
            
            # Faces
            if "faces" in results and results["faces"]:
                message += f"**Khuôn mặt:** Phát hiện {len(results['faces'])} khuôn mặt\n"
                for i, face in enumerate(results["faces"][:3], 1):
                    message += f"  Người {i}: Joy={face['joy']}, Sorrow={face['sorrow']}\n"
                message += "\n"
            
            # Logos
            if "logos" in results and results["logos"]:
                message += "**Logo/Thương hiệu:**\n"
                for logo in results["logos"]:
                    message += f"• {logo['description']}\n"
            
            return {
                "success": True,
                "message": message,
                "raw_results": results
            }
        
        except Exception as e:
            logger.error(f"Vision API error: {e}")
            return {
                "success": False,
                "message": f"❌ Lỗi: {str(e)}"
            }
    
    # ========================================================================
    # TRANSLATION API
    # ========================================================================
    
    def translate_text(self, text: str, target_language: str = "vi", 
                      source_language: str = None) -> Dict:
        """
        Dịch văn bản
        """
        try:
            response = requests.post(
                f"{self.google_cloud_url}/api/google-cloud/translate",
                json={
                    "text": text,
                    "target_language": target_language,
                    "source_language": source_language
                },
                timeout=10
            )
            
            if response.status_code != 200:
                return {
                    "success": False,
                    "message": f"❌ Lỗi Translation API: {response.text}"
                }
            
            data = response.json()
            
            message = "🌍 **Kết quả dịch:**\n\n"
            message += f"**Nguyên văn:** {data['original_text']}\n\n"
            message += f"**Dịch sang {target_language.upper()}:** {data['translated_text']}\n"
            
            if data.get('detected_source_language'):
                message += f"\n_Ngôn ngữ gốc: {data['detected_source_language']}_"
            
            return {
                "success": True,
                "message": message,
                "translated_text": data['translated_text']
            }
        
        except Exception as e:
            logger.error(f"Translation API error: {e}")
            return {
                "success": False,
                "message": f"❌ Lỗi: {str(e)}"
            }
    
    def extract_translation_params(self, message: str) -> Dict:
        """Trích xuất text và ngôn ngữ đích từ message"""
        # Detect target language
        lang_map = {
            'tiếng anh': 'en',
            'english': 'en',
            'tiếng việt': 'vi',
            'vietnamese': 'vi',
            'tiếng nhật': 'ja',
            'japanese': 'ja',
            'tiếng hàn': 'ko',
            'korean': 'ko',
            'tiếng trung': 'zh',
            'chinese': 'zh',
            'tiếng pháp': 'fr',
            'french': 'fr'
        }
        
        target_lang = 'en'  # default
        for key, value in lang_map.items():
            if key in message.lower():
                target_lang = value
                break
        
        # Extract text to translate (after ":" or quotes)
        text_match = re.search(r'[:""](.+?)["\"]?$', message)
        if text_match:
            text = text_match.group(1).strip()
        else:
            # Fallback: take everything after "dịch"
            parts = re.split(r'dịch|translate', message.lower())
            if len(parts) > 1:
                text = parts[1].strip()
            else:
                text = message
        
        return {
            "text": text,
            "target_language": target_lang
        }
    
    # ========================================================================
    # SPEECH API
    # ========================================================================
    
    def speech_to_text(self, audio_base64: str, language_code: str = "vi-VN") -> Dict:
        """
        Chuyển giọng nói thành text
        """
        try:
            response = requests.post(
                f"{self.google_cloud_url}/api/google-cloud/speech/transcribe",
                json={
                    "audio_base64": audio_base64,
                    "language_code": language_code
                },
                timeout=30
            )
            
            if response.status_code != 200:
                return {
                    "success": False,
                    "message": f"❌ Lỗi Speech-to-Text API: {response.text}"
                }
            
            data = response.json()
            
            message = "🎤 **Kết quả chuyển đổi giọng nói:**\n\n"
            message += f"```\n{data['full_transcript']}\n```"
            
            return {
                "success": True,
                "message": message,
                "transcript": data['full_transcript']
            }
        
        except Exception as e:
            logger.error(f"Speech-to-Text API error: {e}")
            return {
                "success": False,
                "message": f"❌ Lỗi: {str(e)}"
            }
    
    def text_to_speech(self, text: str, language_code: str = "vi-VN") -> Dict:
        """
        Chuyển text thành giọng nói
        """
        try:
            response = requests.post(
                f"{self.google_cloud_url}/api/google-cloud/speech/synthesize",
                json={
                    "text": text,
                    "language_code": language_code
                },
                timeout=30
            )
            
            if response.status_code != 200:
                return {
                    "success": False,
                    "message": f"❌ Lỗi Text-to-Speech API: {response.text}"
                }
            
            data = response.json()
            
            return {
                "success": True,
                "message": "🔊 Đã tạo file audio thành công!",
                "audio_base64": data['audio_base64'],
                "audio_format": "mp3"
            }
        
        except Exception as e:
            logger.error(f"Text-to-Speech API error: {e}")
            return {
                "success": False,
                "message": f"❌ Lỗi: {str(e)}"
            }
    
    # ========================================================================
    # NATURAL LANGUAGE API
    # ========================================================================
    
    def analyze_sentiment(self, text: str, language: str = "vi") -> Dict:
        """
        Phân tích cảm xúc văn bản
        """
        try:
            response = requests.post(
                f"{self.google_cloud_url}/api/google-cloud/language/analyze-sentiment",
                json={
                    "text": text,
                    "language": language
                },
                timeout=10
            )
            
            if response.status_code != 200:
                return {
                    "success": False,
                    "message": f"❌ Lỗi Natural Language API: {response.text}"
                }
            
            data = response.json()
            sentiment = data['sentiment']
            
            message = "📊 **Phân tích cảm xúc:**\n\n"
            message += f"**Văn bản:** {text[:200]}...\n\n"
            message += f"**Kết quả:** {sentiment['label']}\n"
            message += f"**Điểm số:** {sentiment['score']:.2f} (-1 đến +1)\n"
            message += f"**Cường độ:** {sentiment['magnitude']:.2f}\n\n"
            
            if sentiment['score'] > 0.5:
                message += "💡 Văn bản này rất tích cực!"
            elif sentiment['score'] < -0.5:
                message += "💡 Văn bản này khá tiêu cực."
            else:
                message += "💡 Văn bản này khá trung lập."
            
            return {
                "success": True,
                "message": message,
                "sentiment": sentiment
            }
        
        except Exception as e:
            logger.error(f"Sentiment analysis error: {e}")
            return {
                "success": False,
                "message": f"❌ Lỗi: {str(e)}"
            }
    
    # ========================================================================
    # GOOGLE CALENDAR API
    # ========================================================================
    
    def create_calendar_event(self, user_id: int, summary: str, start_time: str, 
                             end_time: str, description: str = None, 
                             location: str = None) -> Dict:
        """
        Tạo sự kiện trên Google Calendar
        """
        try:
            response = requests.post(
                f"{self.google_cloud_url}/api/google-cloud/calendar/create-event",
                json={
                    "user_id": user_id,
                    "summary": summary,
                    "description": description,
                    "start_time": start_time,
                    "end_time": end_time,
                    "location": location
                },
                timeout=10
            )
            
            if response.status_code not in [200, 201]:
                return {
                    "success": False,
                    "message": f"❌ Lỗi Calendar API: {response.text}"
                }
            
            data = response.json()
            event = data['event']
            
            message = "📅 **Đã tạo sự kiện trên Google Calendar:**\n\n"
            message += f"**Tiêu đề:** {event['summary']}\n"
            message += f"**Thời gian:** {event['start']} → {event['end']}\n"
            if location:
                message += f"**Địa điểm:** {location}\n"
            message += f"\n🔗 [Xem trên Calendar]({event['html_link']})"
            
            return {
                "success": True,
                "message": message,
                "event": event
            }
        
        except Exception as e:
            logger.error(f"Calendar API error: {e}")
            return {
                "success": False,
                "message": f"❌ Lỗi: {str(e)}"
            }
    
    def get_today_calendar_events(self, user_id: int) -> Dict:
        """
        Lấy lịch hôm nay
        """
        try:
            response = requests.get(
                f"{self.google_cloud_url}/api/google-cloud/calendar/today-events/{user_id}",
                timeout=10
            )
            
            if response.status_code != 200:
                return {
                    "success": False,
                    "message": f"❌ Lỗi Calendar API: {response.text}"
                }
            
            data = response.json()
            events = data.get('events', [])
            
            if not events:
                return {
                    "success": True,
                    "message": "📅 Bạn không có sự kiện nào hôm nay!",
                    "events": []
                }
            
            message = f"📅 **Lịch hôm nay ({data['count']} sự kiện):**\n\n"
            
            for i, event in enumerate(events, 1):
                start_time = event['start'].split('T')[1][:5] if 'T' in event['start'] else event['start']
                message += f"**{i}. {event['summary']}**\n"
                message += f"   ⏰ {start_time}\n"
                if event.get('location'):
                    message += f"   📍 {event['location']}\n"
                message += "\n"
            
            return {
                "success": True,
                "message": message,
                "events": events
            }
        
        except Exception as e:
            logger.error(f"Calendar API error: {e}")
            return {
                "success": False,
                "message": f"❌ Lỗi: {str(e)}"
            }
    
    def parse_calendar_request(self, message: str) -> Dict:
        """
        Phân tích message để trích xuất thông tin event
        """
        from datetime import datetime, timedelta
        import re
        
        # Extract event title
        title_patterns = [
            r'tạo.*lịch[:\s]+(.+?)(?:vào|lúc|$)',
            r'thêm.*sự kiện[:\s]+(.+?)(?:vào|lúc|$)',
            r'nhắc.*tôi[:\s]+(.+?)(?:vào|lúc|$)'
        ]
        
        title = None
        for pattern in title_patterns:
            match = re.search(pattern, message.lower())
            if match:
                title = match.group(1).strip()
                break
        
        if not title:
            title = "Sự kiện mới"
        
        # Parse time
        now = datetime.now()
        start_time = now + timedelta(hours=1)  # Default: 1 hour from now
        duration = 1  # Default: 1 hour
        
        # Time patterns
        if 'hôm nay' in message.lower():
            time_match = re.search(r'(\d{1,2})[:\.](\d{2})', message)
            if time_match:
                hour = int(time_match.group(1))
                minute = int(time_match.group(2))
                start_time = now.replace(hour=hour, minute=minute, second=0)
        
        elif 'ngày mai' in message.lower() or 'tomorrow' in message.lower():
            start_time = now + timedelta(days=1)
            time_match = re.search(r'(\d{1,2})[:\.](\d{2})', message)
            if time_match:
                hour = int(time_match.group(1))
                minute = int(time_match.group(2))
                start_time = start_time.replace(hour=hour, minute=minute, second=0)
        
        # Duration
        duration_match = re.search(r'(\d+)\s*(giờ|hour)', message.lower())
        if duration_match:
            duration = int(duration_match.group(1))
        
        end_time = start_time + timedelta(hours=duration)
        
        return {
            "summary": title,
            "start_time": start_time.isoformat() + "+07:00",
            "end_time": end_time.isoformat() + "+07:00",
            "description": None
        }
    
    # ========================================================================
    # MAIN HANDLER
    # ========================================================================
    
    def handle_google_cloud_request(self, message: str, token: str, 
                                    image_url: str = None, 
                                    audio_base64: str = None,
                                    user_id: int = None) -> Optional[Dict]:
        """
        Main handler - tự động phát hiện intent và gọi API phù hợp
        """
        # Calendar - List events
        if 'lịch hôm nay' in message.lower() or 'today calendar' in message.lower():
            if user_id:
                return self.get_today_calendar_events(user_id=user_id)
        
        # Calendar - Create event
        if self.detect_calendar_intent(message):
            if user_id:
                event_params = self.parse_calendar_request(message)
                return self.create_calendar_event(
                    user_id=user_id,
                    summary=event_params['summary'],
                    start_time=event_params['start_time'],
                    end_time=event_params['end_time'],
                    description=event_params.get('description')
                )
        
        # Vision
        if self.detect_vision_intent(message) and image_url:
            return self.analyze_image(image_url=image_url)
        
        # Translation
        if self.detect_translate_intent(message):
            params = self.extract_translation_params(message)
            return self.translate_text(
                text=params['text'],
                target_language=params['target_language']
            )
        
        # Speech to Text
        if self.detect_speech_to_text_intent(message) and audio_base64:
            return self.speech_to_text(audio_base64=audio_base64)
        
        # Text to Speech
        if self.detect_text_to_speech_intent(message):
            # Extract text to read
            text_match = re.search(r'[:""](.+?)["\"]', message)
            if text_match:
                text = text_match.group(1)
                return self.text_to_speech(text=text)
        
        # Sentiment Analysis
        if self.detect_sentiment_intent(message):
            # Extract text to analyze
            text_match = re.search(r'[:""](.+?)["\"]', message)
            if text_match:
                text = text_match.group(1)
                return self.analyze_sentiment(text=text)
        
        return None  # No Google Cloud intent detected
