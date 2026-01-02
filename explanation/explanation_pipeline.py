from explanation.prompt_builder import build_explanation_prompt
from explanation.explainer import generate_explanation

def explain_match(scores, cv_structured, job_structured):
    prompt = build_explanation_prompt(scores, cv_structured, job_structured)
    return generate_explanation(prompt)
