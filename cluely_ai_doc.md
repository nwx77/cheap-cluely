# Building a Cluely-like AI Desktop Assistant (using Gemini API and Vibe Coding)

Cluely is an **"undetectable" desktop AI assistant** that listens to
meetings and on-screen content, then gives real-time answers. It "just
thinks for you" in every conversation. Our goal is to recreate Cluely's
core functionality in a free, local-first tool using Python (or a
similar environment) plus Google's Gemini API (with user-supplied API
keys). The key features to implement include: capturing on-screen text
via OCR, capturing audio and transcribing it, sending context to Gemini
for answers, and displaying a hidden always-on-top overlay UI. We'll use
a vibe coding (AI-assisted) approach to speed development.

![Cluely Interface](https://example.com/cluely.png) *Figure: Cluely's
desktop interface (from its website). The AI assistant appears as a
**translucent, always-on-top overlay**. It listens to your meeting and
screen context and provides instant answers.*

## Key Features to Implement

-   **Context capture**: Read on-screen text (presentations, chat, code,
    etc.) using OCR, and listen to meeting audio for speech recognition.
    Cluely "responds with context of what's happening in a conversation
    and what's on your screen."\
-   **Invisible overlay UI**: Show results in a small, hideable overlay
    window. The overlay should be always-on-top and semi-transparent, so
    it doesn't block work. Cluely's UI is described as *"translucent and
    hideable"* and **"never in your way"**.\
-   **Real-time AI responses**: On each prompt, send the collected
    context and user query to Gemini (e.g. the `gemini-2.0-flash`
    model). Display Gemini's answer instantly. This mimics Cluely's
    **live answer** behavior.\
-   **Invisibility to others**: The assistant must not join or appear in
    the meeting. Do not share or project the overlay. Cluely "never
    joins your meetings" and is *"invisible to others"*. We will ensure
    our tool only listens to system audio/mic, never becoming a meeting
    participant or visible in screen shares.

## Development Approach: Vibe Coding

We can use a **vibe coding** (AI-assisted coding) workflow to build this
app faster. For example, on a platform like Replit you could describe:
"Build a Python desktop app that captures the current screen text and
audio, then uses Google's Gemini API to answer user prompts in real
time," and let an AI agent generate scaffolding code. The process is
iterative: describe a feature in plain language, let the AI write the
code, test it, and refine. This approach lets us focus on the
functionality (ideas and logic) while the AI handles boilerplate.

## Step 1: Set Up the Development Environment

1.  **Install Python and libraries.** Use Python 3.9+ on your machine.
    Create a virtual environment and install required packages:
    -   **Google GenAI SDK:** `pip install -U google-genai`. This
        provides the Gemini API client.\
    -   **OCR support:** e.g. install `screen-ocr`
        (`pip install screen-ocr`) or `pytesseract` (requires
        Tesseract). The `screen-ocr` package is designed to perform OCR
        on screen regions easily.\
    -   **Speech-to-text:** install OpenAI Whisper
        (`pip install -U openai-whisper`) or another STT library.
        Whisper allows local transcription of audio with commands like
        `model = whisper.load_model("small")` and
        `result = model.transcribe("audio.wav")`.\
    -   **GUI library:** e.g. PyQt5 or PySide6 for the overlay window
        (`pip install PyQt5`). You can also use Tkinter (built-in) or
        other frameworks.\
    -   **Others:** If using system audio capture on Windows, PyAudio or
        sounddevice may help (`pip install sounddevice`). For global
        hotkeys, the `keyboard` library can register triggers
        (`pip install keyboard`).
2.  **Set up the Gemini API key.** Obtain a free Gemini API key from
    Google AI Studio. Set it as an environment variable,
    e.g. `export GEMINI_API_KEY=your_key`, so the GenAI client library
    picks it up automatically.

## Step 2: Capture Screen Text (OCR)

Use a screen-capture + OCR approach to read any visible text on the
screen. For example, with the `screen-ocr` library you can easily grab
the entire screen or a region and get text:

``` python
from screen_ocr import Reader
reader = Reader()
text = reader.read_screen()  # captures current screen and runs OCR
```

Alternatively, you can use Pillow or PyAutoGUI to grab a screenshot and
feed it to Tesseract:

``` python
from PIL import ImageGrab
import pytesseract

im = ImageGrab.grab()               # take full-screen screenshot
text = pytesseract.image_to_string(im)
```

Collect this text as "screen context." Cluely uses this context to
answer questions about slides, code, or chat on your screen. Be sure to
handle cases where the screen content changes; you might capture in a
loop or only when a prompt is activated.

## Step 3: Capture and Transcribe Audio

Next, capture meeting audio (microphone or system output) and transcribe
it. For a **local-first** approach, record audio locally using Python.
For example: - On Windows, enable "Stereo Mix" or use sounddevice with
WASAPI to capture system audio.\
- On all platforms, you could simply use the mic (`sounddevice`) if
speakers play meeting audio out loud.

Once you have an audio stream, feed it to Whisper or another ASR engine.
Using Whisper in Python:

``` python
import whisper
model = whisper.load_model("small")
result = model.transcribe("meeting_audio.wav")  # or pass an audio array
transcript = result["text"]
```

This gives you the conversation transcript. Cluely "listens to your
meetings in the background and takes real-time notes." You'll use this
transcript as part of the context for Gemini. (If low latency is needed,
consider streaming chunks or using Whisper's streaming capabilities.)

## Step 4: Integrate Google Gemini API

Combine the captured screen text, the transcribed audio, and any user
prompt into a single context string, then query Gemini. Using the Google
GenAI SDK in Python:

``` python
from google import genai
client = genai.Client()  # picks up GEMINI_API_KEY from env
prompt = f"{audio_context}\n{screen_context}\nUser: {user_query}\nAssistant:"
response = client.models.generate_content(
    model="gemini-2.0-flash",
    contents=prompt
)
answer = response.text
```

This is analogous to the quickstart example, which shows
`client.models.generate_content(model="gemini-2.5-flash", contents="…")`.
In our case we use the `gemini-2.0-flash` model (for free usage with a
personal key) and include our combined context. Gemini will respond with
a helpful answer based on the meeting context. Display `answer` in the
overlay UI.

## Step 5: Build the Overlay UI

Create a small GUI window that floats over all other apps. Using PyQt5
(for example), you can make a frameless, semi-transparent window:

``` python
from PyQt5 import QtWidgets, QtCore
app = QtWidgets.QApplication([])
window = QtWidgets.QWidget()
# Always on top, no window frame
window.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint | QtCore.Qt.FramelessWindowHint)
# Transparent background
window.setAttribute(QtCore.Qt.WA_TranslucentBackground)
```

Inside this window, add a text input (for user queries) and a text
display area for the answer. You can style it lightly so it looks like
an overlay widget. The user can invoke it via a global hotkey or voice
command. When the assistant is idle, keep it hidden or minimized. As
Cluely's documentation states, the assistant's window is *"translucent
and hideable"* and is "never in your way." Implement show/hide
functionality (e.g. pressing a hotkey toggles the window's visibility).

## Step 6: Prompt-Response Loop

Wire everything together: when the user enters a query (or uses a voice
trigger), do the following steps in order:

1.  **Gather context**: Capture the latest screen text and recent audio
    transcript since the last query.
2.  **Call the AI**: Form the prompt (context + user question) and send
    it to Gemini as shown above. Wait for the `answer`.\
3.  **Display the answer**: Show Gemini's response in the overlay.
    Optionally highlight keywords, or allow the user to copy the answer
    text.\
4.  **Continue listening**: After responding, continue running the
    background capture so you're ready for the next question.

You may implement this loop in a background thread or async callbacks so
the UI stays responsive. Check for errors (e.g. network or API limits)
and handle them gracefully. Over time, refine the prompts sent to Gemini
to get the best context-aware answers.

## Step 7: Ensure Invisibility and Local-First Operation

Finally, make sure the assistant remains **invisible to others**. Do not
join the video call or share the overlay screen. Cluely's site
emphasizes it "never joins your meetings" so that there are no bot
participants, and it remains *"invisible to others"*. In practice,
simply run this app as a regular program (not as a virtual camera or
participant) and capture audio via the OS---then no one on the call sees
it. All processing (screen capture, transcription, UI) happens on the
local machine, except the call to Gemini's cloud API. By letting users
bring their own Gemini key, the app itself has no usage cost.

On privacy: since we're capturing sensitive screen and audio locally, be
sure to handle data securely. Do not send any context to Gemini except
what's needed for the query (and remind users that their own prompt and
any captured transcript goes to Google's servers).

## Testing and Deployment

Test the app by running it during a mock video call or presentation.
Verify that the overlay appears correctly and Gemini provides relevant
answers. Make sure the overlay truly hides when not needed and does not
interfere with normal workflows. Once stable, you can package the Python
app with PyInstaller or similar for easy distribution, or deploy in a
Replit/desktop environment as desired.

**Summary:** By following the above steps, you can build a local desktop
AI assistant similar to Cluely. We leverage Python (or any language of
choice) to capture screen and audio context, use the free Google Gemini
API (with user-provided keys) for AI processing, and create an
always-on-top overlay UI to interact. A vibe coding approach can speed
development. The result is a context-aware, real-time assistant that
works across any meeting platform, just as Cluely does.
