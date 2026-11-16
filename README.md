# Brain MRI Tumor Segmentation

Project 3 · Days 31–45 · Python, PyTorch, MONAI

Objective: develop a research prototype to highlight annotated abnormality regions in brain MRI. This repository currently completes **Days 31–33 only**. No trained segmentation model or interactive application is included yet.

## Day 31 — repository and environment

Python 3.11 isolated environment with PyTorch, MONAI, NumPy, Matplotlib, nibabel and tifffile. Exact installed dependencies are saved in `requirements-lock.txt`.

```bash
python3.11 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements-lock.txt
python -m pip check
```

Verified imports and a small MONAI 2D UNet forward pass with three input channels and one output channel. This smoke check uses random weights and is not a trained tumor model.

## Day 32 — small annotated MRI subset

```bash
python scripts/download_data.py
```

Downloads 12 axial image/mask pairs (slices 10–21 from one case) from Mateusz Buda's [Brain MRI segmentation dataset](https://www.kaggle.com/datasets/mateuszbuda/lgg-mri-segmentation). This is a deliberately small **inspection subset**, not the full 110-patient dataset. Download URLs, sizes and SHA-256 hashes are written to `data/manifest.json`. The script requires `curl` and internet access. The publisher's current-file endpoint is used, so hashes document this download snapshot rather than guaranteeing future source immutability.

Data are stored locally under `data/raw/` and excluded from Git. Dataset metadata identifies the license as **CC BY-NC-SA 4.0**; retain the source attribution and review its conditions before redistribution or other use. Source images originated in TCIA's TCGA lower-grade glioma collection.

## Day 33 — inspect MRI and mask representation

```bash
python scripts/inspect_data.py
```

Checks every pair's shape and pixel values, saves a machine-readable inspection report, and creates `results/mri_mask_inspection.png` with FLAIR MRI, manual annotation and overlay for three slices. Reports and figures remain local under `results/`.

See [DATASET.md](DATASET.md) for channel order, mask meaning and limitations.

## Planned later deliverables

- Train or adapt a brain MRI segmentation model.
- Visualize predicted tumor/abnormality masks.
- Evaluate Dice/IoU and compare predictions with expert annotations.
- Build an interactive application.
- Record a demonstration and document reproducible use.

One patient's neighboring slices are unsuitable for independent training/validation splits. Download more patients and split by patient before model evaluation. These materials are for learning and research; no diagnostic performance has been established.
