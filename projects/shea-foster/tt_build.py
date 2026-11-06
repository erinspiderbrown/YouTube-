"""Vertical TikTok cut of the Shea Foster video (1080x1920), with nothing cropped.

The full 16:9 master is scaled to the frame width and centred. A hook title sits above it and big word-by-word
captions sit below it. Everything stays inside TikTok's safe area: clear of the top tabs, the right-hand
button column and the bottom caption bar.

Run after sf_build.py:  python3 projects/shea-foster/tt_build.py
"""
import difflib, json, os, re, subprocess, sys
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sf_build as S

P = S.P
MASTER = f"{P}/out/shea_foster_v1.mp4"
OUT = f"{P}/out/shea_foster_tiktok_v1.mp4"
R = S.R
VW, VH, VY = 1080, 608, 640           # video box inside the 1080x1920 frame
CAP_Y = 1400                          # caption centre
TITLE = ("EVERYONE WAS WATCHING", "THE WRONG RUNNER")

# Foster's own words in the five real-audio bites (exact, from the source)
BITE_TEXT = {
    "sixth": "In 2021 I came in sixth place at the NCAA track and field championships. The five runners who finished ahead of me all run professionally now.",
    "news": "Frightening new dash cam video. It's an extreme case of distracted driving. Your old boy is in critical condition after a crash in Kenner earlier today. Police say the car and an 18-wheeler crashed into each other on Airline Highway.",
    "world": "My whole world stopped. Just like that.",
    "doctors": "I asked the doctors, when was I gonna be able to run again? She said, you'll be lucky enough if you're able to walk again.",
    "surface": "On the surface, I don't look disabled at all.",
}


def norm(w):
    return re.sub(r"[^a-z0-9]", "", w.lower())


def align(script_words, timed):
    """Give every script word (correct spelling) a time from the whisper words (correct timing)."""
    a = [norm(w) for w in script_words]
    b = [norm(t["w"]) for t in timed]
    out = []
    for op, i1, i2, j1, j2 in difflib.SequenceMatcher(None, a, b, autojunk=False).get_opcodes():
        if op == "equal":
            out += [(script_words[i1 + k], timed[j1 + k]["s"], timed[j1 + k]["e"]) for k in range(i2 - i1)]
        elif i2 > i1:
            if j2 > j1:
                s, e = timed[j1]["s"], timed[j2 - 1]["e"]
            else:  # nothing heard: squeeze between neighbours
                s = timed[j1 - 1]["e"] if j1 else 0.0
                e = timed[j1]["s"] if j1 < len(timed) else s + 0.3 * (i2 - i1)
            n = i2 - i1
            out += [(script_words[i1 + k], s + (e - s) * k / n, s + (e - s) * (k + 1) / n) for k in range(n)]
    return out


def vo_words():
    sec = json.load(open(f"{S.SCR}/sections.json"))
    text = " ".join(re.sub(r"\[[^\]]*\]", " ", sec[k]) for k in sorted(sec))
    words = [w for w in text.replace("…", "… ").split() if norm(w)]
    timed = [w for w in S.WORDS if norm(w["w"])]
    return [(w, S.F(s), S.F(s) + (e - s)) for w, s, e in align(words, timed)]


def bite_words():
    from faster_whisper import WhisperModel
    m = WhisperModel("small.en", compute_type="int8")
    out = []
    for name, cut, src, a, b in S.BITES:
        f = f"{R}/aud/{name}.wav"
        x = np.frombuffer(subprocess.run(["ffmpeg", "-v", "error", "-i", f, "-ac", "1", "-ar", "16000", "-f", "f32le", "-"],
                                         capture_output=True).stdout, np.float32)
        segs, _ = m.transcribe(x, word_timestamps=True)
        timed = [dict(w=w.word.strip(), s=w.start, e=w.end) for s in segs for w in s.words if norm(w.word)]
        t0 = cut + S.off(cut) - S.BL[name] + S.PAD
        out += [(w, t0 + s, t0 + e) for w, s, e in align(BITE_TEXT[name].split(), timed)]
    return out


