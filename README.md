# MONOTONE · Laser Forensics

**A real‑time hand‑tracking laser beam system with a forensic theme.**  
Show both hands to fire glowing, dynamic beams between your extended fingertips.

![FLUX demo](https://img.shields.io/badge/demo-live-brightgreen) ![MediaPipe](https://img.shields.io/badge/MediaPipe-vision-blue) ![License](https://img.shields.io/badge/license-MIT-lightgrey)

---

## ✨ Features

- **Dual‑hand laser beams** – beams link corresponding extended fingertips, with cross‑weave and palm‑to‑palm effects.
- **4 beam styles** – Glow, Solid, Dashed, Neon – each with a distinct visual feel.
- **6 color modes** – Shape‑shift (dynamic based on hand shape), Cyan, Magenta, Lime, Gold, and more.
- **Particle system** – glowing particles burst from beam midpoints and fingertips (toggle on/off).
- **Skeleton overlay** – show/hide the hand wireframe for reference.
- **Snapshot export** – save the current view (camera + beams + particles) as a PNG.
- **Forensic‑inspired UI** – dark grid background, glass‑morphism dashboard, and monospaced typography.
- **Optimized performance** – efficient rendering with smooth 60 FPS tracking.

---

## 🖐️ How it works

1. **Allow camera access** – the app uses your webcam.
2. **Show both hands** – beams appear when at least two hands are detected.
3. **Extend fingers** – only extended fingertips (both hands) generate beams.
4. **Customize** – use the top dashboard to change beam color, style, and toggle particles or skeleton.
5. **Snap** – click the camera icon to save an evidence‑style screenshot.

---

## 🛠️ Technologies

- [MediaPipe Hands](https://developers.google.com/mediapipe/solutions/vision/hand_landmarker) – real‑time hand landmark detection.
- Vanilla JavaScript – no external libraries, self‑contained.
- HTML5 Canvas – rendering and drawing.
- CSS – custom dark theme with backdrop blur and grid overlay.

---

## 🚀 Usage

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/flux-laser-forensics.git
   ```
2. Open `index.html` in a modern browser (Chrome, Edge, Firefox).
3. Allow camera permissions.
4. Show both hands and start playing!

> **Note:** Requires a webcam and a browser that supports `getUserMedia` and ES modules.

---

## 📦 File structure

```
├── index.html          # main entry point (all code included)
└── README.md           # this file
```

All code is self‑contained in a single HTML file – no build step needed.

---

## 📄 License

MIT – feel free to use, modify, and distribute.
