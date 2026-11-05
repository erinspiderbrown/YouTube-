"""Oscar Pistorius documentary build: voiceover-driven, real news/race/court footage + Commons photos,
neon motion graphics. Same pipeline as projects/jon-drummond/jd_build.py (v2), plus:

  - opts 'cb' / 'ct': crop this fraction off the bottom / top of a source (removes news tickers and captions)
  - opts 'label' / 'sub': neon name plate on an archive shot (judge, prosecutor, athletes)
  - opts 'soft': respectful shot (Reeva Steenkamp, her family, the night itself). Cuts touching a soft shot are
    plain cuts: no glitch transition, no transition/HUD/photo sounds, no keyword pop-ups.

Shot kinds:  g graphic (op_mograph) · a archive full-bleed · f archive framed in neon · p Commons photo card
Stages: shots -> transitions -> compose -> audio -> mux
Run:  python3 -I projects/oscar-pistorius/op_build.py [stage ...]
"""
import json, os, subprocess, sys
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageEnhance, ImageOps

ROOT = "/home/user/YouTube-"
P = f"{ROOT}/projects/oscar-pistorius"
SCR = "/tmp/claude-0/-home-user-YouTube-/bff383cd-82f6-5dd5-b6f3-63c9b3879318/scratchpad"
R = f"{SCR}/render_op"; os.makedirs(f"{R}/frames", exist_ok=True)
REAL = f"{SCR}/pistorius/real"      # YouTube imports via vidIQ (credits.md)
PHOTOS = f"{SCR}/pistorius/photos"  # Wikimedia Commons (credits.md)
sys.path.insert(0, f"{ROOT}/tools"); sys.path.insert(0, P)
import mograph as M
import neon as N
N.PHOTOS = PHOTOS
M.finish = N.finish
import op_mograph as G, hud, sounds, transitions as TR
import gfx

FPS = 24
VO = f"{P}/oscar-pistorius_voiceover_v1.mp3"   # approved 7:49 read; never regenerated here
END = 476.0
OUT = f"{SCR}/output/oscar-pistorius_v1_master.mp4"
SFXDIR = f"{ROOT}/projects/jon-drummond/sfx"   # the user's ElevenLabs effects

def run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode: print(" ".join(cmd)[:800]); print(r.stderr[-2000:]); raise SystemExit(1)

def rl(n): return f"{REAL}/{n}.mp4"

L12 = "London · Olympics 2012"; LP12 = "London · Paralympics 2012"; T14 = "Pretoria · Trial 2014"
TAGS = {rl("athens2004"): "Athens · Paralympics 2004", rl("itn_400semi_qual"): L12, rl("olympic_400semis"): L12,
        rl("ipc_moment"): LP12, rl("para_400final"): LP12, rl("aljaz_outburst"): LP12, rl("para_200final_fan"): LP12,
        rl("afp_ipc"): LP12, rl("reuters_tashas"): T14, rl("euronews_cries"): "Pretoria · Feb 2013",
        rl("citypress_court_feb15"): "Pretoria · Feb 2013", rl("cgtn_house_arrest"): "Pretoria · Feb 2013",
        rl("ap_court_aug2013"): "Pretoria · Aug 2013", rl("telegraph_crossexam"): T14, rl("ap_crossexam"): T14,
        rl("telegraph_card"): T14, rl("ewn_nel_wraps"): T14, rl("guardian_verdict"): "Pretoria · Sep 2014",
        rl("nyt_verdict"): "Pretoria · Sep 2014", rl("ap_5years"): "Pretoria · Oct 2014",
        rl("ewn_sca_report"): "Bloemfontein · Dec 2015", rl("ewn_sca_murder"): "Bloemfontein · Dec 2015",
        rl("euronews_6years"): "Pretoria · Jul 2016", rl("sabc_6years"): "Pretoria · Jul 2016",
        rl("ap_13years"): "Pretoria · Court", rl("ap_noparole_2023"): "Pretoria · Archive",
        rl("newzroom_released"): "Pretoria · Archive", rl("sntv_history"): "South Africa · Track",
        rl("itn_training"): "Training · 2012", rl("ap_cas2008"): "Press conference · 2008",
        rl("ap_interview_2012"): L12, rl("rte_career"): LP12, rl("ap_reenactment"): T14,
        rl("ap_court_leave_aug2013"): "Pretoria · Aug 2013", rl("guardian_reeva"): "Reeva Steenkamp",
        rl("reeva_tropika_event"): "Reeva Steenkamp · TV", rl("reeva_tropika_goodbye"): "Reeva Steenkamp · TV",
        rl("reeva_father"): "Barry & June Steenkamp"}
REEVA = {"soft": True}

