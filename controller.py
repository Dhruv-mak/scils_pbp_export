from PyQt6.QtWidgets import (
    QPushButton,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QFileDialog,
    QLineEdit,
    QComboBox,
    QMessageBox,
)
from Worker import Worker
from feature_loading_handler import FeatureLoadingHandler
from logger_service import logger
from export_handler import ExportHandler
from PyQt6.QtCore import pyqtSignal


class Controller(QWidget):
    """
    Controller class for managing the GUI inputs for the input slx, output csv location
    and the dropdown selection for the feature list
    """
    def __init__(self, threadpool):
        super().__init__()
        self.layout = QVBoxLayout()
        self.threadpool = threadpool
        
        # Initialize data handler
        self.data_handler = FeatureLoadingHandler()
        
        # Initialize data storage
        self.feature_lists = []
        self.regions = []

        # Simple vertical layout for all controls
        self.layout = QVBoxLayout()
        self.layout.setSpacing(15)
        self.layout.setContentsMargins(20, 20, 20, 20)
        
        # Input SLX File
        slx_layout = QHBoxLayout()
        slx_layout.setSpacing(10)
        slx_label = QLabel("📁 SLX File:")
        slx_label.setMinimumWidth(100)
        slx_label.setMaximumWidth(100)
        slx_layout.addWidget(slx_label)
        self.slx_file_path = QLineEdit()
        self.slx_file_path.setPlaceholderText("Select your SLX file...")
        self.slx_file_path.setReadOnly(True)
        slx_button = QPushButton("Browse")
        slx_button.setMinimumWidth(80)
        slx_button.setMaximumWidth(80)
        slx_button.clicked.connect(self.select_slx_file)
        slx_layout.addWidget(self.slx_file_path, 1)
        slx_layout.addWidget(slx_button)
        
        # Output CSV File
        csv_layout = QHBoxLayout()
        csv_layout.setSpacing(10)
        csv_label = QLabel("💾 CSV File:")
        csv_label.setMinimumWidth(100)
        csv_label.setMaximumWidth(100)
        csv_layout.addWidget(csv_label)
        self.csv_file_path = QLineEdit()
        self.csv_file_path.setPlaceholderText("Select output location...")
        self.csv_file_path.setReadOnly(True)
        csv_button = QPushButton("Browse")
        csv_button.setMinimumWidth(80)
        csv_button.setMaximumWidth(80)
        csv_button.clicked.connect(self.select_csv_file)
        csv_layout.addWidget(self.csv_file_path, 1)
        csv_layout.addWidget(csv_button)
        
        # Feature List
        feature_layout = QHBoxLayout()
        feature_layout.setSpacing(10)
        feature_label = QLabel("🎯 Feature List:")
        feature_label.setMinimumWidth(100)
        feature_label.setMaximumWidth(100)
        feature_layout.addWidget(feature_label)
        self.feature_combo_box = QComboBox()
        self.feature_combo_box.setPlaceholderText("Select Feature...")
        self.feature_combo_box.setEnabled(False)
        feature_layout.addWidget(self.feature_combo_box, 1)
        
        # Run Button
        self.run_button = QPushButton("🚀 Start Export")
        self.run_button.setObjectName("primaryButton")
        
        # Add all layouts to main layout
        self.layout.addLayout(slx_layout)
        self.layout.addLayout(csv_layout)
        self.layout.addLayout(feature_layout)
        self.layout.addWidget(self.run_button)

        self._setup_signals()
        self.setLayout(self.layout)
    
    def _setup_signals(self):
        """Connect signals from data handler to GUI methods"""
        self.data_handler.features_loaded.connect(self._on_features_loaded)
        self.data_handler.error_occurred.connect(self._on_error_occurred)
        self.data_handler.warning_occurred.connect(self._on_warning_occurred)
        self.feature_combo_box.currentIndexChanged.connect(self.handle_index_change)
    
    def handle_index_change(self):
        print(self.feature_combo_box.currentIndex())

    def _on_features_loaded(self, feature_lists, regions):
        """Handle successful feature loading - runs on main thread"""
        self.feature_lists = feature_lists
        self.regions = regions
        message = f"Features found: {len(self.feature_lists)}"
        print(message)
        logger.log_info(message)

        self.feature_combo_box.setEnabled(True)
        self.feature_combo_box.clear()
        self.feature_combo_box.addItems([feature_list.name for feature_list in self.feature_lists])
    
    def _on_error_occurred(self, error_type, message):
        """Handle errors - runs on main thread"""
        logger.log_error(message)
        QMessageBox.critical(
            self,
            "Error: File open somewhere!!",
            message,
            defaultButton=QMessageBox.StandardButton.Ok
        )
    
    def _on_warning_occurred(self, message, total_regions, unique_regions):
        """Handle warnings - runs on main thread"""
        warning_message = f"{message}\nTotal Regions: {total_regions}, Unique Regions: {unique_regions}"
        logger.log_warning(warning_message)
        QMessageBox.warning(
            self,
            "Warning: Duplicate region names found!!",
            warning_message,
            defaultButton=QMessageBox.StandardButton.Ok
        )
    
    def update_progress(self, value):
        self.export_progress.emit(value)

    def get_region_length(self):
        if hasattr(self, 'regions'):
            return len(self.regions)
        return 0
    
    def get_region_list(self):
        if hasattr(self, 'regions'):
            return self.regions
        return []

    def get_feature_lists(self):
        if hasattr(self, 'feature_lists'):
            return self.feature_lists
        return []

    def get_slx_filepath(self):
        if hasattr(self, 'slx_file_path'):
            return self.slx_file_path.text()
        return ""
    
    def get_csv_filepath(self):
        if hasattr(self, 'csv_file_path'):
            return self.csv_file_path.text()
        return ""

    def load_features_from_file(self, file_path):
        """Load features using the data handler in a worker thread"""
        if not file_path:
            self.feature_combo_box.setEnabled(False)
            return
        
        logger.log_info(f"Starting to load features from: {file_path}")
        worker = Worker(self.data_handler.load_features_and_regions, file_path)
        self.threadpool.start(worker)

    def select_slx_file(self):
        file_dialog = QFileDialog()
        file_dialog.setFileMode(QFileDialog.FileMode.ExistingFile)
        file_dialog.setNameFilter("SLX files (*.slx)")
        file_dialog.fileSelected.connect(self.load_features_from_file)
        if file_dialog.exec():
            selected_file = file_dialog.selectedFiles()[0]
            self.slx_file_path.setText(selected_file)
            logger.log_info(f"Selected SLX file: {selected_file}")  # Test logging

    def select_csv_file(self):
        file_dialog = QFileDialog()
        file_dialog.setFileMode(QFileDialog.FileMode.AnyFile)
        file_dialog.setNameFilter("CSV files (*.csv)")
        if file_dialog.exec():
            selected_file = file_dialog.selectedFiles()[0]
            self.csv_file_path.setText(selected_file)