import io
import json
import pandas as pd

def results_to_csv(results):
    columns = ["candidate","ats_score","semantic_similarity","llm_score",
               "classification","keyword_coverage","matched_keywords",
               "missing_keywords","matched_skills","missing_skills"]
    rows = []
    for r in results:
        row = {}
        for c in columns:
            v = r.get(c, "")
            row[c] = ", ".join(v) if isinstance(v, list) else v
        rows.append(row)
    out = io.StringIO()
    pd.DataFrame(rows, columns=columns).to_csv(out, index=False)
    return out.getvalue()

def result_to_json(result):
    return json.dumps(result, indent=2, ensure_ascii=False)
