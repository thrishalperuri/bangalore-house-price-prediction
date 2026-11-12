
import json
import pickle
import numpy as np
from pathlib import Path

__locations = None
__data_columns = None
__model = None

# Get the project root directory
BASE_DIR = Path(__file__).resolve().parent.parent
MODEL_DIR = BASE_DIR / "model"


def get_estimated_price(location, sqft, bath, bhk):
    try:
        loc_index = __data_columns.index(location.lower())
    except ValueError:
        loc_index = -1

    x = np.zeros(len(__data_columns))

    x[0] = sqft
    x[1] = bath
    x[2] = bhk

    if loc_index >= 0:
        x[loc_index] = 1

    prediction = __model.predict([x])[0]
    prediction = max(prediction, 0)

    return round(prediction, 2)


def get_location_names():
    return __locations


def load_artifacts():
    global __data_columns, __locations, __model

    print("Loading artifacts started...")

    columns_path = MODEL_DIR / "columns.json"
    model_path = MODEL_DIR / "banglore_home_prices.pickle"

    with open(columns_path, "r") as f:
        __data_columns = json.load(f)["data_columns"]

    __locations = __data_columns[3:]

    with open(model_path, "rb") as f:
        __model = pickle.load(f)

    print("Loading artifacts completed!")


if __name__ == "__main__":
    load_artifacts()
    print(get_location_names())
    print(get_estimated_price("1st Phase JP Nagar", 1000, 3, 3))
