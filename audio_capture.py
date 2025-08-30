import os
import time
import threading
import tempfile
import wave
import numpy as np
import sounddevice as sd
import whisper
import logging
from typing import Optional, List
from config import Config

class AudioCapture:
    """Handles audio capture and transcription using Whisper"""
    
    def __init__(self):
        self.audio_buffer = []
        self.transcript_buffer = []
        self.is_recording = False
        self.recording_thread = None
        self.whisper_model = None
        self.logger = logging.getLogger(__name__)
        
        # Initialize Whisper model
        try:
            self.whisper_model = whisper.load_model("small")
            self.logger.info("Whisper model loaded successfully")
        except Exception as e:
            self.logger.error(f"Failed to load Whisper model: {e}")
            raise
    
    def start_recording(self):
        """Start continuous audio recording"""
        if self.is_recording:
            return
        
        self.is_recording = True
        self.recording_thread = threading.Thread(target=self._recording_loop, daemon=True)
        self.recording_thread.start()
        self.logger.info("Started audio recording")
    
    def stop_recording(self):
        """Stop audio recording"""
        self.is_recording = False
        if self.recording_thread:
            self.recording_thread.join(timeout=1)
        self.logger.info("Stopped audio recording")
    
    def _recording_loop(self):
        """Background loop for continuous audio recording and transcription"""
        while self.is_recording:
            try:
                # Record audio chunk
                audio_chunk = self._record_audio_chunk()
                if audio_chunk is not None:
                    # Transcribe the chunk
                    transcript = self._transcribe_audio(audio_chunk)
                    if transcript:
                        self.transcript_buffer.append({
                            'text': transcript,
                            'timestamp': time.time()
                        })
                        
                        # Keep only recent transcripts (last 5 minutes)
                        cutoff_time = time.time() - 300
                        self.transcript_buffer = [
                            t for t in self.transcript_buffer 
                            if t['timestamp'] > cutoff_time
                        ]
                
            except Exception as e:
                self.logger.error(f"Error in recording loop: {e}")
                time.sleep(1)
    
    def _record_audio_chunk(self) -> Optional[np.ndarray]:
        """Record a chunk of audio"""
        try:
            # Record audio for the specified duration
            audio_data = sd.rec(
                int(Config.AUDIO_RECORD_SECONDS * Config.AUDIO_SAMPLE_RATE),
                samplerate=Config.AUDIO_SAMPLE_RATE,
                channels=Config.AUDIO_CHANNELS,
                dtype=np.float32
            )
            sd.wait()  # Wait for recording to complete
            
            return audio_data
            
        except Exception as e:
            self.logger.error(f"Error recording audio: {e}")
            return None
    
    def _transcribe_audio(self, audio_data: np.ndarray) -> Optional[str]:
        """Transcribe audio using Whisper"""
        try:
            # Save audio to temporary file
            with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_file:
                temp_filename = temp_file.name
            
            # Save as WAV file
            with wave.open(temp_filename, 'wb') as wav_file:
                wav_file.setnchannels(Config.AUDIO_CHANNELS)
                wav_file.setsampwidth(2)  # 16-bit
                wav_file.setframerate(Config.AUDIO_SAMPLE_RATE)
                wav_file.writeframes((audio_data * 32767).astype(np.int16).tobytes())
            
            # Transcribe with Whisper
            result = self.whisper_model.transcribe(temp_filename)
            transcript = result["text"].strip()
            
            # Clean up temporary file
            os.unlink(temp_filename)
            
            # Only return non-empty transcripts
            if transcript and len(transcript) > 5:
                return transcript
            
            return None
            
        except Exception as e:
            self.logger.error(f"Error transcribing audio: {e}")
            return None
    
    def get_audio_context(self) -> str:
        """Get the recent audio transcript context"""
        if not self.transcript_buffer:
            return ""
        
        # Combine recent transcripts
        recent_texts = [t['text'] for t in self.transcript_buffer[-10:]]  # Last 10 chunks
        return " ".join(recent_texts)
    
    def clear_transcript_buffer(self):
        """Clear the transcript buffer"""
        self.transcript_buffer.clear()
        self.logger.info("Cleared transcript buffer")
