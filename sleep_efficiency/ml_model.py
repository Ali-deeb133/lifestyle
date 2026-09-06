import joblib
import pandas as pd
import numpy as np
from django.conf import settings
from sklearn.preprocessing import FunctionTransformer

rf_model = joblib.load(settings.SLEEP_MODEL_PATH)


def preprocess_pipeline(X):
    X = X.copy()

    X['Smoking status'] = X['Smoking status'].map({'No': 0, 'Yes': 1})
    X['Gender'] = X['Gender'].map({'Female': 0, 'Male': 1})

    X['Bedtime'] = pd.to_datetime(X['Bedtime'])
    X['Bedtime_hour'] = X['Bedtime'].dt.hour + X['Bedtime'].dt.minute / 60
    X['Bedtime_sin'] = np.sin(2*np.pi*X['Bedtime_hour']/24)
    X['Bedtime_cos'] = np.cos(2*np.pi*X['Bedtime_hour']/24)

    for col in ['Caffeine consumption', 'Alcohol consumption', 'Awakenings']:
        X[col + '_log'] = np.log1p(X[col])

    X['REM_est'] = 0.5 * X['Sleep duration']
    X['Deep_est'] = 0.5 * X['Sleep duration']
    X['Restorative_sleep'] = X['REM_est'] + X['Deep_est']

    final_features = [
        'Age','Sleep duration','Exercise frequency','Smoking status','Gender',
        'Bedtime_sin','Bedtime_cos','Caffeine consumption_log',
        'Alcohol consumption_log','Awakenings_log','Restorative_sleep'
    ]

    return X[final_features]


preprocessor = FunctionTransformer(preprocess_pipeline)