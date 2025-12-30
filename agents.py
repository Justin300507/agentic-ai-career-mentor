# agents.py

try:
    from openai import OpenAI
    OPENAI_AVAILABLE = True
except:
    OPENAI_AVAILABLE = False


# ===============================
# CONFIG
# ===============================
USE_LLM = True  # set False if no API key

API_KEY = "YOUR_API_KEY_HERE"  # <-- replace OR set USE_LLM=False


if OPENAI_AVAILABLE and USE_LLM and API_KEY != "YOUR_API_KEY_HERE":
    client = OpenAI(api_key=API_KEY)
else:
    client = None
    USE_LLM = False


# ===============================
# Resume Analyzer Agent
# ===============================
def resume_analyzer(resume_text):
    """
    Tries LLM-based semantic extraction.
    Falls back to rule-based extraction if LLM fails.
    """

    # -------- LLM PATH --------
    if USE_LLM and client:
        try:
            prompt = f"""
You are an expert career AI.

Infer skills even if indirect.
Map concepts:
- scripting languages -> Python
- servers / operating systems -> Linux
- packet analysis / troubleshooting -> Networking
- defensive security / blue team -> Cybersecurity

Return ONLY a valid Python dictionary with keys:
skills (list), interest (string), education (string), experience (string).

Resume:
{resume_text}
"""

            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}]
            )

            raw = response.choices[0].message.content
            print("\n=== RAW LLM OUTPUT ===")
            print(raw)
            print("======================\n")

            return eval(raw)

        except Exception as e:
            print("⚠️ LLM FAILED, FALLING BACK")
            print(e)

    # -------- FALLBACK PATH --------
    text = resume_text.lower()

    skills = []
    if "python" in text or "scripting" in text:
        skills.append("Python")
    if "linux" in text or "server" in text or "operating system" in text:
        skills.append("Linux")
    if "network" in text or "packet" in text:
        skills.append("Networking")

    interest = "Cybersecurity" if "security" in text else "General IT"

    return {
        "skills": skills,
        "interest": interest,
        "education": "Unknown",
        "experience": "Beginner"
    }


# ===============================
# Career Decision Agent
# ===============================
def career_decision_agent(profile):
    ROLES = {
        "Cybersecurity Analyst": ["Python", "Linux", "Networking"],
        "Data Analyst": ["Python", "SQL"],
        "Web Developer": ["HTML", "JavaScript"]
    }

    user_skills = set(profile.get("skills", []))
    scores = {}

    for role, skills in ROLES.items():
        if len(skills) == 0:
            scores[role] = 0
        else:
            scores[role] = round(
                (len(user_skills.intersection(skills)) / len(skills)) * 100, 2
            )

    best_role = max(scores, key=scores.get)
    missing_skills = list(set(ROLES[best_role]) - user_skills)

    return best_role, scores, missing_skills


# ===============================
# Readiness Score Agent
# ===============================
def career_readiness_score(scores, role):
    return scores.get(role, 0)


# ===============================
# Roadmap Planner Agent
# ===============================
def roadmap_planner(role, missing_skills):
    roadmap = f"📌 Career Roadmap: {role}\n\n"

    if missing_skills:
        for i, skill in enumerate(missing_skills, start=1):
            roadmap += f"Week {i}: Learn {skill}\n"
        roadmap += f"Week {len(missing_skills)+1}: Build a project\n"
    else:
        roadmap += "Week 1: Advanced tools & techniques\n"
        roadmap += "Week 2: Build an advanced project\n"

    roadmap += """
Week 4: Resume & LinkedIn optimization
Week 5: Mock interviews
Week 6: Apply for roles
"""

    return roadmap


# ===============================
# Feedback Learning Agent
# ===============================
def feedback_agent(feedback, roadmap):
    if feedback == "Rejected":
        return roadmap + """
🔁 Strategy Update:
- Improve resume keywords
- Add another project
"""

    if feedback == "Interview":
        return roadmap + """
🔁 Strategy Update:
- Focus on interview prep
- Revise fundamentals
"""

    return roadmap

