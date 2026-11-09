from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.responses import HTMLResponse
from pathlib import Path

app = FastAPI(
    title="PyBodySwap AI",
    description="Python-only video replacement application scaffold.",
    version="0.1.0",
)

PAGE = """<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <title>PyBodySwap AI</title>
  <style>
    :root{color-scheme:dark;font-family:Inter,system-ui,sans-serif}
    body{margin:0;background:#0b1020;color:#eef2ff;min-height:100vh;display:grid;place-items:center}
    main{width:min(720px,calc(100% - 32px));padding:32px 0}
    .panel{background:#141c31;border:1px solid #293653;border-radius:18px;padding:24px;margin:16px 0}
    h1{font-size:clamp(2rem,6vw,3.2rem);margin:0 0 8px}
    p{color:#b8c3d9;line-height:1.6}
    label{display:block;font-weight:650;margin:18px 0 8px}
    input[type=file]{width:100%;padding:14px;background:#0d1528;border:1px dashed #526487;border-radius:12px;color:#dce6fa}
    button{margin-top:20px;padding:13px 18px;border:0;border-radius:10px;background:#8b9cff;color:#10152a;font-weight:750;font-size:1rem}
    button:disabled{opacity:.5}
    .note{font-size:.9rem;background:#211d31;border-left:3px solid #b49aff;padding:12px 14px;border-radius:8px}
    #status{white-space:pre-wrap;margin-top:16px}
    a{color:#aebcff}
  </style>
</head>
<body><main>
  <p>PYTHON VIDEO WORKSPACE</p>
  <h1>PyBodySwap AI</h1>
  <p>Full-body video replacement project scaffold. Upload controls and API are deployed; a CPU-only video analysis preview is available as a separate Python command-line tool.</p>
  <section class="panel">
    <form id="upload-form">
      <label for="source">Source video</label>
      <input id="source" name="source" type="file" accept="video/mp4,video/quicktime,video/webm" required>
      <label for="reference">Reference image</label>
      <input id="reference" name="reference" type="file" accept="image/png,image/jpeg,image/webp" required>
      <label><input id="consent" type="checkbox" required> I have permission from the people depicted to create this edited video.</label>
      <button id="submit" type="submit">Check files</button>
    </form>
    <div id="status" role="status"></div>
  </section>
  <section class="panel note">
    <strong>Current deployment status</strong>
    <p>This Vercel deployment hosts the Python interface and API only. The repository includes a CPU-only Python preview tool that detects a person's pose and segmentation mask, but it does not replace their identity. Full-body photorealistic replacement is not implemented; CPU processing is slow and standard Vercel functions are not suitable for long video jobs.</p>
  </section>
  <p><a href="/docs">Open Python API documentation</a></p>
</main>
<script>
const form=document.getElementById('upload-form');
const status=document.getElementById('status');
form.addEventListener('submit',async e=>{
  e.preventDefault();
  const source=document.getElementById('source').files[0];
  const reference=document.getElementById('reference').files[0];
  if(!source||!reference||!document.getElementById('consent').checked)return;
  status.textContent='Checking file types and sizes…';
  const data=new FormData();data.append('source',source);data.append('reference',reference);
  try{
    const response=await fetch('/api/validate', {method:'POST',body:data});
    const result=await response.json();
    status.textContent=response.ok?result.message:(result.detail||'Validation failed');
  }catch(err){status.textContent='Request failed: '+err.message;}
});
</script>
</body></html>"""


@app.get("/", response_class=HTMLResponse)
async def home():
    return PAGE


@app.get("/api/health")
async def health():
    return {"status": "ok", "app": "PyBodySwap AI", "generation": "not_configured"}


@app.post("/api/validate")
async def validate_files(
    source: UploadFile = File(...),
    reference: UploadFile = File(...),
):
    video_types = {"video/mp4", "video/quicktime", "video/webm"}
    image_types = {"image/jpeg", "image/png", "image/webp"}

    if source.content_type not in video_types:
        raise HTTPException(status_code=415, detail="Source must be MP4, MOV, or WebM.")
    if reference.content_type not in image_types:
        raise HTTPException(status_code=415, detail="Reference must be JPG, PNG, or WebP.")

    # Read only a small prefix; do not retain user media in serverless memory or storage.
    video_header = await source.read(32)
    image_header = await reference.read(32)
    if not video_header or not image_header:
        raise HTTPException(status_code=400, detail="Both files must be non-empty.")

    return {
        "valid": True,
        "message": (
            "File types checked successfully. Generation is not enabled in this "
            "Vercel deployment; no media was saved or processed."
        ),
        "generation": "not_configured",
    }
