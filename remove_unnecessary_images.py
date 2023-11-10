from pathlib import Path
from tqdm import tqdm
import random

root = Path('images')

subfolders = {f.parent for f in root.rglob('*.png')}

for subfolder in subfolders:
    print(subfolder)
    imgs = list(subfolder.rglob('*.png'))
    random.shuffle(imgs)
    for img in tqdm(imgs[20:]):
        img.unlink()
    