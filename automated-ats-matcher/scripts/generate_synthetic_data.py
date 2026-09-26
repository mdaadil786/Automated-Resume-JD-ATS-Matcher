import argparse, random, os, json
from pathlib import Path
from faker import Faker

try:
    from openai import OpenAI
except ImportError:
    OpenAI = None

fake = Faker()
Faker.seed(42)
random.seed(42)

ROOT = Path(__file__).resolve().parents[1]
RES = ROOT / "data" / "resumes"
JDS = ROOT / "data" / "jds"

ROLES = [
("Software Engineer", ["java","spring boot","rest","sql","git","docker"]),
("Python Developer", ["python","flask","fastapi","pandas","sql","docker"]),
("Data Analyst", ["python","sql","pandas","numpy","power bi","excel"]),
("Cloud Engineer", ["aws","ec2","s3","iam","docker","terraform"]),
("QA Engineer", ["selenium","pytest","api","sql","git","jenkins"]),
("ML Engineer", ["python","machine learning","pandas","numpy","pytorch"]),
("Backend Developer", ["java","spring boot","postgresql","redis","kafka"]),
("Frontend Developer", ["javascript","typescript","react","html","css","git"]),
("DevOps Engineer", ["linux","docker","kubernetes","jenkins","aws","terraform"]),
("Cybersecurity Analyst", ["linux","python","siem","networking","sql","git"]),
]

def resume(role, skills):
    s = skills[:]
    random.shuffle(s)
    present = s[:random.randint(3,len(s))]
    return f"""{fake.name()}
{role}
{fake.email()} | {fake.city()}

SUMMARY
Entry-level {role.lower()} with practical project experience and problem-solving skills.
Experienced with {", ".join(present)}.

SKILLS
{", ".join(present)}

EXPERIENCE
Software Engineering Intern | Example Technologies | 2025-2026
- Built and tested application components using {present[0]}.
- Collaborated with engineers and documented technical changes.
- Debugged issues and participated in code reviews.

PROJECTS
- Developed a portfolio project using {present[0]} and {present[1] if len(present)>1 else present[0]}.
- Implemented APIs, testing and data persistence where applicable.

EDUCATION
B.Tech / B.E. in Engineering
2026
"""

def jd(role, skills):
    return f"""JOB TITLE: {role}

ABOUT THE ROLE
We are looking for a {role} to build reliable and maintainable solutions.

RESPONSIBILITIES
- Design, implement, test and maintain software.
- Collaborate with engineers and stakeholders.
- Debug issues and improve reliability.
- Participate in documentation and code reviews.

REQUIRED SKILLS
{", ".join(skills)}

PREFERRED
Strong problem-solving, communication and ability to learn new technologies.

EDUCATION
Bachelor's degree in Computer Science, Engineering or related discipline.
"""

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--resumes", type=int, default=24)
    p.add_argument("--jds", type=int, default=6)
    p.add_argument("--use-llm", action="store_true", help="Use OpenAI to enrich generated text")
    args=p.parse_args()
    RES.mkdir(parents=True,exist_ok=True); JDS.mkdir(parents=True,exist_ok=True)
    for f in RES.glob("*.txt"): f.unlink()
    for f in JDS.glob("*.txt"): f.unlink()
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY")) if args.use_llm and OpenAI and os.getenv("OPENAI_API_KEY") else None
    for i in range(args.resumes):
        role,skills=ROLES[i%len(ROLES)]
        text = resume(role,skills)
        if client:
            try:
                r = client.chat.completions.create(model=os.getenv("OPENAI_MODEL","gpt-4o-mini"), temperature=0.4, messages=[{"role":"system","content":"Create concise synthetic resume variations. Never use real people, employers or contact details."},{"role":"user","content":f"Rewrite this synthetic resume for a {role}. Preserve these skills: {skills}. Keep it clearly synthetic and fictional.\n\n{text}"}])
                text = r.choices[0].message.content or text
            except Exception:
                pass
        (RES/f"resume_{i+1:02d}.txt").write_text(text,encoding="utf-8")
    for i in range(args.jds):
        role,skills=ROLES[i%len(ROLES)]
        (JDS/f"jd_{i+1:02d}_{role.lower().replace(' ','_')}.txt").write_text(
            jd(role,skills),encoding="utf-8")
    print(f"Generated {args.resumes} resumes and {args.jds} JDs.")

if __name__=="__main__":
    main()
