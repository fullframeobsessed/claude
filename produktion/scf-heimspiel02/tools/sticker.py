"""Papier-Ausschnitt-Look: weißer Schnittrand + weicher Schatten, eingebrannt ins PNG (assets/sticker_<name>.png)."""
import numpy as np
from PIL import Image, ImageFilter
from scipy import ndimage
B, PAD, MAXH = 14, 60, 1100
for n in ["thuerauf", "clain", "kandra", "hameed", "steinmann"]:
    im = Image.open(f"assets/cut/{n}.png").convert("RGBA")
    if im.height > MAXH:
        im = im.resize((round(im.width * MAXH / im.height), MAXH), Image.LANCZOS)
    W, H = im.width + 2 * PAD, im.height + 2 * PAD
    a = np.zeros((H, W), np.float32); a[PAD:PAD + im.height, PAD:PAD + im.width] = np.array(im)[..., 3] / 255
    hard = a > 0.35
    yy, xx = np.mgrid[-B:B + 1, -B:B + 1]
    border = ndimage.binary_dilation(hard, structure=(xx ** 2 + yy ** 2) <= B * B)
    border = ndimage.binary_fill_holes(ndimage.binary_closing(border, iterations=4))
    bimg = Image.fromarray((border * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(1.2))
    sh = Image.fromarray((border * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(14))
    out = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    shadow = Image.new("RGBA", (W, H), (0, 0, 0, 0)); shadow.putalpha(sh.point(lambda v: int(v * 0.55)))
    out.alpha_composite(shadow, (10, 18))
    paper = Image.new("RGBA", (W, H), (250, 248, 243, 0)); paper.putalpha(bimg)
    out.alpha_composite(paper)
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0)); layer.paste(im, (PAD, PAD))
    out.alpha_composite(layer)
    out = out.crop(out.getbbox())
    out.save(f"assets/sticker_{n}.png", optimize=True)
    print(n, out.size)
