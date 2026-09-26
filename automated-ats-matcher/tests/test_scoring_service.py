from app.services.scoring_service import classification, hybrid_score

def test_boundaries():
    assert classification(90) == "Top Fit / Highly Recommended"
    assert classification(70) == "Moderate Fit"
    assert classification(69.99) == "Low Match / Requires Tailoring"

def test_range():
    x = hybrid_score(1.0, 100)
    assert 0 <= x <= 100
