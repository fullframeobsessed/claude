"""SVG-Bausteine für Otto und die Szenen von Video 01 (1920x1080)."""

W, H = 1920, 1080
INK = "#1E1E1E"
ORANGE = "#FF7A1A"
ORANGE_D = "#D9600F"
SKIN = "#F6D2B3"
HAIR = "#5B3A29"
BG = "#FFF8EE"
GREY = "#6B7280"
FONT = "'DejaVu Sans', 'Liberation Sans', Arial, sans-serif"


def esc(t):
    return t.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def text(x, y, s, size=40, weight="bold", color=INK, anchor="middle", extra=""):
    return (f'<text x="{x}" y="{y}" font-size="{size}" font-weight="{weight}" fill="{color}" '
            f'text-anchor="{anchor}" font-family="{FONT}" {extra}>{esc(s)}</text>')


def lines(x, y, rows, size=40, lh=1.25, **kw):
    return "".join(text(x, y + i * size * lh, r, size, **kw) for i, r in enumerate(rows))


def page(inner, bg=BG):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">'
            f'<rect width="{W}" height="{H}" fill="{bg}"/>{inner}</svg>')


# ---------------------------------------------------------------- Otto ----

def _head_base():
    return f'''<g stroke="{INK}" stroke-width="6" stroke-linejoin="round">
      <ellipse cx="-106" cy="12" rx="18" ry="26" fill="#F2C6A4"/>
      <ellipse cx="106" cy="12" rx="18" ry="26" fill="#F2C6A4"/>
      <ellipse cx="0" cy="0" rx="105" ry="115" fill="{SKIN}"/>
      <path fill="{HAIR}" d="M-108,0 C-122,-85 -70,-138 0,-132 C72,-138 122,-85 108,0 C98,-38 84,-55 62,-60 L52,-34 L38,-64 C14,-56 -6,-58 -24,-66 L-36,-38 L-50,-66 C-76,-60 -96,-38 -108,0 Z"/>
      <path fill="{HAIR}" d="M-28,-128 L-20,-168 L2,-130 Z"/>
      <path fill="{HAIR}" d="M8,-131 L44,-160 L36,-122 Z"/>
      <path fill="{HAIR}" d="M-62,-112 L-88,-138 L-44,-124 Z"/></g>'''


