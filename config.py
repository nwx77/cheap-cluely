import os
from typing import Optional

class Config:
    """Configuration class for the Cluely-like AI assistant"""
    
    # Gemini API Configuration
    GEMINI_API_KEY: Optional[str] = "AIzaSyBD2rqJJZugMHVC-TORgUDdCWb8hDOo3rI"
    GEMINI_MODEL: str = "gemini-2.0-flash"
    
    # Audio Configuration
    AUDIO_SAMPLE_RATE: int = 16000
    AUDIO_CHANNELS: int = 1
    AUDIO_CHUNK_SIZE: int = 1024
    AUDIO_RECORD_SECONDS: int = 5  # How long to record audio chunks
    
    # OCR Configuration
    OCR_CONFIDENCE_THRESHOLD: float = 0.6
    SCREEN_CAPTURE_INTERVAL: float = 2.0  # seconds
    
    # UI Configuration
    OVERLAY_WIDTH: int = 400
    OVERLAY_HEIGHT: int = 300
    OVERLAY_OPACITY: float = 0.9
    OVERLAY_CORNER_RADIUS: int = 10
    
    # Hotkeys
    TOGGLE_HOTKEY: str = "ctrl+alt+c"
    VOICE_TRIGGER_HOTKEY: str = "ctrl+alt+v"
    
    # File paths
    TEMP_AUDIO_DIR: str = "temp_audio"
    LOG_FILE: str = "cluely_assistant.log"
    
    @classmethod
    def validate_config(cls) -> bool:
        """Validate that all required configuration is present"""
        if not cls.GEMINI_API_KEY:
            print("[ERROR] GEMINI_API_KEY environment variable not set!")
            print("Please set your Gemini API key:")
            print("Windows: set GEMINI_API_KEY=your_key_here")
            print("Linux/Mac: export GEMINI_API_KEY=your_key_here")
            return False
        return True
