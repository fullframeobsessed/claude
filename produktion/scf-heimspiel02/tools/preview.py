import sys
from PIL import Image
A="assets/cut"; tiles=[]
for f in sys.argv[1:]:
    src=Image.open(f"assets/src/{f}.jpg").convert("RGB")
    for kind in ["sam"]:
        m=Image.open(f"{A}/{f}_{kind}.png").convert("L").resize(src.size)
        g=Image.new("RGB",src.size,(60,200,90)); g.paste(src,(0,0),m)
        tiles.append(g.resize((int(src.width*700/src.height),700)))
W=sum(t.width for t in tiles); s=Image.new("RGB",(W,700)); x=0
for t in tiles: s.paste(t,(x,0)); x+=t.width
s.save("/tmp/claude-0/sam.jpg")
