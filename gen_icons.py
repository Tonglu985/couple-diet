"""
生成 Hello Kitty 健身图标 + 多尺寸 PWA 图标
"""
from PIL import Image, ImageDraw, ImageFilter
import os

OUT = '/workspace/couple-diet/icons'
os.makedirs(OUT, exist_ok=True)

def make_hellokitty(size=1024, transparent_bg=True):
    """生成 Hello Kitty 健身图标（程序化绘制）"""
    img = Image.new('RGBA', (size, size), (0,0,0,0) if transparent_bg else (255, 240, 246, 255))
    d = ImageDraw.Draw(img)

    # 粉色圆形背景（圆角）
    pad = int(size * 0.02)
    r = int(size * 0.22)  # 圆角半径
    bg_color = (255, 220, 232, 255)  # 浅粉
    # 用圆角矩形作为背景
    bg = Image.new('RGBA', (size, size), (0,0,0,0))
    bgd = ImageDraw.Draw(bg)
    bgd.rounded_rectangle([pad, pad, size-pad, size-pad], radius=r, fill=bg_color)
    img = Image.alpha_composite(img, bg) if transparent_bg else bg
    d = ImageDraw.Draw(img)

    s = size / 1024.0  # 缩放因子

    def pt(x):
        return int(x * s)

    # ===== 身体（蓝色背心+短裤）=====
    # 蓝色背心
    d.polygon([
        (pt(380), pt(720)),   # 左肩下
        (pt(644), pt(720)),   # 右肩下
        (pt(680), pt(820)),   # 右腋下
        (pt(344), pt(820)),   # 左腋下
    ], fill=(74, 144, 217, 255))

    # 短裤
    d.rectangle([pt(340), pt(810), pt(684), pt(940)], fill=(74, 144, 217, 255))

    # 短裤中线
    d.line([(pt(512), pt(810)), (pt(512), pt(940))], fill=(40, 110, 180, 255), width=pt(4))

    # 腿（白色）
    d.rectangle([pt(370), pt(940), pt(490), pt(1010)], fill=(255, 255, 255, 255))
    d.rectangle([pt(534), pt(940), pt(654), pt(1010)], fill=(255, 255, 255, 255))

    # ===== 头部（白色猫脸）=====
    # 脸部轮廓 - 大圆
    d.ellipse([pt(260), pt(220), pt(764), pt(720)], fill=(255, 255, 255, 255))

    # 左耳
    d.polygon([(pt(280), pt(280)), (pt(220), pt(180)), (pt(340), pt(220))], fill=(255, 255, 255, 255))
    # 右耳
    d.polygon([(pt(744), pt(280)), (pt(804), pt(180)), (pt(684), pt(220))], fill=(255, 255, 255, 255))
    # 左耳内侧粉
    d.polygon([(pt(290), pt(270)), (pt(245), pt(205)), (pt(325), pt(230))], fill=(255, 180, 200, 255))
    # 右耳内侧粉
    d.polygon([(pt(734), pt(270)), (pt(779), pt(205)), (pt(699), pt(230))], fill=(255, 180, 200, 255))

    # ===== 眼睛（黑色圆点）=====
    d.ellipse([pt(385), pt(420), pt(445), pt(485)], fill=(50, 50, 50, 255))
    d.ellipse([pt(580), pt(420), pt(640), pt(485)], fill=(50, 50, 50, 255))
    # 眼睛高光
    d.ellipse([pt(410), pt(440), pt(425), pt(455)], fill=(255, 255, 255, 255))
    d.ellipse([pt(605), pt(440), pt(620), pt(455)], fill=(255, 255, 255, 255))

    # 鼻子（黄色小三角）
    d.polygon([(pt(500), pt(515)), (pt(525), pt(515)), (pt(512), pt(540))], fill=(255, 213, 79, 255))

    # 胡须（左右各3根）
    for y_off in [pt(540), pt(555), pt(570)]:
        d.line([(pt(300), y_off), (pt(380), y_off+pt(5))], fill=(80, 80, 80, 255), width=pt(3))
        d.line([(pt(724), y_off), (pt(644), y_off+pt(5))], fill=(80, 80, 80, 255), width=pt(3))

    # ===== 蝴蝶结（粉色）=====
    # 蝴蝶结中心
    cx, cy = pt(680), pt(310)
    # 左蝴蝶结
    d.polygon([(cx, cy), (cx-pt(80), cy-pt(40)), (cx-pt(80), cy+pt(40))], fill=(255, 105, 180, 255))
    # 右蝴蝶结
    d.polygon([(cx, cy), (cx+pt(80), cy-pt(40)), (cx+pt(80), cy+pt(40))], fill=(255, 105, 180, 255))
    # 中心结
    d.ellipse([cx-pt(18), cy-pt(18), cx+pt(18), cy+pt(18)], fill=(255, 105, 180, 255))

    # ===== 哑铃（左右各一个）=====
    def draw_dumbbell(left_x, right_x, y):
        # 杠
        d.rectangle([pt(left_x), pt(y-15), pt(right_x), pt(y+15)], fill=(180, 180, 180, 255))
        # 左大圆盘
        d.ellipse([pt(left_x-50), pt(y-90), pt(left_x+50), pt(y+90)], fill=(255, 105, 180, 255))
        d.ellipse([pt(left_x-30), pt(y-70), pt(left_x+30), pt(y+70)], fill=(220, 80, 150, 255))
        # 右大圆盘
        d.ellipse([pt(right_x-50), pt(y-90), pt(right_x+50), pt(y+90)], fill=(255, 105, 180, 255))
        d.ellipse([pt(right_x-30), pt(y-70), pt(right_x+30), pt(y+70)], fill=(220, 80, 150, 255))

    draw_dumbbell(100, 280, 820)
    draw_dumbbell(744, 924, 820)

    return img

# 生成主图标
master = make_hellokitty(1024)
master.save(os.path.join(OUT, 'icon-master.png'))

# 生成 PWA 各种尺寸
sizes = [16, 32, 48, 72, 96, 120, 144, 152, 167, 180, 192, 256, 512]
for sz in sizes:
    img = make_hellokitty(sz)
    img.save(os.path.join(OUT, f'icon-{sz}.png'))

# 苹果特殊尺寸
apple_sizes = {57: 'apple-touch-icon-57', 60: 'apple-touch-icon-60', 72: 'apple-touch-icon-72',
               76: 'apple-touch-icon-76', 114: 'apple-touch-icon-114', 120: 'apple-touch-icon-120',
               144: 'apple-touch-icon-144', 152: 'apple-touch-icon-152', 167: 'apple-touch-icon-167',
               180: 'apple-touch-icon-180'}
for sz, name in apple_sizes.items():
    img = make_hellokitty(sz)
    img.save(os.path.join(OUT, f'{name}.png'))

# 浏览器 favicon
fav32 = make_hellokitty(32)
fav32.save(os.path.join(OUT, 'favicon-32.png'))
fav16 = make_hellokitty(16)
fav16.save(os.path.join(OUT, 'favicon-16.png'))

# 主 apple touch icon
apple = make_hellokitty(180)
apple.save(os.path.join(OUT, 'apple-touch-icon.png'))

print("✅ 生成所有图标")
print(f"📁 位置: {OUT}")
print(f"📦 文件数: {len(os.listdir(OUT))}")
for f in sorted(os.listdir(OUT)):
    sz = os.path.getsize(os.path.join(OUT, f))
    print(f"  - {f}  ({sz} bytes)")