def chunks(words):
    """2-3 word caption chunks, broken at punctuation and pauses."""
    out, cur = [], []
    for i, (w, s, e) in enumerate(words):
        cur.append((w, s, e))
        nxt = words[i + 1] if i + 1 < len(words) else None
        brk = (len(cur) >= 3 or re.search(r"[.?!,…:]$", w) or (nxt and nxt[1] - e > 0.35)
               or (len(cur) >= 2 and sum(len(x[0]) for x in cur) > 14) or nxt is None)
        if brk:
            out.append(cur)
            cur = []
    return out


def ass_time(t):
    t = max(0, t)
    return f"{int(t // 3600)}:{int(t % 3600 // 60):02d}:{t % 60:05.2f}"


def clean(w):
    return w.upper().replace("{", "").replace("}", "")


def build_ass(words, path, end):
    head = f"""[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920
WrapStyle: 2

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Cap,Inter Display Black,86,&H00FFFFFF,&H00FFFFFF,&H00000000,&H96000000,0,0,0,0,100,100,0,0,1,7,3,5,60,60,0,1
Style: Title,Inter Display Black,82,&H00FFFFFF,&H00FFFFFF,&H00000000,&H96000000,0,0,0,0,100,100,0,0,1,6,2,5,60,60,0,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
    ev = [f"Dialogue: 1,{ass_time(0)},{ass_time(end)},Title,,0,0,0,,{{\\pos(540,400)}}{TITLE[0]}",
          f"Dialogue: 1,{ass_time(0)},{ass_time(end)},Title,,0,0,0,,{{\\pos(540,500)\\c&H00D7FF&}}{TITLE[1]}"]
    chs = chunks(words)
    for ci, ch in enumerate(chs):
        nxt = chs[ci + 1][0][1] - 0.05 if ci + 1 < len(chs) else end
        for k, (w, s, e) in enumerate(ch):
            st = s if k else s - 0.04
            en = ch[k + 1][1] if k + 1 < len(ch) else min(e + 0.35, nxt)
            if en <= st:
                continue
            txt = " ".join(("{\\c&H00D7FF&}" + clean(x) + "{\\c&HFFFFFF&}") if j == k else clean(x) for j, (x, _, _) in enumerate(ch))
            pop = "{\\fscx108\\fscy108\\t(0,90,\\fscx100\\fscy100)}" if k == 0 else ""
            ev.append(f"Dialogue: 0,{ass_time(st)},{ass_time(en)},Cap,,0,0,0,,{{\\pos(540,{CAP_Y})}}{pop}{txt}")
    open(path, "w").write(head + "\n".join(ev) + "\n")
    return len(ev)


def main():
    words = sorted(vo_words() + bite_words(), key=lambda x: x[1])
    # no overlaps: a word ends no later than the next one starts
    words = [(w, s, min(e, words[i + 1][1]) if i + 1 < len(words) else e) for i, (w, s, e) in enumerate(words)]
    json.dump(words, open(f"{R}/tt_words.json", "w"))
    ass = f"{R}/tt_captions.ass"
    print("caption events", build_ass(words, ass, S.END))
    vf = (f"[0:v]scale={VW}:{VH}:flags=lanczos,setsar=1,pad=1080:1920:0:{VY}:black,"
          f"ass={ass}:fontsdir=/usr/share/fonts/opentype/inter,format=yuv420p[v]")
    S.run(["ffmpeg", "-v", "error", "-y", "-i", MASTER, "-filter_complex", vf, "-map", "[v]", "-map", "0:a",
           "-c:v", "libx264", "-preset", "slow", "-crf", "18", "-profile:v", "high", "-r", "30",
           "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", OUT])
    print("wrote", OUT)


if __name__ == "__main__":
    main()
