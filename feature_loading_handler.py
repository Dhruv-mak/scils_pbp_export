from PyQt6.QtCore import QObject, pyqtSignal
from scilslab import LocalSession
from scils_utils import get_feature_lists, get_region_list


class FeatureLoadingHandler(QObject):
    """Handles data operations separately from GUI"""

    # Signals to communicate with the main thread
    features_loaded = pyqtSignal(list, list)  # features, regions
    error_occurred = pyqtSignal(str, str)  # error_type, message
    warning_occurred = pyqtSignal(
        str, int, int
    )  # message, total_regions, unique_regions

    def load_features_and_regions(self, file_path):
        """Load features and regions from SLX file - runs in worker thread"""
        print(f"Loading features from: {file_path}")

        if not file_path:
            return

        try:
            session = LocalSession(file_path)
            features = get_feature_lists(session, file_path)
            regions = get_region_list(session, file_path)

            print(f"Found {len(regions)} leaf regions")

            # Check for duplicate region names
            region_name_set = set([region.name for region in regions])
            if len(region_name_set) != len(regions):
                self.warning_occurred.emit(
                    f"Duplicate region names found in the SLX file. Please ensure all region names are unique to avoid issues.",
                    len(regions),
                    len(region_name_set),
                )

            session.close()
            self.features_loaded.emit(features, regions)

        except Exception as e:
            self.error_occurred.emit(
                "file_access_error",
                f"The file {file_path} is already open in SCiLS Lab or another application. Please close it and try again.",
            )
            print("Error occurred while getting features:", e)