def _face(kind, bags="normal"):
    bag_col, bag_w = ("#7d4f6e", 7) if bags == "dark" else ("#B48A8A", 4)
    nose = '<path d="M2,22 Q12,42 -4,46" fill="none" stroke-width="5"/>'
    eyes_open = ('<ellipse cx="-38" cy="8" rx="22" ry="24" fill="#FFF"/>'
                 '<ellipse cx="38" cy="8" rx="22" ry="24" fill="#FFF"/>')
    bagsvg = f'<path d="M-56,40 Q-38,50 -20,40 M20,40 Q38,50 56,40" fill="none" stroke="{bag_col}" stroke-width="{bag_w}"/>'
    lids = (f'<path d="M-61,9 A22,24 0 0 1 -15,9 Z" fill="{SKIN}"/>'
            f'<path d="M15,9 A22,24 0 0 1 61,9 Z" fill="{SKIN}"/>')
    f = {
        "tired": eyes_open + f'<circle cx="-34" cy="14" r="9" fill="{INK}" stroke="none"/><circle cx="42" cy="14" r="9" fill="{INK}" stroke="none"/>'
                 + lids + bagsvg + '<path d="M-62,-30 L-16,-24 M16,-26 L62,-36" fill="none"/>' + nose
                 + '<path d="M-26,72 Q4,82 32,62" fill="none"/>',
        "shock": '<ellipse cx="-38" cy="4" rx="27" ry="32" fill="#FFF"/><ellipse cx="38" cy="4" rx="27" ry="32" fill="#FFF"/>'
                 f'<circle cx="-38" cy="6" r="6" fill="{INK}" stroke="none"/><circle cx="38" cy="6" r="6" fill="{INK}" stroke="none"/>'
                 '<path d="M-64,-34 Q-40,-54 -14,-38 M14,-38 Q40,-54 64,-34" fill="none"/>' + nose
                 + '<ellipse cx="0" cy="78" rx="18" ry="24" fill="#6B2A2A"/>',
        "aha": '<ellipse cx="-38" cy="6" rx="23" ry="26" fill="#FFF"/><ellipse cx="38" cy="6" rx="23" ry="26" fill="#FFF"/>'
               f'<circle cx="-36" cy="6" r="12" fill="{INK}" stroke="none"/><circle cx="40" cy="6" r="12" fill="{INK}" stroke="none"/>'
               '<circle cx="-31" cy="1" r="4" fill="#FFF" stroke="none"/><circle cx="45" cy="1" r="4" fill="#FFF" stroke="none"/>'
               '<path d="M-62,-38 Q-40,-50 -16,-38 M16,-38 Q40,-50 62,-38" fill="none"/>' + nose
               + '<path d="M-44,58 Q0,112 44,58 Z" fill="#6B2A2A"/><path d="M-20,82 Q0,96 20,82 Q0,74 -20,82 Z" fill="#E36A6A" stroke-width="3"/>',
        "excuse": eyes_open + f'<circle cx="-24" cy="10" r="9" fill="{INK}" stroke="none"/><circle cx="52" cy="10" r="9" fill="{INK}" stroke="none"/>'
                  '<path d="M-62,-26 L-16,-34 M16,-34 L62,-26" fill="none"/>' + nose
                  + '<path d="M-30,72 q10,-10 20,0 t20,0 t20,0" fill="none"/>'
                  '<path d="M-78,-58 q-14,22 0,30 q14,-8 0,-30 Z" fill="#7CC4FF" stroke-width="4"/>',
        "happy": '<path d="M-60,14 Q-38,-12 -16,14 M16,14 Q38,-12 60,14" fill="none" stroke-width="7"/>'
                 '<path d="M-62,-34 Q-40,-46 -16,-36 M16,-36 Q40,-46 62,-34" fill="none"/>' + nose
                 + '<path d="M-40,60 Q0,104 40,60 Z" fill="#6B2A2A"/>'
                 '<ellipse cx="-62" cy="46" rx="14" ry="8" fill="#F4A9A0" stroke="none"/><ellipse cx="62" cy="46" rx="14" ry="8" fill="#F4A9A0" stroke="none"/>',
        "sad": eyes_open + f'<circle cx="-38" cy="18" r="9" fill="{INK}" stroke="none"/><circle cx="38" cy="18" r="9" fill="{INK}" stroke="none"/>'
               + bagsvg + '<path d="M-62,-22 L-18,-38 M18,-38 L62,-22" fill="none"/>' + nose
               + '<path d="M-28,80 Q0,62 28,80" fill="none"/>',
        "smirk": eyes_open + f'<circle cx="-30" cy="14" r="9" fill="{INK}" stroke="none"/><circle cx="46" cy="14" r="9" fill="{INK}" stroke="none"/>'
                 + lids + bagsvg + '<path d="M-62,-26 L-16,-24 M16,-32 L62,-44" fill="none"/>' + nose
                 + '<path d="M-20,70 Q10,76 36,56" fill="none"/>',
    }[kind]
    return f'<g stroke="{INK}" stroke-width="6" stroke-linecap="round" stroke-linejoin="round">{f}</g>'


def head(x, y, s=1.0, face="tired", bags="normal"):
    return f'<g transform="translate({x},{y}) scale({s})">{_head_base()}{_face(face, bags)}</g>'


def mug(x, y, label="SPÄTER", s=1.0):
    return f'''<g transform="translate({x},{y}) scale({s})" stroke="{INK}" stroke-width="6" stroke-linejoin="round">
      <path d="M-2,8 C-30,8 -30,48 -2,48" fill="none" stroke-width="10"/>
      <rect x="0" y="0" width="70" height="78" rx="8" fill="#FFF"/>
      {text(35, 46, label, 14, color=ORANGE, extra='stroke="none"')}
      <path d="M20,-10 q-8,-12 0,-22 q8,-10 0,-22 M45,-10 q-8,-12 0,-22 q8,-10 0,-22" fill="none" stroke="#9AA0A6" stroke-width="4" stroke-linecap="round"/></g>'''


