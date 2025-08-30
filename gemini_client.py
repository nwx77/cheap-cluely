import logging
from typing import Optional
from google import genai
from google.api_core import exceptions
from config import Config

class GeminiClient:
    """Client for interacting with Google's Gemini API"""

    def __init__(self):
        self.client = None
        self.logger = logging.getLogger(__name__)
        self.api_keys = Config.GEMINI_API_KEYS
        self.current_key_index = 0
        self._initialize_client()

    def _initialize_client(self):
        """Initialize the Gemini client"""
        try:
            if not self.api_keys:
                raise ValueError("GEMINI_API_KEYS list is empty in config")
            
            api_key = self.api_keys[self.current_key_index]
            self.client = genai.Client(api_key=api_key)
            self.logger.info(f"Gemini client initialized successfully with key index {self.current_key_index}")

        except Exception as e:
            self.logger.error(f"Failed to initialize Gemini client: {e}")
            raise

    def _rotate_key_and_reinitialize(self):
        """Rotate to the next API key and re-initialize the client"""
        self.current_key_index = (self.current_key_index + 1) % len(self.api_keys)
        self.logger.info(f"Rotating to next API key index: {self.current_key_index}")
        self._initialize_client()

    def generate_response(self, screen_context: str, audio_context: str, user_query: str) -> Optional[str]:
        """Generate AI response using Gemini API"""
        for _ in range(len(self.api_keys)):
            try:
                prompt = self._build_prompt(screen_context, audio_context, user_query)
                response = self.client.models.generate_content(
                    model=Config.GEMINI_MODEL,
                    contents=prompt
                )
                if response and hasattr(response, 'text'):
                    return response.text.strip()
                else:
                    self.logger.error("Empty response from Gemini API")
                    return None
            except exceptions.PermissionDenied as e:
                self.logger.warning(f"API key at index {self.current_key_index} failed: {e}. Rotating key.")
                self._rotate_key_and_reinitialize()
            except Exception as e:
                self.logger.error(f"Error generating Gemini response: {e}")
                return None
        
        self.logger.error("All API keys failed.")
        return "All API keys failed. Please check your API keys in config.py."

    def _build_prompt(self, screen_context: str, audio_context: str, user_query: str) -> str:
        """Build a comprehensive prompt for Gemini"""
        
        prompt_parts = [
            "You are Cluely, an AI assistant that helps users during meetings and presentations. ",
            "You have access to both screen content and meeting audio context. ",
            "Provide helpful, concise, and contextually relevant answers. ",
            "Focus on being practical and actionable in your responses.\n\n"
        ]
        
        if screen_context:
            prompt_parts.append(f"SCREEN CONTENT:\n{screen_context}\n\n")
        
        if audio_context:
            prompt_parts.append(f"MEETING AUDIO TRANSCRIPT:\n{audio_context}\n\n")
        
        prompt_parts.append(f"USER QUESTION: {user_query}\n\n")
        prompt_parts.append("ASSISTANT:")
        
        return "".join(prompt_parts)

    def test_connection(self) -> bool:
        """Test the connection to Gemini API"""
        for _ in range(len(self.api_keys)):
            try:
                response = self.client.models.generate_content(
                    model=Config.GEMINI_MODEL,
                    contents="Hello, this is a test message."
                )
                return response is not None and hasattr(response, 'text')
            except exceptions.PermissionDenied as e:
                self.logger.warning(f"API key at index {self.current_key_index} failed during test: {e}. Rotating key.")
                self._rotate_key_and_reinitialize()
            except Exception as e:
                self.logger.error(f"Gemini API test failed: {e}")
                return False
        
        self.logger.error("All API keys failed during test.")
        return False