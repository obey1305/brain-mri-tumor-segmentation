# MRI data and annotation representation

Source: [Mateusz Buda — Brain MRI segmentation](https://www.kaggle.com/datasets/mateuszbuda/lgg-mri-segmentation), derived from TCIA/TCGA lower-grade glioma imaging. Publisher description: https://mateuszbuda.com/2017/12/01/brainseg.html

The source dataset has 110 cases. This project downloads only slices 10–21 of `TCGA_CS_4941_19960909`: 12 image/mask pairs for inspection, not a representative model-development cohort.

## Images

Images are 256 × 256 TIFF arrays with three channels. According to the publisher's README, the channel order is:

1. Pre-contrast MRI.
2. FLAIR MRI.
3. Post-contrast MRI.

The channels represent registered MRI sequences, not red/green/blue photographic color. In some source cases a missing sequence is replaced with FLAIR. The FLAIR channel is always available in the source release. Plot each sequence in grayscale; the inspection figure uses channel index 1 (FLAIR).

## Masks

A mask shares its image's filename with `_mask` before `.tif`. It is a single-channel binary annotation: zero denotes background, positive values denote manually segmented FLAIR abnormality. Convert to a learning target with `(mask > 0).astype(np.float32)`. The inspection JSON records the exact observed stored label values rather than assuming positives are encoded as 1 or 255.

Binary foreground does not distinguish edema, enhancing tumor, or other tumor subregions. It also does not provide separate instance IDs. A zero-area slice is a valid negative slice; do not silently discard it. Masks are manual annotations, not predictions.

## Provenance and licensing

Publisher-listed license: CC BY-NC-SA 4.0. Source publication: Mateusz Buda, Ashirbani Saha, Maciej A. Mazurowski, “Association of genomic subtypes of lower-grade gliomas with shape features automatically extracted by a deep learning algorithm,” Computers in Biology and Medicine (2019). The downloaded publisher README remains under `data/raw/` locally. Dataset files and annotations are not pushed to GitHub.

## Scope

These exported 2D TIFFs do not preserve the full original DICOM/NIfTI spatial metadata. Pixel counts are not physical tumor volumes. Adjacent slices from one patient are strongly related: split by patient for future training/evaluation, and do not report independent validation from this inspection subset.

## Verified download, 16 November 2026

24 TIFF files (12 image/mask pairs), 3,226,176 bytes. All image/mask pairs decoded with matching spatial dimensions. Image shape is 256 × 256 × 3; mask values are 0 and 255. Eight slices have foreground annotations and four are negative. All download hashes match the saved manifest.
