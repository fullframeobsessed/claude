"""Szenenliste für Video 01: Bild (SVG) + Sprechertext (eine Zeile = ein Untertitel-Block)."""
from art import *

CHANNEL = "Otto Normalpsyche"   # Platzhalter-Kanalname, hier ändern
NEXT_TITLE = ["Warum du kurz vor der", "Deadline plötzlich", "ein Genie bist"]

OTTO_Y = 360  # Kopfmitte bei Scale 1 -> Füße bei 860 (Untertitel-Zone bleibt frei)

SCENES = []


def scene(sid, svg, lines_=(), silent=0.0):
    SCENES.append({"id": sid, "svg": svg, "lines": list(lines_), "silent": silent})


# ---------------------------------------------------------------- INTRO ----
scene("s01_hook", page(
    otto(560, OTTO_Y, 1.0, "tired") + laptop(900, 520, 1.1) + clock(1520, 220, "09:00")),
    ["Das ist Otto.", "Otto hat heute genau eine Aufgabe.", "Und Otto wird sie nicht machen."])

scene("s02_bad", page(
    otto(620, OTTO_Y, 1.0, "happy", pose="raised", item="x", held=spray(150, -110)) + clock(1520, 220, "11:30")
    + sparkle(1050, 420, 1.4) + sparkle(1200, 600, 0.9) + sparkle(980, 700, 1.1) + sparkle(1300, 380, 0.7)),
    ["Stattdessen putzt Otto das Bad."])

socks = "".join(sock(980 + i * 130, 560, c, 0.9) for i, c in enumerate(["#FF4D4D", "#FFB300", "#FFE14D", "#4CD964", "#3FA9F5", "#9B59B6"]))
scene("s03_socken", page(otto(520, OTTO_Y, 1.0, "aha") + socks + clock(1520, 220, "14:00")),
      ["Sortiert seine Socken nach Farbe."])

scene("s04_pinguine", page(
    otto(560, OTTO_Y, 1.0, "aha", item="phone") + clock(1520, 220, "17:30")
    + card(980, 330, 520, 420, "#FFF") + text(1240, 400, "Pinguine – Wikipedia", 34)
    + penguin(1120, 560, 1.6) + penguin(1300, 590, 1.2) + penguin(1420, 610, 0.9)),
    ["Und liest zwei Stunden lang über Pinguine."])

scene("s05_faul", page(otto(520, OTTO_Y, 1.0, "excuse", pose="down") + text(1240, 560, "FAUL?", 260, color=INK)),
      ["Jetzt würden die meisten sagen: Otto ist faul."])

scene("s06_nicht_faul", page(
    otto(520, OTTO_Y + 40, 1.0, "happy", pose="raised", item="x", held=sock(150, -60, "#3FA9F5", 0.8))
    + text(1240, 560, "FAUL", 260, color=INK) + strike(930, 600, 1560, 420) + sparkle(160, 300, 0.9)),
    ["Aber faule Menschen sortieren keine Socken."])

chest = f'''<g transform="translate(1260,560)" stroke="{INK}" stroke-width="6" stroke-linejoin="round">
  <rect x="-200" y="-60" width="400" height="200" rx="16" fill="#C68A4E"/>
  <path d="M-200,-60 Q0,-170 200,-60 Z" fill="#D9A066"/>
  <rect x="-40" y="-40" width="80" height="90" rx="10" fill="#FFD43B"/>
  <path d="M-24,-40 v-30 a24,24 0 0 1 48,0 v30" fill="none" stroke-width="10"/>
  {text(0, 120, "TRICK", 48, color="#FFF", extra='stroke="none"')}</g>'''
scene("s07_versprechen", page(otto(480, OTTO_Y, 1.0, "smirk") + chest + text(1260, 260, "kommt am Ende …", 56)),
      ["Was mit Otto los ist, und vermutlich auch mit dir, ist etwas völlig anderes.",
       "Und wenn du es einmal verstanden hast, schiebst du deutlich weniger auf.",
       "Am Ende zeige ich dir einen Trick, der so simpel ist, dass er fast peinlich ist.",
       "Aber er ist wissenschaftlich getestet."])

# ---------------------------------------------------------- KAPITEL 1 ----
scene("s08_kap1", chapter_card(1, "Du bist nicht faul"), silent=2.2)

