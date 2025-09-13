import os
import subprocess

def test_training_produces_model():
    """Run the training script and check model.pkl is created."""
    result = subprocess.run(
        ["python", "01_cicd_pipeline/train.py"],
        capture_output=True, text=True
    )

    # Ensure script exits cleanly
    assert result.returncode == 0, f"Training failed: {result.stderr}"

    # Check that model file exists
    assert os.path.exists("artifacts/model.pkl"), "Model file not created"