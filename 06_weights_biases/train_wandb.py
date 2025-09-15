import wandb
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

# Initialize sweep config
sweep_config = {
    "method": "grid",   # could be random or bayes
    "metric": {"name": "accuracy", "goal": "maximize"},
    "parameters": {
        "n_estimators": {"values": [50, 100, 200]},
        "max_depth": {"values": [3, 5, None]},
    },
}

sweep_id = wandb.sweep(sweep_config, project="iris-classifier")

def train():
    # Start a run
    wandb.init()
    
    # Load dataset
    X, y = load_iris(return_X_y=True)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    
    # Train model
    clf = RandomForestClassifier(
        n_estimators=wandb.config.n_estimators,
        max_depth=wandb.config.max_depth,
        random_state=42,
    )
    clf.fit(X_train, y_train)
    
    # Evaluate
    acc = accuracy_score(y_test, clf.predict(X_test))
    
    # Log metrics
    wandb.log({"accuracy": acc})

# Launch the sweep
wandb.agent(sweep_id, function=train, count=5)  # run 5 configs