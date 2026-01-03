import matplotlib.pyplot as plt


def plot_strengths(scores_mean):
    categories = {
        "Hard skills": scores_mean.get("hard_skills", 0),
        "Soft skills": scores_mean.get("soft_skills", 0),
        "Domain knowledge": scores_mean.get("domain_knowledge", 0),
        "Tools / Tech": scores_mean.get("tools_technologies", 0),
        "Experience": scores_mean.get("experience", 0),
        "Education": scores_mean.get("education", 0),
    }

    strength = medium = weakness = 0

    for score in categories.values():
        if score >= 0.6:
            strength += 1
        elif score >= 0.4:
            medium += 1
        else:
            weakness += 1

    labels = ["Forces", "Adéquation moyenne", "Faiblesses"]
    values = [strength, medium, weakness]
    colors = ["#2ecc71", "#f1c40f", "#e74c3c"]

    fig, ax = plt.subplots(figsize=(5, 5))
    ax.pie(
        values,
        labels=labels,
        autopct="%1.0f%%",
        startangle=90,
        colors=colors
    )
    ax.set_title("Analyse Forces / Faiblesses du CV")
    ax.axis("equal")

    return fig
