"""Gegner per SAM segmentieren und von der Higgsfield-Freistellung abziehen; fehlende Teile (Schläger) per SAM ergänzen.
Ausgabe: assets/cut/<name>.png (RGBA, auf Inhalt beschnitten)."""
import sys
import numpy as np
from PIL import Image, ImageFilter
from scipy import ndimage
from rembg import new_session, remove

A = "assets"
# Gruppen: (positive Punkte, negative Punkte, Box oder None)
OPP = {
 "thuerauf": [([(430,180)],[(660,310)],None), ([(400,330),(380,420)],[(600,420),(470,480)],None), ([(400,540),(360,620)],[(470,640),(500,560)],None),
              ([(340,700),(330,790)],[(420,760)],None), ([(650,800),(645,760)],[(580,820)],None), ([(300,560),(285,580)],[(330,450)],None), ([(370,382),(352,400)],[(330,450),(420,480)],None)],
 "clain": [([(365,230),(345,195),(340,255),(375,262)],[(470,220),(420,300)],None), ([(290,330),(270,380)],[(380,400)],None), ([(310,760),(305,840)],[(250,700)],None),
           ([(420,820),(420,760)],[(480,760),(250,900)],None), ([(110,650),(150,600)],[(250,700)],None), ([(240,420)],[(330,450)],None)],
 "hameed": [([(650,560)],[(575,380)],None), ([(680,720),(720,850)],[(560,700)],None), ([(660,1010)],[(560,1000)],None),
            ([(270,1280)],[(400,1290)],None), ([(770,1290),(770,1100)],[(660,1310)],None), ([(330,1180),(400,1080),(470,1140)],[(550,1100),(420,1220)],None),
            ([(700,940)],[(560,920)],None)],
}
FADE = {"hameed": (880, 1000)}
OPP["steinmann"] = [([(820, 150), (800, 70)], [(650, 250), (740, 260)], None), ([(850, 290), (880, 250)], [(760, 300), (700, 420)], None),
                    ([(770, 380), (772, 340)], [(700, 450), (760, 300), (765, 480), (790, 520), (820, 545)], None),
                    ([(870, 420), (863, 495)], [(800, 520), (885, 568), (840, 552)], None),
                    ([(745, 530)], [(800, 540), (790, 505)], None), ([(940, 140)], [(700, 200)], None)]
OPP["svec"] = [([(272, 585), (268, 605), (278, 545)], [(180, 610), (330, 520), (230, 520)], None), ([(405, 445)], [(330, 470), (450, 520)], None)]
ADD = {"hameed": [([(95,470),(60,200)],[],[30,70,180,500])]}
s = new_session("sam")


def seg(im, pos, neg, box):
    pr = [{"type": "point", "data": list(p), "label": 1} for p in pos] + [{"type": "point", "data": list(p), "label": 0} for p in neg]
    if box:
        pr.append({"type": "rectangle", "data": box, "label": 1})
    return np.array(remove(im, session=s, sam_prompt=pr, only_mask=True).convert("L").resize(im.size)) > 127


for name in sys.argv[1:] or ["thuerauf", "clain", "hameed", "kandra", "steinmann", "svec"]:
    im = Image.open(f"{A}/src/{name}.jpg").convert("RGB")
    raw = np.array(Image.open(f"{A}/cut/{name}_raw.png").convert("RGBA")).astype(np.float32)
    alpha = raw[..., 3] / 255
    opp = np.zeros(alpha.shape, bool)
    for g in OPP.get(name, []):
        opp |= seg(im, *g)
    opp = ndimage.binary_fill_holes(ndimage.binary_closing(opp, iterations=3))
    lab, n = ndimage.label(opp)  # Sprenkel (z. B. auf dem Gesicht des Spielers) verwerfen
    if n:
        sz = ndimage.sum(opp, lab, range(1, n + 1))
        opp = np.isin(lab, [i + 1 for i, v in enumerate(sz) if v >= 800])
    Image.fromarray((opp * 255).astype(np.uint8)).save(f"{A}/cut/{name}_opp.png")
    soft = np.array(Image.fromarray((opp * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(1.5))) / 255
    alpha = alpha * (1 - soft)
    # dünne Reste (Umrisslinien des Gegners) in der Nähe des Gegners entfernen
    zone = ndimage.binary_dilation(opp, iterations=14)
    opened = ndimage.binary_opening(alpha > 0.4, iterations=3)
    alpha = np.where(zone & ~opened, 0, alpha)
    rgb = raw[..., :3]
    for g in ADD.get(name, []):
        add = seg(im, *g)
        Image.fromarray((add * 255).astype(np.uint8)).save(f"{A}/cut/{name}_add.png")
        a2 = np.array(Image.fromarray((add * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(0.8))) / 255
        rgb = np.where(a2[..., None] > alpha[..., None], np.array(im).astype(np.float32), rgb)
        alpha = np.maximum(alpha, a2)
    # nur die größte zusammenhängende Fläche (plus Teile > 0,3 % davon) behalten
    lab, n = ndimage.label(alpha > 0.15)
    if n > 1:
        sizes = ndimage.sum(np.ones_like(alpha), lab, range(1, n + 1))
        keep = np.isin(lab, [i + 1 for i, sz in enumerate(sizes) if sz >= 0.02 * sizes.max()])
        alpha = alpha * ndimage.binary_dilation(keep, iterations=2)
    if name in FADE:  # weich nach unten ausblenden (Beine überschneiden sich mit dem Gegner)
        y0, y1 = FADE[name]
        ys = np.arange(alpha.shape[0])[:, None]
        alpha = alpha * np.clip((y1 - ys) / (y1 - y0), 0, 1)
    out = np.dstack([rgb, alpha * 255]).clip(0, 255).astype(np.uint8)
    img = Image.fromarray(out, "RGBA")
    img = img.crop(img.getbbox())
    img.save(f"{A}/cut/{name}.png")
    print(name, img.size)
