'''
def fuse_scores(structured_scores, fulltext_scores, alpha=0.4):
    fused = {}

    keys = set(structured_scores) | set(fulltext_scores)

    for k in keys:
        s = structured_scores.get(k, 0)
        f = fulltext_scores.get(k, 0)
        fused[k] = alpha * s + (1 - alpha) * f

    return fused
'''

def fuse_scores(structured_scores, fulltext_scores, alpha=0.4):
    fused = {}

    for k in structured_scores:
        if k in fulltext_scores:
            fused[k] = alpha * structured_scores[k] + (1 - alpha) * fulltext_scores[k]
        else:
            fused[k] = structured_scores[k]  # IMPORTANT

    return fused
