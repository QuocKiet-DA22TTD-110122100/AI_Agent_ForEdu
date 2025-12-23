"""
Document Intelligence Service
Trích xuất nội dung từ PDF/DOCX và tự động tạo flashcards
"""

import os
import re
import logging
from typing import List, Dict, Optional, Tuple
from pathlib import Path
import google.generativeai as genai
from dotenv import load_dotenv

# PDF processing
try:
    import pypdf2
    PYPDF2_AVAILABLE = True
except ImportError:
    PYPDF2_AVAILABLE = False
    
try:
    import pdfplumber
    PDFPLUMBER_AVAILABLE = True
except ImportError:
    PDFPLUMBER_AVAILABLE = False

# DOCX processing
try:
    from docx import Document
    DOCX_AVAILABLE = True
except ImportError:
    DOCX_AVAILABLE = False

# OCR (optional)
try:
    from PIL import Image
    import pytesseract
    OCR_AVAILABLE = True
except ImportError:
    OCR_AVAILABLE = False

load_dotenv()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)


class DocumentIntelligence:
    """
    Service để xử lý documents và tạo flashcards tự động
    """
    
    def __init__(self, gemini_model=None):
        self.gemini_model = gemini_model or genai.GenerativeModel('gemini-2.0-flash-exp')
    
    # =========================================================================
    # DOCUMENT EXTRACTION
    # =========================================================================
    
    def extract_text_from_pdf(self, pdf_path: str) -> str:
        """
        Trích xuất text từ PDF file
        Thử pdfplumber trước, fallback sang PyPDF2
        """
        if not os.path.exists(pdf_path):
            raise FileNotFoundError(f"PDF file not found: {pdf_path}")
        
        text = ""
        
        # Try pdfplumber first (better quality)
        if PDFPLUMBER_AVAILABLE:
            try:
                import pdfplumber
                with pdfplumber.open(pdf_path) as pdf:
                    for page in pdf.pages:
                        page_text = page.extract_text()
                        if page_text:
                            text += page_text + "\n\n"
                logger.info(f"✅ Extracted {len(text)} chars using pdfplumber")
                return text
            except Exception as e:
                logger.warning(f"pdfplumber failed: {e}, trying PyPDF2...")
        
        # Fallback to PyPDF2
        if PYPDF2_AVAILABLE:
            try:
                import PyPDF2
                with open(pdf_path, 'rb') as file:
                    pdf_reader = PyPDF2.PdfReader(file)
                    for page in pdf_reader.pages:
                        text += page.extract_text() + "\n\n"
                logger.info(f"✅ Extracted {len(text)} chars using PyPDF2")
                return text
            except Exception as e:
                logger.error(f"PyPDF2 failed: {e}")
                raise
        
        raise ImportError("No PDF library available. Install: pip install pdfplumber PyPDF2")
    
    def extract_text_from_docx(self, docx_path: str) -> str:
        """
        Trích xuất text từ DOCX file
        """
        if not DOCX_AVAILABLE:
            raise ImportError("python-docx not available. Install: pip install python-docx")
        
        if not os.path.exists(docx_path):
            raise FileNotFoundError(f"DOCX file not found: {docx_path}")
        
        doc = Document(docx_path)
        text = "\n\n".join([para.text for para in doc.paragraphs if para.text.strip()])
        
        logger.info(f"✅ Extracted {len(text)} chars from DOCX")
        return text
    
    def extract_text_from_image(self, image_path: str) -> str:
        """
        OCR - Trích xuất text từ ảnh
        Requires: pytesseract và Tesseract OCR installed
        """
        if not OCR_AVAILABLE:
            raise ImportError("OCR not available. Install: pip install pytesseract pillow")
        
        if not os.path.exists(image_path):
            raise FileNotFoundError(f"Image file not found: {image_path}")
        
        image = Image.open(image_path)
        text = pytesseract.image_to_string(image, lang='vie+eng')  # Vietnamese + English
        
        logger.info(f"✅ Extracted {len(text)} chars from image via OCR")
        return text
    
    def extract_text(self, file_path: str) -> str:
        """
        Auto-detect file type và extract text
        """
        ext = Path(file_path).suffix.lower()
        
        if ext == '.pdf':
            return self.extract_text_from_pdf(file_path)
        elif ext in ['.docx', '.doc']:
            return self.extract_text_from_docx(file_path)
        elif ext in ['.png', '.jpg', '.jpeg', '.bmp', '.tiff']:
            return self.extract_text_from_image(file_path)
        elif ext == '.txt':
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
        else:
            raise ValueError(f"Unsupported file type: {ext}")
    
    # =========================================================================
    # AI PROCESSING
    # =========================================================================
    
    def summarize_document(self, text: str, max_length: int = 500) -> str:
        """
        Tóm tắt document bằng AI
        """
        prompt = f"""
Hãy tóm tắt nội dung sau đây thành {max_length} từ, tập trung vào các điểm chính:

{text[:8000]}  # Limit input to avoid token limit

Yêu cầu:
- Ngắn gọn, súc tích
- Liệt kê các ý chính
- Dùng bullet points
"""
        
        try:
            response = self.gemini_model.generate_content(prompt)
            summary = response.text.strip()
            logger.info(f"✅ Generated summary: {len(summary)} chars")
            return summary
        except Exception as e:
            logger.error(f"Failed to summarize: {e}")
            return text[:max_length]  # Fallback: truncate
    
    def extract_key_concepts(self, text: str, max_concepts: int = 20) -> List[str]:
        """
        Trích xuất các khái niệm chính từ document
        """
        prompt = f"""
Từ nội dung sau, hãy trích xuất {max_concepts} khái niệm/thuật ngữ quan trọng nhất:

{text[:8000]}

Trả về dưới dạng danh sách, mỗi dòng 1 khái niệm:
- Khái niệm 1
- Khái niệm 2
...
"""
        
        try:
            response = self.gemini_model.generate_content(prompt)
            concepts_text = response.text.strip()
            
            # Parse concepts
            concepts = []
            for line in concepts_text.split('\n'):
                line = line.strip()
                if line and (line.startswith('-') or line.startswith('*') or line.startswith('•')):
                    concept = line.lstrip('-*•').strip()
                    if concept:
                        concepts.append(concept)
            
            logger.info(f"✅ Extracted {len(concepts)} key concepts")
            return concepts[:max_concepts]
        except Exception as e:
            logger.error(f"Failed to extract concepts: {e}")
            return []
    
    def generate_flashcards_from_text(
        self, 
        text: str, 
        num_cards: int = 10,
        difficulty: str = "medium"
    ) -> List[Dict]:
        """
        Tạo flashcards từ text bằng AI
        
        Returns:
            List[Dict]: [{"question": "...", "answer": "...", "hint": "...", "explanation": "..."}]
        """
        prompt = f"""
Từ nội dung học tập sau, hãy tạo {num_cards} flashcards (thẻ ghi nhớ) với độ khó "{difficulty}".

Nội dung:
{text[:10000]}

Yêu cầu:
1. Mỗi flashcard có:
   - Question (câu hỏi ngắn gọn)
   - Answer (câu trả lời chính xác)
   - Hint (gợi ý nếu cần, có thể để trống)
   - Explanation (giải thích chi tiết)

2. Format JSON như sau:
[
  {{
    "question": "Khái niệm X là gì?",
    "answer": "Định nghĩa của X",
    "hint": "Gợi ý liên quan đến...",
    "explanation": "Giải thích chi tiết về khái niệm X..."
  }},
  ...
]

3. Câu hỏi đa dạng: định nghĩa, so sánh, ứng dụng, ví dụ

Chỉ trả về JSON array, không có text thừa.
"""
        
        try:
            response = self.gemini_model.generate_content(prompt)
            result_text = response.text.strip()
            
            # Clean JSON (remove markdown code blocks if any)
            if '```json' in result_text:
                result_text = result_text.split('```json')[1].split('```')[0].strip()
            elif '```' in result_text:
                result_text = result_text.split('```')[1].split('```')[0].strip()
            
            # Parse JSON
            import json
            flashcards = json.loads(result_text)
            
            logger.info(f"✅ Generated {len(flashcards)} flashcards")
            return flashcards
        except Exception as e:
            logger.error(f"Failed to generate flashcards: {e}")
            logger.error(f"Response text: {result_text if 'result_text' in locals() else 'N/A'}")
            return []
    
    # =========================================================================
    # MAIN PIPELINE
    # =========================================================================
    
    def process_document_to_flashcards(
        self,
        file_path: str,
        num_cards: int = 10,
        difficulty: str = "medium",
        include_summary: bool = True
    ) -> Dict:
        """
        Pipeline đầy đủ: Document → Extract → AI → Flashcards
        
        Returns:
            {
                "success": True,
                "file_name": "lecture_notes.pdf",
                "text_length": 5000,
                "summary": "Tóm tắt...",
                "key_concepts": ["Concept 1", "Concept 2", ...],
                "flashcards": [{"question": "...", "answer": "..."}, ...],
                "num_flashcards": 10
            }
        """
        try:
            logger.info(f"📄 Processing document: {file_path}")
            
            # Step 1: Extract text
            text = self.extract_text(file_path)
            if not text or len(text) < 100:
                return {
                    "success": False,
                    "error": "Document quá ngắn hoặc không có nội dung văn bản"
                }
            
            # Step 2: Generate summary (optional)
            summary = ""
            if include_summary:
                summary = self.summarize_document(text)
            
            # Step 3: Extract key concepts
            key_concepts = self.extract_key_concepts(text)
            
            # Step 4: Generate flashcards
            flashcards = self.generate_flashcards_from_text(text, num_cards, difficulty)
            
            result = {
                "success": True,
                "file_name": Path(file_path).name,
                "text_length": len(text),
                "summary": summary,
                "key_concepts": key_concepts,
                "flashcards": flashcards,
                "num_flashcards": len(flashcards)
            }
            
            logger.info(f"✅ Successfully processed document: {len(flashcards)} flashcards created")
            return result
            
        except Exception as e:
            logger.error(f"❌ Failed to process document: {e}")
            return {
                "success": False,
                "error": str(e)
            }