# (start_sec, kind, source, offset, opts)   each shot runs until the next one starts (times = VO word timings)
SHOTS = [
    # ---- 01 cold open
    (0.0, "g", "date_open", 0, REEVA),
    (8.12, "g", "door", 0, REEVA),                                                            # no gunshot sounds
    (16.98, "f", rl("reeva_tropika_event"), 2.0, {"e": 8.0, **REEVA}),                        # "his girlfriend, Reeva Steenkamp"
    (22.38, "f", rl("rte_career"), 21.0, {"e": 24.0, "tag": LP12}),                          # "the man holding the gun?"
    (24.26, "a", rl("ipc_moment"), 19.0, {"e": 27.5}),                                        # "most inspiring athletes"
    (29.06, "f", rl("sntv_history"), 7.0, {"e": 11.0}),                                       # "a double amputee..."
    (31.3, "a", rl("itn_400semi_qual"), 25.0, {"e": 28.0}),                                   # "...in the Olympics, on blades"
    (33.42, "g", "profile", 0),                                                               # "the Blade Runner, Oscar Pistorius"
    (37.38, "f", rl("reuters_tashas"), 1.0, {"e": 16.0}),                                     # "He said it was an accident"
    (41.10, "f", rl("guardian_verdict"), 52.0, {"e": 61.0}),                                  # "back and forth for years"
    (43.72, "f", rl("ewn_sca_murder"), 2.0, {"e": 6.0, "cb": 0.0}),                           # "caught people off guard"
    (47.08, "f", rl("para_400final"), 3.0, {"e": 9.0}),                                       # "most inspiring sprinters..."
    (49.6, "f", rl("ap_noparole_2023"), 71.0, {"e": 79.5, "tag": "Pretoria · Archive"}),     # "...in prison for murder?"
    (52.32, "g", "title", 0),
    # ---- 02 who he was
    (57.0, "g", "born", 0),                                                                   # "born in Johannesburg in 1986"
    (58.64, "g", "fibula", 0),                                                                # fibula, 11 months
    (68.52, "f", rl("sntv_history"), 31.0, {"e": 39.5}),                                      # "His mama, Sheila..."
    (72.28, "f", rl("ap_interview_2012"), 33.0, {"e": 40.0}),                                 # "put his legs on"
    (75.6, "f", rl("ap_interview_2012"), 41.0, {"e": 49.5}),
    (78.44, "f", rl("itn_training"), 27.0, {"e": 31.5}),                                      # "No special treatment"
    (80.96, "f", rl("itn_training"), 3.0, {"e": 8.0}),                                        # "rugby, water polo, all of it"
    (84.36, "g", "sheila", 0, REEVA),                                                         # his mother's death: quiet
    (88.88, "f", rl("ap_interview_2012"), 5.0, {"e": 13.0, "cb": 0.18}),                      # "even at the Olympics..."
    (92.72, "f", rl("sntv_history"), 21.0, {"e": 27.5}),                                      # "he found track"
    (97.30, "f", rl("athens2004"), 3.0, {"e": 13.0}),                                         # "2004, Athens Paralympics"
    (101.30, "f", rl("athens2004"), 15.0, {"e": 21.0}),                                       # "gold in the 200"
    (103.2, "f", rl("athens2004"), 23.5, {"e": 27.5}),
    (105.04, "a", rl("para_400final"), 73.0, {"e": 78.0}),                                    # "best Paralympian"
    (107.86, "f", rl("itn_training"), 33.0, {"e": 38.0}),                                     # "race the able-bodied dudes"
    (110.44, "a", rl("itn_400semi_qual"), 12.5, {"e": 14.9}),                                 # "He wanted the Olympics"
    (112.54, "g", "ch_fight", 0),
    # ---- 03 the fight to run
    (115.54, "p", "OscarPistorius_Citizenheadline_20080116", 0, {"label": "The Citizen", "sub": "16 January 2008", "tag": "Photo · Jan 2008"}),
    (119.4, "g", "ban", 0),
    (125.70, "f", rl("ap_cas2008"), 11.0, {"e": 16.5}),                                       # "Court of Arbitration for Sport"
    (129.00, "f", rl("ap_cas2008"), 85.5, {"e": 91.0}),                                       # "he won"
    (131.52, "g", "cas", 0),
    (135.58, "p", "2008_Summer_Paralympics_Athletism_Beijing_National_Stadium", 0, {"label": "Beijing 2008", "sub": "Paralympics, not the Olympics", "tag": "Photo · Beijing 2008"}),
    (138.96, "a", rl("itn_400semi_qual"), 25.0, {"e": 28.5}),                                 # "London, August 2012"
    (141.6, "p", "Oscar_Pistorius_the_first_round_of_the_400m_at_the_London_20", 0, {"label": "Oscar Pistorius", "sub": "400m round one · 4 Aug 2012", "tag": "Photo · London 2012"}),
    (144.44, "a", rl("itn_400semi_qual"), 10.2, {"e": 12.6}),                                 # "first double amputee..."
    (146.6, "p", "Mens_400m_semi_final_2_Oscar_Pistorius_Nigel_Levine", 0, {"label": "Men's 400m", "sub": "Olympic semi-final · London 2012", "tag": "Photo · London 2012"}),
    (149.28, "a", rl("itn_400semi_qual"), 14.5, {"e": 18.5}),                                 # "made it out his heat"
    (151.0, "a", rl("olympic_400semis"), 7.0, {"e": 22.0}),                                   # semi 2 start list
    (152.52, "a", rl("olympic_400semis"), 196.0, {"e": 205.0}),                               # "finished last in that semi"
    (155.0, "a", rl("olympic_400semis"), 115.0, {"e": 119.0, "label": "Kirani James", "sub": "Grenada · won Olympic gold"}),
    (157.96, "a", rl("olympic_400semis"), 238.5, {"e": 252.0}),                               # the bib swap
    (161.62, "p", "Oscar_Pistorius_2", 0, {"label": "Oscar Pistorius", "sub": "Anchor · SA 4x400", "tag": "Photo · Archive"}),
    (165.46, "a", rl("olympic_400semis"), 317.0, {"e": 330.0}),                               # "stadium on their feet"
    (168.32, "a", rl("ipc_moment"), 58.5, {"e": 62.0}),                                       # "that was the peak"
    (170.84, "p", "Oscar_Pistorius_leading_South_Africa_s_Paralympic_Team_in_th", 0, {"label": "Flag bearer", "sub": "Paralympics opening · 2012", "tag": "Photo · London 2012"}),
    (174.4, "f", rl("afp_ipc"), 33.0, {"e": 36.5}),
    # ---- 04 the cracks
    (177.70, "g", "ch_cracks", 0),
    (181.64, "a", rl("rte_career"), 30.0, {"e": 52.5}),                                       # 200m T44 final
    (187.62, "a", rl("aljaz_outburst"), 16.5, {"e": 21.0, "label": "Alan Oliveira", "sub": "Brazil · 200m T44 gold"}),
    (190.24, "f", rl("para_200final_fan"), 185.0, {"e": 192.0, "tag": "Stadium scoreboard · 2012"}),
    (193.16, "a", rl("rte_career"), 57.5, {"e": 61.8}),                                       # "went off on live TV"
    (196.98, "a", rl("rte_career"), 63.0, {"e": 67.5}),
    (199.0, "a", rl("aljaz_outburst"), 21.5, {"e": 24.0}),                                    # "blades was too long"
    (201.00, "f", rl("aljaz_outburst"), 49.0, {"e": 53.0}),                                   # IPC press conference
    (203.4, "f", rl("aljaz_outburst"), 117.5, {"e": 121.5}),                                  # podium with Oliveira
    (205.74, "g", "guns", 0),
    (209.74, "g", "tashas", 0),
    (219.28, "f", rl("guardian_verdict"), 102.5, {"e": 106.6, "tag": "Pretoria · Sep 2014"}),  # caption: guilty on the restaurant count
    (222.04, "g", "countdown", 0),
    # ---- 05 Valentine's Day 2013 (respectful: plain cuts, no SFX, no pop-ups)
    (225.78, "f", rl("guardian_reeva"), 4.0, {"e": 7.0, **REEVA}),                            # "who was Reeva Steenkamp?"
    (228.50, "f", rl("guardian_reeva"), 75.0, {"e": 83.0, **REEVA}),                          # "a model from Port Elizabeth"
    (231.30, "f", rl("guardian_reeva"), 28.5, {"e": 31.5, **REEVA}),                          # "law degree" (Guardian caption)
    (233.16, "f", rl("reeva_tropika_event"), 37.0, {"e": 44.0, **REEVA}),                     # "on TV"
    (236.5, "f", rl("newzroom_released"), 91.5, {"e": 94.2, "tag": "SA Sports Awards · 2012", **REEVA}),
    (240.12, "g", "feb14", 0, REEVA),
    (242.90, "g", "night", 0, REEVA),
    (249.88, "f", rl("newzroom_released"), 86.8, {"e": 90.5, "tag": "Reeva Steenkamp · 1983–2013", **REEVA}),
    (253.64, "f", rl("reuters_tashas"), 57.0, {"e": 63.5, **REEVA}),                          # "Here's Oscar's side"
    (255.50, "g", "account", 0, REEVA),
    (266.52, "f", rl("ap_court_aug2013"), 37.0, {"e": 47.5, **REEVA}),
    (269.54, "f", rl("ap_court_aug2013"), 67.0, {"e": 79.5, **REEVA}),
    (275.06, "f", rl("euronews_cries"), 57.0, {"e": 60.0, "tag": "Reeva Steenkamp", **REEVA}),
    (277.46, "f", rl("euronews_cries"), 1.0, {"e": 13.0}),                                    # "charged with murder"
    (280.8, "p", "Cape_Times_newspaper_poster_dated_15_February_2013_about_the", 0, {"label": "Cape Times", "sub": "15 February 2013", "tag": "Photo · Feb 2013"}),
    (283.90, "f", rl("cgtn_house_arrest"), 7.0, {"e": 13.0, "cb": 0.24}),                     # "did he really think..."
    # ---- 06 the trial
    (286.98, "f", rl("ap_reenactment"), 41.0, {"e": 44.0, "tag": "North Gauteng High Court · 2014"}),
    (289.4, "a", rl("telegraph_crossexam"), 226.5, {"e": 230.0}),                             # live TV, every day
    (291.96, "a", rl("telegraph_card"), 7.0, {"e": 20.0}),
    (296.36, "a", rl("telegraph_crossexam"), 12.0, {"e": 26.0, "label": "Gerrie Nel", "sub": "State prosecutor"}),
    (299.96, "f", rl("ap_crossexam"), 95.0, {"e": 100.0}),
    (301.86, "a", rl("telegraph_crossexam"), 66.0, {"e": 82.0}),
    (305.82, "f", rl("ap_crossexam"), 42.0, {"e": 48.0}),                                     # neighbours heard screaming
    (309.04, "f", rl("reuters_tashas"), 65.0, {"e": 72.0}),                                   # "that was him screaming"
    (313.12, "f", rl("ewn_nel_wraps"), 20.0, {"e": 27.0}),                                    # "cried on the stand"
    (316.48, "a", rl("telegraph_card"), 61.0, {"e": 66.0}),                                   # Valentine's card read in court
    (319.5, "f", rl("guardian_reeva"), 45.0, {"e": 47.5, **REEVA}),
    (321.92, "f", rl("guardian_reeva"), 72.0, {"e": 75.0, **REEVA}),                          # "it said she loved him"
    (326.70, "a", rl("nyt_verdict"), 11.0, {"e": 26.0, "label": "Thokozile Masipa", "sub": "Judge · North Gauteng High Court"}),
    (330.28, "a", rl("guardian_verdict"), 52.0, {"e": 58.0}),                                 # "not guilty of murder"
    (331.94, "g", "verdict1", 0),
    (336.00, "a", rl("guardian_verdict"), 75.0, {"e": 90.0}),
    (339.84, "a", rl("ap_5years"), 19.0, {"e": 28.0}),                                        # "five years"
    (342.5, "f", rl("ap_5years"), 0.3, {"e": 4.0, "tag": "Pretoria · Prison"}),
    (345.08, "a", rl("telegraph_crossexam"), 328.0, {"e": 345.0}),                            # "prosecutors wasn't done"
    (347.36, "f", rl("ewn_sca_report"), 1.0, {"e": 4.5, "tag": "Supreme Court of Appeal · 2015"}),
    (350.0, "f", rl("ewn_sca_murder"), 8.0, {"e": 20.0, "label": "Justice Eric Leach", "sub": "Supreme Court of Appeal"}),
    (353.60, "g", "sca_rule", 0),
    (363.16, "f", rl("ewn_sca_murder"), 30.0, {"e": 40.0}),                                   # "gambled with a life"
    (366.06, "a", rl("euronews_6years"), 141.0, {"e": 160.0, "cb": 0.235, "label": "Judge Thokozile Masipa", "sub": "Sentencing · July 2016"}),
    (369.5, "a", rl("sabc_6years"), 7.0, {"e": 15.0, "cb": 0.13}),
    (371.56, "g", "six_vs_15", 0),
    (376.90, "a", rl("euronews_6years"), 43.0, {"e": 62.0, "cb": 0.235, **REEVA}),           # Steenkamp family in court
    (378.26, "f", rl("ap_13years"), 3.0, {"e": 14.0, "cb": 0.24}),                            # "appeals court more than doubled it"
    (382.50, "g", "y13", 0),
    # ---- 07 parole & ending
    (385.26, "f", rl("ap_noparole_2023"), 29.0, {"e": 36.0, "tag": "Parole hearing · March 2023", "label": "June Steenkamp", "sub": "Reeva's mother", **REEVA}),
    (389.56, "f", rl("ewn_due_release"), 68.0, {"e": 77.5, "cb": 0.13, "tag": "Pretoria · Archive"}),  # "went back up..."
    (394.96, "g", "release", 0),
    (398.6, "f", rl("ewn_due_release"), 87.0, {"e": 94.0, "cb": 0.13, "tag": "Pretoria · Archive"}),
    (401.92, "g", "parole", 0),
    (412.56, "f", rl("ewn_due_release"), 105.5, {"e": 111.0, "cb": 0.12, "tag": "Pretoria · Archive", "label": "Barry Steenkamp", "sub": "Reeva's father · died 2023", **REEVA}),
    (416.84, "f", rl("guardian_reeva"), 57.0, {"e": 69.5, "cb": 0.3, "tag": "June Steenkamp", **REEVA}),
    (420.68, "g", "june_quote", 0, REEVA),
    (424.78, "a", rl("olympic_400semis"), 84.0, {"e": 90.0}),                                 # "I'ma keep it a buck"
    (428.06, "g", "night_plain", 0, REEVA),
    (431.96, "f", rl("ewn_sca_report"), 11.0, {"e": 15.0}),                                   # "the highest court..."
    (435.30, "g", "four_shots", 0, REEVA),
    (441.82, "f", rl("ap_interview_2012"), 51.0, {"e": 58.0}),
    (444.62, "a", rl("rte_career"), 80.5, {"e": 86.0}),                                       # "proving folks wrong"
    (448.30, "a", rl("olympic_400semis"), 223.0, {"e": 231.0}),
    (450.64, "a", rl("itn_400semi_qual"), 15.0, {"e": 18.5}),                                 # "he did it anyway"
    (452.14, "f", rl("sntv_history"), 7.5, {"e": 11.5}),                                      # blades
    (454.48, "f", rl("ap_cas2008"), 86.0, {"e": 90.0}),                                       # "beat that in court"
    (456.36, "a", rl("rte_career"), 93.5, {"e": 101.0}),
    (460.90, "a", rl("ipc_moment"), 35.0, {"e": 46.0}),                                       # "the Blade Runner for London"
    (464.80, "f", rl("newzroom_released"), 58.5, {"e": 62.0}),                                # "They remember Valentine's Day"
    (467.04, "f", rl("guardian_reeva"), 0.5, {"e": 4.0, **REEVA}),                            # "Reeva Steenkamp should still be here"
    (470.6, "g", "end", 0, REEVA),
]

