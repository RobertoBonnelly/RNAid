# compare_medians_mannwhitney.py
import pandas as pd
import numpy as np
from scipy.stats import mannwhitneyu, levene
import matplotlib.pyplot as plt
import seaborn as sns
import os
import argparse

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

def bootstrap_rankbiserial_ci(wf, af, n_boot=20000, seed=0):
    """Bootstrap 95% CI for rank-biserial effect size."""
    rng = np.random.default_rng(seed)
    n1, n2 = len(wf), len(af)
    stats = np.empty(n_boot)
    for i in range(n_boot):
        wf_sample = rng.choice(wf, n1, replace=True)
        af_sample = rng.choice(af, n2, replace=True)
        U, _, rb = mann_whitney_test_and_effect(wf_sample, af_sample)
        stats[i] = rb
    lo, hi = np.percentile(stats, [2.5, 97.5])
    return lo, hi

def save_medians_to_csv(df_medians, outpath):
    """Save medians DataFrame (seq1, median_similarity) to CSV."""
    df_medians.to_csv(outpath, index=False)

def describe_distribution(arr, label):
    """Return quantiles and spread statistics for one group."""
    arr = np.asarray(arr, dtype=float)
    desc = {
        f"{label}_n": len(arr),
        f"{label}_mean": np.mean(arr),
        f"{label}_std": np.std(arr, ddof=1),
        f"{label}_iqr": np.percentile(arr, 75) - np.percentile(arr, 25),
        f"{label}_min": np.min(arr),
        f"{label}_q10": np.percentile(arr, 10),
        f"{label}_median": np.median(arr),
        f"{label}_q90": np.percentile(arr, 90),
        f"{label}_max": np.max(arr),
    }
    return desc

def append_results(csv_path, family, pval, rb, ci_low, ci_high, wf, af):
    """Append results to CSV, add header if file does not exist."""
    wf_stats = describe_distribution(wf, "WF")
    af_stats = describe_distribution(af, "AF")

    # Levene's test
    stat, p_var = levene(wf, af)
    wf_var = np.var(wf, ddof=1)
    af_var = np.var(af, ddof=1)
    if wf_var > af_var:
        larger_var_group = "WF"
    elif af_var > wf_var:
        larger_var_group = "AF"
    else:
        larger_var_group = "equal"    
    row = {
        "family": family,
        "p_value": pval,
        "rank_biserial": rb,
        "ci_low": ci_low,
        "ci_high": ci_high,
        "variance_test_p": p_var,
        "larger_var_group": larger_var_group,
    }
    row.update(wf_stats)
    row.update(af_stats)

    df_row = pd.DataFrame([row])
    if not os.path.exists(csv_path):
        df_row.to_csv(csv_path, index=False)
    else:
        df_row.to_csv(csv_path, mode="a", header=False, index=False)

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
    parser = argparse.ArgumentParser(description="Run Mann-Whitney U test on family vs across-family medians.")
    parser.add_argument("--af", required=True, help="CSV file with across-family pairwise similarities")
    parser.add_argument("--wf", required=True, help="CSV file with within-family pairwise similarities")
    parser.add_argument("--family", required=True, help="Family name")
    parser.add_argument("--out", default="pvalues.csv", help="Output CSV to store p-values and CIs")
    args = parser.parse_args()
    # Paths for af and wf
    af_pairs_csv = args.af      # across-family pairwise similarities
    wf_pairs_csv = args.wf   # within-family pairwise similarities

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

    # 4) Bootstrap CI
    ci_low, ci_high = bootstrap_rankbiserial_ci(wf=wf_medians, af=af_medians)
    print(f"95% CI for rank-biserial: [{ci_low:.3f}, {ci_high:.3f}]")

    # 5) Variability and Quantiles
    wf_desc = describe_distribution(wf_medians, "WF")
    af_desc = describe_distribution(af_medians, "AF")
    print("\nWF summary", wf_desc)
    print("AF summary:", af_desc)

    # 5) Report
    print(f"Mann-Whitney U (wf vs af) = {U:.3f}")
    print(f"p-value = {p:.3e}")
    print(f"Rank-biserial effect size = {rank_biserial:.3f}   (range -1..1; positive => WF > AF)")

    # 6) Plots
    print("Plotting distributions ...")
    plot_distributions(wf_medians, af_medians)

    print("Done. Medians saved: af_per_sequence_medians.csv , wf_per_sequence_medians.csv")
    print("Plots saved: median_histogram.png, median_boxplot.png")

    # 7) Append results
    append_results(args.out, args.family, p, rank_biserial, ci_low, ci_high, wf=wf_medians, af=af_medians)
    print(f"Results writen to {args.out}")

if __name__ == "__main__":
    main()
