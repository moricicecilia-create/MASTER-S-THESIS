from __future__ import annotations
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from .metrics import reliability_bins


def save_reliability_figure(dataset, model, seed, scenario_predictions, y_by_scenario, output_dir, n_bins=5):
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    scenarios = list(scenario_predictions.keys())
    n_rows = (len(scenarios) + 2) // 3
    fig, axes = plt.subplots(n_rows, 3, figsize=(15, 4.4*n_rows), squeeze=False)
    axes = axes.ravel()
    methods = list(next(iter(scenario_predictions.values())))
    for i, scenario in enumerate(scenarios):
        ax = axes[i]
        ax.plot([0, 1], [0, 1], linestyle="--", linewidth=1, label="Perfect calibration")
        y = y_by_scenario[scenario]
        for method in methods:
            p = scenario_predictions[scenario][method]
            bins = reliability_bins(y, p, n_bins=n_bins)
            valid = [b for b in bins if b["count"] > 0]
            if valid:
                ax.plot([b["mean_probability"] for b in valid],
                        [b["fraction_positive"] for b in valid],
                        marker="o", linewidth=1.5, label=method)
                for b in valid:
                    ax.annotate(str(b["count"]), (b["mean_probability"], b["fraction_positive"]), fontsize=7)
        ax.set_title(scenario)
        ax.set_xlim(0, 1); ax.set_ylim(0, 1)
        ax.set_xlabel("Mean predicted probability of class 1")
        ax.set_ylabel("Observed fraction of class 1")
        ax.grid(alpha=0.25)
        if i == 0:
            ax.legend(fontsize=7)
    for j in range(len(scenarios), len(axes)):
        axes[j].set_visible(False)
    fig.suptitle(f"Reliability diagrams | {dataset} | {model} | seed {seed}")
    fig.tight_layout(rect=[0, 0, 1, 0.97])
    path = output_dir / f"{dataset}_{model.replace('/', '_')}_seed_{seed}.png"
    fig.savefig(path, dpi=160)
    plt.close(fig)
    return path
