import pandas as pd
import numpy as np
import argparse

def benjamini_hochberg(pvals):
    """Return BH-adjusted p-values (FDR)."""
    pvals = np.asarray(pvals)
    n = len(pvals)
    order = np.argsort(pvals)
    ranked = pvals[order]
    adj = ranked * n / (np.arange(1, n+1))
    # Ensure monotonicity
    adj = np.minimum.accumulate(adj[::-1])[::-1]
    adj = np.clip(adj, 0, 1)
    out = np.empty_like(adj)
    out[order] = adj
    return out

def main():
    parser = argparse.ArgumentParser(description="Apply Benjamini-Hochberg FDR correction to MWU and Levene p-values.")
    parser.add_argument("--input", help="CSV file with columns 'p_value' and 'variance_test_p'")
    parser.add_argument("--out", default="results_with_fdr.csv", help="Name of output CSV file (default: results_with_fdr.csv)")
    args = parser.parse_args()

    # Load CSV
    df = pd.read_csv(args.input)

    # Check required columns
    for col in ["p_value", "variance_test_p"]:
        if col not in df.columns:
            raise ValueError(f"Input CSV must contain '{col}' column")

    # Apply BH FDR to both sets of p-values
    df["p_value_fdr"] = benjamini_hochberg(df["p_value"].values)
    df["variance_test_p_fdr"] = benjamini_hochberg(df["variance_test_p"].values)

    # Add boolean flags for quick filtering
    df["p_value_significant"] = df["p_value_fdr"] < 0.05
    df["variance_significant"] = df["variance_test_p_fdr"] < 0.05

    # Save
    df.to_csv(args.out, index=False)
    print(f"Corrected results written to {args.out}")

    # Print summary
    print("\nSummary:")
    print(df[["family","p_value","p_value_fdr","p_value_significant",
              "variance_test_p","variance_test_p_fdr","variance_significant"]])

if __name__ == "__main__":
    main()