grid = "".join(person(1060 + (i % 10) * 76, 470 + (i // 10) * 120, ORANGE if i % 5 == 0 else "#C5CCD6", 0.8) for i in range(20))
scene("s09_zahlen", page(
    text(560, 380, "95 %", 220, color=ORANGE) + lines(560, 470, ["der Studierenden", "schieben regelmäßig auf"], 40, weight="normal")
    + grid + text(1400, 300, "jeder 5. Erwachsene: chronisch", 40) + text(W / 2, 860, "Quelle: Steel (2007), Psychological Bulletin", 26, weight="normal", color="#777")),
    ["Fangen wir mit einer Zahl an.",
     "Laut einer großen Übersichtsarbeit des Psychologen Piers Steel schieben bis zu 95 Prozent der Studierenden regelmäßig Dinge auf.",
     "Und etwa jeder fünfte Erwachsene tut es chronisch.",
     "Das sind nicht alles Faulpelze. Das ist einfach menschlich."])

scene("s10_zitat", page(
    card(260, 200, 1100, 520, "#FFF")
    + text(330, 330, "„", 160, color=ORANGE, anchor="start")
    + lines(810, 400, ["Aufschieben ist kein Problem", "des Zeitmanagements, sondern", "der Gefühlsregulation."], 54)
    + text(810, 660, "– sinngemäß nach Sirois & Pychyl (2013)", 30, weight="normal", color="#777")
    + otto(1600, OTTO_Y + 40, 0.9, "excuse", pose="down")),
    ["Der Psychologe Tim Pychyl forscht seit Jahrzehnten zu genau diesem Thema.",
     "Gemeinsam mit Fuschia Sirois hat er es auf einen Satz gebracht:",
     "Aufschieben ist kein Problem des Zeitmanagements, sondern der Gefühlsregulation."])

scene("s11_wolke", page(
    laptop(260, 580, 1.0, "") + cloud(560, 330, 1.1, words=("Langeweile", "Überforderung", "Angst, Fehler zu machen"))
    + otto(1450, OTTO_Y, 1.0, "shock", pose="down")),
    ["Heißt übersetzt: Otto vermeidet nicht die Steuererklärung.",
     "Otto vermeidet das Gefühl, das die Steuererklärung in ihm auslöst.",
     "Langeweile. Überforderung. Die Angst, etwas falsch zu machen."])

scene("s12_flucht", page(
    otto(520, OTTO_Y, 1.0, "happy", pose="raised", item="x", held=spray(150, -110))
    + sparkle(840, 300, 1.2) + sparkle(900, 520, 0.8)
    + card(1020, 330, 720, 300, "#FFF") + lines(1380, 450, ["Flucht vor dem", "GEFÜHL, nicht vor", "der Arbeit"], 56)),
    ["Und das Bad putzen? Das fühlt sich gut an. Man sieht sofort ein Ergebnis.",
     "Otto flüchtet also nicht vor der Arbeit.",
     "Otto flüchtet vor einem schlechten Gefühl."])

# ---------------------------------------------------------- KAPITEL 2 ----
scene("s13_kap2", chapter_card(2, "Der Kampf im Kopf"),
      ["Und jetzt wird's spannend.",
       "Denn in Ottos Kopf läuft in diesem Moment ein Kampf, den er praktisch nicht gewinnen kann."])

scene("s14_gehirn", page(
    brain(W / 2, 500, 1.9)
    + alarm_guy(720, 470, 1.1) + planner_guy(1220, 470, 1.1)
    + card(560, 612, 320, 100, "#FFF", 20, 4) + card(985, 612, 470, 100, "#FFF", 20, 4)
    + text(720, 650, "AMYGDALA", 36) + text(720, 694, "die Alarmanlage", 30, weight="normal")
    + text(1220, 650, "PRÄFRONTALER KORTEX", 36) + text(1220, 694, "der Planer", 30, weight="normal")),
    ["In deinem Gehirn sitzt die Amygdala, quasi deine Alarmanlage.",
     "Sie reagiert blitzschnell auf alles, was sich unangenehm oder bedrohlich anfühlt.",
     "Und dann gibt es den präfrontalen Kortex, den Planer.",
     "Der weiß, dass die Steuererklärung bis Freitag fertig sein muss."])

scene("s15_bochum", page(
    brain(W / 2, 540, 1.8)
    + '<path d="M830,540 q40,-30 80,0 t80,0 t80,0 t80,0" fill="none" stroke="#1E1E1E" stroke-width="3" stroke-dasharray="10 8"/>'
    + alarm_guy(720, 530, 1.5) + planner_guy(1220, 560, 0.8)
    + text(W / 2, 140, "Ruhr-Uni Bochum, 2018", 52) + text(W / 2, 200, "Schlüter et al., Psychological Science", 30, weight="normal", color="#777")
    + card(640, 718, 160, 60, "#FFF", 16, 4) + text(720, 760, "größer", 40, color="#FF3B30") + text(1020, 500, "schwache Verbindung", 30, weight="normal")),
    ["Forscher der Ruhr-Universität Bochum haben 2018 etwas Spannendes entdeckt.",
     "Bei Menschen, die eher dazu neigen, Dinge aufzuschieben, war die Amygdala größer.",
     "Und die Verbindung zwischen Alarmanlage und Planer war schwächer.",
     "Das heißt: Die Alarmanlage schreit „Gefahr!“, und der Planer kommt mit seinem Klemmbrett einfach nicht dagegen an."])

scene("s16_knopf", page(
    alarm_guy(540, 380, 1.4) + big_button(700, 660, "HANDY", 1.2)
    + otto(1400, OTTO_Y, 1.0, "tired", item="phone")
    + text(W / 2, 140, "Belohnung: JETZT", 64, color=ORANGE)),
    ["Und dann kommt noch dazu: Dein Gehirn liebt Belohnungen, und zwar jetzt.",
     "Das Handy belohnt dich in einer Sekunde."])

scene("s17_waage", page(
    balance(W / 2, 340, phone(-28, -110, 1.0) + heart(0, -150, 0.8),
            envelope(0, -70, [], 0.6), tilt=-14)
    + text(560, 280, "1 Sekunde", 44, color=ORANGE) + text(1380, 200, "Steuerbescheid, Juli", 44, color="#777")),
    ["Die Steuererklärung belohnt dich irgendwann im Juli, mit einem Bescheid vom Finanzamt.",
     "Rate mal, wer gewinnt."])

# ---------------------------------------------------------- KAPITEL 3 ----
scene("s18_kap3", chapter_card(3, "Der Fremde"),
      ["Aber der seltsamste Grund kommt erst noch.",
       "Denn Otto hat einen Mitbewohner, von dem er nichts weiß."])

scene("s19_morgenotto", page(
    otto(620, OTTO_Y, 1.0, "tired")
    + otto(1300, OTTO_Y, 1.0, "smirk", pose="bent", item="x", held=calendar(70, 230, "MORGEN", 0.7), bags="dark")
    + text(620, 120, "Otto", 54) + text(1300, 120, "Morgen-Otto", 54, color=ORANGE)),
    ["Darf ich vorstellen: Morgen-Otto."])

scene("s20_scans", page(
    scan(520, 430, "ich selbst", [(-60, -40, 40), (40, -70, 34), (0, 40, 46)])
    + scan(W / 2, 430, "ich in 10 Jahren", [(80, 10, 34), (-90, 60, 28)])
    + scan(1400, 430, "ein Fremder", [(70, 20, 34), (-80, 50, 30)])
    + text(1180, 150, "≈", 120, color=ORANGE) + text(W / 2, 860, "Hershfield et al. (2009)", 26, weight="normal", color="#777")),
    ["Der Psychologe Hal Hershfield hat Menschen im Hirnscanner gebeten, an sich selbst zu denken, an sich selbst in zehn Jahren und an fremde Personen.",
     "Das Ergebnis: Wenn wir an unser zukünftiges Ich denken, sieht die Gehirnaktivität eher so aus, als würden wir an einen Fremden denken."])

scene("s21_uebergabe", page(
    otto(560, OTTO_Y, 1.0, "smirk", pose="give", item="x", held=stack(212, 236, 4, s=0.8))
    + otto(1350, OTTO_Y, 1.0, "shock", pose="down", bags="dark")
    + text(1350, 120, "Morgen-Otto", 54, color=ORANGE)
    + bubble(120, 120, 520, 120, ["„Mach du das mal.“"], 40)),
    ["Und genau das macht Otto jeden Tag.",
     "Er denkt nicht: „Ich mache das morgen.“",
     "Er denkt, ohne es zu merken: „Der da macht das morgen.“"])

chain = "".join(otto(260 + i * 460, 430, 0.75, "tired" if i < 3 else "shock", pose="give" if i < 3 else "down",
                     item="x", held=stack(212, 236, 3 + i * 2, s=0.8) if i < 3 else "", bags="dark" if i else "normal")
                for i in range(4))
scene("s22_kette", page(
    chain + text(260, 170, "heute", 40) + text(720, 170, "morgen", 40) + text(1180, 170, "übermorgen", 40)
    + clock(1640, 170, "Fr 23:58", 0.8)),
    ["Das Problem: Morgen-Otto hat genau dieselben Gefühle. Dieselbe Alarmanlage. Dasselbe Handy.",
     "Und der schiebt es weiter an Übermorgen-Otto."])

# ---------------------------------------------------------- KAPITEL 4 ----
scene("s23_kap4", chapter_card(4, "Der Teufelskreis"), ["Jetzt passiert etwas Fieses."])

cyc = [("Aufgabe fühlt", "sich mies an", 960, 200, "sad"), ("Aufschieben", "", 1420, 460, "smirk"),
       ("kurze", "Erleichterung", 960, 720, "happy"), ("Schuldgefühl", "", 500, 460, "sad")]
arrows = f'<circle cx="960" cy="460" r="240" fill="none" stroke="{ORANGE}" stroke-width="14" stroke-dasharray="40 26"/>'
nodes = "".join(card(x - 170, y - 85, 340, 170, "#FFF") + head(x - 105, y, 0.42, f) + lines(x + 50, y - 8 + (0 if b else 14), [a, b] if b else [a], 28)
                for a, b, x, y, f in cyc)
scene("s24_kreis", page(arrows + nodes),
      ["Wenn Otto aufschiebt, geht es ihm kurz besser. Erleichterung.",
       "Aber ein paar Stunden später kommt das schlechte Gewissen.",
       "„Warum bin ich so? Ich krieg nichts auf die Reihe.“",
       "Und dieses Schuldgefühl ist ein neues schlechtes Gefühl, das an der Aufgabe klebt.",
       "Die Aufgabe fühlt sich also beim nächsten Mal noch schlimmer an. Also schiebt Otto sie noch weiter auf."])

scene("s25_fertigmachen", page(
    otto(520, OTTO_Y + 60, 0.88, "sad", pose="down")
    + card(980, 280, 760, 340, "#FFF") + lines(1360, 400, ["Sich fertigmachen", "macht es", "SCHLIMMER"], 60)
),
    ["Merkst du was?",
     "Das, was wir normalerweise tun, um uns selbst zu motivieren, also uns fertigmachen, ist genau das, was das Problem schlimmer macht.",
     "Und genau hier setzt der Trick an, den ich dir am Anfang versprochen habe."])

# ---------------------------------------------------------- KAPITEL 5 ----
scene("s26_kap5", chapter_card(5, "Der Ausweg"), ["Also. Was hilft wirklich?"])

bulb = f'''<g transform="translate(150,-150)" stroke="{INK}" stroke-width="6"><path d="M-17,0 a34,34 0 1 1 30,0 l0,26 l-30,0 Z" fill="#FFD43B"/>
  <rect x="-19" y="24" width="34" height="16" rx="4" fill="#9AA0A6"/></g>'''

scene("s27_vergeben", page(
    header("1 · Vergib dir selbst", ORANGE)
    + otto(560, OTTO_Y + 40, 1.0, "happy", pose="down")
    + bubble(860, 250, 840, 220, ["„Okay. War nicht ideal.", "Neuer Versuch.“"], 50)
    + text(1280, 640, "Wohl, Pychyl & Bennett (2010):", 34) + text(1280, 690, "Selbstvergebung → weniger Aufschieben", 34, weight="normal")),
    ["Werkzeug Nummer eins: Vergib dir selbst.",
     "In einer Studie von Michael Wohl, Tim Pychyl und Shannon Bennett wurden Studierende vor zwei Prüfungen begleitet.",
     "Diejenigen, die sich nach der ersten Prüfung selbst verziehen hatten, dass sie das Lernen aufgeschoben hatten, schoben vor der zweiten Prüfung weniger auf.",
     "Nicht Druck, sondern Nachsicht. Klingt nach Kalenderspruch, ist aber Forschung."])

tag = f'''<g transform="translate(1180,620) rotate(-6)" stroke="{INK}" stroke-width="6">
  <rect x="-230" y="-55" width="460" height="110" rx="18" fill="#FFF"/><circle cx="-190" cy="0" r="12" fill="{BG}"/>
  {text(20, 16, "Überforderung", 44, extra='stroke="none"')}</g>'''
scene("s28_benennen", page(
    header("2 · Benenne das Gefühl", ORANGE)
    + otto(480, OTTO_Y + 40, 1.0, "aha", pose="raised", item="x")
    + cloud(1200, 340, 0.55) + tag),
    ["Werkzeug Nummer zwei: Benenne das Gefühl.",
     "Frag dich ehrlich: Was genau will ich gerade nicht fühlen? Langeweile? Angst? Überforderung?",
     "Ein Gefühl, das einen Namen hat, verliert einen Teil seiner Macht."])

step = f'''<g stroke="{INK}" stroke-width="6" stroke-linejoin="round">
  <path d="M860,860 L1060,300 L1150,430 L1220,350 L1380,860 Z" fill="#9AA0A6"/>
  {text(1120, 700, "STEUER-", 44, color="#FFF", extra='stroke="none"')}{text(1120, 752, "ERKLÄRUNG", 44, color="#FFF", extra='stroke="none"')}
  <path d="M1420,560 L1520,560" stroke="{ORANGE}" stroke-width="14" stroke-linecap="round"/><path d="M1505,530 L1545,560 L1505,590" fill="none" stroke="{ORANGE}" stroke-width="14" stroke-linecap="round"/>
  <rect x="1580" y="780" width="220" height="80" rx="8" fill="{ORANGE}"/>
  {text(1690, 760, "Datei öffnen", 36)}</g>'''
scene("s29_schritt", page(header("3 · Der winzige erste Schritt", ORANGE) + otto(480, OTTO_Y + 40, 1.0, "smirk") + step),
      ["Werkzeug Nummer drei: der lächerlich kleine erste Schritt.",
       "Dein Gehirn reagiert auf „Steuererklärung machen“ mit Alarm.",
       "Aber auf „Datei öffnen“? Da passiert nichts. Zu klein, um Angst zu machen."])

scene("s30_timer", page(header("4 · Der 10-Minuten-Deal", ORANGE) + otto(480, OTTO_Y + 40, 1.0, "aha") + timer(1300, 450, "10:00", 1.0)),
      ["Werkzeug Nummer vier: der Zehn-Minuten-Deal.",
       "Mach mit dir einen Deal: nur zehn Minuten. Danach darfst du offiziell aufhören.",
       "Der Witz: Meistens machst du weiter.",
       "Denn das Schlimmste war nie die Arbeit, sondern der Moment davor."])

# ------------------------------------------------------------ AUFLÖSUNG ----
scene("s31_jetzt", page(otto(760, OTTO_Y, 1.0, "happy", label="JETZT") + laptop(1060, 520, 1.1, "") + sparkle(1500, 300, 1.0)),
      ["Otto ist nicht faul. Du auch nicht.",
       "Ihr habt beide nur ein Gehirn, das euch vor schlechten Gefühlen schützen will.",
       "Nur leider auf die dümmste mögliche Art."])

scene("s32_spaeter", page(otto(W / 2, OTTO_Y, 1.0, "smirk", label="SPÄTER")), silent=2.4)

scene("s33_deadline", page(
    otto(560, OTTO_Y, 1.0, "shock", pose="down") + laptop(980, 520, 1.1, "", glow=True)
    + sparks(1170, 500, 1.4) + clock(1520, 200, "Fr 23:58")),
    ["Aber warum Otto dann kurz vor der Deadline plötzlich zu einem Genie wird?",
     "Das ist eine ganz andere Geschichte."])

endcard = (text(W / 2, 150, CHANNEL, 84, color=ORANGE)
           + head(330, 520, 1.0, "smirk")
           + f'<rect x="1080" y="300" width="680" height="383" rx="24" fill="#FFF" stroke="{INK}" stroke-width="6" stroke-dasharray="18 12"/>'
           + text(1420, 260, "Nächstes Video", 40)
           + lines(1420, 440, NEXT_TITLE, 46)
           + f'<rect x="560" y="440" width="380" height="110" rx="55" fill="#FF3B30" stroke="{INK}" stroke-width="6"/>'
           + text(750, 512, "ABONNIEREN", 44, color="#FFF"))
scene("s34_endcard", page(endcard), silent=10.0)
