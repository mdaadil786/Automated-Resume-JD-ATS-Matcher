import logging
from flask import Blueprint, jsonify, request
from app.services.parser_service import parse_uploaded_files
from app.extensions import evaluation_service, job_service
from app.services.report_service import results_to_csv

logger = logging.getLogger(__name__)
api = Blueprint("api", __name__)

@api.get("/health")
def health():
    return jsonify({"status": "healthy", "service": "automated-ats-matcher"})

@api.post("/upload")
def upload():
    files = request.files.getlist("files")
    if not files:
        return jsonify({"error": "No files supplied under 'files'."}), 400
    try:
        docs = parse_uploaded_files(files)
        return jsonify({"count": len(docs), "documents": [
            {"filename": d["filename"], "characters": len(d["text"])} for d in docs
        ]})
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception:
        logger.exception("Upload parsing failed")
        return jsonify({"error": "Failed to parse uploaded files."}), 500

@api.post("/evaluate_single")
def evaluate_single():
    resume = request.files.get("resume")
    jd = request.form.get("job_description", "")
    if resume is None:
        return jsonify({"error": "Resume file is required."}), 400
    try:
        docs = parse_uploaded_files([resume])
        if not docs:
            raise ValueError("No supported resume document was found.")
        return jsonify(evaluation_service.evaluate(docs[0], jd))
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception:
        logger.exception("Single evaluation failed")
        return jsonify({"error": "Evaluation failed."}), 500

@api.post("/evaluate_batch")
def evaluate_batch():
    jd = request.form.get("job_description", "")
    files = request.files.getlist("resumes") or request.files.getlist("files")
    if not files:
        return jsonify({"error": "At least one resume or ZIP is required."}), 400
    try:
        docs = parse_uploaded_files(files)
        results = evaluation_service.evaluate_batch(docs, jd)
        return jsonify({"count": len(results), "results": results,
                        "csv": results_to_csv(results)})
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception:
        logger.exception("Batch evaluation failed")
        return jsonify({"error": "Batch evaluation failed."}), 500

@api.post("/jobs")
def create_job():
    jd = request.form.get("job_description", "")
    files = request.files.getlist("resumes") or request.files.getlist("files")
    if not files:
        return jsonify({"error": "Resume/ZIP files are required."}), 400
    try:
        docs = parse_uploaded_files(files)
        job_id = job_service.submit(docs, jd)
        return jsonify({"job_id": job_id, "status": "queued"}), 202
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

@api.get("/jobs/<job_id>")
def get_job(job_id):
    result = job_service.get(job_id)
    if result is None:
        return jsonify({"error": "Job not found."}), 404
    return jsonify(result)
