import sys
import logging
from typing import Optional, Callable
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, 
    QTextEdit, QLineEdit, QPushButton, QLabel, QFrame
)
from PyQt5.QtCore import Qt, QTimer, pyqtSignal, QThread, pyqtSlot, QRectF
from PyQt5.QtGui import QFont, QPalette, QColor, QPainter, QPainterPath
from config import Config

class OverlayUI(QWidget):
    """Translucent, always-on-top overlay UI for the AI assistant"""
    
    # Signals
    query_submitted = pyqtSignal(str)  # Emitted when user submits a query
    toggle_requested = pyqtSignal()    # Emitted when toggle is requested
    
    def __init__(self):
        super().__init__()
        self.logger = logging.getLogger(__name__)
        self.is_visible = False
        self.setup_ui()
        self.setup_window_properties()
    
    def setup_window_properties(self):
        """Setup window properties for overlay behavior"""
        # Always on top, no window frame, translucent background
        self.setWindowFlags(
            Qt.WindowStaysOnTopHint | 
            Qt.FramelessWindowHint | 
            Qt.Tool  # Prevents taskbar icon
        )
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setAttribute(Qt.WA_ShowWithoutActivating)
        
        # Set size and position
        self.resize(Config.OVERLAY_WIDTH, Config.OVERLAY_HEIGHT)
        self.move_to_corner()
    
    def setup_ui(self):
        """Setup the user interface"""
        # Main layout
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(8)
        
        # Title bar
        title_bar = self.create_title_bar()
        main_layout.addWidget(title_bar)
        
        # Response display area
        self.response_display = QTextEdit()
        self.response_display.setReadOnly(True)
        self.response_display.setMaximumHeight(150)
        self.response_display.setStyleSheet(self.get_text_edit_style())
        main_layout.addWidget(self.response_display)
        
        # Input area
        input_layout = QHBoxLayout()
        
        self.query_input = QLineEdit()
        self.query_input.setPlaceholderText("Ask me anything...")
        self.query_input.returnPressed.connect(self.submit_query)
        self.query_input.setStyleSheet(self.get_input_style())
        input_layout.addWidget(self.query_input)
        
        self.submit_button = QPushButton("Ask")
        self.submit_button.clicked.connect(self.submit_query)
        self.submit_button.setStyleSheet(self.get_button_style())
        input_layout.addWidget(self.submit_button)
        
        main_layout.addLayout(input_layout)
        
        # Status bar
        self.status_label = QLabel("Ready")
        self.status_label.setStyleSheet(self.get_status_style())
        main_layout.addWidget(self.status_label)
        
        # Apply main widget styling
        self.setStyleSheet(self.get_main_style())
    
    def create_title_bar(self) -> QWidget:
        """Create the title bar with controls"""
        title_bar = QWidget()
        title_layout = QHBoxLayout(title_bar)
        title_layout.setContentsMargins(0, 0, 0, 0)
        
        # Title
        title_label = QLabel("🤖 Cluely AI Assistant")
        title_label.setStyleSheet(self.get_title_style())
        title_layout.addWidget(title_label)
        
        title_layout.addStretch()
        
        # Control buttons
        self.minimize_button = QPushButton("−")
        self.minimize_button.setFixedSize(20, 20)
        self.minimize_button.clicked.connect(self.hide_overlay)
        self.minimize_button.setStyleSheet(self.get_control_button_style())
        title_layout.addWidget(self.minimize_button)
        
        self.close_button = QPushButton("×")
        self.close_button.setFixedSize(20, 20)
        self.close_button.clicked.connect(self.close)
        self.close_button.setStyleSheet(self.get_control_button_style())
        title_layout.addWidget(self.close_button)
        
        return title_bar
    
    def move_to_corner(self):
        """Move the overlay to the top-right corner"""
        screen = QApplication.primaryScreen().geometry()
        x = screen.width() - self.width() - 20
        y = 20
        self.move(x, y)
    
    def show_overlay(self):
        """Show the overlay"""
        if not self.is_visible:
            self.show()
            self.is_visible = True
            self.query_input.setFocus()
            self.logger.info("Overlay shown")
    
    def hide_overlay(self):
        """Hide the overlay"""
        if self.is_visible:
            self.hide()
            self.is_visible = False
            self.logger.info("Overlay hidden")
    
    def toggle_overlay(self):
        """Toggle overlay visibility"""
        if self.is_visible:
            self.hide_overlay()
        else:
            self.show_overlay()
    
    def submit_query(self):
        """Submit the current query"""
        query = self.query_input.text().strip()
        if query:
            self.query_submitted.emit(query)
            self.query_input.clear()
            self.set_status("Processing...")
    
    def set_response(self, response: str):
        """Set the response text"""
        self.response_display.setPlainText(response)
        self.set_status("Ready")
    
    def set_status(self, status: str):
        """Set the status text"""
        self.status_label.setText(status)
    
    def set_error(self, error: str):
        """Set an error message"""
        self.response_display.setPlainText(f"Error: {error}")
        self.set_status("Error")
    
    def set_loading(self):
        """Set loading state"""
        self.response_display.setPlainText("Thinking...")
        self.set_status("Processing...")
    
    # Styling methods
    def get_main_style(self) -> str:
        return """
        QWidget {
            background-color: rgba(30, 30, 30, 0.9);
            color: white;
            border-radius: 10px;
            border: 1px solid rgba(255, 255, 255, 0.2);
        }
        """
    
    def get_title_style(self) -> str:
        return """
        QLabel {
            color: #00ff88;
            font-weight: bold;
            font-size: 14px;
        }
        """
    
    def get_text_edit_style(self) -> str:
        return """
        QTextEdit {
            background-color: rgba(20, 20, 20, 0.8);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 5px;
            padding: 5px;
            color: #e0e0e0;
            font-size: 12px;
        }
        """
    
    def get_input_style(self) -> str:
        return """
        QLineEdit {
            background-color: rgba(20, 20, 20, 0.8);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 5px;
            padding: 8px;
            color: white;
            font-size: 12px;
        }
        QLineEdit:focus {
            border: 1px solid #00ff88;
        }
        """
    
    def get_button_style(self) -> str:
        return """
        QPushButton {
            background-color: #00ff88;
            color: black;
            border: none;
            border-radius: 5px;
            padding: 8px 16px;
            font-weight: bold;
            font-size: 12px;
        }
        QPushButton:hover {
            background-color: #00cc6a;
        }
        QPushButton:pressed {
            background-color: #00994d;
        }
        """
    
    def get_control_button_style(self) -> str:
        return """
        QPushButton {
            background-color: rgba(255, 255, 255, 0.1);
            color: white;
            border: none;
            border-radius: 10px;
            font-weight: bold;
        }
        QPushButton:hover {
            background-color: rgba(255, 255, 255, 0.2);
        }
        """
    
    def get_status_style(self) -> str:
        return """
        QLabel {
            color: #888888;
            font-size: 10px;
            font-style: italic;
        }
        """
    
    def paintEvent(self, event):
        """Custom paint event for rounded corners and transparency"""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # Create rounded rectangle path
        path = QPainterPath()
        path.addRoundedRect(QRectF(self.rect()), Config.OVERLAY_CORNER_RADIUS, Config.OVERLAY_CORNER_RADIUS)
        
        # Fill with semi-transparent background
        painter.fillPath(path, QColor(30, 30, 30, int(255 * Config.OVERLAY_OPACITY)))
    
    def mousePressEvent(self, event):
        """Handle mouse press for window dragging"""
        if event.button() == Qt.LeftButton:
            self.drag_position = event.globalPos() - self.frameGeometry().topLeft()
            event.accept()
    
    def mouseMoveEvent(self, event):
        """Handle mouse move for window dragging"""
        if event.buttons() == Qt.LeftButton and hasattr(self, 'drag_position'):
            self.move(event.globalPos() - self.drag_position)
            event.accept()
