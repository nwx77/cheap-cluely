# cheap cluely that sorta sucks

a local-first, undetectable AI desktop assistant that listens to meetings and on-screen content, then provides real-time answers using Google's Gemini API. Built with Python and designed to be invisible to others in video calls.

## Features

- **Screen Context Capture**: OCR technology reads text from your screen (presentations, code, chat, etc.)
- **Audio Transcription**: Real-time speech-to-text using Whisper for meeting audio
- **AI-Powered Responses**: Google Gemini API provides context-aware answers
- **Translucent Overlay UI**: Always-on-top, draggable interface that never blocks your work
- **⌨Global Hotkeys**: Quick access with customizable keyboard shortcuts
- **Privacy-First**: All processing happens locally except AI API calls
- **Invisible to Others**: Never joins meetings or appears in screen shares

## Screenshots

The assistant appears as a translucent overlay in the top-right corner of your screen, providing instant AI-powered responses based on your current context.

## Installation

### Prerequisites

- Python 3.9 or higher
- Windows 10/11 (primary support)
- Google Gemini API key (free tier available)

### Step 1: Clone and Setup

```bash
git clone <repository-url>
cd hintly
```

### Step 2: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 3: Install Additional Dependencies

#### For OCR (Choose one):
- **Option A**: Install Tesseract OCR
  - Windows: Download from [GitHub](https://github.com/UB-Mannheim/tesseract/wiki)
  - Add to PATH: `C:\Program Files\Tesseract-OCR`
- **Option B**: Use screen-ocr (automatic fallback)

#### For Audio:
- Ensure your microphone is working
- For system audio capture on Windows, enable "Stereo Mix" in sound settings

### Step 4: Set Up Gemini API

1. Get a free API key from [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Set the environment variable:

**Windows:**
```cmd
set GEMINI_API_KEY=your_api_key_here
```

**Linux/Mac:**
```bash
export GEMINI_API_KEY=your_api_key_here
```

## Usage

### Starting the Assistant

```bash
python cluely_assistant.py
```

### Controls

- **Toggle Overlay**: `Ctrl + Alt + C` (default)
- **Voice Trigger**: `Ctrl + Alt + V` (optional)
- **Drag**: Click and drag the overlay to reposition
- **Minimize**: Click the `−` button to hide
- **Close**: Click the `×` button to exit

### How to Use

1. **Start the assistant** - It will appear in the top-right corner
2. **Join a meeting** - The assistant listens to audio and captures screen content
3. **Ask questions** - Type queries about the meeting, presentation, or screen content
4. **Get instant answers** - AI provides context-aware responses

### Example Queries

- "What's the main topic of this meeting?"
- "Summarize the key points from the presentation"
- "What code is currently on my screen?"
- "What questions should I ask about this topic?"
- "Help me understand this technical discussion"

## Configuration

Edit `config.py` to customize:

- **Hotkeys**: Change keyboard shortcuts
- **UI Settings**: Adjust overlay size, opacity, position
- **Audio Settings**: Modify recording duration, sample rate
- **OCR Settings**: Change capture intervals, confidence thresholds

## Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Screen Capture│    │  Audio Capture  │    │   Gemini API    │
│   (OCR)         │    │   (Whisper)     │    │   (AI)          │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         └───────────────────────┼───────────────────────┘
                                 │
                    ┌─────────────────┐
                    │  Main Assistant │
                    │   (Orchestrator)│
                    └─────────────────┘
                                 │
                    ┌─────────────────┐
                    │  Overlay UI     │
                    │  (PyQt5)        │
                    └─────────────────┘
```

## Privacy & Security

- **Local Processing**: Screen capture and audio transcription happen locally
- **Selective Sharing**: Only your query and necessary context are sent to Gemini
- **No Meeting Participation**: The assistant never joins calls or appears in recordings
- **Data Retention**: Audio transcripts are kept only in memory and cleared regularly

## Troubleshooting

### Common Issues

1. **"GEMINI_API_KEY not set"**
   - Ensure the environment variable is set correctly
   - Restart your terminal after setting the variable

2. **OCR not working**
   - Install Tesseract OCR or ensure screen-ocr is available
   - Check that text is visible and not too small

3. **Audio not capturing**
   - Check microphone permissions
   - Enable "Stereo Mix" for system audio capture
   - Ensure Whisper model downloaded successfully

4. **Overlay not appearing**
   - Check if another application is blocking it
   - Try the hotkey `Ctrl + Alt + C`
   - Restart the application

### Logs

Check `cluely_assistant.log` for detailed error information.

## Development

### Project Structure

```
hintly/
├── cluely_assistant.py    # Main application entry point
├── config.py             # Configuration settings
├── screen_capture.py     # OCR and screen capture
├── audio_capture.py      # Audio recording and transcription
├── gemini_client.py      # Google Gemini API integration
├── overlay_ui.py         # PyQt5 overlay interface
├── hotkey_manager.py     # Global hotkey handling
├── requirements.txt      # Python dependencies
└── README.md            # This file
```

### Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is open source. Please respect the privacy and security guidelines when using or modifying this software.

## Acknowledgments

- Inspired by [Cluely](https://cluely.ai)
- Built with Google Gemini API
- Uses OpenAI Whisper for speech recognition
- PyQt5 for the user interface

## Support

For issues and questions:
1. Check the troubleshooting section
2. Review the logs
3. Open an issue on GitHub

---

**Note**: This is a local-first implementation designed for personal use. Always respect privacy and security best practices when using AI assistants.
