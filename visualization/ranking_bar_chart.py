import matplotlib.pyplot as plt

def plot_ranking_bar_chart(ranked_jobs, top_k=10):
    jobs = [item["job_id"] for item in ranked_jobs[:top_k]]
    scores = [item["score"] for item in ranked_jobs[:top_k]]

    #plt.figure(figsize=(10, 6))

    plt.figure()
    plt.barh(jobs, scores)
    plt.xlabel("Matching Score")
    plt.ylabel("Job ID")
    plt.title("Top Job Matches")
    plt.gca().invert_yaxis()
    plt.tight_layout()
    plt.show()
