import keyboard
import logging
from typing import Callable, Optional
from config import Config

class HotkeyManager:
    """Manages global hotkeys for the AI assistant"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.registered_hotkeys = {}
        self.is_active = False
    
    def register_hotkey(self, hotkey: str, callback: Callable, description: str = ""):
        """Register a global hotkey"""
        try:
            keyboard.add_hotkey(hotkey, callback, suppress=True)
            self.registered_hotkeys[hotkey] = {
                'callback': callback,
                'description': description
            }
            self.logger.info(f"Registered hotkey: {hotkey} - {description}")
        except Exception as e:
            self.logger.error(f"Failed to register hotkey {hotkey}: {e}")
    
    def unregister_hotkey(self, hotkey: str):
        """Unregister a global hotkey"""
        try:
            keyboard.remove_hotkey(hotkey)
            if hotkey in self.registered_hotkeys:
                del self.registered_hotkeys[hotkey]
            self.logger.info(f"Unregistered hotkey: {hotkey}")
        except Exception as e:
            self.logger.error(f"Failed to unregister hotkey {hotkey}: {e}")
    
    def register_default_hotkeys(self, toggle_callback: Callable, voice_callback: Optional[Callable] = None):
        """Register the default hotkeys for the assistant"""
        # Toggle overlay hotkey
        self.register_hotkey(
            Config.TOGGLE_HOTKEY, 
            toggle_callback, 
            "Toggle AI Assistant overlay"
        )
        
        # Voice trigger hotkey (optional)
        if voice_callback:
            self.register_hotkey(
                Config.VOICE_TRIGGER_HOTKEY,
                voice_callback,
                "Voice trigger for AI Assistant"
            )
    
    def unregister_all_hotkeys(self):
        """Unregister all hotkeys"""
        for hotkey in list(self.registered_hotkeys.keys()):
            self.unregister_hotkey(hotkey)
    
    def get_registered_hotkeys(self) -> dict:
        """Get all registered hotkeys"""
        return self.registered_hotkeys.copy()
    
    def is_hotkey_registered(self, hotkey: str) -> bool:
        """Check if a hotkey is registered"""
        return hotkey in self.registered_hotkeys
    
    def start_listening(self):
        """Start listening for hotkeys"""
        if not self.is_active:
            self.is_active = True
            self.logger.info("Hotkey manager started")
    
    def stop_listening(self):
        """Stop listening for hotkeys"""
        if self.is_active:
            self.unregister_all_hotkeys()
            self.is_active = False
            self.logger.info("Hotkey manager stopped")
