import logging
from typing import Optional
from google import genai
from config import Config

class GeminiClient:
    """Client for interacting with Google's Gemini API"""
    
    def __init__(self):
        self.client = None
        self.logger = logging.getLogger(__name__)
        self._initialize_client()
    
    def _initialize_client(self):
        """Initialize the Gemini client"""
        try:
            if not Config.GEMINI_API_KEY:
                raise ValueError("GEMINI_API_KEY not set in environment")
            
            self.client = genai.Client()
            self.logger.info("Gemini client initialized successfully")
            
        except Exception as e:
            self.logger.error(f"Failed to initialize Gemini client: {e}")
            raise
    
    def generate_response(self, screen_context: str, audio_context: str, user_query: str) -> Optional[str]:
        """Generate AI response using Gemini API"""
        try:
            # Build the prompt with context
            prompt = self._build_prompt(screen_context, audio_context, user_query)
            
            # Call Gemini API
            response = self.client.models.generate_content(
                model=Config.GEMINI_MODEL,
                contents=prompt
            )
            
            if response and hasattr(response, 'text'):
                return response.text.strip()
            else:
                self.logger.error("Empty response from Gemini API")
                return None
                
        except Exception as e:
            self.logger.error(f"Error generating Gemini response: {e}")
            return None
    
    def _build_prompt(self, screen_context: str, audio_context: str, user_query: str) -> str:
        """Build a comprehensive prompt for Gemini"""
        
        prompt_parts = [
            "You are Cluely, an AI assistant that helps users during meetings and presentations. ",
            "You have access to both screen content and meeting audio context. ",
            "Provide helpful, concise, and contextually relevant answers. ",
            "Focus on being practical and actionable in your responses.\n\n"
        ]
        
        # Add screen context if available
        if screen_context:
            prompt_parts.append(f"SCREEN CONTENT:\n{screen_context}\n\n")
        
        # Add audio context if available
        if audio_context:
            prompt_parts.append(f"MEETING AUDIO TRANSCRIPT:\n{audio_context}\n\n")
        
        # Add user query
        prompt_parts.append(f"USER QUESTION: {user_query}\n\n")
        prompt_parts.append("ASSISTANT:")
        
        return "".join(prompt_parts)
    
    def test_connection(self) -> bool:
        """Test the connection to Gemini API"""
        try:
            response = self.client.models.generate_content(
                model=Config.GEMINI_MODEL,
                contents="Hello, this is a test message."
            )
            return response is not None and hasattr(response, 'text')
        except Exception as e:
            self.logger.error(f"Gemini API test failed: {e}")
            return False
