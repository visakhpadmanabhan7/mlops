import wandb
import yaml
import argparse
from sklearn.datasets import load_wine, load_iris
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
import os

def train():
    wandb.init(project="wine-quality-classifier")

    # Load dataset
    if args.dataset == "iris":
        from sklearn.datasets import load_iris
        X, y = load_iris(return_X_y=True)
    else:
        X, y = load_wine(return_X_y=True)

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    clf = RandomForestClassifier(
        n_estimators=wandb.config.n_estimators,
        max_depth=wandb.config.max_depth,
        criterion=wandb.config.criterion,
        min_samples_split=wandb.config.min_samples_split,
        random_state=42,
        n_jobs=-1
    )
    clf.fit(X_train, y_train)
    y_pred = clf.predict(X_test)

    acc = accuracy_score(y_test, y_pred)
    prec = precision_score(y_test, y_pred, average="macro")
    rec = recall_score(y_test, y_pred, average="macro")
    f1 = f1_score(y_test, y_pred, average="macro")

    wandb.log({"accuracy": acc, "precision": prec, "recall": rec, "f1_score": f1})

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--dataset", type=str, default="wine")
    parser.add_argument("--count", type=int, default=20)
    parser.add_argument("--sweep_file", type=str, default="sweep.yaml")
    args = parser.parse_args()

    with open(args.sweep_file, "r") as f:
        sweep_config = yaml.safe_load(f)

    # 👇 Dynamically pick project from env (set in GitHub Actions)
    project_name = os.getenv("WANDB_PROJECT", "wine-quality-classifier")

    sweep_id = wandb.sweep(sweep=sweep_config, project=project_name)
    wandb.agent(sweep_id, function=train, count=args.count)