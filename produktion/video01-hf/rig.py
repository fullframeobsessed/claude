"""Otto-Rig und kleine HTML-Helfer, gemeinsam genutzt von Cartoon- und Doku-Version."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "video01"))
from art import INK, ORANGE, ORANGE_D, SKIN, GREY, mug, _arm, _hand, _head_base, _face  # noqa: E402


# ------------------------------------------------------------ Otto-Rig
def otto_svg(p, faces=("tired",), pose="down", item=None, held="", label="SPÄTER", bags="normal"):
    """Otto als SVG (600x760 Box, Kopfmitte bei 300,200). Gesichter einzeln schaltbar: #p-face-<name>."""
    b = []
    for lx in (-1, 1):
        d = f"M{45*lx},330 L{52*lx},470"
        b.append(f'<path d="{d}" stroke="{INK}" stroke-width="60" fill="none" stroke-linecap="round"/>'
                 f'<path d="{d}" stroke="{GREY}" stroke-width="48" fill="none" stroke-linecap="round"/>')
    b.append(f'<g stroke="{INK}" stroke-width="6" fill="#FFF"><path d="M-100,500 Q-100,462 -60,462 Q-28,462 -22,500 Z"/>'
             f'<path d="M100,500 Q100,462 60,462 Q28,462 22,500 Z"/></g>'
             f'<path d="M-100,494 L-22,494 M22,494 L100,494" stroke="{ORANGE}" stroke-width="5"/>')
    b.append(_arm("M-86,170 Q-132,235 -124,318") + _hand(-124, 336))
    b.append(f'''<g stroke="{INK}" stroke-width="6">
      <path d="M-92,100 Q0,160 92,100 Q112,150 78,168 L-78,168 Q-112,150 -92,100 Z" fill="{ORANGE_D}"/>
      <rect x="-22" y="100" width="44" height="50" fill="{SKIN}"/>
      <path d="M-96,152 Q0,132 96,152 L110,330 Q0,348 -110,330 Z" fill="{ORANGE}"/>
      <rect x="-112" y="318" width="224" height="26" rx="10" fill="{ORANGE_D}"/>
      <path d="M-52,142 Q0,200 52,142" fill="none"/>
      <path d="M-18,178 L-24,238 M18,178 L24,232" fill="none" stroke-width="5"/>
      <circle cx="-24" cy="244" r="6" fill="#FFF" stroke-width="4"/><circle cx="24" cy="238" r="6" fill="#FFF" stroke-width="4"/>
      <path d="M-62,256 L62,256 L78,318 L-78,318 Z" fill="#F08A3E"/></g>''')
    arm = f'<g id="{p}-arm">'
    if pose == "bent":
        arm += _arm("M86,170 Q140,230 126,272 Q100,300 30,244")
        arm += (mug(48, 190, label) + _hand(24, 234)) if item == "mug" else (held + _hand(30, 244))
    elif pose == "raised":
        arm += _arm("M86,170 Q150,140 150,40") + held + _hand(150, 28)
    else:
        arm += _arm("M86,170 Q132,235 124,318") + _hand(124, 336)
    arm += "</g>"
    b.append(arm)
    fs = "".join(f'<g id="{p}-face-{f}" opacity="{1 if i == 0 else 0}">{_face(f, bags)}</g>' for i, f in enumerate(faces))
    b.append(f'<g id="{p}-head">{_head_base()}{fs}</g>')
    return (f'<svg viewBox="-300 -200 600 760" width="600" height="760" overflow="visible">'
            f'{"".join(b)}</svg>')


def actor(id_, x, y, w, h, inner, extra=""):
    return f'<div id="{id_}" class="actor" style="left:{x}px;top:{y}px;width:{w}px;height:{h}px" {extra}>{inner}</div>'


def svgbox(inner, vb, w, h):
    return f'<svg viewBox="{vb}" width="{w}" height="{h}" overflow="visible">{inner}</svg>'