def phone(x, y, s=1.0, screen="#8EC5FF", icon=""):
    return f'''<g transform="translate({x},{y}) scale({s})" stroke="{INK}" stroke-width="6" stroke-linejoin="round">
      <rect x="0" y="0" width="56" height="100" rx="10" fill="#2B2B2B"/>
      <rect x="7" y="10" width="42" height="74" rx="4" fill="{screen}" stroke-width="3"/>{icon}</g>'''


def _arm(d, col=ORANGE):
    return (f'<path d="{d}" stroke="{INK}" stroke-width="54" fill="none" stroke-linecap="round"/>'
            f'<path d="{d}" stroke="{col}" stroke-width="42" fill="none" stroke-linecap="round"/>')


def _hand(x, y):
    return f'<circle cx="{x}" cy="{y}" r="21" fill="{SKIN}" stroke="{INK}" stroke-width="6"/>'


def otto(x, y, s=1.0, face="tired", pose="bent", item="mug", label="SPÄTER", bags="normal", held=""):
    """x,y = Kopfmitte. Füße enden bei y+500*s. pose: bent|raised|down|give. held = SVG am Handpunkt."""
    p = [f'<g transform="translate({x},{y}) scale({s})" stroke-linejoin="round">']
    for lx in (-1, 1):
        d = f"M{45*lx},330 L{52*lx},470"
        p.append(f'<path d="{d}" stroke="{INK}" stroke-width="60" fill="none" stroke-linecap="round"/>')
        p.append(f'<path d="{d}" stroke="{GREY}" stroke-width="48" fill="none" stroke-linecap="round"/>')
    p.append(f'<g stroke="{INK}" stroke-width="6" fill="#FFF"><path d="M-100,500 Q-100,462 -60,462 Q-28,462 -22,500 Z"/>'
             f'<path d="M100,500 Q100,462 60,462 Q28,462 22,500 Z"/></g>'
             f'<path d="M-100,494 L-22,494 M22,494 L100,494" stroke="{ORANGE}" stroke-width="5"/>')
    p.append(_arm("M-86,170 Q-132,235 -124,318") + _hand(-124, 336))
    p.append(f'''<g stroke="{INK}" stroke-width="6">
      <path d="M-92,100 Q0,160 92,100 Q112,150 78,168 L-78,168 Q-112,150 -92,100 Z" fill="{ORANGE_D}"/>
      <rect x="-22" y="100" width="44" height="50" fill="{SKIN}"/>
      <path d="M-96,152 Q0,132 96,152 L110,330 Q0,348 -110,330 Z" fill="{ORANGE}"/>
      <rect x="-112" y="318" width="224" height="26" rx="10" fill="{ORANGE_D}"/>
      <path d="M-52,142 Q0,200 52,142" fill="none"/>
      <path d="M-18,178 L-24,238 M18,178 L24,232" fill="none" stroke-width="5"/>
      <circle cx="-24" cy="244" r="6" fill="#FFF" stroke-width="4"/><circle cx="24" cy="238" r="6" fill="#FFF" stroke-width="4"/>
      <path d="M-62,256 L62,256 L78,318 L-78,318 Z" fill="#F08A3E"/></g>''')
    if pose == "bent":
        p.append(_arm("M86,170 Q140,230 126,272 Q100,300 30,244"))
        if item == "mug":
            p.append(mug(48, 190, label))
            p.append(_hand(24, 234))
        elif item == "phone":
            p.append(phone(20, 170, 1.0))
            p.append(_hand(30, 250))
        else:
            p.append(held)
            p.append(_hand(30, 244))
    elif pose == "raised":
        p.append(_arm("M86,170 Q150,140 150,40"))
        if item == "mug":
            p.append(mug(140, -70, label))
        else:
            p.append(held)
        p.append(_hand(150, 28))
    elif pose == "give":
        p.append(_arm("M86,170 Q140,220 205,235"))
        p.append(held)
        p.append(_hand(212, 238))
    else:  # down
        p.append(_arm("M86,170 Q132,235 124,318") + _hand(124, 336))
    p.append(_head_base() + _face(face, bags))
    p.append("</g>")
    return "".join(p)


