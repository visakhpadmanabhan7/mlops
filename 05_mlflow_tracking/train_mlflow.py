import mlflow
import mlflow.sklearn
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

# -------------------------
# 1. Load dataset
# -------------------------
X, y = load_iris(return_X_y=True)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Enable autologging (captures parameters, metrics, artifacts, model)
mlflow.sklearn.autolog()

# -------------------------
# 2. Train with different hyperparameters
# -------------------------
param_grid = [
    {"n_estimators": 50, "max_depth": 3},
    {"n_estimators": 100, "max_depth": 5},
    {"n_estimators": 200, "max_depth": None},
    {"n_estimators": 1, "max_depth": None},
]

for params in param_grid:
    with mlflow.start_run() as run:
        # Train model
        clf = RandomForestClassifier(**params, random_state=42)
        clf.fit(X_train, y_train)

        # Evaluate
        y_pred = clf.predict(X_test)
        acc = accuracy_score(y_test, y_pred)

        # Log custom params/metrics (autologging already does this, but explicit is fine)
        mlflow.log_params(params)
        mlflow.log_metric("accuracy", acc)

        print(f"✅ Run ID: {run.info.run_id}, Params: {params}, Accuracy: {acc:.4f}")

# -------------------------
# 3. Pick best run and register model
# -------------------------
print("\n🔍 Searching for best run...")

exp = mlflow.get_experiment_by_name("Default")

# Search best run by accuracy
best_run = mlflow.search_runs(
    experiment_ids=[exp.experiment_id],
    order_by=["metrics.accuracy DESC"],
    max_results=1
).iloc[0]

best_run_id = best_run.run_id
best_acc = best_run["metrics.accuracy"]

print(f"🏆 Best run: {best_run_id}, Accuracy={best_acc:.4f}")

# Register the best model
model_uri = f"runs:/{best_run_id}/model"
result = mlflow.register_model(model_uri, "IrisClassifier")

print(f"📦 Registered model 'IrisClassifier' as Version {result.version}")