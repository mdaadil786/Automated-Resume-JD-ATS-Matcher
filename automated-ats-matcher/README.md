# Automated Resume-JD ATS Matcher

Production-style implementation of the supplied Automated Resume-JD ATS Matcher specification.

## Included
- PDF, DOCX, TXT and ZIP ingestion, including nested ZIP archives
- Flask REST API: `/api/upload`, `/api/evaluate_single`, `/api/evaluate_batch`
- Background job endpoints: `/api/jobs`, `/api/jobs/<id>`
- Streamlit UI with both matching modes
- Sentence Transformers `all-MiniLM-L6-v2`
- Persistent ChromaDB vector storage
- OpenAI structured JSON evaluation
- Hybrid semantic + LLM ATS scoring
- Missing keyword/skill analysis
- Tailored resume recommendations
- Candidate ranking and filtering
- >=90% highlighted with `#FFCCCC`
- JSON and CSV downloads
- Faker-based synthetic dataset generator (24 resumes + 6 JDs included)
- Validation, safe ZIP extraction, logging, tests
- Docker and docker-compose
- VS Code launch configuration

## Scoring
The source specification requires a hybrid semantic-vector + LLM evaluation but does not define numeric weights. To avoid inventing a source requirement, the weights are configurable in `.env`.

Defaults are 50% semantic + 50% LLM. Change them only if your project/team specifies different weights.

## VS Code

Python 3.11 recommended.

Windows PowerShell:

```powershell
cd automated-ats-matcher
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
copy .env.example .env
```

Add your OpenAI key to `.env`:

```env
OPENAI_API_KEY=your_key_here
OPENAI_MODEL=gpt-4o-mini
```

Start backend:

```powershell
python run_backend.py
```

Then another VS Code terminal:

```powershell
python run_frontend.py
```

Open `http://localhost:8501`.

Backend health: `http://127.0.0.1:5000/api/health`

The first `all-MiniLM-L6-v2` run downloads the model.

## No OpenAI key
The project has a deterministic local fallback. The UI/API remains runnable for demonstrations, while an OpenAI key enables the intended LLM evaluation.

## Tests

```powershell
pip install -r requirements-dev.txt
pytest -q
```

## Synthetic data

```powershell
python scripts/generate_synthetic_data.py --resumes 24 --jds 6
```

The included dataset already contains 24 resumes and 6 JDs.

## Docker

```powershell
docker compose up --build
```

Frontend: `http://localhost:8501`
Backend: `http://localhost:5000`

## Workflow

1. Upload PDF/DOCX/TXT/ZIP in Streamlit.
2. Flask parses the documents and recursively unpacks ZIPs.
3. Sentence Transformers creates dense vectors.
4. ChromaDB stores resume vectors.
5. OpenAI evaluates resume vs JD using structured JSON.
6. The hybrid scorer combines semantic and LLM scores using configured weights.
7. Keyword gaps, strengths, weaknesses and tailoring recommendations are shown.
8. Batch mode ranks candidates.
9. Candidates with ATS score >=90% are highlighted in light red `#FFCCCC`.
10. Reports can be downloaded.

## Security
Uploaded files are never executed. ZIP path traversal is blocked by using archive member basenames, nesting and file-count limits are enforced, file size is limited by Flask, secrets come from environment variables, and LLM input is bounded. For public production deployment, add authentication, rate limiting, malware scanning and managed persistent infrastructure.
