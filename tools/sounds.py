"""Synthesized audio: a dark suspense bed, plus per-instance futuristic transition/UI sounds.

Every sound is generated from a seed, so each transition gets its own variation
(pitch, length, texture) instead of the same sample over and over.
"""
import wave
import numpy as np

SR = 48000

def save(path, x):
    x = np.asarray(x, np.float32)
    if x.ndim == 1: x = np.stack([x, x], 1)
    peak = np.abs(x).max() + 1e-9
    x = x / peak * 0.89
    w = wave.open(path, "wb"); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
    w.writeframes((x * 32767).astype(np.int16).tobytes()); w.close()

def _t(d): return np.arange(int(d * SR)) / SR

def _lp(x, fc):  # one-pole low-pass, fc may be an array
    a = np.exp(-2 * np.pi * np.broadcast_to(fc, x.shape) / SR)
    y = np.empty_like(x); acc = 0.0
    for i in range(len(x)):
        acc = (1 - a[i]) * x[i] + a[i] * acc; y[i] = acc
    return y

def _fft_lp(x, fc):
    X = np.fft.rfft(x); f = np.fft.rfftfreq(len(x), 1 / SR)
    X *= 1 / np.sqrt(1 + (f / fc) ** 4); return np.fft.irfft(X, len(x))

def _bp_noise(n, lo, hi, rng):
    X = np.fft.rfft(rng.normal(0, 1, n)); f = np.fft.rfftfreq(n, 1 / SR)
    X[(f < lo) | (f > hi)] = 0; return np.fft.irfft(X, n)

def _reverb(x, secs, rng, wet=0.35):
    n = int(secs * SR)
    ir = rng.normal(0, 1, n) * np.exp(-np.arange(n) / SR * (6.9 / secs))
    ir = _fft_lp(ir, 4000)
    L = len(x) + n
    y = np.fft.irfft(np.fft.rfft(x, L) * np.fft.rfft(ir, L), L)[:len(x)]
    y /= np.abs(y).max() + 1e-9
    return (1 - wet) * x / (np.abs(x).max() + 1e-9) + wet * y

