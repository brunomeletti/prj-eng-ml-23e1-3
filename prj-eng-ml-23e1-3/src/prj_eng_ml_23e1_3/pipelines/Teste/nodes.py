"""
This is a boilerplate pipeline 'Teste'
generated using Kedro 0.18.7
"""
from sklearn.metrics import log_loss, f1_score
import requests
import pandas as pd
import json

# Aplica o critério de seleção de dados e retorna o dataset de testes
def select_data(data, shot_type):
    return data.query('shot_type == @shot_type')

# Prediz o resultado dos arremessos de três pontos e registra métricas
def predict_three_points_shot(data, url, features, target, label):
    data.dropna(inplace=True)
    sample = data[features]
    y_true = data[target]

    input_data  = sample.to_dict(orient='records')

    payload = {
        'dataframe_records': input_data
    }

    response = requests.post(url, json=payload)

    if response.status_code == 200:
        json_data = json.loads(response.text)

        missed_shots_total = json_data['predictions'].count(0.0)
        correct_shots_total = json_data['predictions'].count(1.0)
        
        print('')
        print('---- PREDICTIONS {} ----'.format(label))
        print('Total de amostras: {}\nTotal de arremessos errados: {}\nTotal de arremessos convertidos: {}'.format(data.shape[0], missed_shots_total, correct_shots_total))
        print('---- PREDICTIONS ----')
        print('')

        predicted_series = pd.json_normalize(response.json())
        y_pred = predicted_series['predictions'].squeeze()

        data['prediction'] = y_pred

        log_loss_score = log_loss(y_true, y_pred)
        f1_scr = f1_score(y_true, y_pred, average='weighted')
        
        print('')
        print('---- NEW LOG LOSS & F1 SCORE {} ----'.format(label))
        print('Log Loss Score: {}. F1 Score: {}'.format(log_loss_score, f1_scr))
        print('---- NEW LOG LOSS & F1 SCORE ----')
        print('')
        
        metrics = {
            'samples_total': data.shape[0],
            'correct_shots_total': correct_shots_total,
            'missed_shots_total': missed_shots_total,
            'new_log_loss_score': log_loss_score,
            'new_f1_score': f1_scr,
        }
    else:
        print('Erro:', response.text)

        metrics = {
            'samples_total': 0,
            'correct_shots_total': 0,
            'missed_shots_total': 0,
            'missed_shots_total': 0,
            'new_log_loss_score': 0,
            'new_f1_score': 0,
        }

    dic = {
        key: {'value': float(value), 'step': 1}
        for key, value in metrics.items()
    }

    return dic, data[[
        'lat',
        'lon',
        'minutes_remaining',
        'period',
        'playoffs',
        'shot_distance',
        'prediction'
    ]]

# Prediz o resultado dos arremessos de dois pontos e registra métricas
def predict_two_points_shot(data, url, features, label):
    data.dropna(inplace=True)
    sample = data[features]

    input_data  = sample.to_dict(orient='records')

    payload = {
        'dataframe_records': input_data
    }

    response = requests.post(url, json=payload)

    if response.status_code == 200:
        json_data = json.loads(response.text)

        missed_shots_total = json_data['predictions'].count(0.0)
        correct_shots_total = json_data['predictions'].count(1.0)
        
        print('')
        print('---- PREDICTIONS {} ----'.format(label))
        print('Total de amostras: {}\nTotal de arremessos errados: {}\nTotal de arremessos convertidos: {}'.format(data.shape[0], missed_shots_total, correct_shots_total))
        print('---- PREDICTIONS ----')
        print('')

        predicted_series = pd.json_normalize(response.json())
        data['prediction'] = predicted_series['predictions'].squeeze()
      
        metrics = {
            'samples_total': data.shape[0],
            'correct_shots_total': correct_shots_total,
            'missed_shots_total': missed_shots_total
        }
    else:
        print('Erro:', response.text)

        metrics = {
            'samples_total': 0,
            'correct_shots_total': 0,
            'missed_shots_total': 0,
            'missed_shots_total': 0,
        }

    dic = {
        key: {'value': float(value), 'step': 1}
        for key, value in metrics.items()
    }

    return dic, data[[
        'lat',
        'lon',
        'minutes_remaining',
        'period',
        'playoffs',
        'shot_distance',
        'prediction'
    ]]