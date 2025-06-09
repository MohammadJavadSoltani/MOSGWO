import geopandas as gpd
import numpy as np
import math
import matplotlib.pyplot as plt
from scipy.stats import zscore
import pandas as pd
import os
from matplotlib.patches import Patch

def Geometric_Acc(segments_Path, reference_Path, output_folder, K_Factor):
    """
    Calculate geometric accuracy metrics between segmentation results and reference polygons.
    
    Computes:
    - Intersection-over-Union (IoU) per polygon
    - Weighted mean IoU (area-weighted)
    - F1-score per class
    - Over-segmentation factor (OSF)
    - Eliminated polygon analysis

    Args:
        segments_Path (str): Path to segmented polygons shapefile
        reference_Path (str): Path to ground truth reference shapefile
        output_folder (str): Directory to save outputs (CSVs/plots)
        K_Factor (float): Normalization factor for over-segmentation (typically 1-10)

    Returns:
        dict: Dictionary containing:
            - mean_iou (float)
            - weighted_mean_iou (float)
            - average_f1_score (float)
            - num_eliminated_polygons (float)
            - over_segmentation_factor (float)

    Output Files:
        - eliminated_polygons.csv: Outliers with low IoU
        - conf_matrix.csv: Class-wise metrics
        - iou_plot.png: Visual IoU distribution

    Example:
        >>> metrics = Geometric_Acc(
        ...     "results/segments.shp",
        ...     "ground_truth.shp",
        ...     "output_analysis",
        ...     K_Factor=2.5
        ... )
    """
    print(f"Geometric_Acc Called for Wolf: {output_folder}")

    # CSV File Paths
    output_csv = os.path.join(output_folder, "eliminated_polygons.csv")
    conf_matrix_csv = os.path.join(output_folder, "conf_matrix.csv")
    plot_output_path = os.path.join(output_folder, "iou_plot.png")

    # Step 1: Load Shapefiles
    try:
        segments_gdf = gpd.read_file(segments_Path)
        reference_gdf = gpd.read_file(reference_Path)
    except Exception as e:
        print(f"Failed to read shapefiles: {e}")
        return {}

    # Step 2: CRS Check & Fix
    if segments_gdf.crs != reference_gdf.crs:
        reference_gdf = reference_gdf.to_crs(segments_gdf.crs)
    if segments_gdf.crs.is_geographic:
        segments_gdf = segments_gdf.to_crs(epsg=32639)  # UTM Zone 39N
        reference_gdf = reference_gdf.to_crs(epsg=32639)

    # Step 3: Geometry Validation
    segments_gdf = segments_gdf[segments_gdf.geometry.is_valid & ~segments_gdf.geometry.is_empty]
    reference_gdf = reference_gdf[reference_gdf.geometry.is_valid & ~reference_gdf.geometry.is_empty]

    print(f"Segments Count: {len(segments_gdf)}, References Count: {len(reference_gdf)}")

    iou_values = {}
    weighted_iou_values = []
    eliminated_polygons = []
    over_segmentation_values = []

    # Step 4: IoU Calculation
    for ref_idx, ref_row in reference_gdf.iterrows():
        ref_geom = ref_row.geometry
        ref_area = ref_geom.area

        # Find intersecting segments
        intersecting_segments = segments_gdf[segments_gdf.geometry.intersects(ref_geom)].copy()
        intersecting_segments['intersection_area'] = intersecting_segments.geometry.apply(
            lambda seg: seg.intersection(ref_geom).area if seg.is_valid else 0
        )
        intersecting_segments['segment_area'] = intersecting_segments.geometry.area
        intersecting_segments['overlap_ratio'] = intersecting_segments['intersection_area'] / intersecting_segments['segment_area']

        significant_segments = intersecting_segments[intersecting_segments['overlap_ratio'] > 0.5]
        over_segmentation_values.append(len(significant_segments))

        if not significant_segments.empty:
            combined_geometry = significant_segments.geometry.unary_union
            intersection_area = combined_geometry.intersection(ref_geom).area
            union_area = combined_geometry.union(ref_geom).area
            iou = intersection_area / union_area if union_area > 0 else 0
            iou_values[ref_idx] = iou
            weighted_iou_values.append(iou * ref_area)
        else:
            if not intersecting_segments.empty:
                most_representative = intersecting_segments.loc[
                    intersecting_segments['intersection_area'].idxmax()
                ]
                intersection_area = most_representative.geometry.intersection(ref_geom).area
                union_area = most_representative.geometry.union(ref_geom).area
                iou = intersection_area / union_area if union_area > 0 else 0
                iou_values[ref_idx] = iou
                weighted_iou_values.append(iou * ref_area)
            else:
                iou_values[ref_idx] = 0

    # Step 5: Over-Segmentation Factor
    total_polygons = len(reference_gdf)
    over_segmentation_factor = sum(
        [max(0, count - 1) for count in over_segmentation_values]
    ) / (total_polygons * K_Factor)  
    print(f"Over-Segmentation Factor: {over_segmentation_factor}")

    # Step 6: Eliminated Polygons (Outliers based on IoU)
    iou_array = np.array(list(iou_values.values()))
    if len(iou_array) > 0:
        z_scores = zscore(iou_array)
        for idx, z in zip(iou_values.keys(), z_scores):
            if z < -2:  # IoU lower than -2 standard deviations
                eliminated_polygons.append({
                    "Polygon_Index": idx,
                    "IoU": iou_values[idx],
                    "Z_Score": z,
                    "Layer": reference_gdf.loc[idx, "layer"] if "layer" in reference_gdf.columns else "Unknown"
                })

    num_eliminated_polygons = len(eliminated_polygons) / math.sqrt(total_polygons)

    print(f"Eliminated Polygons Factor: {num_eliminated_polygons}")

    # Save eliminated polygons to CSV
    if eliminated_polygons:
        eliminated_df = pd.DataFrame(eliminated_polygons)
        eliminated_df.to_csv(output_csv, index=False)
        print(f"Eliminated polygons CSV saved: {output_csv}")
    else:
        print("No polygons eliminated.")

    # Step 7: Weighted Mean IoU
    total_area = reference_gdf.geometry.area.sum()
    weighted_mean_iou = sum(weighted_iou_values) / total_area if total_area > 0 else 0
    print(f"Weighted Mean IoU: {weighted_mean_iou}")

    # Step 8: Confusion Matrix (Layer Metrics)
    reference_gdf['IoU'] = reference_gdf.index.map(iou_values).fillna(0)
    layer_metrics = reference_gdf.groupby("layer").agg(
        mean_iou=("IoU", "mean"),
        precision=("IoU", lambda x: np.mean(x > 0.5))
    ).reset_index()

    layer_metrics['f1_score'] = 2 * layer_metrics['mean_iou'] * layer_metrics['precision'] / (
        layer_metrics['mean_iou'] + layer_metrics['precision'] + 1e-6
    )
    average_f1_score = layer_metrics['f1_score'].mean()

    # Save Confusion Matrix CSV
    layer_metrics.to_csv(conf_matrix_csv, index=False)
    print(f"Confusion matrix CSV saved: {conf_matrix_csv}")

    # Step 9: Plot IoU Results
    valid_polygons_gdf = reference_gdf[~reference_gdf.index.isin(
        [p['Polygon_Index'] for p in eliminated_polygons])]
    eliminated_polygons_gdf = reference_gdf.loc[
        [p['Polygon_Index'] for p in eliminated_polygons] if eliminated_polygons else []
    ]

    fig, ax = plt.subplots(figsize=(12, 8), dpi=300)
    valid_polygons_gdf.plot(
        ax=ax, column='IoU', cmap='viridis', legend=True,
        legend_kwds={"label": "IoU Values", "orientation": "vertical"},
        alpha=0.7, edgecolor='black'
    )
    eliminated_polygons_gdf.plot(
        ax=ax, color='red', alpha=0.5, edgecolor='black', label='Eliminated Polygons'
    )
    ax.set_title(f"IoU Plot - Weighted Mean IoU: {weighted_mean_iou:.4f}", fontsize=14, fontweight='bold')

    legend_elements = [
        Patch(facecolor='yellow', edgecolor='black', label='Valid Polygons'),
        Patch(facecolor='red', edgecolor='black', label='Eliminated Polygons')
    ]
    ax.legend(handles=legend_elements, loc='lower right')

    plt.tight_layout()
    plt.savefig(plot_output_path, dpi=300)
    print(f"IoU plot saved: {plot_output_path}")
    plt.close()

    return {
        "mean_iou": np.mean(iou_array) if len(iou_array) > 0 else 0,
        "weighted_mean_iou": weighted_mean_iou,
        "average_f1_score": average_f1_score,
        "num_eliminated_polygons": num_eliminated_polygons,
        "over_segmentation_factor": over_segmentation_factor,
    }