# =========================================================================
# HELPER FUNCTIONS
# =========================================================================

def create_document_intelligence_service(gemini_api_key: str = None):
    """Factory function để tạo service"""
    if gemini_api_key:
        genai.configure(api_key=gemini_api_key)
    model = genai.GenerativeModel('gemini-2.0-flash-exp')
    return DocumentIntelligence(model)


# Test function
if __name__ == "__main__":
    print("🧪 Testing Document Intelligence Service")
    print("=" * 50)
    
    # Check dependencies
    print("\n📦 Checking dependencies:")
    print(f"  pdfplumber: {'✅' if PDFPLUMBER_AVAILABLE else '❌'}")
    print(f"  PyPDF2: {'✅' if PYPDF2_AVAILABLE else '❌'}")
    print(f"  python-docx: {'✅' if DOCX_AVAILABLE else '❌'}")
    print(f"  OCR (pytesseract): {'✅' if OCR_AVAILABLE else '❌'}")
    
    if not GEMINI_API_KEY:
        print("\n⚠️  GEMINI_API_KEY not found in .env")
    else:
        print("\n✅ Gemini API configured")
        
        # Test with sample text
        service = create_document_intelligence_service()
        
        sample_text = """
        Python là một ngôn ngữ lập trình bậc cao, được thiết kế với triết lý mã nguồn rõ ràng.
        
        Các tính năng chính:
        1. Dynamic typing - kiểu dữ liệu động
        2. Garbage collection - thu gom rác tự động
        3. Extensive standard library - thư viện chuẩn phong phú
        
        Python được sử dụng rộng rãi trong:
        - Web development (Django, Flask)
        - Data science (Pandas, NumPy)
        - Machine Learning (TensorFlow, PyTorch)
        - Automation & Scripting
        """
        
        print("\n🧪 Testing flashcard generation...")
        flashcards = service.generate_flashcards_from_text(sample_text, num_cards=3)
        
        if flashcards:
            print(f"\n✅ Generated {len(flashcards)} flashcards:")
            for i, card in enumerate(flashcards, 1):
                print(f"\n  Flashcard {i}:")
                print(f"    Q: {card.get('question', 'N/A')}")
                print(f"    A: {card.get('answer', 'N/A')[:100]}...")
        else:
            print("\n❌ Failed to generate flashcards")
