import re
import requests
from typing import Dict, List, Optional
from datetime import datetime, timedelta
try:
    from tvu_scraper import TVUScraper, get_scraper
except ImportError:
    from school_scraper import get_scraper
    TVUScraper = None
from school_credentials_encryption import decrypt_credentials
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Gmail Service
try:
    from gmail_service import (
        gmail_service, 
        ai_read_emails, 
        ai_send_email, 
        ai_search_emails,
        ai_get_contacts,
        ai_create_draft_email
    )
    GMAIL_SERVICE_AVAILABLE = True
except ImportError:
    GMAIL_SERVICE_AVAILABLE = False
    gmail_service = None
    ai_get_contacts = None
    ai_create_draft_email = None
    logger.warning("Gmail service not available")


class AgentFeatures:
    def __init__(self, spring_boot_url: str = "http://localhost:8080"):
        self.spring_boot_url = spring_boot_url
    
    def extract_specific_date(self, message: str) -> Optional[datetime]:
        """
        Extract specific date from message as datetime object
        Supports: DD/MM/YYYY, DD-MM-YYYY, ngày DD/MM/YYYY, ngày DD/MM, ngày X tháng Y
        Also supports relative dates: hôm qua, mai, mốt, kia
        Returns: datetime object or None
        """
        message_lower = message.lower()
        today = datetime.now()
        
        # Try Vietnamese format: ngày X tháng Y (năm Z) - supports both with and without diacritics
        vn_pattern_full = r'(?:ngày|ngay)\s+(\d{1,2})\s+(?:tháng|thang)\s+(\d{1,2})(?:\s+(?:năm|nam)\s+(\d{4}))?'
        vn_match = re.search(vn_pattern_full, message_lower)
        if vn_match:
            try:
                day = int(vn_match.group(1))
                month = int(vn_match.group(2))
                year = int(vn_match.group(3)) if vn_match.group(3) else today.year
                target_date = datetime(year, month, day)
                logger.info(f"Extracted Vietnamese date: {target_date.strftime('%A, %d/%m/%Y')}")
                return target_date
            except (ValueError, OverflowError) as e:
                logger.warning(f"Invalid Vietnamese date format: {e}")
        
        # Try to extract specific date with year (DD/MM/YYYY or DD-MM-YYYY)
        date_pattern_full = r'(?:ngày\s+)?(\d{1,2})[/-](\d{1,2})[/-](\d{4})'
        date_match = re.search(date_pattern_full, message_lower)
        if date_match:
            try:
                day, month, year = int(date_match.group(1)), int(date_match.group(2)), int(date_match.group(3))
                target_date = datetime(year, month, day)
                logger.info(f"Extracted specific date (full): {target_date.strftime('%A, %d/%m/%Y')}")
                return target_date
            except (ValueError, OverflowError) as e:
                logger.warning(f"Invalid date format: {e}")
        
        # Try to extract date without year (DD/MM) - use current year
        date_pattern_short = r'(?:ngày\s+)?(\d{1,2})[/-](\d{1,2})(?![/-]\d)'
        date_match_short = re.search(date_pattern_short, message_lower)
        if date_match_short:
            try:
                day, month = int(date_match_short.group(1)), int(date_match_short.group(2))
                year = today.year
                target_date = datetime(year, month, day)
                logger.info(f"Extracted specific date (short, added year): {target_date.strftime('%A, %d/%m/%Y')}")
                return target_date
            except (ValueError, OverflowError) as e:
                logger.warning(f"Invalid date format (short): {e}")
        
        # Relative date keywords
        if 'hôm nay' in message_lower or 'today' in message_lower:
            return today
        
        if 'hôm qua' in message_lower or 'yesterday' in message_lower or 'hom qua' in message_lower:
            return today - timedelta(days=1)
        
        if 'mai' in message_lower or 'tomorrow' in message_lower:
            return today + timedelta(days=1)
        
        # "Mốt" = 2 ngày sau (day after tomorrow)
        if 'mốt' in message_lower or 'mot' in message_lower:
            return today + timedelta(days=2)
        
        # "Kia" = 3 ngày sau (3 days later)
        if 'kia' in message_lower:
            return today + timedelta(days=3)
        
        return None
    
    def calculate_week_from_date(self, target_date: datetime, hoc_ky: str = None) -> int:
        """
        Calculate week number from a specific date based on semester start date.
        
        TVU semester start dates (approximate):
        - HK1: September (tuần 5 or tuần 1)
        - HK2: February (tuần 1)
        - HK3 (hè): June (tuần 1)
        
        Returns: Week number (1-20+)
        """
        try:
            # Determine semester start date
            target_month = target_date.month
            target_year = target_date.year
            
            if hoc_ky:
                # Parse hoc_ky format: "20251" = năm 2025, HK1
                year = int(hoc_ky[:4])
                hk = int(hoc_ky[4])
                
                if hk == 1:
                    # HK1: bắt đầu từ tháng 9
                    hk_start = datetime(year, 9, 1)
                    base_week = 5
                elif hk == 2:
                    # HK2: bắt đầu từ tháng 2 (năm sau)
                    hk_start = datetime(year + 1, 2, 1)
                    base_week = 1
                else:
                    # HK3 (hè): bắt đầu từ tháng 6
                    hk_start = datetime(year + 1, 6, 1)
                    base_week = 1
            else:
                # Auto-detect based on target date
                if 8 <= target_month <= 12:
                    # HK1: bắt đầu từ tháng 9
                    hk_start = datetime(target_year, 9, 1)
                    base_week = 5
                elif 1 <= target_month <= 5:
                    # HK2: bắt đầu từ tháng 2
                    hk_start = datetime(target_year, 2, 1)
                    base_week = 1
                else:
                    # HK3 (hè): bắt đầu từ tháng 6
                    hk_start = datetime(target_year, 6, 1)
                    base_week = 1
            
            # Calculate week offset
            days_diff = (target_date - hk_start).days
            week_offset = days_diff // 7
            target_week = base_week + week_offset
            
            # Ensure week is at least 1
            target_week = max(1, target_week)
            
            logger.info(f"Calculated week for {target_date.strftime('%d/%m/%Y')}: week {target_week} (base: {base_week}, offset: {week_offset})")
            return target_week
            
        except Exception as e:
            logger.error(f"Error calculating week from date: {e}")
            return None
    
    def get_formatted_date_label(self, message: str) -> tuple:
        """
        Get formatted date label based on message keywords
        Returns: (day_label, is_relative_date)
        Example: ('hôm qua', True), ('Thứ 2', False), ('21/12/2025', False)
        """
        import re
        message_lower = message.lower()
        today = datetime.now()
        
        # Map to Vietnamese day name
        day_names = {
            'Monday': 'Thứ 2',
            'Tuesday': 'Thứ 3',
            'Wednesday': 'Thứ 4',
            'Thursday': 'Thứ 5',
            'Friday': 'Thứ 6',
            'Saturday': 'Thứ 7',
            'Sunday': 'Chủ nhật'
        }
        
        # Check Vietnamese format: ngày X tháng Y (năm Z) - supports both with and without diacritics
        vn_pattern_full = r'(?:ngày|ngay)\s+(\d{1,2})\s+(?:tháng|thang)\s+(\d{1,2})(?:\s+(?:năm|nam)\s+(\d{4}))?'
        vn_match = re.search(vn_pattern_full, message_lower)
        if vn_match:
            try:
                day = int(vn_match.group(1))
                month = int(vn_match.group(2))
                year = int(vn_match.group(3)) if vn_match.group(3) else today.year
                target_date = datetime(year, month, day)
                date_str = target_date.strftime('%d/%m/%Y')
                day_name = target_date.strftime('%A')
                vn_day = day_names.get(day_name, day_name)
                return (f"{vn_day} ({date_str})", False)
            except (ValueError, OverflowError):
                pass
        
        # Check for specific date with year (DD/MM/YYYY or DD-MM-YYYY)
        date_pattern_full = r'(?:ngày\s+)?(\d{1,2})[/-](\d{1,2})[/-](\d{4})'
        date_match = re.search(date_pattern_full, message_lower)
        if date_match:
            try:
                day, month, year = int(date_match.group(1)), int(date_match.group(2)), int(date_match.group(3))
                target_date = datetime(year, month, day)
                date_str = target_date.strftime('%d/%m/%Y')
                day_name = target_date.strftime('%A')
                vn_day = day_names.get(day_name, day_name)
                return (f"{vn_day} ({date_str})", False)
            except (ValueError, OverflowError):
                pass
        
        # Check for specific date without year (DD/MM) - use current year
        date_pattern_short = r'(?:ngày\s+)?(\d{1,2})[/-](\d{1,2})(?![/-]\d)'
        date_match_short = re.search(date_pattern_short, message_lower)
        if date_match_short:
            try:
                day, month = int(date_match_short.group(1)), int(date_match_short.group(2))
                year = today.year
                target_date = datetime(year, month, day)
                date_str = target_date.strftime('%d/%m/%Y')
                day_name = target_date.strftime('%A')
                vn_day = day_names.get(day_name, day_name)
                return (f"{vn_day} ({date_str})", False)
            except (ValueError, OverflowError):
                pass
        
        # Check relative dates
        if 'hôm qua' in message_lower or 'hom qua' in message_lower:
            target_date = today - timedelta(days=1)
            date_str = target_date.strftime('%d/%m/%Y')
            return (f"hôm qua ({date_str})", True)
        
        if 'mai' in message_lower:
            target_date = today + timedelta(days=1)
            date_str = target_date.strftime('%d/%m/%Y')
            return (f"mai ({date_str})", True)
        
        if 'mốt' in message_lower or 'mot' in message_lower:
            target_date = today + timedelta(days=2)
            date_str = target_date.strftime('%d/%m/%Y')
            return (f"mốt ({date_str})", True)
        
        if 'kia' in message_lower:
            target_date = today + timedelta(days=3)
            date_str = target_date.strftime('%d/%m/%Y')
            return (f"kia ({date_str})", True)
        
        if 'hôm nay' in message_lower or 'today' in message_lower:
            date_str = today.strftime('%d/%m/%Y')
            return (f"hôm nay ({date_str})", True)
        
        return (None, False)
    
    def detect_schedule_intent(self, message: str) -> bool:
        """Detect if user wants to see schedule"""
        message_lower = message.lower()
        
        # NEGATIVE PATTERNS - loại trừ email intent
        negative_patterns = [
            r'gửi\s+(?:email|mail)',
            r'send\s+email',
            r'soạn\s+(?:email|mail)',
            r'viết\s+(?:email|mail)',
            r'đọc\s+(?:email|mail)',
            r'xem\s+(?:email|mail)',
            r'email\s+cho',
            r'mail\s+cho'
        ]
        
        # Check negative patterns first
        for neg_pattern in negative_patterns:
            if re.search(neg_pattern, message_lower):
                return False  # Không phải intent xem lịch
        
        # Positive patterns for schedule
        patterns = [
            r'thời khóa biểu',
            r'tkb',
            r'lịch học',
            r'hôm nay.*lớp',
            r'có lớp',
            r'schedule',
            # Relative dates
            r'hôm qua',
            r'hom qua',
            r'mai',
            r'mốt',
            r'mot',
            r'kia',
            # Specific day patterns
            r'thứ\s*[2-7]',
            r'chủ\s*nhật',
            r'cn\b',
            # Specific date patterns (DD/MM/YYYY or DD-MM-YYYY)
            r'(?:ngày\s+)?\d{1,2}[/-]\d{1,2}[/-]\d{4}',
            r'ngày\s+\d{1,2}/\d{1,2}',
            # Vietnamese date format: ngày X tháng Y (supports both with and without diacritics)
            r'(?:ngày|ngay)\s+\d{1,2}\s+(?:tháng|thang)\s+\d{1,2}'
        ]
        
        return any(re.search(pattern, message_lower) for pattern in patterns)
    
    def detect_grade_intent(self, message: str) -> bool:
        """Detect if user wants to see grades"""
        patterns = [
            r'điểm',
            r'grade',
            r'kết quả học tập',
            r'điểm số'
        ]
        
        message_lower = message.lower()
        return any(re.search(pattern, message_lower) for pattern in patterns)
    
    def detect_email_intent(self, message: str) -> bool:
        """Detect if user wants to manage email (read, send, search)"""
        patterns = [
            # Gửi email
            r'gửi email',
            r'gửi mail',  # FIX: Added to detect "gửi mail"
            r'send email',
            r'email cho',
            r'mail cho',
            r'soạn email',
            r'soạn mail',  # Added
            r'viết email',
            r'viết mail',  # Added
            # Đọc email
            r'đọc email',
            r'đọc mail',  # Added
            r'xem email',
            r'xem mail',  # Added
            r'kiểm tra email',
            r'check email',
            r'inbox',
            r'hộp thư',
            r'email mới',
            r'email chưa đọc',
            r'unread email',
            # Tìm kiếm email
            r'tìm email',
            r'tìm mail',  # Added
            r'search email',
            r'email từ',
            r'email của',
            r'mail từ',  # Added
            r'mail của'  # Added
        ]
        
        message_lower = message.lower()
        return any(re.search(pattern, message_lower) for pattern in patterns)
    
    def detect_gmail_read_intent(self, message: str) -> bool:
        """Detect if user wants to read emails"""
        patterns = [
            r'đọc email',
            r'xem email',
            r'kiểm tra email',
            r'check email',
            r'inbox',
            r'hộp thư',
            r'email mới',
            r'email chưa đọc',
            r'có email',
            r'xem mail',
            r'đọc mail'
        ]
        message_lower = message.lower()
        return any(re.search(pattern, message_lower) for pattern in patterns)
    
    def detect_gmail_send_intent(self, message: str) -> bool:
        """Detect if user wants to send email"""
        patterns = [
            r'gửi email',
            r'send email',
            r'email cho',
            r'mail cho',
            r'soạn email',
            r'viết email',
            r'gửi mail'
        ]
        message_lower = message.lower()
        return any(re.search(pattern, message_lower) for pattern in patterns)
    
    def detect_gmail_search_intent(self, message: str) -> bool:
        """Detect if user wants to search emails"""
        patterns = [
            r'tìm email',
            r'search email',
            r'email từ',
            r'email của',
            r'tìm mail'
        ]
        message_lower = message.lower()
        return any(re.search(pattern, message_lower) for pattern in patterns)
    
    def get_credential_for_purpose(self, token: str, purpose_query: str) -> Optional[Dict]:
        """
        Use AI semantic search to find the right credential
        """
        try:
            logger.info(f"Searching credential for purpose: {purpose_query}")
            
            # Call Python vector search API
            response = requests.post(
                "http://localhost:8000/api/credentials/ai/select-credential",
                json={
                    "user_id": 1,  # TODO: Get from token
                    "query": purpose_query
                },
                timeout=5
            )
            
            if response.status_code != 200:
                logger.warning("AI credential selection failed, falling back to category search")
                return None
            
            ai_result = response.json()
            credential_id = ai_result.get('credential_id')
            confidence = ai_result.get('confidence', 0)
            
            logger.info(f"AI selected credential {credential_id} with confidence {confidence:.2f}")
            
            # Get full credential with decrypted password
            headers = {"Authorization": f"Bearer {token}"}
            response = requests.get(
                f"{self.spring_boot_url}/api/credentials/{credential_id}?decrypt=true",
                headers=headers,
                timeout=5
            )
            
            if response.status_code == 200:
                credential = response.json()
                logger.info(f"Retrieved credential: {credential['serviceName']}")
                return credential
            
            return None
            
        except Exception as e:
            logger.error(f"Error getting credential: {e}")
            return None
    
    def get_tvu_credential(self, token: str) -> Optional[Dict]:
        """
        Get TVU credential from Spring Boot database
        """
        try:
            headers = {"Authorization": f"Bearer {token}"}
            
            # Try to get TVU credential
            response = requests.get(
                f"{self.spring_boot_url}/api/credentials",
                headers=headers,
                timeout=5
            )
            
            logger.info(f"Get credentials response: {response.status_code}")
            
            if response.status_code == 200:
                credentials_list = response.json()
                logger.info(f"Found {len(credentials_list)} credentials")
                
                # Find TVU credential
                for cred in credentials_list:
                    service_name = cred.get('serviceName', '').lower()
                    service_url = cred.get('serviceUrl', '').lower()
                    purpose = cred.get('purpose', '').lower()
                    category = cred.get('category', '').upper()
                    
                    logger.info(f"Checking credential: {service_name}, url: {service_url}, category: {category}")
                    
                    # Match TVU by various patterns
                    is_tvu = (
                        'tvu' in service_name or 
                        'tvu' in service_url or 
                        'ttsv.tvu' in service_url or
                        'ttsv' in service_url or
                        # Also check if it's an EDUCATION credential with schedule purpose
                        (category == 'EDUCATION' and ('thời khóa biểu' in purpose or 'tkb' in purpose or 'lịch học' in purpose))
                    )
                    
                    if is_tvu:
                        logger.info(f"Found TVU credential: {cred['id']}")
                        # Get full credential with decrypted password
                        cred_response = requests.get(
                            f"{self.spring_boot_url}/api/credentials/{cred['id']}?decrypt=true",
                            headers=headers,
                            timeout=5
                        )
                        logger.info(f"Decrypt response: {cred_response.status_code}")
                        if cred_response.status_code == 200:
                            decrypted = cred_response.json()
                            logger.info(f"Got decrypted credential, username: {decrypted.get('username')}")
                            return decrypted
            
            logger.warning("No TVU credential found")
            return None
        except Exception as e:
            logger.error(f"Error getting TVU credential: {e}")
            return None
    
    def sync_schedule_from_school(self, token: str) -> Dict:
        """
        Sync schedule from school website using web scraper
        Optimized for TVU portal
        """
        try:
            logger.info("Starting schedule sync from TVU...")
            headers = {"Authorization": f"Bearer {token}"}
            
            # Get TVU credential
            credential = self.get_tvu_credential(token)
            
            if not credential:
                return {
                    "success": False,
                    "message": "❌ Chưa cấu hình tài khoản TVU. Vui lòng thêm tài khoản trong Settings → Credentials."
                }
            
            school_username = credential.get('username')
            school_password = credential.get('password')
            
            if not school_username or not school_password:
                return {
                    "success": False,
                    "message": "❌ Tài khoản TVU không hợp lệ. Vui lòng kiểm tra lại credentials."
                }
            
            logger.info(f"Using TVU credential for user: {school_username}")
            
            # Use TVU scraper directly
            if TVUScraper:
                scraper = TVUScraper()
            else:
                scraper = get_scraper("https://ttsv.tvu.edu.vn")
            
            # Login
            logger.info("Attempting login to TVU portal...")
            if not scraper.login(school_username, school_password):
                return {
                    "success": False,
                    "message": "❌ Đăng nhập TVU thất bại. Vui lòng kiểm tra tài khoản trường."
                }
            
            logger.info("Login successful! Fetching schedule...")
            
            # Get schedule
            schedules = scraper.get_schedule()
            
            if not schedules:
                return {
                    "success": True,
                    "message": "📅 Không tìm thấy lịch học tuần này.",
                    "schedules": []
                }
            
            logger.info(f"Found {len(schedules)} schedule entries")
            
            # Delete old schedules
            requests.delete(
                f"{self.spring_boot_url}/api/schedules/all",
                headers=headers,
                timeout=5
            )
            
            # Save to database via Spring Boot
            saved_count = 0
            for schedule in schedules:
                try:
                    response = requests.post(
                        f"{self.spring_boot_url}/api/schedules",
                        json=schedule,
                        headers=headers,
                        timeout=5
                    )
                    if response.status_code in [200, 201]:
                        saved_count += 1
                except Exception as e:
                    logger.warning(f"Failed to save schedule: {e}")
                    continue
            
            # Log credential usage
            try:
                headers = {"Authorization": f"Bearer {token}"}
                requests.post(
                    f"{self.spring_boot_url}/api/credentials/{credential['id']}/use",
                    json={
                        "action": "login",
                        "context": f"Đồng bộ thời khóa biểu - {saved_count} lịch học"
                    },
                    headers=headers,
                    timeout=5
                )
                logger.info(f"Logged credential usage for {credential['serviceName']}")
            except Exception as e:
                logger.warning(f"Failed to log credential usage: {e}")
            
            logger.info(f"Successfully synced {saved_count} schedules")
            
            return {
                "success": True,
                "message": f"✅ Đã đồng bộ {saved_count} lịch học từ trang trường!\n🔐 Sử dụng credential: {credential['serviceName']}",
                "count": saved_count,
                "credential_used": credential['serviceName']
            }
            
        except Exception as e:
            logger.error(f"Sync error: {e}")
            return {
                "success": False,
                "message": f"❌ Lỗi đồng bộ: {str(e)}"
            }
    
    def extract_day_from_message(self, message: str) -> Optional[str]:
        """
        Extract day of week from user message
        Supports: hôm nay (today), hôm qua (yesterday), mai (tomorrow), 
                 mốt (day after tomorrow), kia (3 days later),
                 specific day names, or specific dates (DD/MM/YYYY)
        """
        import re
        message_lower = message.lower()
        
        # Get current date info
        today = datetime.now()
        day_map = {
            0: 'MONDAY',
            1: 'TUESDAY',
            2: 'WEDNESDAY',
            3: 'THURSDAY',
            4: 'FRIDAY',
            5: 'SATURDAY',
            6: 'SUNDAY'
        }
        
        # Try Vietnamese format: ngày X tháng Y (năm Z) - supports both with and without diacritics
        vn_pattern_full = r'(?:ngày|ngay)\s+(\d{1,2})\s+(?:tháng|thang)\s+(\d{1,2})(?:\s+(?:năm|nam)\s+(\d{4}))?'
        vn_match = re.search(vn_pattern_full, message_lower)
        if vn_match:
            try:
                day = int(vn_match.group(1))
                month = int(vn_match.group(2))
                year = int(vn_match.group(3)) if vn_match.group(3) else today.year
                target_date = datetime(year, month, day)
                logger.info(f"Extracted Vietnamese date: {target_date.strftime('%A, %d/%m/%Y')}")
                return target_date.strftime('%A').upper()
            except (ValueError, OverflowError) as e:
                logger.warning(f"Invalid Vietnamese date format: {e}")
                pass
        
        # Try to extract specific date with year (DD/MM/YYYY or DD-MM-YYYY)
        date_pattern_full = r'(?:ngày\s+)?(\d{1,2})[/-](\d{1,2})[/-](\d{4})'
        date_match = re.search(date_pattern_full, message_lower)
        if date_match:
            try:
                day, month, year = int(date_match.group(1)), int(date_match.group(2)), int(date_match.group(3))
                target_date = datetime(year, month, day)
                logger.info(f"Extracted specific date (full): {target_date.strftime('%A, %d/%m/%Y')}")
                return target_date.strftime('%A').upper()
            except (ValueError, OverflowError) as e:
                logger.warning(f"Invalid date format: {e}")
                pass
        
        # Try to extract date without year (DD/MM) - use current year
        date_pattern_short = r'(?:ngày\s+)?(\d{1,2})[/-](\d{1,2})(?![/-]\d)'
        date_match_short = re.search(date_pattern_short, message_lower)
        if date_match_short:
            try:
                day, month = int(date_match_short.group(1)), int(date_match_short.group(2))
                year = today.year
                target_date = datetime(year, month, day)
                logger.info(f"Extracted specific date (short): {target_date.strftime('%A, %d/%m/%Y')}")
                return target_date.strftime('%A').upper()
            except (ValueError, OverflowError) as e:
                logger.warning(f"Invalid date format (short): {e}")
                pass
        
        # Relative date keywords
        if 'hôm nay' in message_lower or 'today' in message_lower:
            return today.strftime('%A').upper()
        
        if 'hôm qua' in message_lower or 'yesterday' in message_lower or 'hom qua' in message_lower:
            yesterday = today - timedelta(days=1)
            return yesterday.strftime('%A').upper()
        
        if 'mai' in message_lower or 'tomorrow' in message_lower:
            tomorrow = today + timedelta(days=1)
            return tomorrow.strftime('%A').upper()
        
        # "Mốt" = 2 ngày sau (day after tomorrow)
        if 'mốt' in message_lower or 'mot' in message_lower:
            day_after_tomorrow = today + timedelta(days=2)
            return day_after_tomorrow.strftime('%A').upper()
        
        # "Kia" = 3 ngày sau
        if 'kia' in message_lower:
            three_days_later = today + timedelta(days=3)
            return three_days_later.strftime('%A').upper()
        
        # Map Vietnamese day names to English (absolute day names)
        day_name_map = {
            'thứ 2': 'MONDAY',
            'thứ hai': 'MONDAY',
            'monday': 'MONDAY',
            't2': 'MONDAY',
            'thứ 3': 'TUESDAY',
            'thứ ba': 'TUESDAY',
            'tuesday': 'TUESDAY',
            't3': 'TUESDAY',
            'thứ 4': 'WEDNESDAY',
            'thứ tư': 'WEDNESDAY',
            'wednesday': 'WEDNESDAY',
            't4': 'WEDNESDAY',
            'thứ 5': 'THURSDAY',
            'thứ năm': 'THURSDAY',
            'thursday': 'THURSDAY',
            't5': 'THURSDAY',
            'thứ 6': 'FRIDAY',
            'thứ sáu': 'FRIDAY',
            'friday': 'FRIDAY',
            't6': 'FRIDAY',
            'thứ 7': 'SATURDAY',
            'thứ bảy': 'SATURDAY',
            'saturday': 'SATURDAY',
            't7': 'SATURDAY',
            'chủ nhật': 'SUNDAY',
            'cn': 'SUNDAY',
            'sunday': 'SUNDAY'
        }
        
        for key, value in day_name_map.items():
            if key in message_lower:
                return value
        
        return None  # Default to today
    
    def extract_week_from_message(self, message: str) -> int:
        """
        Extract week offset from user message
        Returns: 0 (this week), 1 (next week), -1 (last week), or specific week number
        """
        message_lower = message.lower()
        
        # Check for week keywords
        if 'tuần sau' in message_lower or 'tuần tới' in message_lower or 'next week' in message_lower:
            return 1
        elif 'tuần trước' in message_lower or 'last week' in message_lower:
            return -1
        elif 'tuần này' in message_lower or 'this week' in message_lower:
            return 0
        
        # Try to extract specific week number
        import re
        week_match = re.search(r'tuần\s*(\d+)', message_lower)
        if week_match:
            return int(week_match.group(1))
        
        return 0  # Default to current week
    
    def detect_week_schedule_intent(self, message: str) -> bool:
        """Detect if user wants to see schedule for a week"""
        patterns = [
            r'tuần\s*(này|sau|tới|trước|\d+)',
            r'this week',
            r'next week',
            r'last week',
            r'lịch tuần',
            r'tkb tuần'
        ]
        
        message_lower = message.lower()
        return any(re.search(pattern, message_lower) for pattern in patterns)
    
    def get_schedule(self, token: str, message: str = "", force_sync: bool = False) -> Dict:
        """
        Get user's schedule - auto sync from school if needed
        Supports: today, specific day (DD/MM/YYYY), this week, next week, relative dates (hôm qua, mai, mốt, kia)
        """
        try:
            headers = {"Authorization": f"Bearer {token}"}
            
            # Check if asking for week schedule
            if self.detect_week_schedule_intent(message):
                return self.get_week_schedule(token, message)
            
            # Extract specific date from message (returns datetime object)
            target_date = self.extract_specific_date(message)
            
            # Extract day from message
            requested_day = self.extract_day_from_message(message)
            
            # Get day label
            day_label_map = {
                'MONDAY': 'Thứ 2',
                'TUESDAY': 'Thứ 3',
                'WEDNESDAY': 'Thứ 4',
                'THURSDAY': 'Thứ 5',
                'FRIDAY': 'Thứ 6',
                'SATURDAY': 'Thứ 7',
                'SUNDAY': 'Chủ nhật'
            }
            
            if requested_day:
                day_label = day_label_map.get(requested_day, requested_day)
                
                # Check if it's a relative day and provide better label
                formatted_label, is_relative = self.get_formatted_date_label(message)
                if formatted_label:
                    day_label = formatted_label
                # else use the day name label already set above
            else:
                # Default to today
                today = datetime.now().strftime('%A').upper()
                requested_day = today
                target_date = datetime.now()  # Default to today
                formatted_label, is_relative = self.get_formatted_date_label(message)
                if formatted_label:
                    day_label = formatted_label
                else:
                    day_label = "hôm nay"
            
            # Get TVU credential
            credential = self.get_tvu_credential(token)
            
            if not credential:
                return {
                    "success": False,
                    "message": "❌ Chưa cấu hình tài khoản TVU. Vui lòng thêm tài khoản trong Settings → Credentials."
                }
            
            school_username = credential.get('username')
            school_password = credential.get('password')
            
            logger.info(f"TVU credential - username: {school_username}, password length: {len(school_password) if school_password else 0}")
            
            if not school_username or not school_password:
                return {
                    "success": False,
                    "message": "❌ Tài khoản TVU không hợp lệ."
                }
            
            # Use TVU scraper directly
            if TVUScraper:
                scraper = TVUScraper()
            else:
                scraper = get_scraper("https://ttsv.tvu.edu.vn")
            
            # Login
            logger.info(f"Attempting TVU login with username: {school_username}")
            if not scraper.login(school_username, school_password):
                logger.error("TVU login failed!")
                return {
                    "success": False,
                    "message": "❌ Đăng nhập TVU thất bại. Vui lòng kiểm tra tài khoản."
                }
            
            # Calculate target week if specific date is provided
            target_week = None
            if target_date:
                target_week = self.calculate_week_from_date(target_date)
                logger.info(f"Target date: {target_date.strftime('%d/%m/%Y')}, Target week: {target_week}")
            
            # Get schedules for the target week (or current week if no specific date)
            all_schedules = scraper.get_schedule(week=target_week)
            
            if not all_schedules:
                return {
                    "success": True,
                    "message": f"📅 {day_label.capitalize()} bạn không có lớp nào.",
                    "schedules": []
                }
            
            # Filter by requested day
            schedules = [s for s in all_schedules if s.get('day_of_week') == requested_day]
            
            if not schedules:
                return {
                    "success": True,
                    "message": f"📅 {day_label.capitalize()} bạn không có lớp nào.",
                    "schedules": []
                }
            
            # Format schedule
            message_text = f"📅 **Lịch học {day_label}:**\n\n"
            for schedule in schedules:
                start_time = schedule.get('start_time', '')[:5]
                end_time = schedule.get('end_time', '')[:5]
                time_str = f"{start_time} - {end_time}" if end_time else start_time
                
                message_text += f"🕐 **{time_str}**\n"
                message_text += f"   📚 {schedule.get('subject', 'N/A')}\n"
                message_text += f"   🏫 Phòng {schedule.get('room', 'N/A')}\n"
                if schedule.get('teacher'):
                    message_text += f"   👨‍🏫 {schedule['teacher']}\n"
                message_text += "\n"
            
            return {
                "success": True,
                "message": message_text,
                "schedules": schedules
            }
                
        except Exception as e:
            logger.error(f"Get schedule error: {e}")
            return {
                "success": False,
                "message": f"❌ Lỗi lấy thời khóa biểu: {str(e)}"
            }
    
    def get_week_schedule(self, token: str, message: str = "") -> Dict:
        """
        Get schedule for a specific week
        Supports: tuần này, tuần sau, tuần trước, tuần X
        """
        try:
            # Extract week offset (currently only supports current week)
            week_offset = self.extract_week_from_message(message)
            
            # Get TVU credential
            credential = self.get_tvu_credential(token)
            
            if not credential:
                return {
                    "success": False,
                    "message": "❌ Chưa cấu hình tài khoản TVU. Vui lòng thêm tài khoản trong Settings → Credentials."
                }
            
            school_username = credential.get('username')
            school_password = credential.get('password')
            
            if not school_username or not school_password:
                return {
                    "success": False,
                    "message": "❌ Tài khoản TVU không hợp lệ."
                }
            
            # Use TVU scraper directly
            if TVUScraper:
                scraper = TVUScraper()
            else:
                scraper = get_scraper("https://ttsv.tvu.edu.vn")
            
            # Login
            if not scraper.login(school_username, school_password):
                return {
                    "success": False,
                    "message": "❌ Đăng nhập TVU thất bại."
                }
            
            # Get schedules
            schedules = scraper.get_schedule()
            
            if not schedules:
                return {
                    "success": True,
                    "message": "📅 Tuần này bạn không có lớp nào.",
                    "schedules": []
                }
            
            # Determine week label
            if week_offset == 0:
                week_label = "tuần này"
            elif week_offset == 1:
                week_label = "tuần sau"
            elif week_offset == -1:
                week_label = "tuần trước"
            else:
                week_label = f"tuần {week_offset}"
            
            # Group by day
            days_order = ['MONDAY', 'TUESDAY', 'WEDNESDAY', 'THURSDAY', 'FRIDAY', 'SATURDAY', 'SUNDAY']
            day_names = {
                'MONDAY': 'Thứ 2',
                'TUESDAY': 'Thứ 3',
                'WEDNESDAY': 'Thứ 4',
                'THURSDAY': 'Thứ 5',
                'FRIDAY': 'Thứ 6',
                'SATURDAY': 'Thứ 7',
                'SUNDAY': 'Chủ nhật'
            }
            
            grouped = {}
            for schedule in schedules:
                day = schedule.get('day_of_week', 'MONDAY')
                if day not in grouped:
                    grouped[day] = []
                grouped[day].append(schedule)
            
            # Format message
            message_text = f"📅 **Lịch học {week_label}:**\n\n"
            
            has_class = False
            for day in days_order:
                if day in grouped:
                    has_class = True
                    day_schedules = sorted(grouped[day], key=lambda x: x.get('start_time', '00:00'))
                    message_text += f"**{day_names[day]}:**\n"
                    
                    for schedule in day_schedules:
                        start_time = schedule.get('start_time', '')[:5]
                        end_time = schedule.get('end_time', '')[:5]
                        time_str = f"{start_time}-{end_time}" if end_time else start_time
                        
                        message_text += f"  🕐 {time_str} | {schedule.get('subject', 'N/A')}"
                        if schedule.get('room'):
                            message_text += f" | Phòng {schedule['room']}"
                        message_text += "\n"
                    message_text += "\n"
            
            if not has_class:
                message_text = f"📅 {week_label.capitalize()} bạn không có lớp nào."
            
            return {
                "success": True,
                "message": message_text,
                "schedules": schedules,
                "week_offset": week_offset
            }
            
        except Exception as e:
            logger.error(f"Get week schedule error: {e}")
            return {
                "success": False,
                "message": f"❌ Lỗi: {str(e)}"
            }
    
    def get_grades(self, token: str) -> Dict:
        """Get user's grades"""
        try:
            headers = {"Authorization": f"Bearer {token}"}
            response = requests.get(
                f"{self.spring_boot_url}/api/grades/my-grades",
                headers=headers,
                timeout=5
            )
            
            if response.status_code == 200:
                grades = response.json()
                
                if not grades:
                    return {
                        "success": True,
                        "message": "📊 Chưa có điểm nào được ghi nhận.",
                        "grades": []
                    }
                
                # Group grades by course
                course_grades = {}
                for grade in grades:
                    course_name = grade['courseName']
                    if course_name not in course_grades:
                        course_grades[course_name] = []
                    course_grades[course_name].append(grade)
                
                # Format grades
                message = "📊 **Điểm của bạn:**\n\n"
                total_avg = 0
                course_count = 0
                
                for course_name, grades_list in course_grades.items():
                    message += f"📚 **{course_name}**\n"
                    course_total = 0
                    for grade in grades_list:
                        grade_value = float(grade['grade'])
                        message += f"   • {grade['gradeType']}: {grade_value}/10\n"
                        course_total += grade_value
                    
                    course_avg = course_total / len(grades_list)
                    message += f"   ➡️ Trung bình: **{course_avg:.2f}/10**\n\n"
                    total_avg += course_avg
                    course_count += 1
                
                if course_count > 0:
                    overall_avg = total_avg / course_count
                    message += f"📈 **Trung bình tổng:** {overall_avg:.2f}/10"
                
                return {
                    "success": True,
                    "message": message,
                    "grades": grades
                }
            else:
                return {
                    "success": False,
                    "message": "❌ Không thể lấy điểm số."
                }
        except Exception as e:
            return {
                "success": False,
                "message": f"❌ Lỗi: {str(e)}"
            }
    
    def generate_email_draft(self, recipient_name: str, subject: str, gemini_model) -> str:
        """Generate email draft using AI"""
        prompt = f"""
        Viết email gửi {recipient_name} về {subject}.
        
        Yêu cầu:
        - Tone: Lịch sự, trang trọng
        - Độ dài: Ngắn gọn, súc tích (3-5 câu)
        - Format: Email chuẩn với lời chào và kết thúc
        
        Chỉ trả về nội dung email, không giải thích.
        """
        
        response = gemini_model.generate_content(prompt)
        return response.text.strip()
    
    def handle_email_request(self, message: str, token: str, gemini_model) -> Dict:
        """Handle email sending request"""
        try:
            # Get user's contacts
            headers = {"Authorization": f"Bearer {token}"}
            response = requests.get(
                f"{self.spring_boot_url}/api/contacts",
                headers=headers,
                timeout=5
            )
            
            if response.status_code != 200:
                return {
                    "success": False,
                    "message": "❌ Không thể lấy danh bạ."
                }
            
            contacts = response.json()
            
            # Find recipient in message
            recipient = None
            for contact in contacts:
                if contact['contactName'].lower() in message.lower():
                    recipient = contact
                    break
            
            if not recipient:
                # List available contacts
                contact_list = "\n".join([f"• {c['contactName']}" for c in contacts])
                return {
                    "success": False,
                    "message": f"❌ Không tìm thấy người nhận.\n\n**Danh bạ của bạn:**\n{contact_list}"
                }
            
            # Extract subject
            subject_prompt = f"""
            Từ câu: "{message}"
            Trích xuất chủ đề email (subject).
            Chỉ trả về subject ngắn gọn, không giải thích.
            """
            subject = gemini_model.generate_content(subject_prompt).text.strip()
            
            # Generate email body
            email_body = self.generate_email_draft(recipient['contactName'], subject, gemini_model)
            
            # Return draft for user to review
            message_response = f"""
📧 **Email Draft**

**Người nhận:** {recipient['contactName']} ({recipient['contactEmail']})
**Chủ đề:** {subject}

**Nội dung:**
{email_body}

---
✅ Email draft đã được tạo! Bạn có thể copy và gửi qua email client của mình.
"""
            
            return {
                "success": True,
                "message": message_response,
                "email_draft": {
                    "to": recipient['contactEmail'],
                    "to_name": recipient['contactName'],
                    "subject": subject,
                    "body": email_body
                }
            }
        except Exception as e:
            return {
                "success": False,
                "message": f"❌ Lỗi: {str(e)}"
            }
    # ========== GMAIL API INTEGRATION (OAuth 2.0) ==========
    
    def handle_gmail_request(self, message: str, token: str, user_id: int = None) -> Dict:
        """
        Main handler for Gmail requests using OAuth 2.0
        Routes to appropriate Gmail action based on user intent
        """
        if not GMAIL_SERVICE_AVAILABLE:
            return {
                "success": False,
                "message": "❌ Gmail service không khả dụng. Vui lòng kiểm tra cấu hình."
            }
        
        try:
            # Detect intent
            if self.detect_gmail_send_intent(message):
                return self.handle_gmail_send(message, token, user_id)
            elif self.detect_gmail_search_intent(message):
                return self.handle_gmail_search(message, token, user_id)
            else:
                # Default: read emails
                return self.handle_gmail_read(message, token, user_id)
                
        except Exception as e:
            logger.error(f"Gmail request error: {e}")
            return {
                "success": False,
                "message": f"❌ Lỗi Gmail: {str(e)}"
            }
    
    def handle_gmail_read(self, message: str, token: str, user_id: int = None) -> Dict:
        """
        Handle reading Gmail inbox
        Uses OAuth 2.0 token to access user's Gmail
        """
        try:
            # Determine how many emails to read
            max_results = 5
            if 'tất cả' in message.lower() or 'all' in message.lower():
                max_results = 20
            elif 'mới nhất' in message.lower() or 'latest' in message.lower():
                max_results = 3
            
            # Check for unread filter
            only_unread = 'chưa đọc' in message.lower() or 'unread' in message.lower()
            
            # Call Gmail service
            result = ai_read_emails(
                user_id=user_id,
                max_results=max_results,
                only_unread=only_unread
            )
            
            if result.get('success'):
                emails = result.get('emails', [])
                if not emails:
                    return {
                        "success": True,
                        "message": "📭 Bạn không có email mới."
                    }
                
                # Format emails for display
                email_list = []
                for i, email in enumerate(emails, 1):
                    status = "🔵" if email.get('is_unread') else "⚪"
                    starred = "⭐" if email.get('is_starred') else ""
                    date = email.get('date', '')[:10]
                    email_list.append(
                        f"{status} **{i}. {email['subject'][:50]}** {starred}\n"
                        f"   Từ: {email['from']} | {date}"
                    )
                
                message_response = f"""📧 **Gmail Inbox** ({len(emails)} email)

{chr(10).join(email_list)}

---
💡 Nói "đọc email số X" để xem chi tiết.
"""
                return {
                    "success": True,
                    "message": message_response,
                    "emails": emails
                }
            else:
                # Check if need OAuth authorization
                if result.get('need_auth'):
                    auth_url = result.get('auth_url', 'http://localhost:8003/auth/google')
                    return {
                        "success": False,
                        "message": f"""🔐 **Cần đăng nhập Google**

Để AI có thể đọc Gmail của bạn, bạn cần cấp quyền OAuth 2.0.

👉 [Click vào đây để đăng nhập Google]({auth_url})

Sau khi đăng nhập, hãy thử lại yêu cầu.""",
                        "need_auth": True,
                        "auth_url": auth_url
                    }
                return result
                
        except Exception as e:
            logger.error(f"Gmail read error: {e}")
            return {
                "success": False,
                "message": f"❌ Không thể đọc Gmail: {str(e)}"
            }
    
    def handle_gmail_send(self, message: str, token: str, user_id: int = None) -> Dict:
        """
        Handle sending email via Gmail API - INTERACTIVE FLOW
        
        Flow:
        1. User: "gửi email xin nghỉ học đến thầy"
        2. AI: Suggest contacts (từ Gmail)
        3. User: Chọn contact (bằng số hoặc tên)
        4. AI: Generate draft email
        5. User: Edit/Confirm
        6. AI: Send email
        """
        try:
            # Import helper functions
            from gmail_service import ai_get_contacts, ai_create_draft_email, ai_send_email
            
            message_lower = message.lower()
            
            # ===== STEP 1: Check if user just wants to compose email =====
            # VD: "gửi email xin nghỉ học", "gửi mail hỏi bài", "soạn email"
            # But NOT if they already provided email address
            compose_patterns = [
                r'gửi\s+(?:email|mail)\s+(.+?)(?:\s+(?:cho|đến|tới)|$)',
                r'soạn\s+(?:email|mail)\s+(.+?)(?:\s+(?:cho|đến|tới)|$)',
                r'viết\s+(?:email|mail)\s+(.+?)(?:\s+(?:cho|đến|tới)|$)'
            ]
            
            # First check if email address is present
            has_email = bool(re.search(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', message))
            
            subject_keyword = None
            if not has_email:  # Only suggest contacts if no email provided
                for pattern in compose_patterns:
                    match = re.search(pattern, message_lower)
                    if match:
                        subject_keyword = match.group(1).strip()
                        break
            
            if subject_keyword and not has_email:
                # User muốn compose email NHƯNG chưa chỉ định recipient
                # → Suggest contacts (only if authenticated)
                logger.info(f"📧 Compose email intent detected: {subject_keyword}")
                
                if not user_id:
                    # No authentication - ask for email address
                    return {
                        "success": False,
                        "message": f"""📧 **Soạn email: {subject_keyword}**

Vui lòng cung cấp địa chỉ email người nhận.

**Ví dụ:**
• "gửi mail {subject_keyword} đến teacher@tvu.edu.vn"
• "gửi email {subject_keyword} cho admin@example.com"
"""
                    }
                
                # Get frequent contacts from Gmail (requires auth)
                contacts_result = ai_get_contacts(user_id, max_results=10)
                
                if not contacts_result.get("success"):
                    if contacts_result.get("need_auth"):
                        return {
                            "success": False,
                            "message": """🔐 **Cần kết nối Gmail**

Để gửi email, bạn cần kết nối Google Account trong Settings.

👉 Vào **Settings** → **Connect Google**""",
                            "need_auth": True,
                            "auth_url": contacts_result.get("auth_url")
                        }
                    else:
                        return contacts_result
                
                contacts = contacts_result.get("contacts", [])
                
                if not contacts:
                    return {
                        "success": False,
                        "message": """📭 Không tìm thấy contacts trong Gmail.

**Cách khác:**
Bạn có thể gửi trực tiếp bằng cách:
"Gửi email cho email@example.com chủ đề ... nội dung ..."
"""
                    }
                
                # Format contacts list for user to choose
                contacts_list = []
                for i, contact in enumerate(contacts[:10], 1):
                    name = contact.get("name", "").strip()
                    email = contact.get("email", "")
                    count = contact.get("count", 0)
                    
                    if name and name != email.split("@")[0]:
                        display = f"**{i}. {name}** ({email})"
                    else:
                        display = f"**{i}. {email}**"
                    
                    if count > 1:
                        display += f" _{count} emails_"
                    
                    contacts_list.append(display)
                
                response_msg = f"""📧 **Gửi email: {subject_keyword}**

**📋 Chọn người nhận:**

{chr(10).join(contacts_list)}

---
💡 **Cách chọn:**
• Nhắn số: "1" hoặc "chọn 1"  
• Hoặc gõ email trực tiếp: "teacher@tvu.edu.vn"

🔄 **Sau khi chọn:** AI sẽ tạo nội dung email mẫu để bạn xem trước và chỉnh sửa.
"""
                
                return {
                    "success": True,
                    "message": response_msg,
                    "action": "select_recipient",
                    "subject_keyword": subject_keyword,
                    "contacts": contacts,
                    "awaiting_selection": True
                }
            
            # ===== STEP 2: Parse full email command with recipient =====
            # VD: "gửi email cho teacher@tvu.edu.vn chủ đề ... nội dung ..."
            # Also match: "gửi mail xin nghỉ học đến email@gmail.com"
            to_match = re.search(r'(?:cho|to|tới|đến)\s+([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})', message_lower)
            subject_match = re.search(r'(?:chủ đề|subject|tiêu đề)\s*[:\"]?\s*(.+?)(?:\s*nội dung|\s*body|$)', message, re.IGNORECASE)
            body_match = re.search(r'(?:nội dung|body|content)\s*[:\"]?\s*(.+)', message, re.IGNORECASE)
            
            if not to_match:
                return {
                    "success": False,
                    "message": """📧 **Gửi Email**

Để gửi email, vui lòng cung cấp đầy đủ thông tin:

**Cú pháp:** "Gửi email cho email@example.com chủ đề Xin chào nội dung Đây là nội dung email"

**Ví dụ:**
• "Gửi email cho teacher@tvu.edu.vn chủ đề Xin nghỉ học nội dung Em xin phép nghỉ học ngày mai"
"""
                }
            
            to_email = to_match.group(1)
            subject = subject_match.group(1).strip() if subject_match else None
            body = body_match.group(1).strip() if body_match else None
            
            # ===== AUTO-GENERATE with AI if missing subject or body =====
            if not subject or not body:
                # Extract subject keyword from message
                # VD: "gửi email xin nghỉ học đến an@gmail.com"
                # VD: "gửi mail hỏi bài cho teacher@tvu.edu.vn"
                if not subject:
                    # Try to extract subject from message before email
                    subject_patterns = [
                        r'(?:gửi|soạn|viết)\s+(?:email|mail)\s+(.+?)\s+(?:cho|đến|tới)',
                        r'(?:email|mail)\s+(.+?)\s+(?:cho|đến|tới)',
                        r'(?:gửi|soạn|viết)\s+(?:email|mail)\s+(.+?)$'  # Match until end if no recipient keyword
                    ]
                    for pattern in subject_patterns:
                        match = re.search(pattern, message_lower)
                        if match:
                            subject_keyword = match.group(1).strip()
                            # Remove email address from subject if extracted
                            subject_keyword = re.sub(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', '', subject_keyword).strip()
                            if subject_keyword:
                                break
                    else:
                        subject_keyword = "thông báo"
                else:
                    subject_keyword = subject
                
                logger.info(f"🤖 Auto-generating email content for: {subject_keyword} to {to_email}")
                
                # Generate draft with AI
                draft_result = ai_create_draft_email(
                    subject_keyword=subject_keyword,
                    recipient_name=to_email.split('@')[0]  # Use email username as name
                )
                
                if draft_result.get("success"):
                    ai_subject = draft_result.get("subject", subject or subject_keyword)
                    ai_body = draft_result.get("body", "")
                    
                    # Use AI-generated content for missing parts
                    if not subject:
                        subject = ai_subject
                    if not body:
                        body = ai_body
                    
                    # Show preview with send button
                    return {
                        "success": True,
                        "message": f"""📝 **Xem trước Email**

📧 **Người nhận:** {to_email}
📌 **Chủ đề:** {subject}

**📄 Nội dung:**
{body}

---
💡 Bạn có thể chỉnh sửa nội dung trước khi gửi.""",
                        "action": "email_draft",
                        "email_draft": {
                            "to": to_email,
                            "subject": subject,
                            "body": body,
                            "user_id": user_id
                        }
                    }
                else:
                    # Fallback if AI generation fails
                    if not body:
                        return {
                            "success": False,
                            "message": f"""📝 **Soạn Email**

**Người nhận:** {to_email}
**Chủ đề:** {subject or subject_keyword}

⚠️ Vui lòng thêm nội dung email.
Ví dụ: "...nội dung: Đây là nội dung email của tôi"
"""
                        }
            
            # ===== RETURN DRAFT FOR USER TO REVIEW =====
            # Không tự động gửi, cho user xem và confirm trước
            logger.info(f"📧 Created email draft to {to_email}")
            
            return {
                "success": True,
                "message": f"""📝 **Xem trước Email**

📧 **Người nhận:** {to_email}
📌 **Chủ đề:** {subject}

**📄 Nội dung:**
{body}

---
💡 Bạn có thể chỉnh sửa nội dung trước khi gửi.""",
                "action": "email_draft",
                "email_draft": {
                    "to": to_email,
                    "subject": subject,
                    "body": body,
                    "user_id": user_id
                }
            }
                
        except Exception as e:
            logger.error(f"Gmail send error: {e}")
            return {
                "success": False,
                "message": f"❌ Không thể gửi email: {str(e)}"
            }
    
    def handle_gmail_search(self, message: str, token: str, user_id: int = None) -> Dict:
        """
        Handle searching emails in Gmail
        Supports search by sender, subject, keyword
        """
        try:
            # Extract search query
            search_patterns = [
                r'tìm email (?:từ|của)\s+(.+)',
                r'search email (?:from|of)\s+(.+)',
                r'email từ\s+(.+)',
                r'tìm mail\s+(.+)',
                r'tìm email\s+(.+)'
            ]
            
            query = None
            for pattern in search_patterns:
                match = re.search(pattern, message.lower())
                if match:
                    query = match.group(1).strip()
                    break
            
            if not query:
                return {
                    "success": False,
                    "message": """🔍 **Tìm kiếm Email**

**Cách sử dụng:**
• "Tìm email từ teacher@tvu.edu.vn"
• "Tìm email về thời khóa biểu"
• "Email từ Google"

**Bộ lọc nâng cao:**
• "Tìm email có đính kèm"
• "Tìm email chưa đọc từ..."
"""
                }
            
            # Build Gmail search query
            gmail_query = query
            if '@' in query:
                gmail_query = f"from:{query}"
            
            # Search via Gmail API
            result = ai_search_emails(
                user_id=user_id,
                query=gmail_query,
                max_results=10
            )
            
            if result.get('success'):
                emails = result.get('emails', [])
                if not emails:
                    return {
                        "success": True,
                        "message": f"🔍 Không tìm thấy email nào khớp với '{query}'"
                    }
                
                # Format results
                email_list = []
                for i, email in enumerate(emails, 1):
                    date = email.get('date', '')[:10]
                    email_list.append(
                        f"**{i}. {email['subject'][:50]}**\n"
                        f"   Từ: {email['from']} | {date}"
                    )
                
                return {
                    "success": True,
                    "message": f"""🔍 **Kết quả tìm kiếm** ({len(emails)} email)

Tìm: "{query}"

{chr(10).join(email_list)}
""",
                    "emails": emails
                }
            else:
                if result.get('need_auth'):
                    auth_url = result.get('auth_url', 'http://localhost:8003/auth/google')
                    return {
                        "success": False,
                        "message": f"""🔐 **Cần đăng nhập Google**

👉 [Click vào đây để đăng nhập Google]({auth_url})""",
                        "need_auth": True,
                        "auth_url": auth_url
                    }
                return result
                
        except Exception as e:
            logger.error(f"Gmail search error: {e}")
            return {
                "success": False,
                "message": f"❌ Không thể tìm kiếm email: {str(e)}"
            }