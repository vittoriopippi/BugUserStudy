from pathlib import Path
from tqdm import tqdm
from PIL import Image


src = Path(r'D:\Downloads\bugdiff')
dst = Path(r'D:\Downloads\bugdiff_jpg')

all_imgs = list(src.rglob('*.png'))
for src_img in tqdm(all_imgs):
    dst_img = dst / src_img.relative_to(src).with_suffix('.jpg')
    img = Image.open(src_img)
    dst_img.parent.mkdir(parents=True, exist_ok=True)
    img.save(dst_img, quality=70)