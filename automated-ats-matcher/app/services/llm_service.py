import json
import logging
from openai import OpenAI
from app.config import settings
from app.services.keyword_service import keyword_analysis

logger = logging.getLogger(__name__)

class LLMService:
    def __init__(self):
        self.client = OpenAI(api_key=settings.OPENAI_API_KEY) if settings.OPENAI_API_KEY else None

    def evaluate(self, resume, jd):
        if not self.client:
            return self.fallback(resume, jd)

        system = """
You are an ATS resume evaluator. Compare a candidate resume with a job description.
Return ONLY JSON with:
{
 "llm_score": number,
 "matched_skills": [string],
 "missing_skills": [string],
 "strengths": [string],
 "weaknesses": [string],
 "tailoring_recommendations": [string],
 "summary": string
}
Score 0-100. Do not invent candidate experience.
"""
        try:
            response = self.client.chat.completions.create(
                model=settings.OPENAI_MODEL,
                temperature=0.1,
                response_format={"type": "json_object"},
                messages=[
                    {"role": "system", "content": system},
                    {"role": "user", "content": f"JOB DESCRIPTION:\n{jd}\n\nRESUME:\n{resume}"}
                ])
            data = json.loads(response.choices[0].message.content)
            return self.validate(data)
        except Exception:
            logger.exception("OpenAI evaluation failed; local fallback used.")
            return self.fallback(resume, jd)

    def validate(self, data):
        score = max(0, min(100, float(data.get("llm_score", 0))))
        return {
            "llm_score": round(score,2),
            "matched_skills": list(data.get("matched_skills", [])),
            "missing_skills": list(data.get("missing_skills", [])),
            "strengths": list(data.get("strengths", [])),
            "weaknesses": list(data.get("weaknesses", [])),
            "tailoring_recommendations": list(data.get("tailoring_recommendations", [])),
            "summary": str(data.get("summary", ""))
        }

    def fallback(self, resume, jd):
        a = keyword_analysis(resume, jd)
        score = a["keyword_coverage"]
        missing = a["missing_keywords"]
        return {
            "llm_score": score,
            "matched_skills": a["matched_keywords"][:30],
            "missing_skills": missing[:30],
            "strengths": ["Strong keyword coverage for this job description."]
                         if a["matched_keywords"] else
                         ["Resume text was readable but few exact JD terms were detected."],
            "weaknesses": ["Several job-description terms are absent from the resume."]
                         if missing else ["No exact keyword gaps were detected."],
            "tailoring_recommendations":
                [f"Consider adding truthful evidence for: {', '.join(missing[:10])}."]
                if missing else
                ["Keep your strongest quantified achievements near the top."],
            "summary": "Local fallback evaluation was used because OpenAI was not configured or unavailable."
        }
