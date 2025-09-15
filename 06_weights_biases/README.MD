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


Check YAML file for the method.