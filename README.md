
# Photogrammetry and Gaussian Splatting on Lunar Apollo 17 Imagery

This project explores **Gaussian Splatting for 3D Reconstruction** using Apollo 17 imagery and evaluates how **novel view synthesis** using splatting can enhance **photogrammetric modeling**. The experiment follows a two-part investigation: comparing rendered outputs from splatting with ground truth images and evaluating their utility in improving textured mesh reconstruction.

---

## 📌 Objectives

- Train a **Gaussian Splatting model** using a small Apollo 17 image set.
- Generate **novel views** via neural rendering.
- Perform **photogrammetric modeling** using:
  - Original images only (N=15)
  - Augmented dataset with 10 novel views (N=25)
- Conduct **qualitative and quantitative evaluations** using PSNR, SSIM, and mesh visual comparison.

---

## 📁 Project Structure

```
Photogrammetry-and-Gaussian-Splatting/
│
├── colmap/
│   ├── images/              # Original 15 Apollo 17 images
│   ├── images3/             # 10 novel views (first set)
│   ├── images4/             # 10 novel views (alternative sampling)
│   ├── sparse/              # COLMAP sparse models
│   └── [cameras.txt, images.txt, points3D.txt] - COLMAP outputs
│
├── gsplat-env/
│   ├── renders/
│   │   ├── gaussian_images_output/  # Rendered original view outputs
│   │   ├── novel_views/             # Rendered novel views (video/images)
│   │   └── comparison/              # PSNR, SSIM scripts and logs
│   ├── checkpoints/
│   ├── scripts/
│   │   ├── compare_psnr_ssim.py     # Metrics computation script
│   │   ├── export_splat.py          # Export workaround script
│   │   └── render_images.py         # Render workaround script
│   └── viewer_splat.py              # Custom viewer bypass
│
├── README.md
└── requirements.txt
```

---

## ⚙️ Environment Setup

### System Requirements

- Ubuntu 20.04 or 22.04 (AWS EC2 or local)
- NVIDIA GPU with CUDA support
- Python 3.12
- PyTorch 2.6+
- COLMAP preprocessed `.txt` files

### Python Setup

```bash
python3.12 -m venv gsplat-env
source gsplat-env/bin/activate
pip install -r requirements.txt
```

---

## 🧠 Part A: Gaussian Splatting & Evaluation
### 1. Agisoft Photogrammetry (15 Images)
Import Images- Allign images- Build Model- Add texture
![image](https://github.com/user-attachments/assets/8e5b249f-1c4c-4a40-8bca-a8644ed08296)

### 1. Model Training

```bash
ns-train splatfacto colmap \
  --data /home/ubuntu/colmap \
  --output-dir outputs/apollo17-splating
```

> Make sure COLMAP `.txt` files are inside `colmap/sparse/0` and images in `colmap/images/`.

### 2. Rendering Trained Outputs

```bash
python render_images.py dataset \
  --load-config outputs/apollo17-splating/unnamed/splatfacto/<timestamp>/config.yml \
  --output-path renders/gaussian_images_output
```
![WhatsApp Image 2025-05-10 at 18 24 13_683a0ce9](https://github.com/user-attachments/assets/21543329-a32b-417a-8aa7-b08293c0df00)


### 3. Quantitative Comparison (PSNR/SSIM)
![WhatsApp Image 2025-05-10 at 13 01 07_d8f0fcf5](https://github.com/user-attachments/assets/40a6229e-78b7-4acc-a10d-74f5871b6fa2)

```bash
python compare_psnr_ssim.py
```

Metrics:
- **PSNR (Peak Signal-to-Noise Ratio)**: Measures pixel-wise fidelity.
- **SSIM (Structural Similarity Index)**: Measures perceptual similarity.

---

## 🛰️ Part B: Novel Views & Photogrammetric Improvement

### 1. Generate Novel Views

Rendered using:

```bash
ns-render camera-path \
  --load-config outputs/apollo17-splating/unnamed/splatfacto/<timestamp>/config.yml \
  --output-path renders/novel_views
```

Converted to images:

```bash
mkdir -p /home/ubuntu/colmap/images3 && \
ffmpeg -i novel_views.mp4 -vf "select='not(mod(n\\,3))'" -frames:v 10 /home/ubuntu/colmap/images3/novel_%02d.png
```

### 2. New Photogrammetry

Used **Agisoft Metashape** with:

![image](https://github.com/user-attachments/assets/08d02dc6-02c6-4bc6-aa5b-270063f74edf)

- Original images (15)
- Augmented images (15 + 10 novel)

Mesh was reconstructed and textured using standard photogrammetric workflow.

### 3. Additional Files
#### https://drive.google.com/drive/folders/1xUAvWlKP-TFQp34iiYZQTlOBBZjsGcHb?usp=sharing
---

## 🧪 Qualitative Comparison of Models

| Method                   | Observation                                                                 |
|--------------------------|-----------------------------------------------------------------------------|
| Original Photogrammetry  | Coarse mesh, visible gaps, low texture quality in side angles               |
| Augmented with Splatting | Higher surface continuity, improved texture mapping, better occlusion fill |

### Visual Inspection Criteria

- **Coverage Completeness**: Additional angles filled gaps missed in original.
- **Texturing Fidelity**: New novel views captured angles not present in Apollo images.
- **Structural Continuity**: Fewer floating or disconnected point clouds.

---

## 🧠 Insights & Discussion

- Gaussian splatting is not only useful for view synthesis but can augment photogrammetric datasets effectively.
- Novel views enhanced mesh fidelity in areas with poor coverage.
- The fidelity of novel views was verified using PSNR/SSIM before inclusion.

---

## 📈 Future Scope

- Use **visual servoing** to smartly plan novel view synthesis.
- Integrate **automatic image filtering** to exclude low-fidelity views.
- Explore **multi-view consistency loss** during training.

---

## 🧾 License

This project is released under the MIT License.

---

## 📬 Acknowledgments

- **NASA Apollo Archives** for the dataset
- **Nerfstudio** for the splatting pipeline
- **COLMAP** and **Agisoft** for photogrammetry tools
