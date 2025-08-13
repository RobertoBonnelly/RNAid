import csv
import math
import pandas as pd

def cosine_similarity(v1, v2):
    sumxx = sum(x*x for x in v1)
    sumyy = sum(y*y for y in v2)
    sumxy = sum(x*y for x, y in zip(v1, v2))
    return sumxy / math.sqrt(sumxx * sumyy)

def main():
    df = pd.read_csv("rfam_vectors.csv")
    names = df["seq_name"].tolist()
    vectors = df.drop(columns=["seq_name"]).values.tolist()

    with open("rfam_cosine_pairs.csv", mode="w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["seq1", "seq2", "similarity"])

        for i in range(len(names)):
            for j in range(i, len(names)):  # upper triangle only
                sim = cosine_similarity(vectors[i], vectors[j])
                writer.writerow([names[i], names[j], sim])
                del sim  # optional, not really needed here

if __name__ == "__main__":
    main()