# --------------------------------------------------------------- Props ----

def laptop(x, y, s=1.0, screen="Steuererklärung.pdf", glow=False):
    g = '<rect x="-20" y="-20" width="420" height="270" rx="30" fill="#FFE9A8" stroke="none" opacity="0.7"/>' if glow else ""
    return f'''<g transform="translate({x},{y}) scale({s})" stroke="{INK}" stroke-width="6" stroke-linejoin="round">{g}
      <rect x="20" y="0" width="340" height="210" rx="14" fill="#3A3F47"/>
      <rect x="38" y="18" width="304" height="174" rx="6" fill="#FFF" stroke-width="4"/>
      <rect x="54" y="34" width="60" height="74" fill="#E8EEF6" stroke-width="3"/>
      <path d="M130,48 h190 M130,70 h170 M130,92 h185 M54,128 h260 M54,150 h230 M54,172 h250" stroke="#C5CCD6" stroke-width="6"/>
      <path d="M0,210 L380,210 L400,236 L-20,236 Z" fill="#9AA0A6"/>
      {text(190, 270, screen, 26, color=INK, extra='stroke="none"') if screen else ""}</g>'''


def clock(x, y, t, s=1.0, col=INK):
    return f'''<g transform="translate({x},{y}) scale({s})">
      <rect x="-120" y="-55" width="240" height="110" rx="22" fill="{INK}"/>
      <rect x="-106" y="-41" width="212" height="82" rx="12" fill="#2E3B2E"/>
      {text(0, 22, t, 60, color="#7CFF8A", extra='font-family="DejaVu Sans Mono"')}</g>'''


def sparkle(x, y, s=1.0, col="#FFD43B"):
    return (f'<path transform="translate({x},{y}) scale({s})" d="M0,-40 Q6,-6 40,0 Q6,6 0,40 Q-6,6 -40,0 Q-6,-6 0,-40 Z" '
            f'fill="{col}" stroke="{INK}" stroke-width="4" stroke-linejoin="round"/>')


def spray(x, y, s=1.0):
    return f'''<g transform="translate({x},{y}) scale({s})" stroke="{INK}" stroke-width="6" stroke-linejoin="round">
      <rect x="-30" y="0" width="60" height="110" rx="12" fill="#7CC4FF"/>
      <path d="M-18,0 L-18,-30 L40,-30 L40,-14 L18,-14 L18,0 Z" fill="#FFF"/>
      <path d="M60,-40 l30,-10 M60,-22 l36,0 M60,-4 l30,10" stroke="#7CC4FF" stroke-width="6" stroke-linecap="round"/></g>'''


def sock(x, y, col, s=1.0, rot=0):
    return (f'<g transform="translate({x},{y}) rotate({rot}) scale({s})" stroke="{INK}" stroke-width="6" stroke-linejoin="round">'
            f'<path d="M-22,-80 L22,-80 L22,10 Q22,40 52,40 Q72,40 72,58 Q72,80 44,80 L0,80 Q-22,80 -22,50 Z" fill="{col}"/>'
            f'<path d="M-22,-62 L22,-62" stroke-width="5"/></g>')


