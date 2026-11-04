"""Futuristic two-source transitions (A = outgoing shot, B = incoming shot).

Each transition is 12 frames (0.5 s), centred on the cut. Both shots are available, so
these are real blends/reveals, not one-sided effects:
  scan    - a glowing orange scanline sweeps down, revealing B behind it
  pixel   - A dissolves into growing data blocks, B resolves out of them
  grid    - tiles flip from A to B in a diagonal wave with glowing edges
  zoom    - zoom-through with radial blur, chromatic aberration and a light flash
  streak  - horizontal light streak with motion-blurred push from A to B
  glitch  - RGB split + slice displacement + block noise across the cut
"""
import cv2, numpy as np

W, H = 1920, 1080
ORANGE = np.array([255, 122, 26], np.float32)
KINDS = ["scan", "zoom", "grid", "glitch", "streak", "pixel"]

def _e(p): return p * p * (3 - 2 * p)

def _chroma(f, px):
    if px < 1: return f
    g = f.copy(); px = int(px)
    g[..., 0] = np.roll(f[..., 0], px, axis=1); g[..., 2] = np.roll(f[..., 2], -px, axis=1)
    return g

def _zoom(f, z):
    M = cv2.getRotationMatrix2D((W / 2, H / 2), 0, z)
    return cv2.warpAffine(f, M, (W, H), borderMode=cv2.BORDER_REFLECT)

def _zoomblur(f, z, amt):
    acc = np.zeros_like(f, np.float32)
    for j in range(5): acc += _zoom(f, z * (1 + amt * j / 4)).astype(np.float32)
    return (acc / 5).astype(np.uint8)

def _add(f, glow):
    return np.clip(f.astype(np.float32) + glow, 0, 255).astype(np.uint8)

def frame(kind, A, B, p, rng):
    """p in [0,1): 0.5 is the cut."""
    if kind == "scan":
        y = int(H * _e(p)); out = A.copy(); out[:y] = B[:y]
        glow = np.zeros((H, W, 3), np.float32)
        yy = np.arange(H)[:, None]
        band = np.exp(-((yy - y) / 6.0) ** 2)[:, :, None] * 255 + np.exp(-((yy - y) / 40.0) ** 2)[:, :, None] * ORANGE * 0.8
        glow += band
        out = _add(out, glow * np.sin(np.pi * p))
        y0, y1 = max(0, y - 60), min(H, y + 60)
        out[y0:y1] = _chroma(out[y0:y1], 10 * np.sin(np.pi * p))
        return out
    if kind == "pixel":
        src = A if p < 0.5 else B
        k = 1 - abs(p - 0.5) * 2               # 0 -> 1 -> 0
        bs = int(2 + 70 * k ** 1.5)
        small = cv2.resize(src, (max(1, W // bs), max(1, H // bs)), interpolation=cv2.INTER_AREA)
        out = cv2.resize(small, (W, H), interpolation=cv2.INTER_NEAREST)
        if 0.35 < p < 0.65:
            other = cv2.resize(cv2.resize(B if p < 0.5 else A, (max(1, W // bs), max(1, H // bs)),
                                          interpolation=cv2.INTER_AREA), (W, H), interpolation=cv2.INTER_NEAREST)
            m = (rng.random((H // bs + 1, W // bs + 1)) < 0.35)
            m = np.kron(m, np.ones((bs, bs), bool))[:H, :W]
            out[m] = other[m]
        return _chroma(out, 8 * k)
    if kind == "grid":
        ts = 120; out = A.copy()
        glow = np.zeros((H, W, 3), np.float32)
        for gy in range(0, H, ts):
            for gx in range(0, W, ts):
                order = (gx / W + gy / H) / 2
                lt = (p - 0.15 - order * 0.6) / 0.12
                if lt >= 1:
                    out[gy:gy + ts, gx:gx + ts] = B[gy:gy + ts, gx:gx + ts]
                elif lt > 0:
                    out[gy:gy + ts, gx:gx + ts] = (A[gy:gy + ts, gx:gx + ts] * (1 - lt) + B[gy:gy + ts, gx:gx + ts] * lt)
                    a = (1 - abs(lt - 0.5) * 2)
                    glow[gy:gy + 3, gx:gx + ts] += ORANGE * a; glow[gy + ts - 3:gy + ts, gx:gx + ts] += ORANGE * a
                    glow[gy:gy + ts, gx:gx + 3] += ORANGE * a; glow[gy:gy + ts, gx + ts - 3:gx + ts] += ORANGE * a
                    glow[gy:gy + ts, gx:gx + ts] += ORANGE * 0.18 * a
        return _add(out, glow)
    if kind == "zoom":
        if p < 0.5:
            q = p / 0.5; f = _zoomblur(A, 1 + 0.5 * q ** 2, 0.08 * q)
        else:
            q = (1 - p) / 0.5; f = _zoomblur(B, 1 + 0.35 * q ** 2, 0.06 * q)
        flash = np.exp(-((p - 0.5) / 0.09) ** 2)
        f = _chroma(f, 18 * flash + 4)
        return _add(f, (np.array([255, 230, 200], np.float32) * 0.45 * flash))
    if kind == "streak":
        q = _e(p); off = int(W * 0.5 * q)
        if p < 0.5: f = np.roll(A, -off, axis=1)
        else: f = np.roll(B, W // 2 - off, axis=1)
        k = int(3 + 120 * np.sin(np.pi * p)) | 1
        f = cv2.blur(f, (k, 1))
        yy = np.arange(H)[:, None, None]
        cy = H * (0.45 + 0.1 * np.sin(p * 3))
        band = np.exp(-((yy - cy) / 70.0) ** 2) * (ORANGE * 0.9) + np.exp(-((yy - cy) / 10.0) ** 2) * 255
        return _add(f, band * np.sin(np.pi * p) ** 1.5)
    if kind == "glitch":
        src = A if p < 0.5 else B
        k = 1 - abs(p - 0.5) * 2
        f = _chroma(src, 36 * k)
        for _ in range(int(16 * k) + 1):
            y = rng.integers(0, H - 10); h = int(rng.integers(6, 80))
            f[y:y + h] = np.roll(f[y:y + h], int(rng.integers(-220, 220) * k), axis=1)
        if k > 0.5:  # blocks of the other shot bleed in
            other = B if p < 0.5 else A
            for _ in range(int(10 * k)):
                x = int(rng.integers(0, W - 200)); y = int(rng.integers(0, H - 80))
                w = int(rng.integers(60, 300)); h = int(rng.integers(20, 90))
                f[y:y + h, x:x + w] = other[y:y + h, x:x + w]
        sl = (np.arange(H) % 4 < 2)[:, None, None]
        return np.where(sl, f, (f * 0.85).astype(np.uint8))
    raise ValueError(kind)
