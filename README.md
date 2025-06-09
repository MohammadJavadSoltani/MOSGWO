<table>
<tr>
<td valign="middle" style="padding-right: 20px;">

# <span style="color: #3498db; font-size: 1.2em;">**Multi-Objective Grey Wolf Segmentation Optimization (MOGWSO)**</span>  
### <span style="color: #2ecc71;">**Version 1.0.0**</span>  
#### <span style="color: #e74c3c;">**June 2025**</span>  
#### <span style="color: #9b59b6;">**Credit: M. Javad Soltani**</span>  
**Master Student of Remote Sensing and Photogrammetry**  
**K. N. Toosi University of Technology**  

</td>
<td valign="middle" align="right">

<img src="https://github.com/user-attachments/assets/ce14253f-1d12-48d3-a755-eb745b347776" alt="MOGWSO Logo" style="max-height: 120px; width: auto;">

</td>
</tr>
</table>

<div style="height: 1px; background: linear-gradient(90deg, transparent, #3498db, transparent); margin: 10px 0;"></div>

## <span style="color: #3498db;">📃 Overview</span>  

<div style="background: #f8f9fa; padding: 15px; border-radius: 8px; border-left: 4px solid #3498db; margin-bottom: 20px;">
  
◼️ **MOGWSO** is an advanced optimization algorithm inspired by the hunting behavior of grey wolves, adapted for <strong>multi-objective image segmentation tasks</strong>.  
◼️ Designed for <strong>remote sensing applications</strong>, it efficiently handles <strong>complex, high-dimensional optimization problems</strong> with Pareto-optimal solutions.  
◼️ Combines <strong>Grey Wolf Optimizer (GWO) principles</strong> with <strong>geometric accuracy assessment</strong> (IoU, F1-score) and <strong>thematic validation</strong>.  
</div>

### **Key innovations** 
- 📍 **Hybrid optimization**: introduces a hybrid optimization framework capable of operating on both labeled and unlabeled data.   
- 📎 **Multi-Step labeling**: develops a method for labelling, and eliminating segments. 
- ✡️ **Comprehensive evaluate**: leverages geometric, thematic, and locational metrics for a more holistic evaluation of segmentation quality
- 📐 **Weighted IoU**: applies a multi-objective optimization to tune all key segmentation parameters, explicitly considering area-related effects.
- 🛰️ **new OSF**: proposes a new OS metric as associated with IoU.

### **Theoretical Foundation** 
```math
\text{Objective} = W_1 \times (1 - \text{elim_fac}) + W_2 \times (1 - \text{OSF}) + W_3 \times \text{F1_Score}
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

Follow these simple steps to get your segmentation optimization running quickly:

- Download the complete code package.

- Open the (MOGWSO.ipynb) in your preferred environment (e.g., JupyterLab, VSCode).

- Set the correct paths inside the Python script or notebook to your satellite image data and referenced shapefile:

```python
satellite_image_path = "/path/to/your/satellite_image.tif"
reference_shapefile_path = "/path/to/your/reference_data.shp"
```
- Run the notebook cells or script, and the optimization will start processing using your provided data.

