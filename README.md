# PyBodySwap AI

Python-first full-body video replacement project.

## Current status

- FastAPI browser interface and upload validation on Vercel
- CPU-only video analysis preview using OpenCV and MediaPipe
- Frame-by-frame pose landmark and person-segmentation visualization

**Identity/body replacement is not implemented.** The CPU script is a foundation for analysis only; it highlights the detected person and pose but does not transfer the reference image's identity, face, clothing, or body. Photorealistic full-body replacement is substantially more demanding than pose detection and cannot be honestly promised by this CPU prototype.

The Vercel deployment only hosts the interface and lightweight API. It does not process or store uploaded media. Long CPU video jobs should not run inside a standard Vercel serverless function.

## Run the CPU preview

Use Python 3.10 or 3.11 for the broadest dependency compatibility.

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\\Scripts\\activate
pip install -r requirements-cpu.txt
python cpu_pipeline.py input.mp4 --output preview.mp4
```

The output is an annotated MP4 showing pose landmarks and the estimated person-segmentation mask. It is a diagnostic preview, not a swapped video.

For faster CPU processing, use `--model-complexity 0`. For a heavier pose model, use `--model-complexity 2`.

## Run the web API

```bash
pip install -r requirements.txt
uvicorn api.index:app --reload
```

Open http://127.0.0.1:8000 and http://127.0.0.1:8000/docs.

## API

- `GET /` — web interface
- `GET /api/health` — health check
- `POST /api/validate` — validate source video and reference image

Only use reference material with permission from the people depicted. Label synthetic edits clearly.
