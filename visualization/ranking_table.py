import pandas as pd

def ranking_to_dataframe(ranked_jobs, top_k=10):
    data = []

    for item in ranked_jobs[:top_k]:
        data.append({
            "Job ID": item["job_id"],
            "Score": round(item["score"], 3)
        })

    return pd.DataFrame(data)
