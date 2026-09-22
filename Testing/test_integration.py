import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.metrics import mean_squared_error, r2_score, accuracy_score, classification_report
import matplotlib.pyplot as plt

# Load Data for Testing
sleep_data = pd.read_csv("Sleep_health_and_lifestyle_dataset.csv")

# End-to-End integration test
# Instead of treating each function separately, we check that the entire workflow in a single test to validate the interaction between each components.

def test_integration_workflow():
    
    # 1. Data loading
    sleep_data = pd.read_csv("Sleep_health_and_lifestyle_dataset.csv")

    assert not sleep_data.empty
    assert "Gender" in sleep_data.columns
    assert "Sleep Duration" in sleep_data.columns
    assert "Daily Steps" in sleep_data.columns
    assert "Age" in sleep_data.columns

    # 2. Data preprocessing and transformation
    sleep_data_female = sleep_data[
        sleep_data["Gender"] == "Female"
    ].copy()

    sleep_data_female["Age Group"] = np.select(
        [
            sleep_data_female["Age"] <= 35,
            sleep_data_female["Age"].between(36, 40),
            sleep_data_female["Age"].between(41, 45),
            sleep_data_female["Age"].between(46, 50),
            sleep_data_female["Age"].between(51, 55),
            sleep_data_female["Age"].between(56, 60)
        ],
        [
            "<=35",
            "36-40",
            "41-45",
            "46-50",
            "51-55",
            "56-60"
        ],
        default="Unknown"
    )

    sleep_data_female["Daily Step Level"] = sleep_data_female[
        "Daily Steps"
    ].apply(
        lambda x: "Low" if x <= 5600 else "Medium" if x < 8000 else "High"
    )

    assert not sleep_data_female.empty
    assert "Age Group" in sleep_data_female.columns
    assert "Daily Step Level" in sleep_data_female.columns

    # 3. Machine learning model training
    x = sleep_data_female[["Daily Steps"]]
    y = sleep_data_female["Sleep Duration"]

    x_train, x_test, y_train, y_test = train_test_split(
        x, y, test_size=0.2, random_state=100
    )

    model = RandomForestRegressor(random_state=100)
    model.fit(x_train, y_train)

    predictions = model.predict(x_test)

    # 4. Machine learning model prediction and evaluation
    assert len(predictions) == len(y_test)
    assert np.isfinite(predictions).all()

    r2 = r2_score(y_test, predictions)
    rmse = np.sqrt(mean_squared_error(y_test, predictions))

    assert np.isfinite(r2)
    assert np.isfinite(rmse)
    assert rmse >= 0

    # 5. Data visualization
    plot_data = pd.DataFrame({
        "Daily Steps": x_test["Daily Steps"].values,
        "Actual": y_test.values,
        "Predicted": predictions
    }).sort_values("Daily Steps")

    # Check that visualization data is valid
    assert len(plot_data) == len(y_test)

    assert set(plot_data.columns) == {
        "Daily Steps",
        "Actual",
        "Predicted"
    }

    assert plot_data["Daily Steps"].is_monotonic_increasing

    assert np.isfinite(
        plot_data[["Daily Steps", "Actual", "Predicted"]].values
    ).all()