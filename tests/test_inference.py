import os
import joblib
import numpy as np
import pytest

@pytest.mark.skipif(not os.path.exists("artifacts/model.pkl"), reason="Model not trained yet")
def test_model_can_predict():
    """Load trained model and check it predicts valid class."""
    model_path = "artifacts/model.pkl"
    assert os.path.exists(model_path), "Model file missing"

    model = joblib.load(model_path)
    sample = np.array([[5.1, 3.5, 1.4, 0.2]])  # Iris-setosa
    pred = model.predict(sample)

    # Model should predict one of 0, 1, 2
    assert pred[0] in [0, 1, 2], "Invalid prediction output"