KEYWORDS = [  # (vo_time, text, dur, pos)   never inside soft sections
    (29.3, "Double\namputee.", 2.6, "left"), (102.0, "Gold.\nAge 17.", 2.6, "right"), (123.4, "Banned.", 2.2, "left"),
    (144.6, "First double\namputee.", 2.8, "right"), (157.96, "Swapped\nbibs.", 2.6, "left"),
    (187.9, "Lost by\n0.07s.", 2.8, "right"), (196.98, "'Not a fair\nrace.'", 2.8, "left"),
    (219.4, "Guilty on\nthat shot.", 2.6, "right"), (296.6, "Went at him\nhard.", 2.6, "right"),
    (363.2, "Gambled with\na life.", 3.0, "left"), (374.8, "Shockingly\nlenient.", 2.0, "right"),
]
SFX = [  # (vo_time, file, gain)   kept out of the soft sections
    (33.5, "sub-boom", 0.7), (52.4, "sub-boom", 0.9), (112.6, "whoosh", 0.55), (119.6, "newspaper-rip", 0.55),
    (123.35, "rubber-stamp", 0.9), (177.8, "whoosh", 0.55), (205.8, "sub-boom", 0.6), (331.95, "sub-boom", 0.6),
    (353.65, "rubber-stamp", 0.7), (382.55, "sub-boom", 0.7),
]
MUSIC = [  # (file, start, gain, fade_out_at)
    ("M1_cold-open-rise", 0.0, 0.42, 145.0), ("M2_cracks-night-trial", 141.0, 0.42, 286.0),
    ("M2_cracks-night-trial", 283.0, 0.38, 330.0),  # second pass of M2 (offset below) over the trial
    ("M3_verdicts-ending", 326.0, 0.42, 471.0),
]
MUSIC_OFFS = {2: 40.0}  # start M2's second use 40 s into the track so it doesn't repeat audibly