def penguin(x, y, s=1.0):
    return f'''<g transform="translate({x},{y}) scale({s})" stroke="{INK}" stroke-width="5" stroke-linejoin="round">
      <ellipse cx="0" cy="0" rx="34" ry="46" fill="#2B2B2B"/><ellipse cx="0" cy="10" rx="22" ry="32" fill="#FFF"/>
      <circle cx="-9" cy="-22" r="4" fill="#FFF" stroke="none"/><circle cx="9" cy="-22" r="4" fill="#FFF" stroke="none"/>
      <path d="M-8,-12 L8,-12 L0,-2 Z" fill="#FFB300" stroke-width="3"/>
      <path d="M-18,46 l-10,6 h20 Z M18,46 l10,6 h-20 Z" fill="#FFB300" stroke-width="3"/></g>'''


def cloud(x, y, s=1.0, col="#8C95A3", words=()):
    w = "".join(text(0, -50 + i * 40, t, 28, color="#FFF") for i, t in enumerate(words))
    return f'''<g transform="translate({x},{y}) scale({s})">
      <path d="M-200,60 Q-260,60 -250,0 Q-250,-60 -180,-60 Q-170,-130 -80,-120 Q-30,-170 40,-130 Q120,-160 160,-90 Q250,-90 240,-10 Q270,60 190,70 Z"
            fill="{col}" stroke="{INK}" stroke-width="6" stroke-linejoin="round"/>
      {w}
      <path d="M-120,80 l-20,60 l30,-10 l-20,60" fill="none" stroke="#FFD43B" stroke-width="10" stroke-linecap="round" stroke-linejoin="round"/></g>'''


def card(x, y, w, h, fill="#FFF", r=28, sw=6):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="{fill}" stroke="{INK}" stroke-width="{sw}"/>'


def bubble(x, y, w, h, rows, size=36, tail="left"):
    tx = x + 60 if tail == "left" else x + w - 60
    d = (f'M{tx-20},{y+h-3} L{tx-40 if tail=="left" else tx+40},{y+h+50} L{tx+20},{y+h-3} Z')
    body = card(x, y, w, h)
    return (body + f'<path d="{d}" fill="#FFF" stroke="{INK}" stroke-width="6" stroke-linejoin="round"/>'
            f'<rect x="{tx-16}" y="{y+h-12}" width="32" height="12" fill="#FFF"/>'
            + lines(x + w / 2, y + h / 2 - (len(rows) - 1) * size * 0.62 + size * 0.35, rows, size))


def person(x, y, col, s=1.0):
    return (f'<g transform="translate({x},{y}) scale({s})" stroke="{INK}" stroke-width="5">'
            f'<circle cx="0" cy="-40" r="22" fill="{col}"/><path d="M-32,40 Q-32,-8 0,-8 Q32,-8 32,40 Z" fill="{col}"/></g>')


def brain(x, y, s=1.0, col="#F7A8C4"):
    return f'''<g transform="translate({x},{y}) scale({s})" stroke="{INK}" stroke-width="6" stroke-linejoin="round">
      <path d="M-170,40 Q-210,-20 -160,-80 Q-150,-160 -60,-150 Q0,-200 70,-150 Q160,-170 175,-80 Q220,-20 175,50 Q170,130 80,130 Q20,170 -50,135 Q-150,150 -170,40 Z" fill="{col}"/>
      <path d="M0,-150 Q-20,-60 10,0 Q30,60 0,130 M-120,-70 Q-80,-40 -110,10 M110,-80 Q70,-40 110,0 M-90,70 Q-50,60 -60,110 M90,60 Q60,80 80,110"
            fill="none" stroke="#C9708F" stroke-width="5"/></g>'''


def alarm_guy(x, y, s=1.0):
    return f'''<g transform="translate({x},{y}) scale({s})" stroke="{INK}" stroke-width="6" stroke-linejoin="round">
      <path d="M-40,-60 h80 v-20 q0,-30 -40,-30 q-40,0 -40,30 Z" fill="#FF4D4D"/>
      <path d="M-70,-110 l-20,-20 M70,-110 l20,-20 M0,-130 v-26" stroke="#FF4D4D" stroke-width="8" stroke-linecap="round"/>
      <circle cx="0" cy="0" r="62" fill="#FF8A65"/>
      <ellipse cx="-22" cy="-6" rx="14" ry="18" fill="#FFF"/><ellipse cx="22" cy="-6" rx="14" ry="18" fill="#FFF"/>
      <circle cx="-22" cy="-4" r="5" fill="{INK}" stroke="none"/><circle cx="22" cy="-4" r="5" fill="{INK}" stroke="none"/>
      <ellipse cx="0" cy="30" rx="16" ry="14" fill="#6B2A2A"/></g>'''


