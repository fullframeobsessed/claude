# SPEC: Video 01, Animations-Probe (0:00–0:42.6)

GOAL:    Zuschauer lacht über Otto, erkennt sich wieder und will den versprochenen „peinlichen Trick“ sehen.
OUTPUT:  HyperFrames, 1920 x 1080, 30 fps
TIME:    42.6 s x 30 = 1278 Frames. Uhr = Sprecherspur (Piper Thorsten v2); Texte landen auf ihrem Wort.
LOOK:    Grund #FFF8EE (Creme), Tinte #1E1E1E, Akzent #FF7A1A nur auf Ottos Hoodie, einem Schlüsselwort pro Shot
         und der Kapitelkarte. Stimmungsflächen pro Tätigkeit: Bad #DDEFFF, Socken #FFF0D2, Handy #E6F4EA.
         Display: Archivo Black, Heldenwörter 220–300 px; Text: Nunito 800, 44–64 px; Uhr: Space Mono 64 px.
         Medium: flache 2D-Vektor-Illustration, 6 px Outlines #1E1E1E, keine Verläufe, keine Schatten.
OBJECTS: Otto (Hoodie, Augenringe, Tasse „SPÄTER“), To-do-Zettel mit Kästchen, Digitaluhr, Sprühflasche + Glitzer,
         6 Socken (Regenbogen), Handy-Karte „Pinguine – Wikipedia“ mit Pinguinen, Spiegel mit Rahmen und Halterung,
         Balken „Aufschieben“, Schatztruhe mit Schloss, Stempel „WISSENSCHAFTLICH GETESTET“.
MOTION:  Ankunft expo.out 0.45–0.6 s; Otto/Requisiten federn back.out(1.5) (Dämpfung ≈0.5, verspielt), nie auf Opazität.
         Abgang power3.in, 40 % kürzer. Kamera power2.inOut. Stagger: Socken 0.12 s, Wörter 0.067 s.
         Gesichtswechsel immer mit Squash (Kopf scaleY 0.9 → 1, 0.25 s).
SHOTS:   s1 0–6.63    Otto federt rein · „OTTO“ Buchstabe für Buchstabe · To-do-Zettel · Punch-in auf Tasse SPÄTER
         s2 6.63–15.3 Montage: Bad (Farbflut blau, Glitzer) · Socken fliegen in Reihe · Handy mit Pinguinen; Uhr rollt 11:30→14:00→17:30
         s3 15.3–22.2 Whip rein · „FAUL?“ knallt auf „faul“ · roter Strich auf „Aber“ · Socke ploppt hoch
         s4 22.2–40.4 Spiegel „DU?“ · Balken schrumpft auf „weniger“ · Truhe „TRICK“ · Stempel knallt · Iris aus dem Schloss
         s5 40.4–42.6 Kapitelkarte Orange, Titel Wort für Wort
BANNED:  dunkler Hintergrund, Glow, Partikel als Deko, Verläufe, alles zentriert, alles fade+slide-up,
         Titel, die nach dem Landen weiterdriften, Pillen-Chips, HUD-Ecken.
QA:      t=0.9 Otto steht · t=3.8 Zettel lesbar · t=6.2 Tasse füllt Bild · t=10.8 Sockenreihe · t=17.9 FAUL? ·
         t=19.6 Strich · t=27 Spiegel · t=32 Balken kurz · t=38.5 Stempel · t=41.5 Kapitelkarte
