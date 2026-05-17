<table>
<tr>
<td valign="middle" style="padding-right: 20px;">

# <span style="color: #3498db; font-size: 1.2em;">**Multi-Objective Grey Wolf Segmentation Optimization (MOGWSO)**</span>
### <span style="color: #2ecc71;">**Version 1.0.0**</span>
#### <span style="color: #e74c3c;">**June 2025**</span>
<h3>📜 Credits</h3>
<ul>
  <li><strong style="color: #9b59b6;">Mohammad Javad Soltani</strong></li>
  <li><strong style="color: #9b59b6;">Hooman Latifi</strong></li>
  <li><strong style="color: #9b59b6;">Hamed Naghavi</strong></li>
</ul>

</td>
<td valign="middle" align="right">

<img src="https://github.com/user-attachments/assets/ce14253f-1d12-48d3-a755-eb745b347776" alt="MOGWSO Logo" style="max-height: 120px; width: auto;">

</td>
</tr>
</table>

<div style="height: 1px; background: linear-gradient(90deg, transparent, #3498db, transparent); margin: 10px 0;"></div>

---

[![DOI](https://img.shields.io/badge/DOI-10.1016%2Fj.rsase.2026.102050-blue?style=flat-square&logo=doi)](https://doi.org/10.1016/j.rsase.2026.102050)
[![Python](https://img.shields.io/badge/Python-3.10-3776AB?style=flat-square&logo=python&logoColor=white)](https://www.python.org/downloads/release/python-3100/)
[![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)](LICENSE)
[![Journal](https://img.shields.io/badge/Journal-RSASE%202026-orange?style=flat-square)](https://doi.org/10.1016/j.rsase.2026.102050)

---

## <span style="color: #3498db;">📃 Overview</span>

<div style="background: #f8f9fa; padding: 15px; border-radius: 8px; border-left: 4px solid #3498db; margin-bottom: 20px;">

◼️ **MOGWSO** is an advanced optimization algorithm inspired by the hunting behavior of grey wolves, adapted for **multi-objective image segmentation tasks**.
◼️ Designed for **remote sensing applications**, it efficiently handles **complex, high-dimensional optimization problems** with Pareto-optimal solutions.
◼️ Combines **Grey Wolf Optimizer (GWO) principles** with **geometric accuracy assessment** (IoU, F1-score) and **thematic validation**.

</div>

### **Key Innovations**

| Feature | Description |
|---|---|
| 📍 **Hybrid Optimization** | Framework capable of operating on both labeled and unlabeled data |
| 📎 **Multi-Step Labeling** | Method for labeling and eliminating unreliable segments |
| ✡️ **Comprehensive Evaluation** | Geometric, thematic, and locational metrics for holistic quality assessment |
| 📐 **Weighted IoU** | Multi-objective tuning of all key segmentation parameters considering area effects |
| 🛰️ **Novel OSF** | New oversegmentation metric explicitly linked to IoU |

### **Theoretical Foundation**

```math
\text{Objective} = W_1 \times \text{elim\_fac} + W_2 \times \text{OSF} + W_3 \times \text{F1\_Score}
```

---

## 📊 Performance Metrics

> MOGWSO evaluates segmentation quality using **five complementary metrics**, combining geometric accuracy, elimination strategies, and oversegmentation control for robust optimization.

---

### **1. Intersection over Union (IoU)**

IoU measures the overlap between predicted segments and reference polygons [Sun et al., 2022](https://doi.org/10.1016/j.compag.2022.107273). It is calculated per polygon and averaged across all RoIs:

<div align="center">
  <img src="https://github.com/user-attachments/assets/65777d34-1657-42ca-abea-b1579d5e17ce" alt="Capture" width="250">
</div>

**Where:**
- **K**: Total number of reference polygons
- **C<sub>k</sub>**: The *k*th predicted segment
- **R<sub>k</sub>**: The *k*th reference polygon

---

### **2. Weighted Intersection over Union (W-IoU)**

W-IoU addresses the imbalance caused by varying polygon sizes by assigning area-based weights to each IoU score [Cho, 2024](https://doi.org/10.1016/j.patrec.2024.07.011).

<div align="center">
  <img src="https://github.com/user-attachments/assets/e95ac736-96f1-44e2-aa23-89eeb01b1903" alt="Capture" width="600">
</div>

**Where:**
- **K**: Total number of reference polygons
- **C<sub>k</sub>**: The *k*th predicted segment
- **R<sub>k</sub>**: The *k*th reference polygon

---

### **3. Elimination Factor (Elim<sub>Fac</sub>)**

This metric filters out unreliable polygons by removing those with unusually low IoU values (Z-score < −2), then normalizes the elimination count.

<div align="center">
  <img src="https://github.com/user-attachments/assets/f70820c5-5fd0-4a98-8dbf-38c3ce85a99b" alt="Capture" width="700">
</div>

**Where:**
- **IOU(R<sub>i</sub>)**: IoU of the ith reference polygon
- **f(IOU)**: 1 if Z-score < −2; 0 otherwise
- **k**: Total number of reference polygons

---

### **4. F1-Seg (Custom F1 Score)**

F1-Seg evaluates segmentation by combining the IoU of both labeling stages — recall from first-stage and precision from final labeled output.

<div align="center">
  <img src="https://github.com/user-attachments/assets/476927db-74c9-490f-a80b-eebdac333a37" alt="Capture" width="400">
</div>

**Where:**
- **IoU**: Mean IoU across all labeled segments
- **IoU<sub>Stage1</sub>**: Mean IoU for first-stage reference polygon labels

---

### **5. Oversegmentation Factor (OSF)**

OSF penalizes excessive fragmentation by measuring how many segments are linked to each reference polygon.

<div align="center">
  <img src="https://github.com/user-attachments/assets/7c51bfd3-ac70-4ccd-aa54-0855c09bdadf" alt="Capture" width="400">
</div>

**Where:**
- **n<sub>i</sub>**: Number of labeled segments linked to the ith reference polygon
- **N<sub>TotalRef</sub>**: Total number of reference polygons
- **k**: Normalization constant from oversegmented baseline

---

## 🚀 Quick Start

### ⚙️ System Requirements

> **Python 3.10 is required.** MOGWSO has been developed and tested exclusively on **Python 3.10.x**. Using other Python versions (3.9, 3.11+) may cause dependency conflicts, particularly with GDAL, Rasterio, and PyQt5/PySide6 bindings.

To verify your Python version:
```bash
python --version
# Expected: Python 3.10.x
```

---

### 🗺️ Installation

**1. Create a virtual environment (strongly recommended):**

```bash
python -m venv venv
```

**2. Activate the environment:**

On Windows:
```bash
venv\Scripts\activate
```
On macOS/Linux:
```bash
source venv/bin/activate
```

**3. Upgrade pip, setuptools, and wheel:**

```bash
pip install --upgrade pip setuptools wheel
```

**4. Install all dependencies:**

```bash
pip install -r requirements.txt
```

---

### 📦 Key Dependencies

The following are the **core packages** MOGWSO relies on. All versions are pinned for reproducibility.

| Package | Version | Role |
|---|---|---|
| **Python** | 3.10.x | Base interpreter |
| **GDAL** | 3.10.0 | Geospatial data I/O and raster processing |
| **Rasterio** | 1.4.3 | Raster read/write built on GDAL |
| **GeoPandas** | 1.0.1 | Vector geometry handling and spatial joins |
| **Shapely** | 2.0.6 | Geometric operations (intersection, union, IoU) |
| **Scikit-learn** | 1.6.0 | Machine learning utilities and metrics |
| **SciPy** | 1.15.0 | Statistical computations (Z-score filtering) |
| **Pandas** | 2.2.3 | Tabular data management |
| **Matplotlib** | 3.10.0 | Visualization of optimization convergence |
| **PyProj** | 3.7.0 | Coordinate reference system transformations |
| **Pyogrio** | 0.10.0 | Fast vector I/O backend for GeoPandas |
| **Munkres** | 1.1.4 | Hungarian algorithm for segment-to-reference matching |
| **JobLib** | 1.4.2 | Parallelization of fitness evaluations |

<details>
<summary><b>📋 Full dependency list (click to expand)</b></summary>

```
affine==2.4.0
click-plugins==1.1.1
cligj==0.7.2
GDAL==3.10.0
geopandas==1.0.1
joblib==1.4.2
matplotlib==3.10.0
matplotlib-scalebar==0.8.1
munkres==1.1.4
nbimporter==0.3.4
pandas==2.2.3
pyogrio==0.10.0
pyproj==3.7.0
PyQt5==5.15.9
PyQtWebEngine==5.15.4
PySide6==6.8.1
pywin32==307
rasterio==1.4.3
scikit-learn==1.6.0
scipy==1.15.0
shapely==2.0.6
shiboken6==6.8.1
threadpoolctl==3.5.0
tzdata==2024.2
zstandard==0.23.0
```

> ⚠️ **Note on GDAL:** Installing GDAL via pip on Windows can be error-prone. It is strongly recommended to install the GDAL wheel matching your Python version and system architecture from [Christoph Gohlke's repository](https://github.com/cgohlke/geospatial-wheels) **before** running `pip install -r requirements.txt`.

> ⚠️ **Note on PyQt5 / PySide6:** Both GUI backends are listed as dependencies for notebook rendering compatibility. On Linux/macOS, `pywin32` can be safely ignored or removed from `requirements.txt`.

</details>

---

### ▶️ Running MOGWSO

1. Download the complete code package.
2. Open `MOGWSO.ipynb` in your preferred environment (JupyterLab, VSCode).
3. Set the correct paths to your satellite image and reference shapefile:

```python
satellite_image_path = "/path/to/your/satellite_image.tif"
reference_shapefile_path = "/path/to/your/reference_data.shp"
```

4. Run all notebook cells. The optimizer will initialize the GWO population, evaluate the multi-objective fitness function, and return the Pareto-optimal segmentation parameters.

---

## 📄 Citation

If you use MOGWSO in your research, please cite the following paper:

> (2026). *Multi-Objective Grey Wolf Segmentation Optimization for Remote Sensing Image Segmentation*. **Remote Sensing Applications: Society and Environment**, 102050. https://doi.org/10.1016/j.rsase.2026.102050

**BibTeX:**

```bibtex
@article{
  title   = {Beyond trial-and-error: Geometrically balanced, multi-objective optimization for segmenting remote sensing data over complex environments},
  author  = {Soltani, M.J., Latifi, H., Naghavi, H.},
  journal = {Remote Sensing Applications: Society and Environment},
  volume  = {42},
  pages   = {102050},
  year    = {2026},
  doi     = {10.1016/j.rsase.2026.102050},
  url     = {https://doi.org/10.1016/j.rsase.2026.102050}
}
```

---

## <span style="color: #3498db;">📧 Contact</span>

✉️ mjavadsoltani@email.kntu.ac.ir

🌐 [GitHub](https://github.com/)

🔗 [LinkedIn](https://linkedin.com/)