def shots():
    out = []
    for i, x in enumerate(SHOTS):
        s, k, src, off = x[:4]; opt = x[4] if len(x) > 4 else {}
        e = SHOTS[i + 1][0] if i + 1 < len(SHOTS) else END
        f0, f1 = round(s * FPS), round(e * FPS)
        out.append(dict(i=i, start=f0 / FPS, frames=f1 - f0, kind=k, src=src, off=off, opt=opt))
    return out

def soft_ranges():
    return [(x["start"], x["start"] + x["frames"] / FPS) for x in shots() if x["opt"].get("soft")]

def in_soft(t, pad=0.3):
    return any(a - pad <= t <= b + pad for a, b in soft_ranges())

def dur(path):
    return float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", path],
                                capture_output=True, text=True).stdout)

_crop = {}
def cropdetect(path, at=1.0, overscan=0.0):
    key = (path, round(at, 1), overscan)
    if key not in _crop:
        r = subprocess.run(["ffmpeg", "-v", "info", "-ss", f"{at:.2f}", "-i", path, "-vf", "cropdetect=30:2:0", "-frames:v", "14", "-f", "null", "-"],
                           capture_output=True, text=True).stderr
        c = [l.split("crop=")[-1].strip() for l in r.splitlines() if "crop=" in l]
        if not c: _crop[key] = None
        else:
            w, h, x, y = map(int, Counter(c[2:] or c).most_common(1)[0][0].split(":"))
            ox, oy = int(w * overscan) // 2 * 2, int(h * overscan) // 2 * 2
            _crop[key] = (w - 2 * ox, h - 2 * oy, x + ox, y + oy)
    return _crop[key]

