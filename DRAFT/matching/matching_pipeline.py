# matching/matching_pipeline.py

from typing import Dict
import numpy as np
from matching.scorer import compute_score


def fuse_scores(
    scores_rules: Dict[str, float],
    scores_llm: Dict[str, float],
    alpha: float = 0.4,
) -> Dict[str, float]:
    """
    Fusion pondérée des scores rule-based et LLM-based
    alpha = poids des règles
    """

    fused = {}
    keys = set(scores_rules.keys()) | set(scores_llm.keys())

    for key in keys:
        if key == "total":
            continue

        v_rules = scores_rules.get(key)
        v_llm = scores_llm.get(key)

        if v_rules is not None and v_llm is not None:
            fused[key] = alpha * v_rules + (1 - alpha) * v_llm
        elif v_rules is not None:
            fused[key] = v_rules
        elif v_llm is not None:
            fused[key] = v_llm

    if fused:
        fused["total"] = float(np.mean(list(fused.values())))
    else:
        fused["total"] = 0.0

    return fused
