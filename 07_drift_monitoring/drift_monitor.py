import pandas as pd
from sklearn import datasets
from evidently import Dataset, DataDefinition, Report
from evidently.presets import DataDriftPreset
from prometheus_client import start_http_server, Gauge
import time
import random

# --- Step 1: Load data ---
adult_data = datasets.fetch_openml(name="adult", version=2, as_frame="auto")
adult = adult_data.frame

# Schema definition
schema = DataDefinition(
    numerical_columns=["education-num", "age", "capital-gain", "hours-per-week", "capital-loss", "fnlwgt"],
    categorical_columns=["education", "occupation", "native-country", "workclass",
                         "marital-status", "relationship", "race", "sex", "class"],
)

# --- Step 2: Setup Prometheus Gauges ---
g_drifted = Gauge("ml_drifted_columns", "Number of drifted columns")
g_share = Gauge("ml_share_drifted", "Share of drifted columns")
g_dataset = Gauge("ml_dataset_drift", "1 if dataset drift detected")
g_drifted_column = Gauge("ml_drifted_column_example", "Example of one drifted column encoded as int")

# Start Prometheus server
start_http_server(8000)
print("🚀 Prometheus metrics available at http://localhost:8000/metrics")

# --- Step 3: Loop to simulate drift changing over time ---
while True:
    # Reference (training-like)
    
    adult_ref = adult[~adult.education.isin(["Some-college", "HS-grad", "Bachelors"])]
    adult_prod = adult[adult.education.isin(["Some-college", "HS-grad", "Bachelors"])]
    schema = DataDefinition(
    numerical_columns=["education-num", "age", "capital-gain", "hours-per-week", "capital-loss", "fnlwgt"],
    categorical_columns=["education", "occupation", "native-country", "workclass", "marital-status", "relationship", "race", "sex", "class"],
    )

    eval_data_ref = Dataset.from_pandas(
        pd.DataFrame(adult_prod),
        data_definition=schema
    )

    eval_data_prod = Dataset.from_pandas(
        pd.DataFrame(adult_ref),
        data_definition=schema
    )

    # Evidently drift detection
    report = Report([DataDriftPreset(threshold=0.05)])
    my_eval = report.run(eval_data_prod, eval_data_ref)
    result = my_eval.dict()

    n_drifted, share_drifted, drifted_column = None, None, None
    for metric in result["metrics"]:
        if "DriftedColumnsCount" in metric["metric_id"]:
            n_drifted = metric["value"]["count"]
            share_drifted = metric["value"]["share"]
        if "ValueDrift" in metric["metric_id"] and drifted_column is None:
            # Pick the first drifted column to log its name
            drifted_column = metric["metric_id"]

    dataset_drift = share_drifted > 0.5 if share_drifted is not None else None

    print(f"📊 Drifted columns: {n_drifted}, Share: {share_drifted:.2f}, Drift Detected: {dataset_drift}")
    if drifted_column:
        print(f"🔎 Example drifted column: {drifted_column}")

    # Update Prometheus metrics
    g_drifted.set(n_drifted or 0)
    g_share.set(share_drifted or 0.0)
    g_dataset.set(1 if dataset_drift else 0)
    g_drifted_column.set(hash(drifted_column) % 100 if drifted_column else 0)

    # Wait before next cycle
    time.sleep(30)