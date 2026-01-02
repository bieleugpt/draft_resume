
'''
def build_explanation_prompt(scores, cv_structured, job_structured):
    return f"""
You are an AI recruitment assistant.

Matching scores:
- Skills: {scores['skills']:.2f}
- Experience: {scores['experience']:.2f}
- Education: {scores['education']:.2f}
- Total match score: {scores['total']:.2f}

Candidate skills:
{', '.join(cv_structured['skills'])}

Job required skills:
{', '.join(job_structured['skills'])}

Explain in 4-6 bullet points:
- why the match is strong or weak
- what aligns well
- what is missing or could be improved
Use a neutral and professional tone.
"""

'''

















'''

def build_explanation_prompt(scores, cv_structured, job_structured):
    cv_skills = set(
        sum(cv_structured["skills"].values(), [])
    )
    job_skills = set(
        sum(job_structured["skills"].values(), [])
    )

    common = sorted(cv_skills & job_skills)
    missing = sorted(job_skills - cv_skills)

    return f"""
You are an AI recruitment assistant.

Explain the match between a candidate and a job offer.

Matching scores:
{scores}

Strongly matching skills:
{common[:10]}

Missing or weak skills:
{missing[:10]}

Instructions:
- Be concise and professional
- Base your explanation strictly on the information above
- Do not invent information

Provide:
1) Overall assessment (2 sentences)
2) Strengths (bullet points)
3) Gaps (bullet points)
4) One concrete recommendation
"""

'''







def build_explanation_prompt(scores, cv_structured, job_structured):
    """
    Build a safe explanation prompt even if some structured fields are missing.
    """

    # -------- Safe extraction --------
    cv_skills = []
    if "skills" in cv_structured and isinstance(cv_structured["skills"], dict):
        cv_skills = sum(cv_structured["skills"].values(), [])

    job_skills = []
    if "skills" in job_structured and isinstance(job_structured["skills"], dict):
        job_skills = sum(job_structured["skills"].values(), [])

    cv_experience = cv_structured.get("experience", "")
    cv_education = cv_structured.get("education", "")
    cv_text = cv_structured.get("raw_text", "")

    job_text = job_structured.get("raw_text", "")

    # -------- Prompt --------
    prompt = f"""
You are an AI assistant helping explain the match between a candidate and a job offer.

Matching scores:
- Global similarity score: {scores.get("total", 0):.2f}
- Hard skills score: {scores.get("hard_skills", 0):.2f}
- Soft skills score: {scores.get("soft_skills", 0):.2f}

Candidate profile:
- Skills: {", ".join(cv_skills) if cv_skills else "Not explicitly extracted"}
- Experience summary: {cv_experience if cv_experience else "Not explicitly extracted"}
- Education summary: {cv_education if cv_education else "Not explicitly extracted"}

Job offer summary:
- Required skills: {", ".join(job_skills) if job_skills else "Not explicitly extracted"}

Based on the semantic similarity between the candidate profile and the job description,
explain clearly:
1. Why the candidate matches or does not match the job
2. The main strengths of the candidate
3. Possible gaps or areas for improvement
4. A short recommendation for the candidate
"""

    return prompt




