
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

