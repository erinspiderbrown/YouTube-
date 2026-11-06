"""Native vertical (1080x1920) render of the Shea Foster edit, with NO black space anywhere (user rule).

Uses the same shot list, timing, bites and audio as sf_build.py. Each frame is built from:
  1. a full-screen background: a blurred, darkened cover of the shot's own picture. Black card shots use a
     "bed" photo from that part of the story.
  2. the plate: 16:9 footage/photos at full width, never cropped. Portrait photos get a taller box so they're
     shown big, and their empty sides show the blurred background instead of black.
  3. floating graphics (big numbers, document cards, centred text), cropped to their content and enlarged for
     the phone screen.
  The tt_build.py pass then adds the hook title (top) and word-by-word captions (below the plate).

Run:  python3 projects/shea-foster/sf_vertical.py   → render/base_v.mp4 → out/shea_foster_v1_vertical_master.mp4
"""
import os, subprocess, sys
from multiprocessing import Pool
import numpy as np, cv2
from PIL import Image

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sf_build as S
import sf_gfx as G

VW, VH = 1080, 1920
CY = 900                    # centre line of the plate
PLATE_H = 608               # 16:9 plate height at full width
TALL_H = 880                # box for portrait photos
FLOAT_MAXW, FLOAT_MAXH = 1000, 860
R = S.R
SEGDIR = f"{R}/segs_v"
PLATE_KEYS = ("c_", "lt_", "tag_", "illus", "june", "nov", "teammates")   # graphics tied to the picture
BEDS = [  # (from voiceover time, image) background for black card shots
    (0, f"{S.AS}/team20_allblur.png"), (44.0, f"{S.AS}/ng_podium.png"), (99.0, f"{S.AS}/ng_jeep.png"),
    (131.0, f"{S.AS}/team19_blur.png"), (186.0, f"{S.DB}/15.jpg"), (219.0, f"{S.AS}/team20_foster.png"),
    (279.0, f"{S.AS}/team20_allblur.png"),
]
_bed_cache, _float_cache = {}, {}


