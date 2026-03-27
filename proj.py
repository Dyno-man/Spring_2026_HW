import csv
import math
from collections import defaultdict, Counter
from pathlib import Path

# ============================================================
# CONFIG
# ============================================================

INPUT_CSV = "interaction_dataset.csv"
DAMPING = 0.85
TOLERANCE = 1e-10
MAX_ITER = 1000

# Optional manual metrics for paper table.
# Fill these in ONLY if you actually have them from surveys or notes.
MANUAL_COMPLETION = {
    # "A": 0.94,
    # "B": 0.82,
    # "C": 0.88,
    # "D": 0.69,
    # "E": 0.73,
    # "F": 0.70,
}

MANUAL_AVG_RESPONSE = {
    # "A": 2.9,
    # "B": 4.5,
    # "C": 3.4,
    # "D": 6.2,
    # "E": 5.5,
    # "F": 5.8,
}

MANUAL_PEER_RATE = {
    # "A": 4.8,
    # "B": 4.2,
    # "C": 4.5,
    # "D": 3.9,
    # "E": 4.0,
    # "F": 3.8,
}

# Interaction types that are expected in the dataset
VALID_TYPES = {"reply", "task_support", "code_review", "help_request"}


# ============================================================
# DATA LOADING
# ============================================================

def load_csv(path: str):
    path_obj = Path(path)
    if not path_obj.exists():
        raise FileNotFoundError(f"Input CSV not found: {path}")

    rows = []
    required_columns = {"time", "from", "to", "type", "weight", "description"}

    with open(path_obj, "r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        if reader.fieldnames is None:
            raise ValueError("CSV has no header row.")
        missing = required_columns - set(reader.fieldnames)
        if missing:
            raise ValueError(f"CSV is missing required columns: {sorted(missing)}")

        for idx, row in enumerate(reader, start=2):
            try:
                time_val = int(str(row["time"]).strip())
                src = str(row["from"]).strip()
                dst = str(row["to"]).strip()
                typ = str(row["type"]).strip()
                weight = float(str(row["weight"]).strip())
                desc = str(row["description"]).strip()
            except Exception as e:
                raise ValueError(f"Bad row at line {idx}: {e}")

            if not src or not dst:
                raise ValueError(f"Empty from/to field at line {idx}")
            if src == dst:
                raise ValueError(f"Self-loop found at line {idx}: {src} -> {dst}")
            if typ not in VALID_TYPES:
                raise ValueError(f"Unexpected interaction type at line {idx}: {typ}")
            if not (0.0 <= weight <= 1.0):
                raise ValueError(f"Weight out of range [0,1] at line {idx}: {weight}")

            rows.append({
                "time": time_val,
                "from": src,
                "to": dst,
                "type": typ,
                "weight": weight,
                "description": desc,
            })

    if not rows:
        raise ValueError("CSV contains no data rows.")

    return rows


# ============================================================
# GRAPH BUILDING
# ============================================================

def get_nodes(rows):
    nodes = sorted(set(r["from"] for r in rows) | set(r["to"] for r in rows))
    return nodes


def aggregate_edges(rows):
    """
    Combine repeated edges by summing weights.
    """
    edge_weights = defaultdict(float)
    edge_counts = defaultdict(int)

    for r in rows:
        key = (r["from"], r["to"])
        edge_weights[key] += r["weight"]
        edge_counts[key] += 1

    return edge_weights, edge_counts


def build_transition_matrix(nodes, edge_weights):
    """
    Build row-stochastic transition matrix P where:
    P[i][j] = probability of moving from node i to node j
    based on outgoing edge weights.
    """
    node_index = {node: i for i, node in enumerate(nodes)}
    n = len(nodes)

    # Raw adjacency by summed weight
    matrix = [[0.0 for _ in range(n)] for _ in range(n)]
    out_sums = [0.0 for _ in range(n)]

    for (src, dst), weight in edge_weights.items():
        i = node_index[src]
        j = node_index[dst]
        matrix[i][j] += weight
        out_sums[i] += weight

    # Normalize rows
    transition = [[0.0 for _ in range(n)] for _ in range(n)]
    for i in range(n):
        if out_sums[i] > 0:
            for j in range(n):
                transition[i][j] = matrix[i][j] / out_sums[i]
        else:
            # Dangling node: distribute uniformly
            for j in range(n):
                transition[i][j] = 1.0 / n

    return transition, out_sums


# ============================================================
# PAGERANK
# ============================================================

def pagerank_power_iteration(transition, damping=0.85, tol=1e-10, max_iter=1000):
    """
    Computes PageRank using:
    r_new = alpha * P^T * r_old + (1-alpha) * p
    where p is uniform.
    """
    n = len(transition)
    p = [1.0 / n] * n
    r = [1.0 / n] * n

    for iteration in range(max_iter):
        r_new = [0.0] * n

        for j in range(n):
            incoming_sum = 0.0
            for i in range(n):
                incoming_sum += transition[i][j] * r[i]
            r_new[j] = damping * incoming_sum + (1.0 - damping) * p[j]

        diff = sum(abs(r_new[i] - r[i]) for i in range(n))
        r = r_new

        if diff < tol:
            return r, iteration + 1

    return r, max_iter


# ============================================================
# SUMMARY METRICS
# ============================================================

def compute_user_stats(rows, nodes, edge_weights):
    outgoing_interactions = Counter()
    incoming_interactions = Counter()
    outgoing_weight = Counter()
    incoming_weight = Counter()
    interaction_type_counts = {node: Counter() for node in nodes}

    for r in rows:
        src = r["from"]
        dst = r["to"]
        typ = r["type"]
        wt = r["weight"]

        outgoing_interactions[src] += 1
        incoming_interactions[dst] += 1
        outgoing_weight[src] += wt
        incoming_weight[dst] += wt
        interaction_type_counts[src][typ] += 1

    edge_count_out = Counter()
    edge_count_in = Counter()

    for (src, dst), _ in edge_weights.items():
        edge_count_out[src] += 1
        edge_count_in[dst] += 1

    results = {}
    for node in nodes:
        results[node] = {
            "msg_count": outgoing_interactions[node],  # baseline activity count
            "incoming_interactions": incoming_interactions[node],
            "outgoing_weight_sum": round(outgoing_weight[node], 4),
            "incoming_weight_sum": round(incoming_weight[node], 4),
            "unique_outgoing_edges": edge_count_out[node],
            "unique_incoming_edges": edge_count_in[node],
            "reply_count": interaction_type_counts[node]["reply"],
            "task_support_count": interaction_type_counts[node]["task_support"],
            "code_review_count": interaction_type_counts[node]["code_review"],
            "help_request_count": interaction_type_counts[node]["help_request"],
            "completion": MANUAL_COMPLETION.get(node, ""),
            "avg_response": MANUAL_AVG_RESPONSE.get(node, ""),
            "peer_rate": MANUAL_PEER_RATE.get(node, ""),
        }

    return results


# ============================================================
# FILE EXPORTS
# ============================================================

def write_edge_summary_csv(edge_weights, edge_counts, output_path="edge_summary.csv"):
    with open(output_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["from", "to", "total_weight", "interaction_count"])
        for (src, dst) in sorted(edge_weights.keys()):
            writer.writerow([src, dst, round(edge_weights[(src, dst)], 6), edge_counts[(src, dst)]])


def write_transition_matrix_csv(nodes, transition, output_path="transition_matrix.csv"):
    with open(output_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["from\\to"] + nodes)
        for i, node in enumerate(nodes):
            writer.writerow([node] + [round(x, 8) for x in transition[i]])


def write_results_csv(nodes, pagerank_scores, stats, output_path="pagerank_results.csv"):
    ranked = sorted(nodes, key=lambda n: pagerank_scores[n], reverse=True)

    with open(output_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([
            "user",
            "score",
            "msg_count",
            "incoming_interactions",
            "outgoing_weight_sum",
            "incoming_weight_sum",
            "unique_outgoing_edges",
            "unique_incoming_edges",
            "reply_count",
            "task_support_count",
            "code_review_count",
            "help_request_count",
            "completion",
            "avg_response",
            "peer_rate",
        ])

        for node in ranked:
            s = stats[node]
            writer.writerow([
                node,
                round(pagerank_scores[node], 8),
                s["msg_count"],
                s["incoming_interactions"],
                s["outgoing_weight_sum"],
                s["incoming_weight_sum"],
                s["unique_outgoing_edges"],
                s["unique_incoming_edges"],
                s["reply_count"],
                s["task_support_count"],
                s["code_review_count"],
                s["help_request_count"],
                s["completion"],
                s["avg_response"],
                s["peer_rate"],
            ])


def write_latex_table(nodes, pagerank_scores, stats, output_path="pagerank_results.tex"):
    ranked = sorted(nodes, key=lambda n: pagerank_scores[n], reverse=True)

    lines = []
    lines.append(r"\begin{table}[H]")
    lines.append(r"\centering")
    lines.append(r"\caption{Computed reliability scores from interaction graph}")
    lines.append(r"\label{tab:results}")
    lines.append(r"\begin{tabular}{cccccc}")
    lines.append(r"\toprule")
    lines.append(r"User & Score & Msg Count & Completion & Avg Resp & Peer Rate \\")
    lines.append(r"\midrule")

    for node in ranked:
        s = stats[node]
        completion = s["completion"] if s["completion"] != "" else "--"
        avg_response = s["avg_response"] if s["avg_response"] != "" else "--"
        peer_rate = s["peer_rate"] if s["peer_rate"] != "" else "--"

        lines.append(
            f"{node} & {pagerank_scores[node]:.3f} & {s['msg_count']} & "
            f"{completion} & {avg_response} & {peer_rate} \\\\"
        )

    lines.append(r"\bottomrule")
    lines.append(r"\end{tabular}")
    lines.append(r"\end{table}")

    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))


