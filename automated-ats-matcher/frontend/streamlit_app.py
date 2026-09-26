import json
import requests
import pandas as pd
import streamlit as st
from app.config import settings

API = f"http://127.0.0.1:{settings.FLASK_PORT}/api"

st.set_page_config(page_title="ATS Matcher", page_icon="🎯", layout="wide")
st.markdown("""
<style>
.title{font-size:2.4rem;font-weight:800}
.subtitle{color:#6b7280}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="title">🎯 Automated Resume-JD ATS Matcher</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Hybrid semantic + LLM candidate matching platform</div>',
            unsafe_allow_html=True)

with st.sidebar:
    st.header("Navigation")
    mode = st.radio("Matching mode", ["1 Resume vs 1 JD", "Multiple Resumes vs 1 JD"])
    st.divider()
    try:
        r = requests.get(f"{API}/health", timeout=3)
        st.success("Flask API connected" if r.ok else "API unavailable")
    except requests.RequestException:
        st.error("Start backend: python run_backend.py")
    st.caption(">=90% is highlighted with #FFCCCC.")

jd = st.text_area("Job Description", height=260,
                  placeholder="Paste the complete job description...")

if mode == "1 Resume vs 1 JD":
    uploaded = st.file_uploader("Upload one resume", type=["pdf","docx","txt"])
    if st.button("Evaluate Candidate", type="primary", use_container_width=True):
        if not uploaded or not jd.strip():
            st.warning("Upload a resume and enter a job description.")
        else:
            with st.spinner("Parsing, embedding and evaluating..."):
                try:
                    r = requests.post(
                        f"{API}/evaluate_single",
                        files={"resume": (uploaded.name, uploaded.getvalue(),
                                          uploaded.type or "application/octet-stream")},
                        data={"job_description": jd}, timeout=300)
                    r.raise_for_status()
                    x = r.json()
                    a,b,c = st.columns(3)
                    a.metric("ATS Score", f"{x['ats_score']:.2f}%")
                    b.metric("Semantic", f"{x['semantic_similarity']:.2f}%")
                    c.metric("LLM", f"{x['llm_score']:.2f}%")
                    st.subheader(x["classification"])
                    st.write(x["summary"])

                    left,right = st.columns(2)
                    with left:
                        st.markdown("### Matched Skills")
                        st.write(", ".join(x["matched_skills"]) or "None")
                        st.markdown("### Strengths")
                        for item in x["strengths"]: st.write("• " + item)
                    with right:
                        st.markdown("### Missing Skills")
                        st.write(", ".join(x["missing_skills"]) or "None")
                        st.markdown("### Weaknesses")
                        for item in x["weaknesses"]: st.write("• " + item)

                    st.markdown("### Keyword Analysis")
                    st.write(f"Coverage: **{x['keyword_coverage']:.2f}%**")
                    st.write("Matched: " + (", ".join(x["matched_keywords"]) or "None"))
                    st.write("Missing: " + (", ".join(x["missing_keywords"]) or "None"))

                    st.markdown("### Tailored Resume Recommendations")
                    for item in x["tailoring_recommendations"]: st.write("• " + item)

                    st.download_button("Download JSON Report",
                        data=json.dumps(x, indent=2),
                        file_name="candidate_ats_report.json", mime="application/json")
                except Exception as e:
                    st.error(f"Evaluation failed: {e}")
else:
    uploaded = st.file_uploader("Upload multiple resumes or ZIP",
                                type=["pdf","docx","txt","zip"], accept_multiple_files=True)
    if st.button("Rank Candidates", type="primary", use_container_width=True):
        if not uploaded or not jd.strip():
            st.warning("Upload resumes/ZIP and enter a job description.")
        else:
            with st.spinner("Parsing and ranking candidates..."):
                try:
                    files = [("resumes", (u.name, u.getvalue(),
                              u.type or "application/octet-stream")) for u in uploaded]
                    r = requests.post(f"{API}/evaluate_batch", files=files,
                                       data={"job_description": jd}, timeout=600)
                    r.raise_for_status()
                    payload = r.json()
                    results = payload["results"]
                    rows = [{
                        "Candidate": x["candidate"], "ATS Score": x["ats_score"],
                        "Classification": x["classification"],
                        "Semantic": x["semantic_similarity"],
                        "LLM": x["llm_score"],
                        "Keyword Coverage": x["keyword_coverage"]
                    } for x in results]
                    df = pd.DataFrame(rows)

                    def highlight(row):
                        return (["background-color: #FFCCCC"] * len(row)
                                if float(row["ATS Score"]) >= 90
                                else [""] * len(row))
                    st.success(f"Evaluated {len(results)} candidates")
                    st.dataframe(df.style.apply(highlight, axis=1),
                                 use_container_width=True, hide_index=True)

                    st.markdown("### Candidate Reports")
                    for x in results:
                        with st.expander(f"{x['candidate']} — {x['ats_score']:.2f}% — {x['classification']}"):
                            st.write(x["summary"])
                            st.write("**Matched:** " + (", ".join(x["matched_skills"]) or "None"))
                            st.write("**Missing:** " + (", ".join(x["missing_skills"]) or "None"))
                            for item in x["tailoring_recommendations"]:
                                st.write("• " + item)

                    st.download_button("Download Batch CSV", payload["csv"],
                                       "ats_candidate_ranking.csv", "text/csv")
                    st.download_button("Download Batch JSON",
                                       json.dumps(results, indent=2),
                                       "ats_candidate_reports.json", "application/json")
                except Exception as e:
                    st.error(f"Batch evaluation failed: {e}")

st.divider()
st.caption("Flask + Streamlit + ChromaDB + Sentence Transformers + OpenAI")
