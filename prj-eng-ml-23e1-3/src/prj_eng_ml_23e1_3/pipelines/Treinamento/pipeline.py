"""
This is a boilerplate pipeline 'Treinamento'
generated using Kedro 0.18.7
"""

from kedro.pipeline import Pipeline, node, pipeline

from .nodes import (get_logistic_regression_metrics, train_classification_model, get_classification_model_metrics)

def create_pipeline(**kwargs) -> Pipeline:
    return pipeline([
        node(
            func=get_logistic_regression_metrics,
            name='logistic_regression_metrics',
            inputs=['data_train', 'data_test', 'labels_train', 'labels_test', 'params:test_size', 'params:target', 'params:folds', 'params:random_state'],
            outputs='lr_model_metrics'
        ),
        node(
            func=train_classification_model,
            name='train_classification_model',
            inputs=['data_train', 'data_test', 'labels_train', 'labels_test', 'params:test_size', 'params:target', 'params:folds', 'params:random_state'],
            outputs=['classification_model', 'test_classification_model_metrics']
        ),
        node(
            func=get_classification_model_metrics,
            name='classification_model_metrics',
            inputs=['classification_model', 'data_train', 'labels_train', 'params:target'],
            outputs='classification_model_metrics'
        )
    ])
