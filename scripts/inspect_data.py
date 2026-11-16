"""Validate all downloaded pairs and plot MRI, annotation, and overlay."""
from pathlib import Path
import csv
import json
import numpy as np
import tifffile
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
ROOT=Path(__file__).resolve().parents[1]


def main():
    output=ROOT/'results'
    output.mkdir(exist_ok=True)
    records=[]
    images=sorted((ROOT/'data/raw').glob('*_mask.tif'))
    if not images:
        raise FileNotFoundError('Run scripts/download_data.py first')
    for mask_path in images:
        path=mask_path.with_name(mask_path.name.replace('_mask',''))
        image=tifffile.imread(path)
        mask=tifffile.imread(mask_path)
        if image.ndim!=3 or image.shape[-1]!=3 or mask.shape!=image.shape[:2]:
            raise ValueError(f'Mismatched shapes: {path.name}')
        labels=np.unique(mask).tolist()
        if len(labels)>2 or not np.isfinite(image).all():
            raise ValueError(f'Invalid image or mask: {path.name}')
        records.append(dict(image=path.name,shape=list(image.shape),image_dtype=str(image.dtype),
            mask_dtype=str(mask.dtype),mask_labels=labels,abnormality_pixels=int(np.count_nonzero(mask))))
    (output/'inspection.json').write_text(json.dumps(records,indent=2)+'\n')
    with (output/'inspection.csv').open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(records[0]));w.writeheader();w.writerows(records)
    chosen=[records[0],records[len(records)//2],records[-1]]
    fig,axes=plt.subplots(3,3,figsize=(10,11),layout='constrained')
    for row,record in enumerate(chosen):
        image=tifffile.imread(ROOT/'data/raw'/record['image'])
        mask=tifffile.imread(ROOT/'data/raw'/record['image'].replace('.tif','_mask.tif'))>0
        flair=image[...,1]
        axes[row,0].imshow(flair,cmap='gray')
        axes[row,1].imshow(mask,cmap='gray',vmin=0,vmax=1)
        axes[row,2].imshow(flair,cmap='gray')
        overlay=np.zeros((*mask.shape,4));overlay[mask]=(1,0.15,0.1,0.45)
        axes[row,2].imshow(overlay)
        for col,title in enumerate(('FLAIR MRI','Manual binary annotation','Annotation overlay')):
            axes[row,col].set_title(title if row==0 else '')
            axes[row,col].axis('off')
        axes[row,0].text(0,-0.04,record['image'].split('_')[-1]+f" · {record['abnormality_pixels']:,} labeled pixels",transform=axes[row,0].transAxes,fontsize=9)
    fig.suptitle('Day 33 · MRI images and manual FLAIR-abnormality masks\nSource: Mateusz Buda / TCGA-LGG via Kaggle · Not model predictions',fontsize=14)
    fig.savefig(output/'mri_mask_inspection.png',dpi=150)
    plt.close(fig)
    print(json.dumps(dict(pairs=len(records),positive_slices=sum(r['abnormality_pixels']>0 for r in records),
        observed_mask_values=sorted(set(v for r in records for v in r['mask_labels']))),indent=2))


if __name__=='__main__': main()
