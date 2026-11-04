"""Remove the head's cast shadow from the white wall.

The wall's real lighting is smooth, so a 2D polynomial is fitted to the wall's brightness
around (and left of) the head. Pixels that sit clearly below that surface are shadow. Fitting
is iterative: the shadow drops out of the fit. Those pixels get an edge-accurate gain up to
the model, which keeps the wall texture. Hair, skin, the mic and the poster are protected by
a luma/saturation key.
"""
import cv2, numpy as np
Y = np.array([0.2126, 0.7152, 0.0722], np.float32)

def _nblur(v, m, s):
    return cv2.GaussianBlur(v * m, (0, 0), s) / np.maximum(cv2.GaussianBlur(m, (0, 0), s), 1e-4)

def _design(x, y):
    return np.stack([np.ones_like(x), x, y, x * x, x * y, y * y, x ** 3, y ** 3, x * x * y, x * y * y], 1)

def deshadow(rgb, sofa_y, face_x=None, strength=1.0):
    h, w = rgb.shape[:2]
    f = rgb.astype(np.float32) / 255.0
    sw, sh = w // 8, h // 8
    s = cv2.resize(f, (sw, sh), interpolation=cv2.INTER_AREA)
    L = s @ Y; sat = s.max(2) - s.min(2)
    subj = ((L < 0.38) | (sat > 0.11)).astype(np.uint8)
    subj = cv2.dilate(subj, np.ones((3, 3), np.uint8))
    yy, xx = np.mgrid[0:sh, 0:sw].astype(np.float32)
    fxl = (face_x if face_x is not None else w * 0.4) / 8
    region = (yy < sofa_y / 8 - 2) & (xx < fxl + sw * 0.22)
    wall = region & (subj == 0)
    xs, ys = xx / sw, yy / sh
    use = wall.copy()
    for _ in range(3):
        idx = np.flatnonzero(use)
        if len(idx) < 50: return rgb, None
        A = _design(xs.ravel()[idx], ys.ravel()[idx])
        coef, *_ = np.linalg.lstsq(A, L.ravel()[idx], rcond=None)
        model = (_design(xs.ravel(), ys.ravel()) @ coef).reshape(sh, sw)
        use = wall & (L > model - 0.025)          # drop shadow pixels from the fit
    m = np.clip((model * 0.965 - L) / 0.03, 0, 1) * wall
    if face_x is not None:
        m *= np.clip((fxl + sw * 0.04 - xx) / (sw * 0.05), 0, 1)
    m = cv2.morphologyEx(m.astype(np.float32), cv2.MORPH_OPEN, np.ones((3, 3), np.uint8))
    m = cv2.dilate(m, np.ones((5, 5), np.uint8))
    m = cv2.GaussianBlur(m, (0, 0), 2.5)
    m = cv2.resize(m, (w, h), interpolation=cv2.INTER_CUBIC)
    model = cv2.resize(model.astype(np.float32), (w, h), interpolation=cv2.INTER_CUBIC)
    Lf = f @ Y; satf = f.max(2) - f.min(2)
    prot = ((Lf < 0.4) | (satf > 0.12)).astype(np.uint8)
    prot = cv2.dilate(prot, np.ones((5, 5), np.uint8)).astype(np.float32)
    Lfs = _nblur(Lf, 1 - prot, 3)
    gain = 1 + np.clip(m, 0, 1) * strength * (np.clip(model / np.maximum(Lfs, 1e-3), 1, 2.0) - 1)
    gain = 1 + (gain - 1) * (1 - cv2.GaussianBlur(prot, (0, 0), 1.5))
    out = np.clip(f * gain[..., None], 0, 1)
    return (out * 255 + 0.5).astype(np.uint8), m