GRADE_A = "eq=contrast=1.08:saturation=1.10:gamma=0.97,unsharp=5:5:0.55:5:5:0.0"
GRADE_SOFT = "eq=contrast=1.03:saturation=0.92:gamma=1.0,unsharp=5:5:0.4:5:5:0.0"  # gentler on Reeva / family
NEON_COLS = [N.ORANGE, N.CYAN]

def enc(out):
    return ["-an", "-c:v", "libx264", "-preset", "veryfast", "-crf", "17", "-pix_fmt", "yuv420p", "-r", str(FPS), out]

def nameplate(im, label, sub, col, x=110, y=830):
    d = ImageDraw.Draw(im, "RGBA")
    f = gfx.font("Black", 50); fs = N.mono(24)
    tw = max(d.textlength(label.upper(), font=f), d.textlength(sub.upper(), font=fs)) + 70
    d.rectangle([x, y, x + tw, y + 112], fill=(6, 8, 18, 225), outline=col + (255,), width=3)
    d.rectangle([x, y, x + 10, y + 112], fill=col + (255,))
    d.text((x + 34, y + 12), label.upper(), font=f, fill=N.WHITE)
    d.text((x + 36, y + 74), sub.upper(), font=fs, fill=col + (255,))

def frame_png(tag, box, color, label=None, sub=None, kind="ARCHIVE"):
    key = f"{kind}_{tag}_{box}_{color}_{label}_{sub}".encode().hex()[:150]
    f = f"{R}/frames/{key}.png"
    if not os.path.exists(f):
        im = N.archive_frame(tag, box=box, color=color, accent=N.CYAN if color == N.ORANGE else N.ORANGE, kind=kind)
        if label: nameplate(im, label, sub or "", color, x=(box[0] + 40 if box else 110), y=(box[3] - 150 if box else 830))
        im.save(f)
    return f

