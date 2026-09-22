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

# Create female subset
sleep_data_female = sleep_data[sleep_data["Gender"] == "Female"].copy()

# Test Section 1 - Data loading
def test_data_loading():
    
    # Check that the dataset was loaded as a DataFrame
    assert isinstance(sleep_data, pd.DataFrame)

    # Check that the dataset is not empty
    assert not sleep_data.empty
    
    # Check the number of rows and columns imported correctly
    assert sleep_data.shape == (374, 13)

    # Check that expected columns are present
    expected_columns = [
        "Person ID",
        "Gender",
        "Age",
        "Sleep Duration",
        "Quality of Sleep",
        "Physical Activity Level",
        "Stress Level",
        "BMI Category",
        "Blood Pressure",
        "Heart Rate",
        "Daily Steps",
        "Sleep Disorder",
    ]

    assert all(column in sleep_data.columns for column in expected_columns)
    
    # Check that Person ID contains no duplicate values
    assert sleep_data["Person ID"].duplicated().sum() == 0

# Test Section 2 - Data preprocessing and transformation
def test_data_processing():
    
    # Check that the subset contains only female observations
    assert (sleep_data_female["Gender"] == "Female").all()

    # Check that the subset is not empty
    assert not sleep_data_female.empty

    # Create Age Group variable
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

    # Check that Age Group was created
    assert "Age Group" in sleep_data_female.columns

    # Check that Age Group contains only expected categories
    expected_age_groups = {
        "<=35",
        "36-40",
        "41-45",
        "46-50",
        "51-55",
        "56-60",
        "Unknown"
    }

    assert set(sleep_data_female["Age Group"].unique()).issubset(
        expected_age_groups
    )
    
    # Create Daily Step Level variable
    sleep_data_female["Daily Step Level"] = sleep_data_female["Daily Steps"].apply(
        lambda x: "Low" if x <= 5600 else "Medium" if x < 8000 else "High"
    )

    # Check that the new column was created
    assert "Daily Step Level" in sleep_data_female.columns

    # Check that only expected categories are present
    expected_step_levels = {"Low", "Medium", "High"}
    assert set(sleep_data_female["Daily Step Level"].unique()).issubset(
        expected_step_levels
    )
    
# Test Section 3 - Data visualization
# 1. Barchart comparing Sleep Duration between Male and Female
def test_analysis_visualization_1():
    gender_sleep = sleep_data.groupby("Gender")["Sleep Duration"].mean()

    assert set(gender_sleep.index) == {"Male", "Female"}
    assert len(gender_sleep) == 2
    assert np.isfinite(gender_sleep.values).all()
    assert (gender_sleep > 0).all()
    assert (gender_sleep <= 10).all()

# 2. Barchart comparing Sleep Duration in Female at Different Age Groups
def test_analysis_visualization_2():
    age_group_sleep = sleep_data_female.groupby("Age Group")["Sleep Duration"].mean()

    expected_age_groups = {
        "<=35",
        "36-40",
        "41-45",
        "46-50",
        "51-55",
        "56-60"
    }

    assert set(age_group_sleep.index).issubset(expected_age_groups)
    assert len(age_group_sleep) > 0
    assert np.isfinite(age_group_sleep.values).all()
    assert (age_group_sleep > 0).all()
    assert (age_group_sleep <= 10).all()    

# Test Section 4 -  Machine learning model training, prediction and evaluation
def test_machine_learning_1():
    x1 = sleep_data_female[["Daily Steps"]]
    y1 = sleep_data_female["Sleep Duration"]

    x1_train, x1_test, y1_train, y1_test = train_test_split(
        x1, y1, test_size=0.2, random_state=100
    )

    models = [
        LinearRegression(),
        DecisionTreeRegressor(random_state=100),
        RandomForestRegressor(random_state=100)
    ]

    predictions = []

    for model in models:
        model.fit(x1_train, y1_train)
        pred = model.predict(x1_test)
        predictions.append(pred)

        # Prediction checks
        assert len(pred) == len(y1_test)
        assert np.isfinite(pred).all()

        # Evaluation checks
        r2 = r2_score(y1_test, pred)
        rmse = np.sqrt(mean_squared_error(y1_test, pred))

        assert np.isfinite(r2)
        assert np.isfinite(rmse)
        assert rmse >= 0

    # Check data used for visualization
    plot_data = pd.DataFrame({
        "Daily Steps": x1_test["Daily Steps"].values,
        "Actual": y1_test.values,
        "Linear Regression": predictions[0],
        "Decision Tree": predictions[1],
        "Random Forest": predictions[2]
    }).sort_values("Daily Steps")

    assert len(plot_data) == len(y1_test)

    expected_columns = {
        "Daily Steps",
        "Actual",
        "Linear Regression",
        "Decision Tree",
        "Random Forest"
    }

    assert set(plot_data.columns) == expected_columns
    assert plot_data["Daily Steps"].is_monotonic_increasing
    assert np.isfinite(plot_data.drop(columns=["Daily Steps"]).values).all()

def test_machine_learning_2():
    x2 = sleep_data[["Daily Steps", "Age"]]
    y2 = sleep_data["Sleep Duration"]

    x2_train, x2_test, y2_train, y2_test = train_test_split(
        x2, y2, test_size=0.2, random_state=100
    )

    models = [
        DecisionTreeRegressor(random_state=100),
        RandomForestRegressor(random_state=100),
        GradientBoostingRegressor(random_state=100)
    ]

    predictions = []

    for model in models:
        model.fit(x2_train, y2_train)
        pred = model.predict(x2_test)
        predictions.append(pred)

        # Prediction checks
        assert len(pred) == len(y2_test)
        assert np.isfinite(pred).all()

        # Evaluation checks
        r2 = r2_score(y2_test, pred)
        rmse = np.sqrt(mean_squared_error(y2_test, pred))

        assert np.isfinite(r2)
        assert np.isfinite(rmse)
        assert rmse >= 0

    # Check data used for visualization
    assert len(y2_test) == len(predictions[0])
    assert len(y2_test) == len(predictions[1])
    assert len(y2_test) == len(predictions[2])

    assert np.isfinite(y2_test.values).all()
    assert np.isfinite(predictions[0]).all()
    assert np.isfinite(predictions[1]).all()
    assert np.isfinite(predictions[2]).all()

    # Check prediction line
    line_min = y2_test.min()
    line_max = y2_test.max()

    assert line_min <= line_max