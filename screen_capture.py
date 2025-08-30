import time
import threading
from typing import Optional, List
from PIL import ImageGrab, Image
import pytesseract
from screen_ocr import Reader
import logging
from config import Config

class ScreenCapture:
    """Handles screen capture and OCR text extraction"""
    
    def __init__(self):
        self.current_screen_text = ""
        self.last_capture_time = 0
        self.capture_thread = None
        self.is_capturing = False
        self.logger = logging.getLogger(__name__)
        
        # Try to initialize screen-ocr reader, fallback to pytesseract
        try:
            self.ocr_reader = Reader()
            self.use_screen_ocr = True
            self.logger.info("Using screen-ocr for OCR")
        except Exception as e:
            self.logger.warning(f"screen-ocr not available, falling back to pytesseract: {e}")
            self.use_screen_ocr = False
            # Ensure tesseract is available
            try:
                pytesseract.get_tesseract_version()
            except Exception as e:
                self.logger.error(f"Tesseract not found: {e}")
                raise
    
    def capture_screen_text(self) -> str:
        """Capture current screen and extract text using OCR"""
        try:
            if self.use_screen_ocr:
                # Use screen-ocr library
                text = self.ocr_reader.read_screen()
            else:
                # Use PIL + pytesseract
                screenshot = ImageGrab.grab()
                text = pytesseract.image_to_string(screenshot)
            
            # Clean up the text
            text = self._clean_ocr_text(text)
            self.current_screen_text = text
            self.last_capture_time = time.time()
            
            return text
            
        except Exception as e:
            self.logger.error(f"Error capturing screen text: {e}")
            return ""
    
    def _clean_ocr_text(self, text: str) -> str:
        """Clean and filter OCR text"""
        if not text:
            return ""
        
        # Remove excessive whitespace and normalize
        lines = [line.strip() for line in text.split('\n') if line.strip()]
        text = '\n'.join(lines)
        
        # Filter out very short text that might be noise
        if len(text) < 10:
            return ""
        
        return text
    
    def get_screen_context(self) -> str:
        """Get the current screen context, capture if needed"""
        current_time = time.time()
        
        # Capture new screen if enough time has passed
        if current_time - self.last_capture_time > Config.SCREEN_CAPTURE_INTERVAL:
            self.capture_screen_text()
        
        return self.current_screen_text
    
    def start_background_capture(self):
        """Start background screen capture thread"""
        if self.is_capturing:
            return
        
        self.is_capturing = True
        self.capture_thread = threading.Thread(target=self._capture_loop, daemon=True)
        self.capture_thread.start()
        self.logger.info("Started background screen capture")
    
    def stop_background_capture(self):
        """Stop background screen capture"""
        self.is_capturing = False
        if self.capture_thread:
            self.capture_thread.join(timeout=1)
        self.logger.info("Stopped background screen capture")
    
    def _capture_loop(self):
        """Background loop for continuous screen capture"""
        while self.is_capturing:
            try:
                self.capture_screen_text()
                time.sleep(Config.SCREEN_CAPTURE_INTERVAL)
            except Exception as e:
                self.logger.error(f"Error in capture loop: {e}")
                time.sleep(1)
