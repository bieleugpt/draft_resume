import csv

def load_ground_truth(path="DATA/ground_truth.csv"):
    gt = {}

    with open(path, encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            key = (row["cv_id"], row["job_id"])
            gt[key] = int(row["match"])

    return gt

if __name__ == "__main__":
    gt = load_ground_truth()
    print("Loaded ground truth pairs:", len(gt))
