import sys
import logging
import threading
import time
from typing import Optional
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QThread, pyqtSignal

from config import Config
from screen_capture import ScreenCapture
from audio_capture import AudioCapture
from gemini_client import GeminiClient
from overlay_ui import OverlayUI
from hotkey_manager import HotkeyManager

class AssistantThread(QThread):
    """Background thread for processing AI requests"""
    
    response_ready = pyqtSignal(str)
    error_occurred = pyqtSignal(str)
    
    def __init__(self, gemini_client: GeminiClient, screen_capture: ScreenCapture, audio_capture: AudioCapture):
        super().__init__()
        self.gemini_client = gemini_client
        self.screen_capture = screen_capture
        self.audio_capture = audio_capture
        self.current_query = ""
    
    def process_query(self, query: str):
        """Process a user query"""
        self.current_query = query
        self.start()
    
    def run(self):
        """Run the background processing"""
        try:
            # Gather context
            screen_context = self.screen_capture.get_screen_context()
            audio_context = self.audio_capture.get_audio_context()
            
            # Generate response
            response = self.gemini_client.generate_response(
                screen_context, audio_context, self.current_query
            )
            
            if response:
                self.response_ready.emit(response)
            else:
                self.error_occurred.emit("Failed to generate response")
                
        except Exception as e:
            self.error_occurred.emit(f"Error processing query: {str(e)}")

class CluelyAssistant:
    """Main AI assistant class that orchestrates all components"""
    
    def __init__(self):
        self.logger = self._setup_logging()
        self.logger.info("Initializing Cluely AI Assistant...")
        
        # Validate configuration
        if not Config.validate_config():
            raise ValueError("Invalid configuration")
        
        # Initialize components
        self.screen_capture = None
        self.audio_capture = None
        self.gemini_client = None
        self.overlay_ui = None
        self.hotkey_manager = None
        self.assistant_thread = None
        
        # Qt application
        self.app = QApplication(sys.argv)
        self.app.setQuitOnLastWindowClosed(True)
        
        # Initialize components
        self._initialize_components()
        
        # Connect signals
        self._connect_signals()
        
        self.logger.info("Cluely AI Assistant initialized successfully")
    
    def _setup_logging(self) -> logging.Logger:
        """Setup logging configuration"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(Config.LOG_FILE),
                logging.StreamHandler()
            ]
        )
        return logging.getLogger(__name__)
    
    def _initialize_components(self):
        """Initialize all assistant components"""
        try:
            # Initialize Gemini client
            self.logger.info("Initializing Gemini client...")
            self.gemini_client = GeminiClient()
            
            # Test Gemini connection
            if not self.gemini_client.test_connection():
                raise Exception("Failed to connect to Gemini API")
            
            # Initialize screen capture
            self.logger.info("Initializing screen capture...")
            self.screen_capture = ScreenCapture()
            
            # Initialize audio capture
            self.logger.info("Initializing audio capture...")
            self.audio_capture = AudioCapture()
            
            # Initialize overlay UI
            self.logger.info("Initializing overlay UI...")
            self.overlay_ui = OverlayUI()
            
            # Initialize hotkey manager
            self.logger.info("Initializing hotkey manager...")
            self.hotkey_manager = HotkeyManager()
            
            # Initialize assistant thread
            self.assistant_thread = AssistantThread(
                self.gemini_client, self.screen_capture, self.audio_capture
            )
            
        except Exception as e:
            self.logger.error(f"Failed to initialize components: {e}")
            raise
    
    def _connect_signals(self):
        """Connect all component signals"""
        # Connect overlay UI signals
        self.overlay_ui.query_submitted.connect(self._handle_query)
        self.overlay_ui.toggle_requested.connect(self._toggle_overlay)
        
        # Connect assistant thread signals
        self.assistant_thread.response_ready.connect(self.overlay_ui.set_response)
        self.assistant_thread.error_occurred.connect(self.overlay_ui.set_error)
        
        # Connect hotkeys
        self.hotkey_manager.register_default_hotkeys(
            toggle_callback=self._toggle_overlay
        )
    
    def _handle_query(self, query: str):
        """Handle a user query"""
        self.logger.info(f"Processing query: {query}")
        self.overlay_ui.set_loading()
        self.assistant_thread.process_query(query)
    
    def _toggle_overlay(self):
        """Toggle overlay visibility"""
        self.overlay_ui.toggle_overlay()
    
    def start(self):
        """Start the AI assistant"""
        try:
            self.logger.info("Starting Cluely AI Assistant...")
            
            # Start background capture
            self.screen_capture.start_background_capture()
            self.audio_capture.start_recording()
            
            # Start hotkey manager
            self.hotkey_manager.start_listening()
            
            # Show overlay initially
            self.overlay_ui.show_overlay()
            
            self.logger.info("Cluely AI Assistant started successfully")
            self.logger.info(f"Use {Config.TOGGLE_HOTKEY} to toggle the overlay")
            
            # Run the Qt application
            return self.app.exec_()
            
        except Exception as e:
            self.logger.error(f"Failed to start assistant: {e}")
            raise
    
    def stop(self):
        """Stop the AI assistant"""
        try:
            self.logger.info("Stopping Cluely AI Assistant...")
            
            # Stop background processes
            if self.screen_capture:
                self.screen_capture.stop_background_capture()
            
            if self.audio_capture:
                self.audio_capture.stop_recording()
            
            if self.hotkey_manager:
                self.hotkey_manager.stop_listening()
            
            # Close overlay
            if self.overlay_ui:
                self.overlay_ui.close()
            
            self.logger.info("Cluely AI Assistant stopped")
            
        except Exception as e:
            self.logger.error(f"Error stopping assistant: {e}")
    
    def __enter__(self):
        """Context manager entry"""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        self.stop()

def main():
    """Main entry point"""
    try:
        with CluelyAssistant() as assistant:
            return assistant.start()
    except KeyboardInterrupt:
        print("\nShutting down...")
        return 0
    except Exception as e:
        print(f"Error: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())