def render_archive(sh, out):
    n = sh["frames"]; d = n / FPS; o = sh["opt"]; src = sh["src"]
    cw, ch, cx, cy = cropdetect(src, sh["off"] + 0.3, overscan=0.03)
    cb, ct = o.get("cb", 0.0), o.get("ct", 0.0)
    if cb or ct:
        cy += int(ch * ct) // 2 * 2; ch = int(ch * (1 - cb - ct)) // 2 * 2
    avail = max(0.4, o.get("e", dur(src)) - sh["off"])
    slow = min(2.0, max(1.0, d / avail))
    tag = o.get("tag", TAGS.get(src, "Archive"))
    col = N.CYAN if o.get("soft") else NEON_COLS[sh["i"] % 2]
    grade = GRADE_SOFT if o.get("soft") else GRADE_A
    pre = f"crop={cw}:{ch}:{cx}:{cy},setpts=PTS*{slow:.4f},fps={FPS},tpad=stop_mode=clone:stop_duration=30,{grade}"
    zoom = 0.035 if o.get("soft") else 0.06
    if sh["kind"] == "a":
        yb = o.get("yb", 0.4)
        fc = (f"[0:v]{pre},scale=1920:1080:force_original_aspect_ratio=increase:flags=lanczos,crop=1920:1080:(iw-1920)/2:(ih-1080)*{yb},"
              f"zoompan=z='1+{zoom}*on/{n}':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=1:s=1920x1080:fps={FPS},vignette=angle=PI/5[v];"
              f"[1:v]format=rgba[o];[v][o]overlay=0:0,format=yuv420p[out]")
        png = frame_png(tag, None, col, o.get("label"), o.get("sub"))
    else:
        fh = 900; fw = round(fh * cw / ch / 2) * 2
        if fw > 1640: fw = 1640; fh = round(fw * ch / cw / 2) * 2
        x0, y0 = (1920 - fw) // 2, (1080 - fh) // 2
        fc = (f"[0:v]{pre},split[a][b];"
              f"[a]scale=480:270:force_original_aspect_ratio=increase,crop=480:270,boxblur=10:2,scale=1920:1080,"
              f"eq=brightness=-0.26:saturation=1.3[bg];"
              f"[b]scale={fw}:{fh}:flags=lanczos,zoompan=z='1+{zoom * 0.8:.3f}*on/{n}':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=1:s={fw}x{fh}:fps={FPS}[fg];"
              f"[bg][fg]overlay={x0}:{y0},vignette=angle=PI/4[v];[1:v]format=rgba[o];[v][o]overlay=0:0,format=yuv420p[out]")
        png = frame_png(tag, (x0 - 3, y0 - 3, x0 + fw + 2, y0 + fh + 2), col, o.get("label"), o.get("sub"))
    run(["ffmpeg", "-v", "error", "-y", "-ss", f"{sh['off']:.3f}", "-i", src, "-loop", "1", "-i", png,
         "-filter_complex", fc, "-map", "[out]", "-frames:v", str(n)] + enc(out))

