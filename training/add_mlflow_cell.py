"""
Adds a DagsHub MLflow tracking cell to exp_1.ipynb.
Run once, then open the notebook — the new cell will be at the bottom.
"""
import json, pathlib

NB_PATH = pathlib.Path(__file__).parent / "exp_1.ipynb"

# ── New cells to inject ───────────────────────────────────────────────────────
markdown_cell = {
    "cell_type": "markdown",
    "id": "mlflow_header",
    "metadata": {},
    "source": [
        "## MLflow Tracking — Log to DagsHub\n",
        "Logs parameters, metrics, and the trained model to the DagsHub remote MLflow tracking server."
    ]
}

code_cell = {
    "cell_type": "code",
    "execution_count": None,
    "id": "mlflow_dagshub_tracking",
    "metadata": {},
    "outputs": [],
    "source": [
        "import mlflow\n",
        "import mlflow.sklearn\n",
        "import dagshub\n",
        "from sklearn.metrics import classification_report, accuracy_score\n",
        "\n",
        "# ── Step 1: Connect to DagsHub MLflow Tracking Server ──────────────────────\n",
        "# dagshub.init() automatically sets MLFLOW_TRACKING_URI,\n",
        "# MLFLOW_TRACKING_USERNAME and MLFLOW_TRACKING_PASSWORD.\n",
        "# On first run it will open a browser window to authenticate — log in once.\n",
        "dagshub.init(\n",
        "    repo_owner='SachinMishra-ux',\n",
        "    repo_name='log_classifier_project_1',\n",
        "    mlflow=True\n",
        ")\n",
        "\n",
        "# ── Step 2: Set the experiment name ─────────────────────────────────────────\n",
        "mlflow.set_experiment('experiment1')\n",
        "\n",
        "# ── Step 3: Log everything inside a single run ───────────────────────────────\n",
        "with mlflow.start_run(run_name='LogReg_MiniLM_exp1'):\n",
        "\n",
        "    # --- Parameters ---\n",
        "    mlflow.log_param('model_type', 'LogisticRegression')\n",
        "    mlflow.log_param('embedding_model', 'sentence-transformers/all-MiniLM-L6-v2')\n",
        "    mlflow.log_param('embedding_dim', 384)\n",
        "    mlflow.log_param('max_iter', 1000)\n",
        "    mlflow.log_param('test_size', 0.3)\n",
        "    mlflow.log_param('random_state', 43)\n",
        "    mlflow.log_param('dataset', 'synthetic_logs.csv')\n",
        "    mlflow.log_param('classification_stage', 'stage2_embedding')\n",
        "\n",
        "    # --- Metrics ---\n",
        "    report_dict = classification_report(y_test, y_pred, output_dict=True)\n",
        "\n",
        "    # Overall metrics\n",
        "    mlflow.log_metric('accuracy', report_dict['accuracy'])\n",
        "    mlflow.log_metric('macro_precision', report_dict['macro avg']['precision'])\n",
        "    mlflow.log_metric('macro_recall', report_dict['macro avg']['recall'])\n",
        "    mlflow.log_metric('macro_f1', report_dict['macro avg']['f1-score'])\n",
        "    mlflow.log_metric('weighted_precision', report_dict['weighted avg']['precision'])\n",
        "    mlflow.log_metric('weighted_recall', report_dict['weighted avg']['recall'])\n",
        "    mlflow.log_metric('weighted_f1', report_dict['weighted avg']['f1-score'])\n",
        "\n",
        "    # Per-class metrics\n",
        "    for label in report_dict:\n",
        "        if label not in ('accuracy', 'macro avg', 'weighted avg'):\n",
        "            safe = label.replace(' ', '_')\n",
        "            mlflow.log_metric(f'{safe}_precision', report_dict[label]['precision'])\n",
        "            mlflow.log_metric(f'{safe}_recall',    report_dict[label]['recall'])\n",
        "            mlflow.log_metric(f'{safe}_f1',        report_dict[label]['f1-score'])\n",
        "            mlflow.log_metric(f'{safe}_support',   report_dict[label]['support'])\n",
        "\n",
        "    # --- Model artifact ---\n",
        "    mlflow.sklearn.log_model(clf, artifact_path='log_classifier_model')\n",
        "\n",
        "    run_id = mlflow.active_run().info.run_id\n",
        "    print(f'\\n✅ Run logged successfully!')\n",
        "    print(f'   Run ID  : {run_id}')\n",
        "    print(f'   Accuracy: {report_dict[\"accuracy\"]:.4f}')\n",
        "    print(f'   View on DagsHub → https://dagshub.com/SachinMishra-ux/log_classifier_project_1/experiments')\n",
    ]
}

# ── Inject into notebook ──────────────────────────────────────────────────────
nb = json.loads(NB_PATH.read_text())

# Skip if already injected
ids = [c.get("id") for c in nb["cells"]]
if "mlflow_dagshub_tracking" in ids:
    print("⚠️  MLflow cell already exists in the notebook — skipping.")
else:
    nb["cells"].extend([markdown_cell, code_cell])
    NB_PATH.write_text(json.dumps(nb, indent=1, ensure_ascii=False))
    print("✅ MLflow tracking cell added to exp_1.ipynb successfully!")
    print("   Open the notebook and run the last two cells to log to DagsHub.")