# ============================================================
# REPORTING
# ============================================================

def print_console_report(nodes, pagerank_scores, stats, iterations):
    ranked = sorted(nodes, key=lambda n: pagerank_scores[n], reverse=True)

    print("\n=== PageRank Results ===")
    print(f"Converged in {iterations} iterations\n")
    for node in ranked:
        s = stats[node]
        print(
            f"{node}: "
            f"score={pagerank_scores[node]:.8f}, "
            f"msg_count={s['msg_count']}, "
            f"in_weight={s['incoming_weight_sum']}, "
            f"out_weight={s['outgoing_weight_sum']}"
        )

    total = sum(pagerank_scores.values())
    print(f"\nScore sum check: {total:.12f}")


# ============================================================
# MAIN
# ============================================================

def main():
    rows = load_csv(INPUT_CSV)
    nodes = get_nodes(rows)
    edge_weights, edge_counts = aggregate_edges(rows)
    transition, _ = build_transition_matrix(nodes, edge_weights)

    scores_list, iterations = pagerank_power_iteration(
        transition,
        damping=DAMPING,
        tol=TOLERANCE,
        max_iter=MAX_ITER,
    )

    pagerank_scores = {node: scores_list[i] for i, node in enumerate(nodes)}
    stats = compute_user_stats(rows, nodes, edge_weights)

    print_console_report(nodes, pagerank_scores, stats, iterations)

    write_edge_summary_csv(edge_weights, edge_counts, "edge_summary.csv")
    write_transition_matrix_csv(nodes, transition, "transition_matrix.csv")
    write_results_csv(nodes, pagerank_scores, stats, "pagerank_results.csv")
    write_latex_table(nodes, pagerank_scores, stats, "pagerank_results.tex")

    print("\nFiles written:")
    print("- edge_summary.csv")
    print("- transition_matrix.csv")
    print("- pagerank_results.csv")
    print("- pagerank_results.tex")


if __name__ == "__main__":
    main()