def planner_guy(x, y, s=1.0):
    return f'''<g transform="translate({x},{y}) scale({s})" stroke="{INK}" stroke-width="6" stroke-linejoin="round">
      <rect x="-56" y="-60" width="112" height="124" rx="40" fill="#8EC5FF"/>
      <circle cx="-22" cy="-10" r="16" fill="#FFF"/><circle cx="22" cy="-10" r="16" fill="#FFF"/><path d="M-6,-10 h12" />
      <circle cx="-22" cy="-6" r="5" fill="{INK}" stroke="none"/><circle cx="22" cy="-6" r="5" fill="{INK}" stroke="none"/>
      <path d="M-18,30 Q0,22 18,30" fill="none"/>
      <rect x="40" y="0" width="56" height="74" rx="6" fill="#FFF"/><path d="M52,22 h32 M52,38 h32 M52,54 h24" stroke-width="4"/>
      <rect x="56" y="-8" width="24" height="14" rx="3" fill="#9AA0A6" stroke-width="4"/></g>'''


def big_button(x, y, label, s=1.0):
    return f'''<g transform="translate({x},{y}) scale({s})" stroke="{INK}" stroke-width="6">
      <rect x="-130" y="20" width="260" height="70" rx="16" fill="#9AA0A6"/>
      <ellipse cx="0" cy="20" rx="110" ry="40" fill="#B71C1C"/><path d="M-110,20 L-110,-10 A110,40 0 0 1 110,-10 L110,20 A110,40 0 0 1 -110,20 Z" fill="#FF4D4D"/>
      <ellipse cx="0" cy="-10" rx="110" ry="40" fill="#FF6B6B"/>
      {text(0, 72, label, 40, color="#FFF", extra='stroke="none"')}</g>'''


def envelope(x, y, rows, s=1.0):
    return (f'<g transform="translate({x},{y}) scale({s})" stroke="{INK}" stroke-width="6" stroke-linejoin="round">'
            f'<rect x="-110" y="-70" width="220" height="140" rx="8" fill="#E6E2DA"/><path d="M-110,-70 L0,10 L110,-70" fill="none"/></g>'
            + lines(x, y + 110 * s, rows, 26 * s, weight="bold", color="#555"))


def heart(x, y, s=1.0, col="#FF4D6D"):
    return (f'<path transform="translate({x},{y}) scale({s})" d="M0,30 C-60,-10 -40,-60 0,-30 C40,-60 60,-10 0,30 Z" '
            f'fill="{col}" stroke="{INK}" stroke-width="5" stroke-linejoin="round"/>')


def balance(x, y, left, right, tilt=-14):
    return f'''<g transform="translate({x},{y})" stroke="{INK}" stroke-width="6" stroke-linejoin="round">
      <path d="M-60,300 L60,300 L20,260 L-20,260 Z" fill="#9AA0A6"/><rect x="-10" y="40" width="20" height="222" fill="#C5CCD6"/>
      <g transform="rotate({tilt})">
        <rect x="-330" y="20" width="660" height="22" rx="10" fill="#C5CCD6"/>
        <path d="M-300,40 L-360,170 M-300,40 L-240,170 M300,40 L240,170 M300,40 L360,170" stroke-width="4"/>
        <g transform="translate(-300,170) rotate({-tilt})"><path d="M-90,0 Q0,60 90,0 Z" fill="#E6E2DA"/>{left}</g>
        <g transform="translate(300,170) rotate({-tilt})"><path d="M-90,0 Q0,60 90,0 Z" fill="#E6E2DA"/>{right}</g>
      </g><circle cx="0" cy="40" r="16" fill="{ORANGE}"/></g>'''


