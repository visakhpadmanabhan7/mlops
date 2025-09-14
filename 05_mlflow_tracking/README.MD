📂 MLflow Tracking

🔹 What is MLflow?

MLflow is an open-source MLOps platform that helps manage the end-to-end ML lifecycle:
	•	Experiment tracking (log parameters, metrics, and artifacts)
	•	Model registry (versioning and stage transitions)
	•	Reproducibility (environments, dependencies)
	•	Deployment (serve models locally or via REST API)

🔹 Why do we need MLflow?

Without MLflow:
	•	You might store experiment results manually (e.g., in spreadsheets).
	•	Re-running experiments with the same parameters/environment is hard.
	•	Collaboration is difficult (no central place to track models/metrics).
	•	Version control for ML models is missing.

With MLflow:
	•	Every run logs parameters, metrics, artifacts, and models.
	•	You can compare experiments easily.
	•	Models are versioned and promoted (e.g., Staging → Production).
	•	Deployment is as simple as:

🔹 Key Components
	1.	MLflow Tracking → Logs metrics, params, and artifacts.
	2.	MLflow Projects → Packaged ML code with environment.
	3.	MLflow Models → Format to save/load/serve models.
	4.	MLflow Registry → Central hub for versioning + lifecycle.

⸻

🔹 Benefits

✅ Centralized tracking of experiments
✅ Better reproducibility (auto-logs env + deps)
✅ Model versioning & governance
✅ Easy deployment and serving
✅ Works with multiple frameworks (Sklearn, PyTorch, TensorFlow, etc.)

🔹 Typical Workflow
	1.	Train model → log runs with MLflow
	2.	Compare runs in MLflow UI
	3.	Register best model in Model Registry
	4.	Promote → Staging/Production
	5.	Serve model via REST API


python train_mlflow.py
mlflow ui --host 0.0.0.0 --port 5000
Promote it to Staging or Production
mlflow models serve -m "models:/IrisClassifier/Production" -p 1234
curl -X POST http://127.0.0.1:1234/invocations \
  -H "Content-Type: application/json" \
  -d @predict_request.json

