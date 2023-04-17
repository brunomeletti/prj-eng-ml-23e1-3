"""
This is a boilerplate pipeline 'Treinamento'
generated using Kedro 0.18.7
"""
from pycaret.classification import *
from sklearn.metrics import log_loss, f1_score

# Recupera as métricas do modelo de regressão logística
def get_logistic_regression_metrics(data_train, data_test, labels_train, labels_test, test_size, target, folds, random_state):
    setup(
        data = data_train,
        target=labels_train.squeeze(),
        session_id = random_state,
        fold = folds,
        n_jobs = -2,
        fold_strategy = 'stratifiedkfold',
        experiment_name = 'logistic_regression_xp',
        train_size = (1 - test_size)
    )
  
    add_metric('logloss', 'Log Loss', log_loss, greater_is_better = False)
    
    lr_model = create_model('lr')
    lr_tuned_model = tune_model(lr_model)

    predictions = predict_model(lr_tuned_model, data=data_test)

    log_loss_score = log_loss(labels_test.squeeze(), predictions['prediction_score'])

    metrics = {
        'log_loss': log_loss_score 
    }

    dic = {
        key: {'value': float(value), 'step': 1}
        for key, value in metrics.items()
    }

    return dic

# Treina modelo classificação do sklearn usando a biblioteca pyCaret
def train_classification_model(data_train, data_test, labels_train, labels_test, test_size, target, folds, random_state):
    setup(
        data = data_train,
        target=labels_train.squeeze(),
        session_id = random_state,
        fold = folds,
        n_jobs = -2,
        fold_strategy = 'stratifiedkfold',
        experiment_name = 'classification_xp',
        train_size = (1 - test_size)
    )

    add_metric('logloss', 'Log Loss', log_loss, greater_is_better = False)
    add_metric('F1_score', 'F1 score', f1_score)

    best = compare_models(verbose=True)

    best_tuned = tune_model(best)

    predicted_shots = predict_model(best_tuned, data_test)

    print('')
    print('---- CLASSIFICATION MODEL - PARAMS ----')
    print('Best Tuned Model Params: {}'.format(
        best_tuned.get_params
    ))
    print('---- CLASSIFICATION MODEL - PARAMS ----')
    print('')
    print('---- CLASSIFICATION MODEL - TEST PREDICTIONS ----')
    print('Total de Arremessos: {}\nArremessos Perdidos: {}\nArremessos Convertidos: {}'.format(
        data_test.shape[0],
        predicted_shots['prediction_label'].value_counts()[0],
        predicted_shots['prediction_label'].value_counts()[1]
    ))
    print('---- CLASSIFICATION MODEL - TEST PREDICTIONS ----')
    print('')

    metrics = {
        'test_data_shots_total': data_test.shape[0],
        'test_data_correct_shots': predicted_shots['prediction_label'].value_counts()[0],
        'test_data_missed_shots': predicted_shots['prediction_label'].value_counts()[1],
    }

    dic = {
        key: {'value': float(value), 'step': 1}
        for key, value in metrics.items()
    }

    return best_tuned, dic

# Recupera as métricas do modelo de classificação
def get_classification_model_metrics(model, data_train, labels_train, target):
    predictions = predict_model(model, data=data_train)

    log_loss_score = log_loss(labels_train, predictions['prediction_score'])
    f1 = f1_score(labels_train, predictions['prediction_label'])
  
    metrics = {
        'log_loss': log_loss_score,
        'f1_score': f1,
    }

    dic = {
        key: {'value': float(value), 'step': 1}
        for key, value in metrics.items()
    }

    return dic