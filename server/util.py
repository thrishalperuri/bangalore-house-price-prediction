import json
import pickle
import numpy as np
import pandas as pd
__locations=None
__data_columns=None
__model=None
def get_estimated_price(location, sqft, bath, bhk):
    try:
        loc_index = __data_columns.index(location.lower())
    except:
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
    print("loading artifacts started")
    global __data_columns
    global __locations


    with open("../model/columns.json",'r') as f:
       __data_columns = json.load(f)['data_columns']
       __locations =__data_columns[3:]
    global __model
    with open("../model/banglore_home_prices.pickle", "rb") as f:
        __model = pickle.load(f)
    print('loading artifacts')

if __name__=='__main__':
    load_artifacts()
    print(get_location_names())
    print(get_location_names())
    print(get_estimated_price('1st Phase JP Nagar', 1000, 3, 3))
    print(get_estimated_price('1st Phase JP Nagar', 1000, 2, 2))
    print(get_estimated_price('Khalilli', 1000, 2, 2))  # other location
    print(get_estimated_price('Ejipura', 1000, 2, 2))   # other location