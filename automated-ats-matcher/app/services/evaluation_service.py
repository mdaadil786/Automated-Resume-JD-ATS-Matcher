from app.services.keyword_service import keyword_analysis
from app.services.scoring_service import hybrid_score, classification

class EvaluationService:
    def __init__(self, embeddings, vectors, llm):
        self.embeddings, self.vectors, self.llm = embeddings, vectors, llm

    def evaluate(self, doc, jd):
        if not jd.strip():
            raise ValueError("Job description cannot be empty.")
        semantic = self.vectors.similarity(doc["text"], jd)
        llm = self.llm.evaluate(doc["text"], jd)
        kw = keyword_analysis(doc["text"], jd)
        score = hybrid_score(semantic, llm["llm_score"])
        self.vectors.index_resume(doc["filename"], doc["text"])
        return {
            "candidate": doc["filename"],
            "ats_score": score,
            "semantic_similarity": round(semantic * 100, 2),
            "llm_score": llm["llm_score"],
            "classification": classification(score),
            "highlight": score >= 90,
            "highlight_color": "#FFCCCC" if score >= 90 else None,
            "matched_keywords": kw["matched_keywords"],
            "missing_keywords": kw["missing_keywords"],
            "keyword_coverage": kw["keyword_coverage"],
            "matched_skills": llm["matched_skills"],
            "missing_skills": llm["missing_skills"],
            "strengths": llm["strengths"],
            "weaknesses": llm["weaknesses"],
            "tailoring_recommendations": llm["tailoring_recommendations"],
            "summary": llm["summary"]
        }

    def evaluate_batch(self, docs, jd):
        return sorted([self.evaluate(d, jd) for d in docs],
                      key=lambda x: x["ats_score"], reverse=True)
