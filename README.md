# Automated Resume-JD ATS Matcher

A production-style resume screening tool that compares resumes with a job description using semantic similarity, keyword analysis, and structured LLM evaluation.

It supports both single-candidate evaluation and batch candidate ranking, while providing clear insights into match quality, missing skills, strengths, weaknesses, and resume improvement suggestions.

## Features

### Candidate Evaluation
- Compare one resume against one job description
- Rank multiple resumes against one job description
- Support PDF, DOCX, TXT, and ZIP files
- Recursively process supported files inside ZIP archives
- Generate semantic embeddings using Sentence Transformers
- Store resume vectors with ChromaDB
- Use structured OpenAI evaluation
- Use a local keyword-based fallback when OpenAI is unavailable
- Combine semantic and LLM scores into an ATS score
- Show matched and missing skills
- Generate strengths, weaknesses, summaries, and improvement suggestions
- Export results as JSON and CSV
- Support background evaluation jobs

## Tech Stack

**UI**
- Streamlit
- Pandas

**Backend**
- Flask
- Flask-CORS
- Python

**AI / NLP**
- Sentence Transformers
- OpenAI
- Keyword matching

**Storage & Processing**
- ChromaDB
- pdfplumber
- python-docx
- ZIP processing

**Testing & Deployment**
- Pytest
- Docker
- Docker Compose

## How It Works

The system combines semantic matching, keyword analysis, and LLM-based evaluation to produce a more useful ATS result.

```text
Resume + Job Description
          │
          ▼
      File Parsing
          │
    ┌─────┴─────┐
    ▼           ▼
Keywords    Embeddings
    │           │
    └─────┬─────┘
          ▼
    LLM Evaluation
          │
          ▼
     Hybrid Scoring
          │
          ▼
      ATS Result
```

## Scoring

The ATS score uses a hybrid approach:

```text
ATS Score
= Semantic Similarity × Semantic Weight
+ LLM Score × LLM Weight
```

Default weights:

```text
Semantic = 50%
LLM      = 50%
```

These weights can be adjusted through environment variables.

## Project Structure

```text
automated-ats-matcher/
│
├── app/
│   ├── api/
│   │   └── routes.py
│   ├── services/
│   │   ├── parser_service.py
│   │   ├── scoring_service.py
│   │   ├── keyword_service.py
│   │   ├── embedding_service.py
│   │   ├── vector_store.py
│   │   ├── llm_service.py
│   │   ├── evaluation_service.py
│   │   ├── job_service.py
│   │   └── report_service.py
│   ├── config.py
│   └── extensions.py
│
├── frontend/
│   └── streamlit_app.py
│
├── data/
├── docs/
├── scripts/
├── tests/
├── run_backend.py
├── run_frontend.py
└── docker-compose.yml
```

## API

```text
GET  /api/health
POST /api/upload
POST /api/evaluate_single
POST /api/evaluate_batch
POST /api/jobs
GET  /api/jobs/<job_id>
```

API examples are available in:

```text
docs/API_EXAMPLES.md
```

## Getting Started

### Prerequisites

- Python 3.11
- pip
- OpenAI API key (optional)
- Docker (optional)

### Clone the Repository

```bash
git clone <your-repository-url>
cd automated-ats-matcher
```

### Create Environment

**Windows PowerShell**

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

For development and testing:

```powershell
pip install -r requirements-dev.txt
```

### Environment Variables

Copy the example environment file:

```powershell
copy .env.example .env
```

Example:

```env
FLASK_ENV=development
FLASK_HOST=127.0.0.1
FLASK_PORT=5000
STREAMLIT_PORT=8501

OPENAI_API_KEY=
OPENAI_MODEL=gpt-4o-mini

SEMANTIC_WEIGHT=0.50
LLM_WEIGHT=0.50

EMBEDDING_MODEL=all-MiniLM-L6-v2
CHROMA_PERSIST_DIR=./storage/chroma
MAX_UPLOAD_MB=25
MAX_ZIP_FILES=100
MAX_TEXT_CHARS=30000
```

### Run Backend

```powershell
python run_backend.py
```

Backend:

```text
http://127.0.0.1:5000
```

### Run Frontend

Open another terminal:

```powershell
python run_frontend.py
```

Frontend:

```text
http://localhost:8501
```

The first run may download the Sentence Transformer model.

## Docker

Run the complete application with:

```bash
docker compose up --build
```

Services:

```text
Frontend → http://localhost:8501
Backend  → http://localhost:5000
```

## Testing

Run the test suite with:

```powershell
pytest -q
```

The tests cover areas such as:

- File parsing
- ZIP extraction
- Keyword analysis
- Score boundaries
- Hybrid scoring

## Sample Data

The repository includes sample resumes and job descriptions.

Synthetic data can also be generated with:

```powershell
python scripts/generate_synthetic_data.py --resumes 24 --jds 6
```

## Security & Reliability

The project includes:

- Safe ZIP member name handling
- ZIP nesting and file-count limits
- Configurable upload and text-size limits
- Environment-based secret management
- Centralized logging
- Local fallback when LLM evaluation is unavailable

For public production deployment, additional authentication, rate limiting, malware scanning, and managed infrastructure should be added.

## Key Engineering Highlights

- Hybrid semantic + LLM scoring instead of keyword-only matching
- Modular Flask backend architecture
- Separate services for parsing, scoring, embeddings, LLM evaluation, jobs, and reporting
- Single and batch candidate evaluation
- Explainable results with matched skills, missing skills, strengths, weaknesses, and recommendations
- Docker-based deployment setup
- Automated tests
- API documentation and sample data

## What I Learned

Building this project gave me hands-on experience with:

- AI-assisted resume evaluation
- Semantic similarity and embeddings
- LLM-based structured evaluation
- Hybrid scoring systems
- REST API development with Flask
- Vector storage with ChromaDB
- Document and ZIP file processing
- Background evaluation workflows
- Testing and containerized deployment

## Payment / External Services

The project is primarily focused on resume and job-description matching. External AI services are configurable through environment variables, with a local keyword-based fallback available when OpenAI is not used.

## Future Improvements

- User authentication and candidate accounts
- Resume history and saved evaluations
- Advanced ranking and filtering
- Recruiter dashboards
- More configurable scoring strategies
- Additional document formats
- Automated deployment and monitoring

## Project Goal

The goal of this project is to make resume screening faster and more useful by combining traditional ATS techniques with semantic matching and structured AI evaluation.

Instead of returning only a score, the system explains why a resume matches a job and highlights areas that can be improved.

## License

This project currently does not include an open-source license.

