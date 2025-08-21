import argparse
import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.cluster.hierarchy import linkage, dendrogram, fcluster
from scipy.spatial.distance import squareform
from sklearn.metrics import adjusted_rand_score, homogeneity_score, completeness_score, v_measure_score, silhouette_score
from sklearn.metrics.pairwise import cosine_similarity

def load_family_vectors(arg, id_col):
    """
    arg format: 'FamilyName=path.csv'
    CSV must contain id_col and numeric descriptor columns.
    """
    if "=" not in arg:
        raise ValueError(f"--family expects 'Name=path.csv', got: {arg}")
    family, path = arg.split("=", 1)
    df = pd.read_csv(path)
    if id_col not in df.columns:
        raise ValueError(f"{path} must contain id_col '{id_col}'")
    # Keep numeric descriptor columns
    desc_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    if len(desc_cols) == 0:
        raise ValueError(f"{path} has no numeric descriptor columns.")
    # Drop duplicate ids if any
    df = df.drop_duplicates(subset=[id_col]).reset_index(drop=True)
    df["family"] = family
    df["seq_name"] = df[id_col].astype(str)
    return df, desc_cols

def balanced_sample(df, per_family, seed=0):
    if per_family is None or per_family < 0:
        return df
    rng = np.random.default_rng(seed)
    out = []
    for fam, g in df.groupby("family", sort=True):
        if len(g) <= per_family:
            out.append(g)
        else:
            out.append(g.sample(n=per_family, random_state=int(rng.integers(0, 1_000_000))))
    return pd.concat(out, ignore_index=True)

def build_similarity(df, feature_cols, label_fmt="{family}|{seq_name}"):
    labels = [label_fmt.format(**row) for _, row in df[["family","seq_name"]].iterrows()]
    X = df[feature_cols].to_numpy(dtype=float)
    # cosine similarity (rows normalized internally)
    S = cosine_similarity(X)
    # enforce symmetry and diagonals
    S = np.clip((S + S.T) / 2.0, -1.0, 1.0)
    np.fill_diagonal(S, 1.0)
    return labels, S

def plot_dendrogram(Z, labels, out_png):
    plt.figure(figsize=(12, 6))
    dendrogram(Z, labels=labels, leaf_rotation=90, leaf_font_size=7, color_threshold=None)
    plt.title("Hierarchical clustering (cosine distance)")
    plt.tight_layout()
    plt.savefig(out_png, dpi=300)
    plt.close()

def plot_heatmap(S, labels, families, out_png):
    # Order by family to show block structure
    order = np.argsort(families)
    S_ord = S[np.ix_(order, order)]
    labels_ord = [labels[i] for i in order]
    plt.figure(figsize=(8, 7))
    plt.imshow(S_ord, aspect='auto', interpolation='nearest')
    plt.xticks(range(len(labels_ord)), labels_ord, rotation=90, fontsize=6)
    plt.yticks(range(len(labels_ord)), labels_ord, fontsize=6)
    plt.title("Cosine similarity heatmap (ordered by family)")
    plt.colorbar(fraction=0.046, pad=0.04)
    plt.tight_layout()
    plt.savefig(out_png, dpi=300)
    plt.close()

def compute_purity(clusters, families):
    # majority vote per cluster
    df = pd.DataFrame({"cluster": clusters, "family": families})
    correct = 0
    for c, g in df.groupby("cluster"):
        mode_count = g["family"].value_counts().iloc[0]
        correct += mode_count
    return correct / len(df)

def run(args):
    # Load and combine
    all_dfs = []
    feature_cols_ref = None
    for famarg in args.family:
        df, feat_cols = load_family_vectors(famarg, args.id_col)
        if feature_cols_ref is None:
            feature_cols_ref = feat_cols
        # else:
        #     # keep common numeric columns across families
        #     feature_cols_ref = [c for c in feature_cols_ref if c in feat_cols]
        all_dfs.append(df)

    # if not feature_cols_ref:
    #     raise ValueError("No common numeric descriptor columns across families.")
    df_all = pd.concat(all_dfs, ignore_index=True)

    # Balanced sample
    df_sample = balanced_sample(df_all, args.per_family, seed=args.seed)

    # Build labels and similarity
    labels, S = build_similarity(df_sample, feature_cols_ref)
    families = df_sample["family"].tolist()
    # Get number of families for clusters
    k = len(sorted(set(families)))

    # Save combined families vectors, labels, similarity matrix
    out_pref = args.out_prefix
    df_sample_out = df_sample[["family","seq_name"] + feature_cols_ref].copy()
    df_sample_out.to_csv(f"{out_pref}_vectors_combined.csv", index=False)

    pd.DataFrame({"label": labels, "family": families}).to_csv(f"{out_pref}_labels.csv", index=False)
    sim_df = pd.DataFrame(S, index=labels, columns=labels)
    sim_df.to_csv(f"{out_pref}_similarity_matrix.csv")

    # Distance matrix for clustering
    D = 1.0 - S
    condensed = squareform(D, checks=False)

    # Linkage
    Z = linkage(condensed, method=args.linkage)

    # Dendrogram & heatmap
    plot_dendrogram(Z, labels, f"{out_pref}_dendrogram.png")
    plot_heatmap(S, labels, np.array(families), f"{out_pref}_heatmap.png")

    # Cut into k families
    clusters = fcluster(Z, k, criterion="maxclust")

    # Metrics
    # Similarity between clusters
    ari = adjusted_rand_score(families, clusters)
    # Homogeneity within clusters
    hom = homogeneity_score(families, clusters)
    # How many samples of the same cluster were assigned together
    com = completeness_score(families, clusters)
    # Average of completeness and homogeneity to punish extreme values.
    vms = v_measure_score(families, clusters)
    # Percentage of correctly clustered sequences
    purity = compute_purity(clusters, families)

    # Silhouette on distance matrix (requires >1 cluster and at least some spread)
    sil = None
    try:
        if len(set(clusters)) > 1:
            sil = float(silhouette_score(D, clusters, metric="precomputed"))
    except Exception:
        sil = None

    # Save clusters and report
    pd.DataFrame({"label": labels, "family": families, "cluster": clusters}).to_csv(f"{out_pref}_clusters.csv", index=False)
    report = {
        "n_sequences": int(len(labels)),
        "n_families": int(k),
        "linkage": args.linkage,
        "metrics": {
            "ARI": float(ari),
            "homogeneity": float(hom),
            "completeness": float(com),
            "v_measure": float(vms),
            "purity": float(purity),
            "silhouette": sil
        }
    }
    with open(f"{out_pref}_report.json", "w") as f:
        json.dump(report, f, indent=2)
    print(json.dumps(report, indent=2))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Cluster RNA sequences from descriptor vectors with hierarchical clustering, evaluate vs. family labels.")
    parser.add_argument("--family", action="append", required=True,
                        help="Repeatable. Format: FamilyName=path/to/vectors.csv")
    parser.add_argument("--id_col", default="seq_name", help="ID column in each vectors CSV (default: seq_name)")
    parser.add_argument("--per_family", type=int, default=50, help="Sample size per family (-1 for all)")
    parser.add_argument("--linkage", choices=["average","complete","single","ward"], default="average",
                        help="Linkage method (average=UPGMA recommended for cosine distance)")
    parser.add_argument("--seed", type=int, default=0, help="Random seed for sampling")
    parser.add_argument("--out_prefix", default="clustering", help="Prefix for output files")
    args = parser.parse_args()
    run(args)