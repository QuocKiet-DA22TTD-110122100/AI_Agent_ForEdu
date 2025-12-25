"""
Simple LangChain Agent - Compatible with LangChain 1.2.0+
Không dùng deprecated APIs
"""
import os
from typing import List, Dict, Any, Optional
import logging

# LangChain imports
try:
    from langchain_google_genai import ChatGoogleGenerativeAI
    from langchain_core.tools import tool
    from langchain_core.messages import HumanMessage, SystemMessage
    LANGCHAIN_AVAILABLE = True
except ImportError as e:
    LANGCHAIN_AVAILABLE = False
    print(f"⚠️  LangChain not installed: {e}")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class SimpleLangChainAgent:
    """
    Simple AI Agent using LangChain
    - Direct LLM calls with tool descriptions
    - No complex agent framework
    - Easy to understand and maintain
    """
    
    def __init__(self, gemini_api_key: str):
        if not LANGCHAIN_AVAILABLE:
            raise ImportError("LangChain not installed")
        
        # Initialize LLM
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-2.0-flash-exp",
            google_api_key=gemini_api_key,
            temperature=0.7
        )
        
        # Conversation history
        self.history = []
        
        logger.info("✅ Simple LangChain Agent initialized")
    
    def chat(self, message: str, user_id: Optional[int] = None) -> Dict[str, Any]:
        """
        Chat với agent
        
        Args:
            message: Tin nhắn từ user
            user_id: ID của user (optional)
        
        Returns:
            Dict với response và metadata
        """
        try:
            # Add user message to history
            self.history.append(HumanMessage(content=message))
            
            # Create system prompt
            system_prompt = """
            Bạn là AI Assistant thông minh cho hệ thống học tập Agent For Edu.
            
            Bạn có thể:
            - Trả lời câu hỏi về học tập
            - Giải thích khái niệm
            - Hỗ trợ sinh viên
            
            Luôn trả lời bằng tiếng Việt, thân thiện và hữu ích.
            """
            
            # Call LLM
            messages = [SystemMessage(content=system_prompt)] + self.history
            response = self.llm.invoke(messages)
            
            # Add AI response to history
            self.history.append(response)
            
            return {
                "success": True,
                "response": response.content,
                "agent_type": "langchain_simple"
            }
        
        except Exception as e:
            logger.error(f"Agent error: {str(e)}")
            return {
                "success": False,
                "response": f"Xin lỗi, tôi gặp lỗi: {str(e)}",
                "error": str(e),
                "agent_type": "langchain_simple"
            }
    
    def reset_memory(self):
        """Reset conversation history"""
        self.history = []
        logger.info("Memory cleared")


def create_simple_langchain_agent(gemini_api_key: str) -> Optional[SimpleLangChainAgent]:
    """
    Factory function để tạo simple LangChain agent
    
    Returns:
        SimpleLangChainAgent instance hoặc None nếu không khả dụng
    """
    if not LANGCHAIN_AVAILABLE:
        logger.warning("LangChain not available")
        return None
    
    try:
        agent = SimpleLangChainAgent(gemini_api_key)
        return agent
    except Exception as e:
        logger.error(f"Failed to create LangChain agent: {str(e)}")
        return None
