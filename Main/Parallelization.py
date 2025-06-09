import os
import pandas as pd
import random
import matplotlib.pyplot as plt

from Mapping_Values import map_params
from Segmentation_Evaluation import Geometric_Acc
from Segmentation import RSGISLIB_Seg_Gen

def process_wolf(args):
    """Multiprocessing worker for each wolf: Segmentation + Evaluation."""
    iteration, wolf_idx, wolf, param_bounds, input_img, reference_path, W1, W2, K_Factor, output_dir = args

    wolf_number = wolf_idx + 1  
    print(f"[Wolf-{wolf_number}] Started. Mapping Params...", flush=True)

    try:
        # 1. Map segmentation parameters 
        wolf = map_params(wolf, param_bounds)
        print(f"[Wolf-{wolf_number}] Mapped Params: {wolf}", flush=True)

        # 2. Compute W3 Just Before Weight Calculation
        W1 = W1
        W2 = W2
        W3 = 1 - (W1 + W2)

        # 3. Prepare Weights
        weights = {
            "average_f1_score": W3,
            "over_segmentation_factor": W2,
            "eliminated_polygons": W1,
        }
        print(f"[Wolf-{wolf_number}] Computed Weights: {weights}", flush=True)

        # 4. Create Output Directory
        wolf_output_dir = os.path.join(output_dir, f"wolf_{wolf_number}")
        os.makedirs(wolf_output_dir, exist_ok=True)
        wolf_segments_path = os.path.join(wolf_output_dir, "segments.shp")

        # 5. Remove `W1`, `W2` Before Segmentation Call
        seg_params = {k: v for k, v in wolf.items() if k not in ["W1", "W2"]}
        print(f"[Wolf-{wolf_number}] Running Segmentation with Parameters: {seg_params}", flush=True)

        # 6. Run Segmentation
        RSGISLIB_Seg_Gen(
            input_img=input_img,
            out_shapefile=wolf_segments_path,
            **seg_params,  # Only segmentation params here
            n_Bands=37,
            iteration=iteration + 1,
            wolf=wolf_number,
        )
        print(f"[Wolf-{wolf_number}] Segmentation Completed.", flush=True)

        # 7. Check Shapefile
        if os.path.exists(wolf_segments_path):
            size_kb = os.path.getsize(wolf_segments_path) / 1024
            print(f"[📂 Wolf-{wolf_number}] Shapefile Size: {size_kb:.2f} KB", flush=True)
            if size_kb < 5:
                print(f"[⚠️ Wolf-{wolf_number}] Shapefile too small (<5 KB). Might be empty segmentation.", flush=True)

        # 8. Run Evaluation
        print(f"[📊 Wolf-{wolf_number}] Running Evaluation...", flush=True)
        metrics = Geometric_Acc(
            segments_Path=wolf_segments_path,
            reference_Path=reference_path,
            output_folder=wolf_output_dir,
            K_Factor=K_Factor  
        )
        print(f"[Wolf-{wolf_number}] Evaluation Done: {metrics}", flush=True)

        # 9. Compute Objective Score Using Computed W3
        objective_score = (
            weights["average_f1_score"] * metrics.get("average_f1_score", 0)
            + weights["eliminated_polygons"] * (1 - metrics.get("num_eliminated_polygons", 1))
            + weights["over_segmentation_factor"] * (1 - metrics.get("over_segmentation_factor", 1))
        )
        print(f"[Wolf-{wolf_number}] Objective Score: {objective_score}", flush=True)

        return wolf, metrics, objective_score

    except Exception as e:
        print(f"[Wolf-{wolf_number}] Error Occurred: {e}", flush=True)
        return wolf, {}, -float("inf")