def calendar(x, y, label, s=1.0):
    return f'''<g transform="translate({x},{y}) scale({s})" stroke="{INK}" stroke-width="6" stroke-linejoin="round">
      <rect x="-80" y="-70" width="160" height="150" rx="14" fill="#FFF"/><rect x="-80" y="-70" width="160" height="44" rx="14" fill="#FF4D4D"/>
      <path d="M-40,-86 v30 M40,-86 v30" stroke-linecap="round"/>{text(0, 36, label, 30, extra='stroke="none"')}</g>'''


def stack(x, y, n=4, label="Steuer-\nerklärung", s=1.0):
    sheets = "".join(f'<rect x="{-80 + (i % 2) * 6}" y="{-i * 16}" width="160" height="26" rx="4" fill="#FFF"/>' for i in range(n))
    top = -n * 16 - 90
    tl = label.split("\n")
    return (f'<g transform="translate({x},{y}) scale({s})" stroke="{INK}" stroke-width="5" stroke-linejoin="round">{sheets}'
            f'<rect x="-80" y="{top}" width="160" height="100" rx="6" fill="#FFF3D6"/>'
            + lines(0, top + 42, tl, 24, extra='stroke="none"') + '</g>')


def scan(x, y, label, spots, s=1.0):
    sp = "".join(f'<circle cx="{a}" cy="{b}" r="{r}" fill="#FFB300" opacity="0.85" stroke="none"/>' for a, b, r in spots)
    return (f'<g transform="translate({x},{y}) scale({s})"><ellipse cx="0" cy="0" rx="190" ry="160" fill="#2B2F38" stroke="{INK}" stroke-width="6"/>'
            f'<path d="M0,-150 Q-20,-40 0,0 Q20,60 0,150" fill="none" stroke="#4A5160" stroke-width="5"/>{sp}</g>'
            + text(x, y + 220 * s, label, 38))


def stairs_scene(x, y):
    return f'''<g transform="translate({x},{y})" stroke="{INK}" stroke-width="6" stroke-linejoin="round">
      <path d="M-520,300 L-300,-160 L-230,-60 L-180,-120 L-40,300 Z" fill="#9AA0A6"/>
      <path d="M-300,-160 L-330,-96 L-290,-110 L-262,-94 Z" fill="#FFF"/>
      </g>'''


def timer(x, y, t="10:00", s=1.0):
    return f'''<g transform="translate({x},{y}) scale({s})" stroke="{INK}" stroke-width="6" stroke-linejoin="round">
      <rect x="-24" y="-200" width="48" height="34" rx="6" fill="#9AA0A6"/>
      <circle cx="0" cy="0" r="170" fill="#FFF"/><circle cx="0" cy="0" r="140" fill="#FFF3D6" stroke-width="4"/>
      <path d="M0,0 L0,-140 A140,140 0 0 1 121,70 Z" fill="{ORANGE}" stroke-width="4"/>
      <circle cx="0" cy="0" r="14" fill="{INK}"/>{text(0, 240, t, 64, extra='stroke="none"')}</g>'''


def sparks(x, y, s=1.0):
    return "".join(f'<path transform="translate({x},{y}) scale({s}) rotate({a})" d="M0,-30 L0,-80" stroke="#FFB300" stroke-width="8" stroke-linecap="round"/>'
                   for a in range(-80, 81, 32))


def strike(x1, y1, x2, y2, col="#FF3B30", w=16):
    return f'<path d="M{x1},{y1} L{x2},{y2}" stroke="{col}" stroke-width="{w}" stroke-linecap="round"/>'


def header(t, col=INK):
    return text(W / 2, 110, t, 64, color=col)


def chapter_card(num, title):
    inner = (text(W / 2, 400, f"KAPITEL {num}", 64, color="#FFE0C2")
             + text(W / 2, 540, title, 120, color="#FFF")
             + head(W / 2, 760, 0.7, "tired"))
    return page(inner, bg=ORANGE)