def blur_bg(img_rgb, dark=0.42):
    """Cover-fit a picture to 1080x1920, heavily blurred and darkened."""
    h, w = img_rgb.shape[:2]
    small = cv2.resize(img_rgb, (max(8, w // 8), max(8, h // 8)), interpolation=cv2.INTER_AREA)
    small = cv2.GaussianBlur(small, (0, 0), 6)
    s = max(VW / small.shape[1], VH / small.shape[0])
    big = cv2.resize(small, (int(small.shape[1] * s) + 2, int(small.shape[0] * s) + 2), interpolation=cv2.INTER_LINEAR)
    y0, x0 = (big.shape[0] - VH) // 2, (big.shape[1] - VW) // 2
    return big[y0:y0 + VH, x0:x0 + VW].astype(np.float32) * dark


def bed_for(vt):
    path = [p for t, p in BEDS if t <= vt + 1e-6][-1]
    if path not in _bed_cache:
        _bed_cache[path] = blur_bg(S.load_img(path), 0.38)
    return _bed_cache[path]


def render_vgfx():
    """Draw every graphic natively at 1080x1920 (text wraps to the phone width)."""
    os.makedirs(f"{R}/gfx_v", exist_ok=True)
    G.W, G.H = VW, VH
    for k, fn in S.GFX.items():
        p = f"{R}/gfx_v/{k}.png"
        if not os.path.exists(p):
            fn().save(p)
    G.W, G.H = 1920, 1080


def float_gfx(key):
    """Phone-width graphic cropped to its content: (premult rgb, alpha) at its size."""
    if key not in _float_cache:
        p = f"{R}/gfx_v/{key}.png"
        im = Image.open(p).convert("RGBA")
        bb = im.split()[-1].point(lambda v: 255 if v > 8 else 0).getbbox()
        im = im.crop(bb)
        s = min(FLOAT_MAXW / im.width, FLOAT_MAXH / im.height, 1.0)
        if s < 1:
            im = im.resize((int(im.width * s), int(im.height * s)), Image.LANCZOS)
        a = np.asarray(im, np.float32) / 255
        _float_cache[key] = (a[..., :3] * a[..., 3:], a[..., 3:])
    return _float_cache[key]


def paste(canvas, rgb_premult, alpha, cx, cy, k=1.0):
    h, w = alpha.shape[:2]
    x0, y0 = int(cx - w / 2), int(cy - h / 2)
    xa, ya, xb, yb = max(0, x0), max(0, y0), min(VW, x0 + w), min(VH, y0 + h)
    if xb <= xa or yb <= ya:
        return canvas
    sub = canvas[ya:yb, xa:xb]
    c = rgb_premult[ya - y0:yb - y0, xa - x0:xb - x0]
    a = alpha[ya - y0:yb - y0, xa - x0:xb - x0] * k
    canvas[ya:yb, xa:xb] = sub * (1 - a) + c * 255 * k
    return canvas


def plate_overlays(f, sh, vt):
    for a_, b_, key, dim in sh.get("ov", []):
        if a_ <= vt < b_ and key.startswith(PLATE_KEYS):
            al = max(0, min(min(1, (vt - a_) * S.FPS / 4 + 0.25), min(1, (b_ - vt) * S.FPS / 3)))
            c, a = S.gfx(key)
            f = f * (1 - a * al) + c * 255 * al
    return f


def render_seg_v(seg):
    out = f"{SEGDIR}/{seg['i']:03d}.mp4"
    n = seg["f1"] - seg["f0"]
    if os.path.exists(out) or n <= 0:
        return out
    enc = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{VW}x{VH}", "-r", str(S.FPS),
                            "-i", "-", "-c:v", "libx264", "-preset", "veryfast", "-crf", "16", "-pix_fmt", "yuv420p",
                            "-threads", "2", out + ".tmp.mp4"], stdin=subprocess.PIPE)
    y16 = CY - PLATE_H // 2
    if seg["kind"] == "BITE":
        for j, fr in enumerate(S.video_frames(seg["src"], seg["ss"], n)):
            z = 1.0 + 0.04 * j / n
            f = S.grade(S.warp(fr, S.W / 2, S.H / 2, z, "cover"))
            for key in seg["ov"]:
                c, a = S.gfx(key)
                f = f * (1 - a) + c * 255
            canvas = blur_bg(np.clip(f, 0, 255).astype(np.uint8))
            canvas[y16:y16 + PLATE_H] = cv2.resize(f, (VW, PLATE_H), interpolation=cv2.INTER_AREA)
            enc.stdin.write(np.clip(canvas, 0, 255).astype(np.uint8).tobytes())
        enc.stdin.close(); enc.wait(); os.replace(out + ".tmp.mp4", out)
        return out

    k_shot = seg["shot"]
    t0, sh = S.SHOTS[k_shot]
    nxt = S.SHOTS[k_shot + 1][0] if k_shot + 1 < len(S.SHOTS) else S.VO_END + S.TAIL
    shot_len = nxt - t0
    kind = sh["kind"]
    tall = kind == "I" and sh.get("fit") == "contain"
    if kind == "I":
        img = S.load_img(sh["path"], sh.get("crop"))
        img2 = S.load_img(sh["swap"][1], sh.get("crop")) if "swap" in sh else None
        h, w = img.shape[:2]
        if tall:   # portrait photo: its own tall box, at the same zoom moves
            box_h = TALL_H
            base = min(VW / w, box_h / h)
            ones = np.full((h, w), 255, np.uint8)
        else:
            base = max(S.W / w, S.H / h)
    elif kind == "V":
        frames = S.video_frames(sh["src"], sh["ss"] + seg["lo"] * sh.get("speed", 1.0), n, sh.get("speed", 1.0))
    for j in range(n):
        lt = seg["lo"] + j / S.FPS
        vt = t0 + lt
        bw = sh.get("bw", False) if kind == "V" else (S.in_ranges(lt, sh.get("bw", [])) or S.in_ranges(vt, sh.get("bw", [])))
        plate_alpha = 1.0
        fo = sh.get("fadeout")
        if fo and shot_len - lt < fo:
            plate_alpha = max(0.0, (shot_len - lt) / fo)
        # ---- picture
        if kind == "B":
            canvas = bed_for(vt).copy()
            plate = None
        elif kind == "I" and tall:
            src = img2 if img2 is not None and vt >= sh["swap"][0] else img
            (cx, cy, z), _ = S.kf_at(sh["kf"], lt)
            s = base * z
            M = np.float32([[s, 0, VW / 2 - s * cx], [0, s, box_h / 2 - s * cy]])
            pic = cv2.warpAffine(src, M, (VW, box_h), flags=cv2.INTER_LINEAR, borderValue=(0, 0, 0))
            msk = cv2.warpAffine(ones, M, (VW, box_h), flags=cv2.INTER_LINEAR, borderValue=0).astype(np.float32)[..., None] / 255
            pic = S.grade(pic, bw, sh.get("dark", 0))
            canvas = blur_bg(S.grade(src, bw).astype(np.uint8) if bw else src)
            yb = CY - box_h // 2
            m = msk * plate_alpha
            canvas[yb:yb + box_h] = canvas[yb:yb + box_h] * (1 - m) + pic * m
            plate = None
        else:
            if kind == "I":
                src = img2 if img2 is not None and vt >= sh["swap"][0] else img
                (cx, cy, z), whip = S.kf_at(sh["kf"], lt)
                if whip:
                    acc = np.zeros((S.H, S.W, 3), np.float32)
                    for q in range(6):
                        (qx, qy, qz), _ = S.kf_at(sh["kf"], lt + (q - 2.5) / S.FPS / 3)
                        acc += S.warp(src, qx, qy, base * qz, "cover")
                    fr = acc / 6
                else:
                    fr = S.warp(src, cx, cy, base * z, "cover")
            else:
                fr0 = next(frames)
                z0, z1 = sh["z"]
                fr = S.warp(fr0, S.W / 2, S.H / 2, z0 + (z1 - z0) * lt / shot_len, "cover")
            plate = S.grade(fr, bw, sh.get("dark", 0))
            plate = plate_overlays(plate, sh, vt)
            canvas = blur_bg(np.clip(plate, 0, 255).astype(np.uint8))
        # ---- dim from floating graphics (darkens the picture under a big number)
        dimk = 0.0
        for a_, b_, key, dim in sh.get("ov", []):
            if dim and a_ <= vt < b_ and not key.startswith(PLATE_KEYS):
                dimk = max(dimk, dim * max(0, min(min(1, (vt - a_) * S.FPS / 4 + 0.25), min(1, (b_ - vt) * S.FPS / 3))))
        if plate is not None:
            p = cv2.resize(plate, (VW, PLATE_H), interpolation=cv2.INTER_AREA) * (1 - dimk)
            canvas[y16:y16 + PLATE_H] = canvas[y16:y16 + PLATE_H] * (1 - plate_alpha) + p * plate_alpha
        elif kind == "I" and tall and dimk:
            canvas *= (1 - dimk)
        if kind == "I" and tall:  # plate-bound graphics on portrait photos: place them on the box
            for a_, b_, key, dim in sh.get("ov", []):
                if a_ <= vt < b_ and key.startswith(PLATE_KEYS):
                    c, a = float_gfx(key)
                    paste(canvas, c, a, VW / 2, CY + TALL_H / 2 - a.shape[0] / 2 - 20)
        # ---- floating graphics, enlarged
        for a_, b_, key, dim in sh.get("ov", []):
            if a_ <= vt < b_ and not key.startswith(PLATE_KEYS):
                al = max(0, min(min(1, (vt - a_) * S.FPS / 4 + 0.25), min(1, (b_ - vt) * S.FPS / 3)))
                c, a = float_gfx(key)
                paste(canvas, c, a, VW / 2, CY, al)
        for ft in sh.get("flash", []):
            d = vt - ft
            if 0 <= d < 0.3:
                k = 1 - d / 0.3
                canvas = canvas * (1 - 0.85 * k) + 255 * 0.85 * k
        enc.stdin.write(np.clip(canvas, 0, 255).astype(np.uint8).tobytes())
    enc.stdin.close(); enc.wait()
    os.replace(out + ".tmp.mp4", out)
    return out


def main():
    os.makedirs(SEGDIR, exist_ok=True)
    for k in S.GFX:
        S.gfx(k)
    render_vgfx()
    segs = S.plan()
    if len(sys.argv) > 1:   # test: render only these segment indices
        segs = [s for s in segs if s["i"] in {int(x) for x in sys.argv[1:]}]
    with Pool(3) as pool:
        for k, _ in enumerate(pool.imap_unordered(render_seg_v, segs)):
            if k % 10 == 0:
                print("seg", k, "/", len(segs), flush=True)
    if len(sys.argv) > 1:
        return
    lst = f"{R}/segs_v.txt"
    open(lst, "w").write("".join(f"file '{SEGDIR}/{s['i']:03d}.mp4'\n" for s in segs if s["f1"] > s["f0"]))
    S.run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", lst, "-c", "copy", f"{R}/base_v.mp4"])
    out = f"{S.P}/out/shea_foster_v1_vertical_master.mp4"
    S.run(["ffmpeg", "-v", "error", "-y", "-i", f"{R}/base_v.mp4", "-i", f"{R}/mix.wav", "-map", "0:v", "-map", "1:a",
           "-vf", "noise=alls=3:allf=t,format=yuv420p", "-c:v", "libx264", "-preset", "medium", "-crf", "17",
           "-c:a", "aac", "-b:a", "256k", "-shortest", "-movflags", "+faststart", out])
    print("wrote", out)


if __name__ == "__main__":
    main()
