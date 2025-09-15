import wandb
import yaml
from sklearn.datasets import load_wine
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

def train():
    wandb.init(project="wine-quality-classifier")

    # Load dataset
    X, y = load_wine(return_X_y=True)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    # Model with sweep params
    clf = RandomForestClassifier(
        n_estimators=wandb.config.n_estimators,
        max_depth=wandb.config.max_depth,
        criterion=wandb.config.criterion,
        min_samples_split=wandb.config.min_samples_split,
        random_state=42,
        n_jobs=-1
    )
    clf.fit(X_train, y_train)

    # Predictions
    y_pred = clf.predict(X_test)

    # Metrics (macro = good for multi-class like wine dataset)
    acc = accuracy_score(y_test, y_pred)
    prec = precision_score(y_test, y_pred, average="macro")
    rec = recall_score(y_test, y_pred, average="macro")
    f1 = f1_score(y_test, y_pred, average="macro")

    # Log all metrics to W&B
    wandb.log({
        "accuracy": acc,
        "precision": prec,
        "recall": rec,
        "f1_score": f1
    })

    print(f"✅ Accuracy={acc:.4f}, Precision={prec:.4f}, Recall={rec:.4f}, F1={f1:.4f}")

if __name__ == "__main__":
    # ✅ Load sweep config from YAML
    with open("sweep.yaml", "r") as f:
        sweep_config = yaml.safe_load(f)

    sweep_id = wandb.sweep(sweep=sweep_config, project="wine-quality-classifier")

    # Launch sweep agent (20 experiments)
    wandb.agent(sweep_id, function=train, count=20)