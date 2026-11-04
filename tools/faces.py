import cv2, json, sys, numpy as np
cap = cv2.VideoCapture(sys.argv[1]); casc = cv2.CascadeClassifier(sys.argv[2])
out = []; i = 0
while True:
    ok, f = cap.read()
    if not ok: break
    g = cv2.equalizeHist(cv2.cvtColor(f, cv2.COLOR_BGR2GRAY))
    fs = casc.detectMultiScale(g, 1.1, 6, minSize=(60, 60))
    if len(fs):
        x, y, w, h = max(fs, key=lambda r: r[2] * r[3])
        out.append([i / 4.0, (x + w / 2) / 960, (y + h / 2) / 540, h / 540])
    i += 1
json.dump(out, open(sys.argv[3], "w")); print(len(out), "of", i)
