"""
用原始 Hello Kitty 图片生成所有 PWA 图标尺寸
"""
from PIL import Image
import os

OUT = '/workspace/couple-diet/icons'
SRC = os.path.join(OUT, 'hellokitty-clean.jpg')

# 打开原图
src = Image.open(SRC).convert('RGBA')
print(f"原图尺寸: {src.size}")

def resize_icon(size, name=None, add_bg=True):
    """生成指定尺寸图标，居中裁剪+缩放"""
    if name is None:
        name = f'icon-{size}.png'
    # 居中正方形裁剪
    w, h = src.size
    side = min(w, h)
    left = (w - side) // 2
    top = (h - side) // 2
    cropped = src.crop((left, top, left + side, top + side))
    # 缩放
    img = cropped.resize((size, size), Image.LANCZOS)
    img.save(os.path.join(OUT, name))
    return img

# PWA 图标
sizes = [16, 32, 48, 72, 96, 120, 144, 152, 167, 180, 192, 256, 512]
for sz in sizes:
    resize_icon(sz)

# Apple Touch Icons
apple_sizes = {
    57: 'apple-touch-icon-57',
    60: 'apple-touch-icon-60',
    72: 'apple-touch-icon-72',
    76: 'apple-touch-icon-76',
    114: 'apple-touch-icon-114',
    120: 'apple-touch-icon-120',
    144: 'apple-touch-icon-144',
    152: 'apple-touch-icon-152',
    167: 'apple-touch-icon-167',
    180: 'apple-touch-icon-180',
}
for sz, name in apple_sizes.items():
    resize_icon(sz, f'{name}.png')

# 主 apple touch icon
resize_icon(180, 'apple-touch-icon.png')

# Favicon
resize_icon(16, 'favicon-16.png')
resize_icon(32, 'favicon-32.png')

# 主图标
resize_icon(1024, 'icon-master.png')

# 侧边栏用的图标（76px）
resize_icon(76, 'apple-touch-icon-76.png')

print("✅ 全部用原图重新生成")
print(f"📁 {OUT}")
for f in sorted(os.listdir(OUT)):
    if f.endswith('.png'):
        sz = os.path.getsize(os.path.join(OUT, f))
        print(f"  {f}  ({sz} bytes)")