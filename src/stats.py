# compare_medians_mannwhitney.py
import pandas as pd
import numpy as np
from scipy.stats import mannwhitneyu
import matplotlib.pyplot as plt
import seaborn as sns
#import csv

def load_and_group_medians(pairwise_csv_path):
    """
    Load a pairwise similarity CSV with columns: seq1, seq2, similarity
    Group by seq1 and return a DataFrame with columns: seq1, median_similarity
    """
    df = pd.read_csv(pairwise_csv_path)
    # Basic validation
    if not {"seq1", "seq2", "similarity"}.issubset(df.columns):
        raise ValueError(f"{pairwise_csv_path} must contain columns: seq1, seq2, similarity")

    med_df = df.groupby("seq1", as_index=False)["similarity"].median()
    med_df = med_df.rename(columns={"similarity": "median_similarity"})
    return med_df

def mann_whitney_test_and_effect(wf_medians, af_medians, alternative="two-sided"):
    """
    Run Mann-Whitney U test and compute rank-biserial effect size.
    - wf_medians: 1D array-like (within-family medians)
    - af_medians: 1D array-like (across-family medians)
    - alternative: "two-sided", "greater" (WF > AF) or "less" (WF < AF)
    Returns (U_stat, pvalue, rank_biserial)
    """
    wf = np.asarray(wf_medians, dtype=float)
    af = np.asarray(af_medians, dtype=float)
    if wf.size < 1 or af.size < 1:
        raise ValueError("Both groups must contain at least one value.")

    # SciPy returns U for wf relative to af
    U, p = mannwhitneyu(wf, af, alternative=alternative)
    n1 = wf.size
    n2 = af.size

    # Rank-biserial effect size: (2U)/(n1*n2) - 1
    # This maps to [-1, 1]; positive means wf tends to have larger values than af.
    rank_biserial = (2.0 * U) / (n1 * n2) - 1.0

    return U, p, rank_biserial

def save_medians_to_csv(df_medians, outpath):
    """Save medians DataFrame (seq1, median_similarity) to CSV."""
    df_medians.to_csv(outpath, index=False)

def plot_distributions(wf_medians, af_medians, wf_label="Within-family", af_label="Across-family",
                       hist_out="median_histogram.png", box_out="median_boxplot.png"):
    """Plot histogram and boxplot for two distributions of medians."""
    wf = np.asarray(wf_medians, dtype=float)
    af = np.asarray(af_medians, dtype=float)

    # Combined histogram
    plt.figure(figsize=(8, 5))
    sns.histplot(af, label=af_label, kde=True, stat="density", color="tab:blue", alpha=0.5)
    sns.histplot(wf, label=wf_label, kde=True, stat="density", color="tab:orange", alpha=0.5)
    plt.legend()
    plt.xlabel("Median similarity")
    plt.ylabel("Density")
    plt.title("Distribution of per-sequence median similarities")
    plt.tight_layout()
    plt.savefig(hist_out, dpi=150)
    plt.close()

    # Boxplot side-by-side
    plt.figure(figsize=(6, 5))
    data = [af, wf]
    sns.boxplot(data=data)
    plt.xticks([0, 1], [af_label, wf_label])
    plt.ylabel("Median similarity")
    plt.title("Comparison of medians")
    plt.tight_layout()
    plt.savefig(box_out, dpi=150)
    plt.close()

def main():
    # Paths — change if your filenames differ
    af_pairs_csv = "rfam_cosine_pairs.csv"      # across-family pairwise similarities
    wf_pairs_csv = "sample_cosine_pairs.csv"   # within-family pairwise similarities

    # 1) Load and compute per-sequence medians
    print("Loading and grouping medians ...")
    af_medians_df = load_and_group_medians(af_pairs_csv)   # columns: seq1, median_similarity
    wf_medians_df = load_and_group_medians(wf_pairs_csv)

    # Save medians for inspection
    save_medians_to_csv(af_medians_df, "af_per_sequence_medians.csv")
    save_medians_to_csv(wf_medians_df, "wf_per_sequence_medians.csv")

    # 2) Prepare arrays
    af_medians = af_medians_df["median_similarity"].values
    wf_medians = wf_medians_df["median_similarity"].values

    print(f"AF (across) sequences: {len(af_medians)} medians")
    print(f"WF (within) sequences: {len(wf_medians)} medians")

    # 3) Mann-Whitney U test (two-sided by default)
    # If you have a directional hypothesis (WF > AF), set alternative="greater"
    print("Running Mann-Whitney U test (two-sided)...")
    U, p, rank_biserial = mann_whitney_test_and_effect(wf_medians, af_medians, alternative="two-sided")

    # 4) Report
    print(f"Mann-Whitney U (wf vs af) = {U:.3f}")
    print(f"p-value = {p:.3e}")
    print(f"Rank-biserial effect size = {rank_biserial:.3f}   (range -1..1; positive => WF > AF)")

    # 5) Plots
    print("Plotting distributions ...")
    plot_distributions(wf_medians, af_medians)

    print("Done. Medians saved: af_per_sequence_medians.csv , wf_per_sequence_medians.csv")
    print("Plots saved: median_histogram.png, median_boxplot.png")

if __name__ == "__main__":
    main()
