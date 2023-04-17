"""
This is a boilerplate pipeline 'PreparacaoDados'
generated using Kedro 0.18.7
"""

from kedro.pipeline import Pipeline, node, pipeline

from .nodes import (select_and_conform_data, split_train_test, get_train_test_metrics)

def create_pipeline(**kwargs) -> Pipeline:
    return pipeline([
         node(
            func=select_and_conform_data,
            name='select_data',
            inputs=['raw_kobe_dataset', 'params:shot_type'],
            outputs='data_filtered'
        ),
         node(
            func=split_train_test,
            name='split_train_test',
            inputs=['data_filtered', 'params:target', 'params:features', 'params:test_size', 'params:random_state'],
            outputs=['data_train', 'data_test', 'labels_train', 'labels_test']
        ),
        node(
            func=get_train_test_metrics,
            name='train_test_metrics',
            inputs=['data_train', 'data_test', 'params:test_size'],
            outputs='train_test_metrics'
        )
    ])
