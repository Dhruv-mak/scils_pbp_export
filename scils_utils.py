from scilslab import LocalSession
from dataclasses import dataclass
import pandas as pd
import numpy as np
from logger_service import logger


@dataclass
class FeatureList:
    name: str
    id: str
    num_features: str


@dataclass
class Region:
    name: str
    id: str

@dataclass
class Feature:
    name: str
    id: str


def region_dfs(rt, region_list):
    if rt.subregions == []:
        # region_table.loc[len(region_table)] = [rt.id, rt.name.split('/')[-1]]
        region_list.append(Region(id=rt.id, name=rt.name.split("/")[-1]))
    else:
        for subregion in rt.subregions:
            region_dfs(subregion, region_list)


def get_feature_lists(session: LocalSession, file_path: str) -> list[FeatureList]:
    """
    Get a list of feature lists from the specified SLX file.
    """
    feature_lists = []
    dataset = session.dataset_proxy
    feature_table = dataset.feature_table
    feature_list_df = feature_table.get_feature_lists()
    for feature in feature_list_df.iterrows():
        feature_data = feature[1]
        feature_lists.append(
            FeatureList(
                name=feature_data["name"],
                id=feature_data["id"],
                num_features=feature_data["num_features"],
            )
        )
    return feature_lists


def get_region_list(session: LocalSession, file_path: str) -> list[Region]:
    """
    Get a list of regions from the specified SLX file.
    """
    regions = []
    dataset = session.dataset_proxy
    region_tree = dataset.get_region_tree()
    region_dfs(region_tree, regions)
    return regions

def get_features_from_feature_list(file_path: str, feature_list_id: str) -> list[Feature]:
    pass


def generate_csv(
    slx_filepath: str,
    csv_filepath: str,
    region_list: list[Region],
    feature_list: FeatureList,
    export_progress: callable
):
    discarded_regions = []
    all_region_data = []

    with LocalSession(slx_filepath) as session:
        dataset = session.dataset_proxy
        feature_table = dataset.feature_table
        
        feature_df = feature_table.get_features(feature_list.id)

        features: list[Feature] = []
        for row in feature_df.iterrows():
            features.append(Feature(name=row[1]['name'], id=row[1]['id']))

        # Pre-determine all feature names for consistent column structure
        feature_names = [feature.name for feature in features]
        base_columns = ["spotId", "x", "y", "tissue_id"]
        all_columns = base_columns + feature_names

        for i, region in enumerate(region_list):
            logger.info_message.emit(f"Processing region {i + 1}/{len(region_list)}: {region.name}")
            export_progress.emit(i)
            
            region_spots = dataset.get_region_spots(region.id)

            # Convert to numpy arrays to ensure consistent data types
            region_spot_ids = np.array(region_spots.get("spot_id"))
            region_spot_x = np.array(region_spots.get("x"))
            region_spot_y = np.array(region_spots.get("y"))

            if len(region_spot_ids) == 0:
                print(f"Region id:{region.id} and Region name: {region.name} has no valid spots.")
                discarded_regions.append(region)
                continue

            # Pre-allocate data dictionary with all columns
            region_data = {
                "spotId": region_spot_ids,
                "x": region_spot_x,
                "y": region_spot_y,
                "tissue_id": [region.name.split("/")[-1]] * len(region_spot_ids)
            }
            
            # Initialize all feature columns with NaN
            for feature_name in feature_names:
                region_data[feature_name] = np.full(len(region_spot_ids), np.nan)

            # Create spot_id to index mapping for fast lookups
            spot_id_to_idx = {spot_id: idx for idx, spot_id in enumerate(region_spot_ids)}

            # Fill feature intensities efficiently
            for feature_row in features:
                feature_intensities = feature_table.get_feature_intensities(
                    feature_row.id, region.id
                )
                
                # Use vectorized operations instead of loops
                for spot_id, intensity in zip(feature_intensities.spot_ids, feature_intensities.values):
                    if spot_id in spot_id_to_idx:
                        idx = spot_id_to_idx[spot_id]
                        region_data[feature_row.name][idx] = intensity

            # Create DataFrame from complete data dictionary
            intermediate_df = pd.DataFrame(region_data, columns=all_columns)
            all_region_data.append(intermediate_df)

        # Concatenate all regions at once instead of incrementally
        if all_region_data:
            overall_df = pd.concat(all_region_data, ignore_index=True)
            overall_df.to_csv(csv_filepath, index=False)
        else:
            # Create empty DataFrame with correct columns if no data
            overall_df = pd.DataFrame(columns=all_columns)
            overall_df.to_csv(csv_filepath, index=False)