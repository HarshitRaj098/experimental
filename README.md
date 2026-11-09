# PyBodySwap AI

Python-first full-body video replacement application scaffold.

## Current status

- FastAPI application and browser interface
- Video and reference-image type validation
- Health endpoint and interactive API docs
- Vercel Python deployment configuration

**Video generation is not implemented yet.** A photorealistic full-body replacement pipeline requires pretrained model weights and sustained GPU inference. Standard Vercel Python functions are not a suitable GPU video-generation runtime. This deployment does not save uploaded media or pretend to generate output.

## Run locally for development

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\\Scripts\\activate
pip install -r requirements.txt
uvicorn api.index:app --reload
```

Open http://127.0.0.1:8000 and http://127.0.0.1:8000/docs.

## API

- `GET /` — web interface
- `GET /api/health` — health check
- `POST /api/validate` — validate source video and reference image

Only use reference material with permission from the people depicted. Label synthetic edits clearly.
