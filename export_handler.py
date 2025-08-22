from PyQt6.QtCore import pyqtSignal, QObject
import time
from logger_service import logger
from scils_utils import generate_csv

class ExportHandler(QObject):
    export_finished = pyqtSignal()
    export_progress = pyqtSignal(int)

    def __init__(self):
        super().__init__()

    def start_export(self, regions, features, slx_file_path, csv_file_path):
        generate_csv(slx_file_path, csv_file_path, regions, features, export_progress=self.export_progress)
        self.export_finished.emit()