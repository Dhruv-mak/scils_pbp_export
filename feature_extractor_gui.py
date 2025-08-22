from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QVBoxLayout,
    QPushButton,
    QWidget,
    QMessageBox,
    QStatusBar,
)
import os
from PyQt6.QtCore import QThreadPool, QTimer
from PyQt6.QtGui import QIcon
from controller import Controller
from output import OutputWidget
from logger_service import logger
import sys
from export_handler import ExportHandler
from Worker import Worker


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("🎯 Pixel By Pixel Exporter")
        
        # Set window sizing
        self.setMinimumSize(800, 600)
        self.resize(1000, 700)
        
        # Center the window on screen
        self._center_window()
        
        # Add status bar
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("Ready to export pixel data", 5000)
        
        self.ThreadPool = QThreadPool()
        self.export_handler = ExportHandler()
        self._setup_ui()
        
        # Welcome timer
        self._show_welcome_message()
        
    def _show_welcome_message(self):
        """Show a welcome message after a short delay"""
        timer = QTimer()
        timer.singleShot(1000, lambda: self.status_bar.showMessage(
            "Welcome! Select your SLX file to get started.", 10000))
        
    def _center_window(self):
        """Center the window on the screen"""
        from PyQt6.QtGui import QGuiApplication
        screen = QGuiApplication.primaryScreen().geometry()
        window = self.geometry()
        x = (screen.width() - window.width()) // 2
        y = (screen.height() - window.height()) // 2
        self.move(x, y)

    def handle_export_progress(self, value):
        """Handle export progress updates"""
        self.output.update_progress(value)

    def handle_export_finished(self):
        logger.info_message.emit("Export Finished!")
        self.status_bar.showMessage("✅ Export completed successfully!", 10000)
        QMessageBox.information(
            self, "Export Complete", "The export process has finished successfully."
        )

    def handle_export(self):
        logger.info_message.emit("Export Started!")
        self.status_bar.showMessage("🚀 Export in progress...", 0)
        regions = self.controller.get_region_list()
        if len(regions) == 0:
            self.status_bar.showMessage("❌ No regions found", 5000)
            QMessageBox.warning(
                self,
                "No Regions",
                "No regions found in the SLX file. Please add regions and try again.",
            )
            return
        self.output.progress_bar.setRange(0, len(regions) - 1)
        feature_lists = self.controller.get_feature_lists()
        if len(feature_lists) == 0:
            QMessageBox.warning(
                self,
                "No Features",
                "No Features found in the SLX file. Please add features and try again.",
            )
            return
        if self.controller.feature_combo_box.currentIndex() < 0:
            QMessageBox.critical(
                self,
                "No Feature List Selected",
                "Please select a feature list to export.",
            )
            return
        worker = Worker(
            self.export_handler.start_export,
            regions,
            feature_lists[self.controller.feature_combo_box.currentIndex()],
            self.controller.get_slx_filepath(),
            self.controller.get_csv_filepath(),
        )
        self.ThreadPool.start(worker)

    def _setup_ui(self):
        from PyQt6.QtWidgets import QVBoxLayout
        
        # Create simple vertical layout
        main_layout = QVBoxLayout()
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(20, 20, 20, 20)
        
        # Create main widget
        main_widget = QWidget()
        main_widget.setLayout(main_layout)
        
        # Create controller widget
        self.controller = Controller(self.ThreadPool)
        self.controller.run_button.clicked.connect(self.handle_export)
        
        # Create output widget
        self.output = OutputWidget(self.controller.get_region_length())
        
        # Add widgets to layout
        main_layout.addWidget(self.controller)
        main_layout.addWidget(self.output, 1)  # Give output most of the space
        
        # Set main widget
        self.setCentralWidget(main_widget)
        self._setup_signals()

    def _setup_signals(self):
        logger.info_message.connect(self.output.append_info)
        logger.warning_message.connect(self.output.append_warning)
        logger.error_message.connect(self.output.append_error)
        logger.debug_message.connect(self.output.append_debug)

        # Export signals
        self.export_handler.export_progress.connect(self.handle_export_progress)
        self.export_handler.export_finished.connect(self.handle_export_finished)


if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Get the correct path for both development and compiled versions
    if getattr(sys, 'frozen', False):
        # Running as compiled executable
        base_path = sys._MEIPASS
    else:
        # Running as script
        base_path = os.path.dirname(os.path.abspath(__file__))
    
    style_path = os.path.join(base_path, "static", "style.qss")
    
    try:
        with open(style_path, 'r') as f:
            _style = f.read()
        app.setStyleSheet(_style)
    except FileNotFoundError:
        print(f"Warning: Could not load style file from {style_path}")
        # Continue without styling
    
    window = MainWindow()
    window.show()
    sys.exit(app.exec())