# ------------------------------------------------------------------ suspense bed
def suspense_bed(path, dur=96.0, seed=11):
    rng = np.random.default_rng(seed)
    t = _t(dur); n = len(t)
    out = np.zeros((n, 2))
    # sub drone (E1) with slow swell
    sub = np.sin(2 * np.pi * 41.2 * t) * (0.6 + 0.4 * np.sin(2 * np.pi * t / 23))
    sub += 0.35 * np.sin(2 * np.pi * 82.4 * t + 0.3 * np.sin(2 * np.pi * 0.07 * t))
    out += sub[:, None] * 0.55
    # dark minor pad: detuned saws, slowly moving low-pass
    pad = np.zeros(n)
    for f0 in (82.41, 98.0, 123.47, 146.83):
        for det in (-0.6, 0.0, 0.7):
            ph = 2 * np.pi * (f0 + det) * t
            pad += 2 * ((ph / (2 * np.pi)) % 1) - 1
    cut = 260 + 220 * (0.5 + 0.5 * np.sin(2 * np.pi * t / 31))
    pad = _lp(pad / 12, cut)
    pad *= 0.55 + 0.45 * np.sin(2 * np.pi * t / 17 + 1.2)
    out[:, 0] += pad * 0.9; out[:, 1] += np.roll(pad, int(0.013 * SR)) * 0.9
    # heartbeat: lub-dub every 1.25 s
    hb = np.zeros(n); beat = int(1.25 * SR)
    kick = np.sin(2 * np.pi * 52 * _t(0.25) * (1 - 0.4 * _t(0.25))) * np.exp(-_t(0.25) * 18)
    for s in range(int(0.4 * SR), n - beat, beat):
        hb[s:s + len(kick)] += kick
        s2 = s + int(0.22 * SR); hb[s2:s2 + len(kick)] += 0.6 * kick
    out += (hb * 0.42)[:, None]
    # clock tick texture
    tick = _bp_noise(int(0.012 * SR), 2500, 7000, rng) * np.exp(-_t(0.012) * 400)
    tk = np.zeros(n)
    for i, s in enumerate(range(0, n - len(tick), SR)):
        tk[s:s + len(tick)] += tick * (0.8 if i % 2 else 0.5)
    out[:, 0] += tk * 0.05; out[:, 1] += tk * 0.035
    # eerie high harmonics + sparse piano-like pings
    hi = np.sin(2 * np.pi * 1318.5 * t) * (0.5 + 0.5 * np.sin(2 * np.pi * 5.1 * t)) * \
         np.clip(np.sin(2 * np.pi * t / 19), 0, 1) ** 3
    out[:, 1] += hi * 0.03; out[:, 0] += np.roll(hi, SR // 3) * 0.02
    for s in np.arange(3.0, dur - 4, 7.3):
        f = rng.choice([329.6, 311.1, 246.9, 220.0, 196.0])
        tt = _t(4.0); ping = (np.sin(2 * np.pi * f * tt) + 0.3 * np.sin(2 * np.pi * 2 * f * tt)) * np.exp(-tt * 1.3)
        i0 = int(s * SR); out[i0:i0 + len(ping), int(s) % 2] += ping * 0.12
    for c in range(2): out[:, c] = _reverb(out[:, c], 3.2, rng, 0.4)
    # seamless loop: crossfade tail into head
    xf = int(4 * SR); r = np.linspace(0, 1, xf)[:, None]
    out[:xf] = out[:xf] * r + out[-xf:] * (1 - r); out = out[:-xf]
    save(path, out)

# ------------------------------------------------------------------ transition sounds
def _env(n, a, d):
    e = np.ones(n); na = max(1, int(a * SR)); nd = max(1, int(d * SR))
    e[:na] = np.linspace(0, 1, na); e[-nd:] *= np.linspace(1, 0, nd) ** 2; return e

def trans_sound(kind, path, seed):
    """Sound centred so its impact lands at 0.30 s into the file."""
    rng = np.random.default_rng(seed); p = rng.uniform(0.85, 1.2)
    D = 0.75; n = int(D * SR); t = _t(D); x = np.zeros(n); hit = int(0.30 * SR)
    if kind == "glitch":
        for _ in range(rng.integers(5, 9)):
            s = hit + int(rng.uniform(-0.18, 0.12) * SR); L = int(rng.uniform(0.015, 0.05) * SR)
            b = rng.normal(0, 1, L); q = rng.integers(3, 7)
            b = np.round(b * q) / q
            b = np.repeat(b[::rng.integers(2, 8)], 8)[:L]
            x[s:s + len(b)] += b * rng.uniform(0.4, 1)
        x += np.sin(2 * np.pi * 60 * p * t) * np.exp(-np.abs(t - 0.3) * 30) * 0.8
    elif kind == "scan":
        f = 200 * p * np.exp(np.linspace(0, np.log(18), n))
        tone = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.sin(2 * np.pi * 37 * t)
        x += tone * _env(n, 0.25, 0.3) * 0.5 + _bp_noise(n, 1500, 9000, rng) * _env(n, 0.28, 0.35) * 0.4
    elif kind == "pixel":
        for i in range(rng.integers(7, 12)):
            s = int(rng.uniform(0.05, 0.5) * SR); L = int(0.03 * SR)
            f = rng.choice([880, 1175, 1320, 1568, 1760, 2093]) * p
            x[s:s + L] += np.sign(np.sin(2 * np.pi * f * _t(0.03))) * np.exp(-_t(0.03) * 90) * 0.35
    elif kind == "zoom":
        X = _bp_noise(n, 200, 6000, rng)
        sweep = np.linspace(0, 1, n) ** 2
        x += _fft_lp(X, 3000) * np.clip(sweep * 2, 0, 1) * _env(n, 0.29, 0.4) * 0.8
        tt = t - 0.3; boom = np.where(tt > 0, np.sin(2 * np.pi * 45 * p * tt) * np.exp(-tt * 8), 0)
        x += boom * 1.2
    elif kind == "streak":
        x += _bp_noise(n, 600 * p, 8000, rng) * _env(n, 0.3, 0.42) * 0.7
        x += np.sin(2 * np.pi * 3200 * p * t) * np.exp(-np.abs(t - 0.3) * 14) * 0.12
        pan = np.clip(t / D, 0, 1)
        st = np.stack([x * (1 - pan), x * pan], 1); save(path, st); return
    elif kind == "grid":
        k = rng.integers(10, 16)
        for i in range(k):
            s = int((0.08 + 0.4 * i / k) * SR)
            L = int(0.008 * SR); c = rng.normal(0, 1, L) * np.exp(-_t(0.008) * 600)
            x[s:s + L] += _fft_lp(c, 3000 + 400 * i) * (0.4 + 0.6 * i / k)
        x += np.sin(2 * np.pi * 90 * p * t) * np.exp(-np.abs(t - 0.32) * 25) * 0.6
    save(path, x)

def ui_sound(kind, path, seed):
    rng = np.random.default_rng(seed)
    if kind == "decode":   # data chatter while letters resolve, then a soft confirm blip
        D = 0.9; n = int(D * SR); x = np.zeros(n)
        for i in range(rng.integers(10, 16)):
            s = int(rng.uniform(0.02, 0.5) * SR); L = int(0.012 * SR)
            f = rng.uniform(1800, 4200)
            x[s:s + L] += np.sin(2 * np.pi * f * _t(0.012)) * np.exp(-_t(0.012) * 300) * 0.25
        tt = _t(0.3); f = rng.choice([660, 740, 880])
        bl = (np.sin(2 * np.pi * f * tt) + 0.5 * np.sin(2 * np.pi * 1.5 * f * tt)) * np.exp(-tt * 14)
        s = int(0.55 * SR); x[s:s + len(bl)] += bl * 0.5
        save(path, x)
