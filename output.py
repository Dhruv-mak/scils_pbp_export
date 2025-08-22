from PyQt6.QtWidgets import (
    QProgressBar,
    QLabel,
    QPlainTextEdit,
    QWidget,
    QVBoxLayout
)
from PyQt6.QtCore import pyqtSignal
from PyQt6.QtGui import QTextCursor

class OutputWidget(QWidget):

    def __init__(self, region_length):
        super().__init__()

        layout = QVBoxLayout()
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)

        # Progress Bar
        layout.addWidget(QLabel("📊 Export Progress"))
        self.progress_bar = QProgressBar()
        self.progress_bar.setTextVisible(True)
        self.progress_bar.setFormat("%p% - %v/%m regions processed")
        layout.addWidget(self.progress_bar)

        # Log Display
        layout.addWidget(QLabel("📋 Process Log"))
        self.log_display = QPlainTextEdit()
        self.log_display.setReadOnly(True)
        self.log_display.setPlaceholderText("Export logs will appear here...")
        layout.addWidget(self.log_display)

        self.setLayout(layout)
    
    def update_progress(self, value):
        self.progress_bar.setValue(value)
    
    def append_log(self, message):
        self.log_display.appendPlainText(message)
        # Auto-scroll to the bottom
        self._scroll_to_bottom()
    
    def _scroll_to_bottom(self):
        """Helper method to scroll to bottom"""
        cursor = self.log_display.textCursor()
        cursor.movePosition(QTextCursor.MoveOperation.End)
        self.log_display.setTextCursor(cursor)
    
    def append_info(self, message):
        """Append info message with timestamp"""
        from datetime import datetime
        timestamp = datetime.now().strftime("%H:%M:%S")
        formatted_message = f"[{timestamp}] ℹ️  {message}"
        self.append_log(formatted_message)
    
    def append_warning(self, message):
        """Append warning message with timestamp"""
        from datetime import datetime
        timestamp = datetime.now().strftime("%H:%M:%S")
        formatted_message = f"[{timestamp}] ⚠️  {message}"
        self.append_log(formatted_message)
    
    def append_error(self, message):
        """Append error message with timestamp"""
        from datetime import datetime
        timestamp = datetime.now().strftime("%H:%M:%S")
        formatted_message = f"[{timestamp}] ❌ {message}"
        self.append_log(formatted_message)
    
    def append_debug(self, message):
        """Append debug message with timestamp"""
        from datetime import datetime
        timestamp = datetime.now().strftime("%H:%M:%S")
        formatted_message = f"[{timestamp}] 🔍 {message}"
        self.append_log(formatted_message)