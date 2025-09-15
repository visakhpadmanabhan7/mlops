import mlflow
from mlflow.tracking import MlflowClient

# Choose experiment
experiment_name = "Default"   # or replace with your experiment name
exp = mlflow.get_experiment_by_name(experiment_name)

# Get best run (by accuracy)
best_run = mlflow.search_runs(
    experiment_ids=[exp.experiment_id],
    order_by=["metrics.accuracy DESC"],
    max_results=1
).iloc[0]

best_run_id = best_run.run_id
best_acc = best_run["metrics.accuracy"]

print(f"🏆 Best run: {best_run_id} with accuracy={best_acc:.4f}")

# Register best model
model_uri = f"runs:/{best_run_id}/model"
model_name = "IrisClassifier"

result = mlflow.register_model(model_uri, model_name)
print(f"📦 Registered model '{model_name}' as Version {result.version}")

# Promote to alias (prod)
client = MlflowClient()
client.set_registered_model_alias(
    name=model_name,
    alias="prod",          # could also use "staging"
    version=result.version
)

print(f"🚀 Model {model_name} v{result.version} is now @{ 'prod' }")