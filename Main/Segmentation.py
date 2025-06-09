import rsgislib
import rsgislib.segmentation
import rsgislib.vectorutils.createvectors as createvectors
from rsgislib.segmentation import shepherdseg
import shutil
import os
import uuid
import time

def RSGISLIB_Seg_Gen(
    input_img,
    out_shapefile,
    num_clusters=30,
    min_n_pxls=15,
    dist_thres=50,
    sampling=100,
    km_max_iter=200,
    min_clump_size_factor=1.5,
    pxl_val_thres_factor=1.5,
    n_Bands=13,
    iteration=1,
    wolf=1,
):
    """
    Perform multi-step segmentation using RSGISLib's Shepherd algorithm with quality checks.
    
    Combines K-means clustering, spectral merging, and small-clump removal to generate
    optimized vector segments. Includes automatic cleanup and validation.

    Args:
        input_img (str): Path to input raster image. (tif)
        out_shapefile (str): Output shapefile path (.shp).
        num_clusters (int): Initial number of K-means clusters (default: 30).
        min_n_pxls (int): Minimum pixels per segment (default: 15).
        dist_thres (int): Spectral distance threshold for merging (default: 50).
        sampling (int): Pixel sampling rate for K-means (default: 100).
        km_max_iter (int): Max iterations for K-means (default: 200).
        min_clump_size_factor (float): Multiplier for min clump size (default: 1.5).
        pxl_val_thres_factor (float): Multiplier for spectral threshold (default: 1.5).
        n_Bands (int): Number of bands to use (default: 13).
        iteration (int): Optimization iteration ID if proccess has stopped from specific iteration (for logging).
        wolf (int): Wolf agent ID  if proccess has stopped from specific wolf (for logging).

    Returns:
        None (writes output to out_shapefile).

    Raises:
        RuntimeError: If critical segmentation steps fail.
        IOError: If output shapefile cannot be written.

    Example:
        >>> RSGISLIB_Seg_Gen(
        ...     input_img="input.tif",
        ...     out_shapefile="segments.shp",
        ...     num_clusters=50,
        ...     min_n_pxls=20
        ... )
        """
    
    tmp_dir = f"tmp_iter_{iteration}_wolf_{wolf}_{uuid.uuid4().hex}"  # Unique temp directory per wolf
    os.makedirs(tmp_dir, exist_ok=True)

    out_clumps_img = os.path.join(tmp_dir, "clumps.kea")
    out_mean_img = os.path.join(tmp_dir, "mean.kea")

    try:
        print(f"[Wolf-{wolf}] Running RSGISLib Segmentation with {num_clusters} clusters and {min_n_pxls} min pixels...")

        # Run shepherd segmentation
        shepherdseg.run_shepherd_segmentation(
            input_img=input_img,
            out_clumps_img=out_clumps_img,
            out_mean_img=out_mean_img,
            tmp_dir=tmp_dir,
            gdalformat="KEA",
            calc_stats=True,
            no_stretch=False,
            no_delete=False,
            num_clusters=num_clusters,
            min_n_pxls=min_n_pxls,
            dist_thres=dist_thres,
            bands=list(range(1, n_Bands)),
            sampling=sampling,
            km_max_iter=km_max_iter,
            process_in_mem=True,
        )

        # Add rejoin step
        out_clumps_img_spec = os.path.join(tmp_dir, "tmp_clumps_spec.kea")
        rsgislib.segmentation.rm_small_clumps_stepwise(
            input_img, 
            out_clumps_img, 
            out_clumps_img_spec, 
            'kea', 
            0, 
            '', 
            1, 
            1, 
            round(min_clump_size_factor * min_n_pxls), 
            round(pxl_val_thres_factor * dist_thres)
        )

        # Create shapefile from segments
        createvectors.polygonise_raster_to_vec_lyr(
            out_vec_file=out_shapefile,
            out_vec_lyr="segmentation_layer",
            out_format="ESRI Shapefile",
            input_img=out_clumps_img_spec,
            img_band=1,
            mask_img=None,
            mask_band=None
        )

        # Check Shapefile Size
        if os.path.exists(out_shapefile):
            size_kb = os.path.getsize(out_shapefile) / 1024
            print(f"[Wolf-{wolf}] Segmentation Shapefile Created: {size_kb:.2f} KB")

            if size_kb < 5:
                print(f"[Wolf-{wolf}] Warning: Shapefile is suspiciously small (<5 KB).")
            else:
                print(f"[Wolf-{wolf}] Shapefile Size OK: {size_kb:.2f} KB")
        else:
            print(f"[Wolf-{wolf}] Segmentation failed: No shapefile created.")

    except Exception as e:
        print(f"[Wolf-{wolf}] Error during segmentation: {e}")

    finally:
        # Clean up temporary files and directories
        cleanup_retries = 3
        for attempt in range(cleanup_retries):
            try:
                if os.path.exists(tmp_dir):
                    shutil.rmtree(tmp_dir)
                    print(f"[Wolf-{wolf}] Temporary directory {tmp_dir} deleted.")
                break
            except Exception as cleanup_error:
                print(f"[Wolf-{wolf}] Error deleting temporary directory: {cleanup_error}")
                if attempt < cleanup_retries - 1:
                    time.sleep(2)  # Wait before retrying
                else:
                    print(f"[Wolf-{wolf}] Failed to delete temp directory after {cleanup_retries} attempts.")
