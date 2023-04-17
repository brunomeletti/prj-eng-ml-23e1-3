"""
This is a boilerplate pipeline 'PreparacaoDados'
generated using Kedro 0.18.7
"""

from sklearn.model_selection import train_test_split
import pandas as pd

# Normaliza os dados, aplica o critério de seleção de dados e monta o dataset de trabalho
def select_and_conform_data(data, shot_type):
    conformed_df = data.dropna() 
    conformed_df = conformed_df.query('shot_type == @shot_type')

    new_df = conformed_df[[
        'lat',
        'lon',
        'minutes_remaining',
        'period',
        'playoffs',
        'shot_distance',
        'shot_made_flag'
    ]];

    return new_df

# Separa os dados de treino e teste usando uma escolha aleatória e estratificada
def split_train_test(data, target, features, test_size, random_state):
    train, test = train_test_split(data, stratify=data[target], test_size=test_size, random_state=random_state, shuffle=True)

    X_train = train[features]
    y_train = pd.DataFrame(train[target])
    X_test = test[features]
    y_test = pd.DataFrame(test[target])

    return X_train, X_test, y_train, y_test

# Recupera as métricas de treino e teste
def get_train_test_metrics(data_train, data_test, test_size):
    metrics = {
        'test_size_percent': test_size * 100,
        'train_dataset_size': data_train.shape[0],
        'test_dataset_size': data_test.shape[0]
    }

    return {
        key: {'value': float(value), 'step': 1}
        for key, value in metrics.items()
    }