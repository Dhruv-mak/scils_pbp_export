from PyQt6.QtCore import QObject, pyqtSignal


from PyQt6.QtCore import QObject, pyqtSignal


class LoggerService(QObject):
    """
    Centralized logging service that can be used throughout the application
    """
    
    # Signals for different types of messages
    info_message = pyqtSignal(str)
    warning_message = pyqtSignal(str)
    error_message = pyqtSignal(str)
    debug_message = pyqtSignal(str)
    
    def __init__(self):
        super().__init__()
    
    def log_info(self, message: str):
        """Log an info message"""
        print(f"INFO: {message}")
        self.info_message.emit(message)
    
    def log_warning(self, message: str):
        """Log a warning message"""
        print(f"WARNING: {message}")
        self.warning_message.emit(message)
    
    def log_error(self, message: str):
        """Log an error message"""
        print(f"ERROR: {message}")
        self.error_message.emit(message)
    
    def log_debug(self, message: str):
        """Log a debug message"""
        print(f"DEBUG: {message}")
        self.debug_message.emit(message)


# Global logger instance - simple and reliable
logger = LoggerService()