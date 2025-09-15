What is W&B?

Weights & Biases is an MLOps tool for:
	•	Experiment tracking
	•	Hyperparameter sweeps
	•	Collaboration (dashboards, reports)
	•	Model management

Why W&B?

Without W&B:
	•	Experiments are logged manually (hard to compare).
	•	Sharing results across team is messy.

With W&B:
	•	Centralized dashboard of runs.
	•	Easy comparison of parameters/metrics.
	•	Hyperparameter tuning at scale.

- pip install -r requirements.txt
- wandb login
- python train_wandb.py

🔹 Key Difference in Practice
	•	MLflow:
	•	Run → Compare runs → Register model → Deploy to prod.
	•	Focus = operationalization.
	•	W&B:
	•	Run → Visualize charts → Share report → Tune hyperparams.
	•	Focus = collaboration + exploration.

⸻

🔹 Analogy
	•	MLflow = like Docker + Jenkins → package, version, deploy.
	•	W&B = like Google Docs for ML experiments → easy to share, comment, visualize.


🔹 What are Hyperparameters?
	•	Parameters you set before training, not learned from data.
	•	Examples:
	•	RandomForest → n_estimators, max_depth
	•	Neural nets → learning_rate, batch_size, num_layers
	•	XGBoost → eta, max_depth, colsample_bytree

They strongly influence performance, but there’s no formula for the “best” values.

⸻

🔹 What is Hyperparameter Sweeping?

It’s the process of automatically training the model multiple times with different hyperparameter combinations to find the best-performing one.

Think of it as grid-searching or auto-tuning:
	•	Try n_estimators=50, 100, 200
	•	Try max_depth=3, 5, None
	•	Evaluate each run → pick the one with highest accuracy (or lowest loss).

⸻

🔹 Types of Sweeps
	1.	Grid Search → try all possible combinations.
	    •	    E.g., 3×3 grid = 9 runs.
	    •	Expensive but exhaustive.
	2.	Random Search → pick random combinations.
	    •	Cheaper, surprisingly effective.
	3.	Bayesian Optimization → use past results to pick smarter next combinations.
	    •	Efficient for large search spaces.
	4.	Hyperband / Population-based → advanced methods for deep learning.

🔹 The options
	1.	grid
	•	Tries every possible combination of parameters.
	•	Example:
	•	n_estimators: [50, 100, 200]
	•	max_depth: [5, 10]
	•	→ 3 × 2 = 6 runs total.
	•	✅ Exhaustive, good for small search spaces.
	•	❌ Expensive for large search spaces.

⸻

	2.	random
	•	Picks random combinations from parameter space.
	•	Example: same grid as above → instead of all 6, it might sample 4 random ones.
	•	✅ Efficient for large spaces.
	•	✅ Often finds good configs faster than grid.
	•	❌ Might miss the absolute best if unlucky.

⸻

	3.	bayes (Bayesian optimization)
	•	Uses results of previous runs to guide next hyperparameter choice.
	•	Smarter than random, especially with continuous values (e.g., learning rate).
	•	✅ More sample-efficient.
	•	❌ Slower per-step (needs optimization overhead).


GitHub Actions Workflow
	•	Added .github/workflows/wandb-sweep.yml.
	•	Triggers:
        •	On push to wandb branch.
        •	Manual dispatch (play button in Actions tab).
	•	Steps:
        1.	Checkout repo.
        2.	Setup Python (3.11).
        3.	Install dependencies.
        4.	Run W&B sweep agent.
	•	Configurable workflow inputs:
        •	count → number of runs (default: 20).
        •	dataset → wine or iris.
        •	sweep_file → path to sweep config file.

5. Authentication
	•	W&B API key stored securely in GitHub Secrets (WANDB_API_KEY).

⸻

🔹 Workflow in Action
	1.	Push to wandb branch or manually trigger workflow.
	2.	GitHub runner launches sweep agent.
	3.	Each run:
        •	Trains model with different hyperparams.
        •	Logs metrics (accuracy, precision, recall, f1_score).
	4.	Results visible on wandb.ai dashboard.

🔹 Workflow in Action
	1.	Trigger the workflow
        •	Push to 06_weights_biases branch (dev mode)
        •	Or manually trigger via Actions tab → Run workflow (choose branch & inputs).
	2.	GitHub runner launches W&B sweep agent
        •	Chooses project based on branch:
        •	main → wine-quality-prod
        •	feature branch → wine-quality-dev
	3.	Each run in the sweep
        •	Trains a model with different hyperparameters from sweep.yaml.
        •	Logs metrics to W&B:
        •	Accuracy ✅
        •	Precision ✅
        •	Recall ✅
        •	F1-score ✅
        •	Tagged with GitHub metadata (branch + commit SHA).
        4.	View results in W&B dashboard
        •	Dev runs and Prod runs stay separated.
        •	Easy comparison of hyperparams across multiple runs.
        •	Traceability: every run is linked back to the GitHub branch/commit.