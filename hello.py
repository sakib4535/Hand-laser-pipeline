<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<title>FLUX - Laser Hands</title>
<style>
  * { margin: 0; padding: 0; box-sizing: border-box; }
  body { background: #000; color: #fff; font-family: 'Courier New', monospace; overflow: hidden; height: 100vh; }
  #container { position: relative; width: 100%; height: 100vh; }
  #webcam { position: absolute; top: 0; left: 0; width: 100%; height: 100%; object-fit: cover; display: none; }
  #canvas { position: absolute; top: 0; left: 0; width: 100%; height: 100%; }
  #top-bar { position: absolute; top: 0; left: 0; right: 0; padding: 14px 20px; display: flex; align-items: center; gap: 16px; background: linear-gradient(to bottom, rgba(0,0,0,0.7), transparent); }
  #logo { font-size: 22px; font-weight: 900; letter-spacing: 4px; color: #0ff; text-shadow: 0 0 10px #0ff; }
  #mode-display { font-size: 13px; letter-spacing: 2px; color: #0ff; background: rgba(0,255,255,0.1); border: 1px solid rgba(0,255,255,0.3); padding: 4px 12px; border-radius: 4px; }
  #fps-display { font-size: 12px; color: #888; margin-left: auto; }
  #bottom-bar { position: absolute; bottom: 0; left: 0; right: 0; padding: 10px 20px; display: flex; align-items: center; justify-content: space-between; background: linear-gradient(to top, rgba(0,0,0,0.7), transparent); }
  #mode-btns { display: flex; gap: 8px; }
  .mode-btn { background: rgba(0,0,0,0.6); border: 1px solid #333; color: #666; font-family: 'Courier New', monospace; font-size: 11px; letter-spacing: 1px; padding: 5px 12px; border-radius: 4px; cursor: pointer; transition: all 0.2s; }
  .mode-btn.active { border-color: #0ff; color: #0ff; background: rgba(0,255,255,0.1); text-shadow: 0 0 6px #0ff; }
  .mode-btn:hover { border-color: #0ff; color: #0ff; }
  #clear-btn { background: rgba(0,0,0,0.6); border: 1px solid #333; color: #666; font-family: 'Courier New', monospace; font-size: 11px; letter-spacing: 1px; padding: 5px 12px; border-radius: 4px; cursor: pointer; transition: all 0.2s; }
  #clear-btn:hover { border-color: #f0f; color: #f0f; }
  #start-screen { position: absolute; inset: 0; display: flex; flex-direction: column; align-items: center; justify-content: center; background: #000; z-index: 10; }
  #start-title { font-size: 72px; font-weight: 900; letter-spacing: 16px; color: #0ff; text-shadow: 0 0 30px #0ff, 0 0 60px #0ff; margin-bottom: 8px; }
  #start-sub { font-size: 13px; letter-spacing: 5px; color: #444; margin-bottom: 48px; }
  #start-btn { background: transparent; border: 1px solid #0ff; color: #0ff; font-family: 'Courier New', monospace; font-size: 14px; letter-spacing: 3px; padding: 12px 40px; cursor: pointer; transition: all 0.3s; text-shadow: 0 0 6px #0ff; }
  #start-btn:hover { background: rgba(0,255,255,0.1); box-shadow: 0 0 20px rgba(0,255,255,0.3); }
  #legend { position: absolute; right: 16px; top: 60px; display: flex; flex-direction: column; gap: 5px; }
  .legend-item { display: flex; align-items: center; gap: 6px; font-size: 11px; color: #555; }
  .legend-dot { width: 10px; height: 10px; border-radius: 50%; flex-shrink: 0; }
  #status { font-size: 11px; color: #555; letter-spacing: 1px; }
  #loading { position: absolute; inset: 0; display: flex; flex-direction: column; align-items: center; justify-content: center; background: #000; z-index: 9; }
  #loading-text { color: #0ff; font-size: 14px; letter-spacing: 3px; animation: pulse 1s infinite; }
  #loading-bar { width: 220px; height: 2px; background: #111; margin-top: 16px; overflow: hidden; border-radius: 2px; }
  #loading-fill { height: 100%; background: #0ff; box-shadow: 0 0 8px #0ff; animation: load 2.5s ease forwards; }
  #os-hint { position: absolute; top: 50%; left: 50%; transform: translate(-50%,-50%); color: rgba(0,255,255,0.12); font-size: 12px; letter-spacing: 2px; text-align: center; line-height: 2; pointer-events: none; }
  @keyframes pulse { 0%,100%{opacity:0.3} 50%{opacity:1} }
  @keyframes load { from{width:0} to{width:100%} }
</style>
</head>
<body>
<div id="container">
  <video id="webcam" autoplay playsinline muted></video>
  <canvas id="canvas"></canvas>

  <!-- Start Screen -->
  <div id="start-screen">
    <div id="start-title">FLUX</div>
    <div id="start-sub">LASER · WRITE · CONTROL</div>
    <button id="start-btn" onclick="startApp()">▶ LAUNCH</button>
  </div>

  <!-- Loading Screen -->
  <div id="loading" style="display:none">
    <div id="loading-text">LOADING MEDIAPIPE</div>
    <div id="loading-bar"><div id="loading-fill"></div></div>
  </div>

  <!-- HUD -->
  <div id="top-bar">
    <div id="logo">FLUX</div>
    <div id="mode-display">MODE: LASER</div>
    <div id="fps-display">FPS: --</div>
  </div>

  <div id="legend">
    <div class="legend-item"><div class="legend-dot" style="background:#ff0000"></div>Thumb</div>
    <div class="legend-item"><div class="legend-dot" style="background:#00ff00"></div>Index</div>
    <div class="legend-item"><div class="legend-dot" style="background:#0055ff"></div>Middle</div>
    <div class="legend-item"><div class="legend-dot" style="background:#00ffff"></div>Ring</div>
    <div class="legend-item"><div class="legend-dot" style="background:#ff00ff"></div>Pinky</div>
  </div>

  <div id="os-hint" style="display:none">
    INDEX FINGER → MOVE MOUSE<br>
    THUMB + INDEX → CLICK<br>
    THUMB + MIDDLE → SCROLL
  </div>

  <div id="bottom-bar">
    <div id="mode-btns">
      <button class="mode-btn active" onclick="setMode(1)">1 · LASER</button>
      <button class="mode-btn" onclick="setMode(2)">2 · WRITE</button>
      <button class="mode-btn" onclick="setMode(3)">3 · OS CTRL</button>
      <button id="clear-btn" onclick="clearCanvas()">C · CLEAR</button>
    </div>
    <div id="status">READY</div>
  </div>
</div>

<!-- MediaPipe CDN -->
<script src="https://cdn.jsdelivr.net/npm/@mediapipe/hands/hands.js" crossorigin="anonymous"></script>
<script src="https://cdn.jsdelivr.net/npm/@mediapipe/camera_utils/camera_utils.js" crossorigin="anonymous"></script>

<script>
const video       = document.getElementById('webcam');
const canvas      = document.getElementById('canvas');
const ctx         = canvas.getContext('2d');
const modeDisplay = document.getElementById('mode-display');
const fpsDisplay  = document.getElementById('fps-display');
const statusEl    = document.getElementById('status');
const osHint      = document.getElementById('os-hint');

// ---- CONFIG ----
const FINGER_COLORS  = { 4:'#ff0000', 8:'#00ff00', 12:'#0055ff', 16:'#00ffff', 20:'#ff00ff' };
const FINGERTIP_IDS  = [4, 8, 12, 16, 20];
const LASER_LENGTH   = 180;

// ---- STATE ----
let mode          = 1;
let drawCanvas    = null;
let lastPt        = null;
let isDrawing     = false;
let latestResults = null;
let lastFpsTime   = performance.now();
let frameCount    = 0;
let fps           = 0;
let cameraRunning = false;

// ---- RESIZE ----
function resizeCanvas() {
  canvas.width  = window.innerWidth;
  canvas.height = window.innerHeight;
  if (!drawCanvas || drawCanvas.width !== canvas.width || drawCanvas.height !== canvas.height) {
    const old = drawCanvas;
    drawCanvas = document.createElement('canvas');
    drawCanvas.width  = canvas.width;
    drawCanvas.height = canvas.height;
    if (old) {
      drawCanvas.getContext('2d').drawImage(old, 0, 0);
    }
  }
}
window.addEventListener('resize', resizeCanvas);
resizeCanvas();

// ---- MODE SWITCH ----
function setMode(m) {
  mode = m;
  const names = ['', 'LASER', 'WRITING', 'OS CONTROL'];
  modeDisplay.textContent = 'MODE: ' + names[m];
  document.querySelectorAll('.mode-btn').forEach((b, i) => b.classList.toggle('active', i === m - 1));
  osHint.style.display = m === 3 ? 'block' : 'none';
  if (m !== 2) { isDrawing = false; lastPt = null; }
}

function clearCanvas() {
  if (drawCanvas) drawCanvas.getContext('2d').clearRect(0, 0, drawCanvas.width, drawCanvas.height);
}

// ---- NEON LASER DRAW ----
function drawNeon(c, x1, y1, x2, y2, color, thick) {
  thick = thick || 4;
  const r = parseInt(color.slice(1,3),16);
  const g = parseInt(color.slice(3,5),16);
  const b = parseInt(color.slice(5,7),16);
  c.save();
  c.lineCap = 'round';
  // outer glow
  c.strokeStyle = `rgba(${r},${g},${b},0.15)`;
  c.lineWidth = thick + 14;
  c.beginPath(); c.moveTo(x1,y1); c.lineTo(x2,y2); c.stroke();
  // mid glow
  c.strokeStyle = `rgba(${r},${g},${b},0.35)`;
  c.lineWidth = thick + 7;
  c.beginPath(); c.moveTo(x1,y1); c.lineTo(x2,y2); c.stroke();
  // core color
  c.strokeStyle = color;
  c.lineWidth = thick;
  c.beginPath(); c.moveTo(x1,y1); c.lineTo(x2,y2); c.stroke();
  // white highlight
  c.strokeStyle = 'rgba(255,255,255,0.85)';
  c.lineWidth = Math.max(1, thick / 3);
  c.beginPath(); c.moveTo(x1,y1); c.lineTo(x2,y2); c.stroke();
  // tip dot outer
  c.fillStyle = 'rgba(255,255,255,0.9)';
  c.beginPath(); c.arc(x2, y2, 7, 0, Math.PI*2); c.fill();
  // tip dot inner
  c.fillStyle = color;
  c.beginPath(); c.arc(x2, y2, 4, 0, Math.PI*2); c.fill();
  c.restore();
}

// ---- DIRECTION from wrist to fingertip ----
function getDir(lm, tipIdx) {
  const tip   = lm[tipIdx];
  const wrist = lm[0];
  const dx = tip.x - wrist.x;
  const dy = tip.y - wrist.y;
  const len = Math.hypot(dx, dy);
  return len ? [dx/len, dy/len] : [1, 0];
}

// ---- LANDMARK DISTANCE ----
function dist(a, b) {
  return Math.hypot(a.x - b.x, a.y - b.y);
}

// ---- MEDIAPIPE CALLBACK ----
function onResults(results) {
  latestResults = results;
}

// ---- MAIN RENDER LOOP ----
function drawFrame() {
  resizeCanvas();
  ctx.clearRect(0, 0, canvas.width, canvas.height);
  const W = canvas.width, H = canvas.height;

  // Mirror webcam
  if (cameraRunning && video.readyState >= 2) {
    ctx.save();
    ctx.scale(-1, 1);
    ctx.drawImage(video, -W, 0, W, H);
    ctx.restore();
  }

  const hands = (latestResults && latestResults.multiHandLandmarks) ? latestResults.multiHandLandmarks : [];

  // ---- MODE 1: LASER ----
  if (mode === 1) {
    for (const lm of hands) {
      // flip x because we mirrored the camera
      const flipped = lm.map(p => ({ x: 1 - p.x, y: p.y }));
      for (const idx of FINGERTIP_IDS) {
        const tip = flipped[idx];
        const tx = tip.x * W, ty = tip.y * H;
        const [dx, dy] = getDir(flipped, idx);
        const ex = tx + dx * LASER_LENGTH;
        const ey = ty + dy * LASER_LENGTH;
        drawNeon(ctx, tx, ty, ex, ey, FINGER_COLORS[idx], 4);
      }
    }
  }

  // ---- MODE 2: WRITE ----
  if (mode === 2) {
    ctx.globalAlpha = 0.88;
    ctx.drawImage(drawCanvas, 0, 0);
    ctx.globalAlpha = 1;
    const dc = drawCanvas.getContext('2d');

    for (const lm of hands) {
      const flipped = lm.map(p => ({ x: 1 - p.x, y: p.y }));
      const tip   = flipped[8];
      const pip   = flipped[6];
      const thumb = flipped[4];

      if (tip.y < pip.y) {
        // index extended — draw
        const tx = tip.x * W, ty = tip.y * H;
        if (isDrawing && lastPt) {
          dc.save();
          dc.lineCap = 'round'; dc.lineJoin = 'round';
          dc.strokeStyle = '#00ff88'; dc.lineWidth = 5;
          dc.shadowColor = '#00ff88'; dc.shadowBlur = 10;
          dc.beginPath(); dc.moveTo(lastPt[0], lastPt[1]); dc.lineTo(tx, ty); dc.stroke();
          dc.strokeStyle = 'rgba(255,255,255,0.4)'; dc.lineWidth = 1.5; dc.shadowBlur = 0;
          dc.beginPath(); dc.moveTo(lastPt[0], lastPt[1]); dc.lineTo(tx, ty); dc.stroke();
          dc.restore();
        }
        isDrawing = true;
        lastPt = [tx, ty];
        // draw cursor dot
        ctx.fillStyle = 'rgba(0,255,136,0.8)';
        ctx.beginPath(); ctx.arc(tx, ty, 6, 0, Math.PI*2); ctx.fill();
        ctx.fillStyle = 'rgba(255,255,255,0.9)';
        ctx.beginPath(); ctx.arc(tx, ty, 2.5, 0, Math.PI*2); ctx.fill();
      } else {
        isDrawing = false;
        lastPt = null;
      }

      // pinch to erase
      if (dist(thumb, flipped[8]) < 0.05) {
        const cx = thumb.x * W, cy = thumb.y * H;
        dc.clearRect(cx - 28, cy - 28, 56, 56);
        ctx.strokeStyle = 'rgba(255,0,100,0.6)';
        ctx.lineWidth = 1.5;
        ctx.beginPath(); ctx.arc(cx, cy, 26, 0, Math.PI*2); ctx.stroke();
      }
    }
  }

  // ---- MODE 3: OS CONTROL ----
  if (mode === 3) {
    if (hands.length > 0) {
      const lm      = hands[0];
      const flipped = lm.map(p => ({ x: 1 - p.x, y: p.y }));
      const idx     = flipped[8];
      const thumb   = flipped[4];
      const mid     = flipped[12];
      const sx      = idx.x * W, sy = idx.y * H;

      // crosshair
      ctx.strokeStyle = 'rgba(0,255,255,0.5)';
      ctx.lineWidth = 1;
      ctx.setLineDash([4, 4]);
      ctx.beginPath(); ctx.moveTo(sx - 14, sy); ctx.lineTo(sx + 14, sy); ctx.stroke();
      ctx.beginPath(); ctx.moveTo(sx, sy - 14); ctx.lineTo(sx, sy + 14); ctx.stroke();
      ctx.setLineDash([]);

      // cursor ring
      ctx.strokeStyle = '#0ff'; ctx.lineWidth = 1.5;
      ctx.beginPath(); ctx.arc(sx, sy, 18, 0, Math.PI*2); ctx.stroke();
      ctx.fillStyle = 'rgba(0,255,255,0.08)';
      ctx.beginPath(); ctx.arc(sx, sy, 18, 0, Math.PI*2); ctx.fill();

      // click = thumb+index pinch
      if (dist(thumb, flipped[8]) < 0.05) {
        ctx.fillStyle = 'rgba(0,255,255,0.4)';
        ctx.beginPath(); ctx.arc(sx, sy, 26, 0, Math.PI*2); ctx.fill();
        ctx.fillStyle = '#fff'; ctx.font = '11px Courier New'; ctx.textAlign = 'center';
        ctx.fillText('CLICK', sx, sy - 34);
      }

      // scroll = thumb+middle pinch
      if (dist(thumb, flipped[12]) < 0.05) {
        ctx.fillStyle = 'rgba(255,255,0,0.3)';
        ctx.beginPath(); ctx.arc(sx, sy, 26, 0, Math.PI*2); ctx.fill();
        ctx.fillStyle = '#ff0'; ctx.font = '11px Courier New'; ctx.textAlign = 'center';
        ctx.fillText('SCROLL', sx, sy - 34);
      }
    }
  }

  // ---- FPS ----
  frameCount++;
  const now = performance.now();
  if (now - lastFpsTime >= 500) {
    fps = Math.round(frameCount / ((now - lastFpsTime) / 1000));
    frameCount = 0;
    lastFpsTime = now;
    fpsDisplay.textContent = 'FPS: ' + fps;
  }

  requestAnimationFrame(drawFrame);
}

// ---- KEYBOARD SHORTCUTS ----
document.addEventListener('keydown', e => {
  const k = e.key;
  if (k === '1') setMode(1);
  else if (k === '2') setMode(2);
  else if (k === '3') setMode(3);
  else if (k.toLowerCase() === 'c') clearCanvas();
});

// ---- START ----
async function startApp() {
  document.getElementById('start-screen').style.display = 'none';
  document.getElementById('loading').style.display = 'flex';

  try {
    const stream = await navigator.mediaDevices.getUserMedia({
      video: { width: 1280, height: 720, facingMode: 'user' }
    });
    video.srcObject = stream;
    await new Promise(r => { video.onloadedmetadata = r; });
    cameraRunning = true;
    statusEl.textContent = 'CAM OK — LOADING MODEL';

    if (typeof Hands !== 'undefined') {
      const handTracker = new Hands({
        locateFile: f => `https://cdn.jsdelivr.net/npm/@mediapipe/hands/${f}`
      });
      handTracker.setOptions({
        maxNumHands: 2,
        modelComplexity: 1,
        minDetectionConfidence: 0.7,
        minTrackingConfidence: 0.5
      });
      handTracker.onResults(onResults);

      const cam = new Camera(video, {
        onFrame: async () => { await handTracker.send({ image: video }); },
        width: 1280, height: 720
      });
      await cam.start();
      statusEl.textContent = 'HAND TRACKING ACTIVE';
    } else {
      statusEl.textContent = 'WEBCAM ONLY — MediaPipe not loaded';
    }
  } catch(e) {
    statusEl.textContent = 'ERROR: ' + e.message;
    console.error(e);
  }

  document.getElementById('loading').style.display = 'none';
  drawFrame();
}
</script>
</body>
</html>