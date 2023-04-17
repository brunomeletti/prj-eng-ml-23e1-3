"""
This is a boilerplate pipeline 'Teste'
generated using Kedro 0.18.7
"""

from kedro.pipeline import Pipeline, node, pipeline

from .nodes import (select_data, predict_three_points_shot, predict_two_points_shot)

def create_pipeline(**kwargs) -> Pipeline:
    return pipeline([
        node(
            func=select_data,
            name='select_three_points_shots_data',
            inputs=['raw_kobe_dataset', 'params:three_points_shot_type'],
            outputs='three_points_data_filtered'
        ),
        node(
            func=predict_three_points_shot,
            name='three_points_shots_prediction',
            inputs=['three_points_data_filtered', 'params:mlflow_model_served_url', 'params:features', 'params:target', 'params:three_points_shots_prediction'],
            outputs=['three_points_metrics', 'three_points_predicted_dataset']
        ),
        node(
            func=predict_two_points_shot,
            name='two_points_shots_prediction',
            inputs=['data_test', 'params:mlflow_model_served_url', 'params:features', 'params:two_points_shots_prediction'],
            outputs=['two_points_metrics', 'two_points_predicted_dataset']
        )
    ])
