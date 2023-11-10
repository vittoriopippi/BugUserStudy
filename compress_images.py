from pathlib import Path
from tqdm import tqdm
from PIL import Image


src = Path('images_png')
dst = Path('images_jpg')

all_imgs = list(src.rglob('*.png'))
for src_img in tqdm(all_imgs):
    dst_img = dst / src_img.relative_to(src).with_suffix('.jpg')
    if dst_img.exists():
        continue
    img = Image.open(src_img)
    dst_img.parent.mkdir(parents=True, exist_ok=True)
    img.save(dst_img, quality=95)