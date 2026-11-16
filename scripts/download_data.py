"""Download a small inspection subset from the original Kaggle publisher."""
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import hashlib
import json
import subprocess
from urllib.parse import quote
ROOT=Path(__file__).resolve().parents[1]
CASE='TCGA_CS_4941_19960909'
BASE='https://www.kaggle.com/api/v1/datasets/download/mateuszbuda/lgg-mri-segmentation/'


def fetch(name):
    relative=f'kaggle_3m/{CASE}/{name}'
    url=BASE+quote(relative,safe='')
    dest=ROOT/'data/raw'/name
    dest.parent.mkdir(parents=True,exist_ok=True)
    subprocess.run(['curl','--fail','--silent','--show-error','--location','--retry','2','--max-time','90',url,'--output',str(dest)],check=True)
    content=dest.read_bytes()
    return dict(file=name,source=url,bytes=len(content),sha256=hashlib.sha256(content).hexdigest())


def main():
    names=[f'{CASE}_{i}{suffix}.tif' for i in range(10,22) for suffix in ('','_mask')]
    with ThreadPoolExecutor(max_workers=4) as pool:
        records=list(pool.map(fetch,names))
    (ROOT/'data/manifest.json').write_text(json.dumps(records,indent=2)+'\n')
    print(f'Downloaded {len(records)//2} image/mask pairs; {sum(r["bytes"] for r in records):,} bytes')


if __name__=='__main__': main()
