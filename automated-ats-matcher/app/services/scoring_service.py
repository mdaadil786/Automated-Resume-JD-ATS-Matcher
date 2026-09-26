from app.config import settings

def classification(score):
    if score >= 90:
        return "Top Fit / Highly Recommended"
    if score >= 70:
        return "Moderate Fit"
    return "Low Match / Requires Tailoring"

def hybrid_score(semantic_0_to_1, llm_0_to_100):
    score = semantic_0_to_1 * 100 * settings.SEMANTIC_WEIGHT + llm_0_to_100 * settings.LLM_WEIGHT
    return round(max(0, min(100, score)), 2)
