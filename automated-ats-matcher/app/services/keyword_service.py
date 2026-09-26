import re

STOPWORDS = {
    "and","the","for","with","from","this","that","are","you","your","our",
    "their","have","has","will","into","using","use","years","year","role",
    "work","team","job","description","required","preferred","experience",
    "skills","ability","strong","good","software","developer"
}

def normalize(text):
    return re.sub(r"[^a-z0-9+#.\- ]+", " ", text.lower())

def terms(text):
    return {w for w in normalize(text).split()
            if len(w) >= 3 and w not in STOPWORDS}

def extract_keywords(jd):
    raw = normalize(jd)
    phrases = re.findall(
        r"\b(?:python|java|c\+\+|javascript|typescript|sql|mysql|postgresql|"
        r"mongodb|aws|azure|gcp|docker|kubernetes|kafka|spring boot|flask|"
        r"django|react|node\.js|git|linux|rest|api|machine learning|deep learning|"
        r"nlp|pandas|numpy|scikit-learn|tensorflow|pytorch|fastapi|redis|"
        r"terraform|ci/cd|jenkins|selenium|pytest)\b", raw)
    return sorted(terms(jd) | set(phrases))

def keyword_analysis(resume, jd):
    r, required = terms(resume), set(extract_keywords(jd))
    matched = sorted(x for x in required if x in r)
    missing = sorted(x for x in required if x not in r)
    coverage = len(matched) / len(required) if required else 0
    return {"matched_keywords": matched, "missing_keywords": missing,
            "keyword_coverage": round(coverage * 100, 2)}