def render_photo(sh, out):
    n = sh["frames"]; o = sh["opt"]
    im0 = Image.open(f"{PHOTOS}/{sh['src']}.jpg").convert("RGB")
    w, h = im0.size
    col = NEON_COLS[sh["i"] % 2]
    bg = ImageOps.fit(im0, (480, 270)).filter(ImageFilter.GaussianBlur(9)).resize((1920, 1080), Image.BILINEAR)
    bg = ImageEnhance.Color(ImageEnhance.Brightness(bg).enhance(0.32)).enhance(1.4)
    sc = min(1480 / w, 800 / h); pw, ph = int(w * sc) // 2 * 2, int(h * sc) // 2 * 2
    x0, y0 = (1920 - pw) // 2, (1080 - ph) // 2 - 30
    big = im0.resize((int(pw * 1.08), int(ph * 1.08)), Image.LANCZOS)
    frame = N.glow_rect((1920, 1080), [x0 - 3, y0 - 3, x0 + pw + 2, y0 + ph + 2], col, width=4, blur=20)
    tagl = N.archive_frame(o.get("tag", "Photo"), box=None, color=col, kind="IMG")
    proc = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", "1920x1080", "-r", str(FPS), "-i", "-"] + enc(out),
                            stdin=subprocess.PIPE)
    for i in range(n):
        t = i / FPS
        z = 1.0 + 0.07 * i / max(1, n - 1)
        ww, hh = big.width / z / 1.08, big.height / z / 1.08
        cx, cy = big.width / 2, big.height / 2
        pic = big.crop((int(cx - ww / 2), int(cy - hh / 2), int(cx + ww / 2), int(cy + hh / 2))).resize((pw, ph), Image.BILINEAR)
        k = N.eback(N.seg(t, 0, 0.4)); s = 0.9 + 0.1 * k
        im = bg.copy()
        if s < 0.999:
            pp = pic.resize((int(pw * s), int(ph * s)), Image.BILINEAR)
            im.paste(pp, (x0 + (pw - pp.width) // 2, y0 + (ph - pp.height) // 2))
        else:
            im.paste(pic, (x0, y0))
        im.paste(frame, (0, 0), frame); im.paste(tagl, (0, 0), tagl)
        ka = N.eo(N.seg(t, 0.25, 0.6))
        if o.get("label") and ka > 0:
            d = ImageDraw.Draw(im, "RGBA")
            f = gfx.font("Black", 46); fs = N.mono(22)
            lab = o["label"].upper(); sub = o.get("sub", "").upper()
            tw = max(d.textlength(lab, font=f), d.textlength(sub, font=fs)) + 60
            bx, by = x0 + 30, min(y0 + ph - 40, 930)
            d.rectangle([bx, by, bx + tw * ka, by + 104], fill=(6, 8, 18, 225), outline=col + (255,), width=3)
            d.rectangle([bx, by, bx + 10, by + 104], fill=col + (255,))
            if ka > 0.6:
                d.text((bx + 34, by + 14), lab, font=f, fill=N.WHITE)
                d.text((bx + 36, by + 70), sub, font=fs, fill=col + (255,))
        proc.stdin.write(im.tobytes())
    proc.stdin.close(); proc.wait()

def render_shot(sh):
    out = f"{R}/shot_{sh['i']:03d}.mp4"
    if os.path.exists(out): return out
    d = sh["frames"] / FPS
    if sh["kind"] == "g": M.render(G.GRAPHICS[sh["src"]], d, out)
    elif sh["kind"] in ("a", "f"): render_archive(sh, out)
    elif sh["kind"] == "p": render_photo(sh, out)
    return out

def stage_shots():
    sh = shots()
    with ThreadPoolExecutor(4) as ex: files = list(ex.map(render_shot, sh))
    with open(f"{R}/concat.txt", "w") as f:
        for x in files: f.write(f"file '{x}'\n")
    run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", f"{R}/concat.txt", "-c", "copy", f"{R}/base.mp4"])
    print("base", dur(f"{R}/base.mp4"))

def _grab(path, times):
    t0 = max(0, min(times)); n = round((max(times) - t0) * FPS) + 2
    r = subprocess.run(["ffmpeg", "-v", "error", "-ss", f"{t0:.4f}", "-i", path, "-frames:v", str(n), "-f", "rawvideo", "-pix_fmt", "rgb24", "-"],
                       capture_output=True)
    fr = np.frombuffer(r.stdout, np.uint8).reshape(-1, 1080, 1920, 3)
    return [fr[min(len(fr) - 1, max(0, round((t - t0) * FPS)))] for t in times]

SECTION_STARTS = {52.32, 112.54, 177.70, 286.98}

def cut_list():
    sh = shots(); cuts = []
    for j, x in enumerate(sh[1:], 1):
        prev = sh[j - 1]
        if x["opt"].get("soft") or prev["opt"].get("soft"): continue  # plain cuts around Reeva / family / the night
        if x["kind"] == "g" or prev["kind"] == "g" or any(abs(x["start"] - s) < 0.05 for s in SECTION_STARTS) or j % 3 == 0:
            cuts.append(x["start"])
    return cuts

def stage_transitions():
    base = f"{R}/base.mp4"; ev = []
    for j, T in enumerate(cut_list()):
        kind = TR.KINDS[j % len(TR.KINDS)]
        out = f"{R}/tr_{j:03d}.mp4"
        if not os.path.exists(out):
            TR.ORANGE = np.array(NEON_COLS[(j // len(TR.KINDS)) % 2], np.float32)
            times = [T + (i - 6) / FPS for i in range(12)]
            fa = _grab(base, [min(t, T - 1 / FPS) for t in times]); fb = _grab(base, [max(t, T) for t in times])
            rng = np.random.default_rng(j)
            p = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", "1920x1080", "-r", str(FPS), "-i", "-"] + enc(out), stdin=subprocess.PIPE)
            for i in range(12): p.stdin.write(np.ascontiguousarray(TR.frame(kind, fa[i], fb[i], (i + 0.5) / 12, rng)).tobytes())
            p.stdin.close(); p.wait()
        ev.append(dict(start=T - 6 / FPS, cut=T, kind=kind, file=out))
    json.dump(ev, open(f"{R}/trans.json", "w"))
    print("transitions", len(ev))

def stage_compose():
    tev = json.load(open(f"{R}/trans.json"))
    kws = []
    for i, (t, txt, d, pos) in enumerate(KEYWORDS):
        assert not in_soft(t), f"keyword inside a soft section: {txt}"
        f = f"{R}/hud_{i:02d}.mov"
        if not os.path.exists(f): hud.render(txt, i + 1, d, pos, f, seed=200 + i, neon=True)
        kws.append(dict(start=round(t * FPS) / FPS, dur=d, file=f))
    json.dump(kws, open(f"{R}/kws.json", "w"))
    inputs = ["-i", f"{R}/base.mp4"]; fc = []; last = "[0:v]"; k = 1
    for tr in tev:
        inputs += ["-i", tr["file"]]
        fc.append(f"[{k}:v]setpts=PTS-STARTPTS+{tr['start']:.4f}/TB[t{k}]")
        fc.append(f"{last}[t{k}]overlay=eof_action=pass:enable='between(t,{tr['start']:.4f},{tr['start'] + 0.499:.4f})'[v{k}]"); last = f"[v{k}]"; k += 1
    for g in kws:
        inputs += ["-i", g["file"]]
        fc.append(f"[{k}:v]format=rgba,setpts=PTS-STARTPTS+{g['start']:.4f}/TB[g{k}]")
        fc.append(f"{last}[g{k}]overlay=eof_action=pass:format=auto:enable='between(t,{g['start']:.4f},{g['start'] + g['dur']:.4f})'[v{k}]"); last = f"[v{k}]"; k += 1
    fc.append(f"{last}noise=alls=5:allf=t,fade=in:st=0:d=0.8,format=yuv420p[out]")
    open(f"{R}/compose.txt", "w").write(";\n".join(fc))
    run(["ffmpeg", "-v", "error", "-y"] + inputs + ["-filter_complex_script", f"{R}/compose.txt", "-map", "[out]",
         "-c:v", "libx264", "-preset", "medium", "-crf", "20", "-pix_fmt", "yuv420p", "-r", str(FPS), f"{R}/video.mp4"])
    print("video", dur(f"{R}/video.mp4"))

def stage_audio():
    tev = json.load(open(f"{R}/trans.json")); kws = json.load(open(f"{R}/kws.json"))
    sdir = f"{R}/sfx"; os.makedirs(sdir, exist_ok=True)
    inputs = ["-i", VO]; fc = ["[0:a]aresample=48000,aformat=channel_layouts=stereo,apad=whole_dur=%.3f,asplit=2[vo][sc]" % END]
    k = 1; mus = []
    for j, (name, s, g, fo) in enumerate(MUSIC):
        inputs += ["-i", f"{P}/music/{name}.mp3"]
        ms = int(s * 1000); fl = fo - s; so = MUSIC_OFFS.get(j, 0.0)
        fc.append(f"[{k}:a]aresample=48000,aformat=channel_layouts=stereo,atrim={so}:{so + fl + 3:.2f},asetpts=PTS-STARTPTS,"
                  f"afade=t=in:d=3,afade=t=out:st={fl:.2f}:d=3,volume={g},adelay={ms}|{ms}[m{k}]")
        mus.append(f"[m{k}]"); k += 1
    fc.append(f"{''.join(mus)}amix=inputs={len(mus)}:normalize=0,equalizer=f=220:t=q:w=1.1:g=-3.5[mbus]")
    fc.append("[mbus][sc]sidechaincompress=threshold=0.035:ratio=6:attack=25:release=500:makeup=1[mduck]")
    fx = []
    for t, name, g in SFX:
        assert not in_soft(t), f"sfx inside a soft section at {t}"
        inputs += ["-i", f"{SFXDIR}/{name}.mp3"]; ms = int(t * 1000)
        fc.append(f"[{k}:a]aresample=48000,aformat=channel_layouts=stereo,volume={g},adelay={ms}|{ms}[x{k}]"); fx.append(f"[x{k}]"); k += 1
    for j, tr in enumerate(tev):  # varied synthesized transition sounds
        f = f"{sdir}/tr_{j:03d}.wav"; sounds.trans_sound(tr["kind"], f, 5000 + j)
        inputs += ["-i", f]; ms = int(max(0, tr["cut"] - 0.30) * 1000)
        fc.append(f"[{k}:a]volume=0.2,adelay={ms}|{ms}[x{k}]"); fx.append(f"[x{k}]"); k += 1
    for j, g in enumerate(kws):
        f = f"{sdir}/kw_{j:02d}.wav"; sounds.ui_sound("decode", f, 6000 + j)
        inputs += ["-i", f]; ms = int(g["start"] * 1000)
        fc.append(f"[{k}:a]volume=0.17,adelay={ms}|{ms}[x{k}]"); fx.append(f"[x{k}]"); k += 1
    for j, sh in enumerate(x for x in shots() if x["kind"] == "p" and not x["opt"].get("soft")):
        f = f"{sdir}/ph_{j:02d}.wav"; sounds.ui_sound("decode", f, 7000 + j)
        inputs += ["-i", f]; ms = int(sh["start"] * 1000)
        fc.append(f"[{k}:a]volume=0.11,adelay={ms}|{ms}[x{k}]"); fx.append(f"[x{k}]"); k += 1
    fc.append(f"{''.join(fx)}amix=inputs={len(fx)}:normalize=0[fx]")
    fc.append(f"[vo][mduck][fx]amix=inputs=3:normalize=0,atrim=0:{END:.3f},afade=t=out:st={END - 3:.2f}:d=3,loudnorm=I=-14:TP=-1:LRA=9,aresample=48000[out]")
    open(f"{R}/audio.txt", "w").write(";\n".join(fc))
    run(["ffmpeg", "-v", "error", "-y"] + inputs + ["-filter_complex_script", f"{R}/audio.txt", "-map", "[out]", "-c:a", "pcm_s16le", f"{R}/mix.wav"])
    print("mix", dur(f"{R}/mix.wav"))

def stage_mux():
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    run(["ffmpeg", "-v", "error", "-y", "-i", f"{R}/video.mp4", "-i", f"{R}/mix.wav", "-map", "0:v", "-map", "1:a",
         "-c:v", "copy", "-c:a", "aac", "-b:a", "256k", "-shortest", "-movflags", "+faststart", OUT])
    print("wrote", OUT, dur(OUT))

if __name__ == "__main__":
    for s in sys.argv[1:] or ["shots", "transitions", "compose", "audio", "mux"]:
        print("==", s, flush=True); globals()["stage_" + s]()
