from app.services.keyword_service import keyword_analysis

def test_keyword_analysis():
    x = keyword_analysis("Python SQL Docker developer",
                         "Python SQL Docker Kubernetes developer")
    assert "python" in x["matched_keywords"]
    assert "kubernetes" in x["missing_keywords"]
    assert x["keyword_coverage"] > 0
