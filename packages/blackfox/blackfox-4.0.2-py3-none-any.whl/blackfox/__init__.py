# coding: utf-8

# flake8: noqa

"""
    blackfox

    Module *blackfox* exposes *BlackFox*, a class with all the optimization methods and controls.

"""


from __future__ import absolute_import

from blackfox_restapi.rest import ApiException

# import models into sdk package
from blackfox_restapi.models.convergency_criterion import ConvergencyCriterion
from blackfox_restapi.models.input_config import InputConfig
from blackfox_restapi.models.input_window_config import InputWindowConfig
from blackfox_restapi.models.input_window_range_config import InputWindowRangeConfig
from blackfox_restapi.models.output_window_config import OutputWindowConfig
from blackfox_restapi.models.optimization_engine_config import OptimizationEngineConfig
from blackfox_restapi.models.range import Range
from blackfox_restapi.models.range_int import RangeInt
from blackfox_restapi.models.neural_network_type import NeuralNetworkType
from blackfox_restapi.models.binary_metric import BinaryMetric
from blackfox_restapi.models.regression_metric import RegressionMetric
from blackfox_restapi.models.encoding import Encoding
from blackfox_restapi.models.neural_network_activation_function import NeuralNetworkActivationFunction
from blackfox_restapi.models.neural_network_training_algorithm import NeuralNetworkTrainingAlgorithm

# import ann models
from blackfox_restapi.models.ann_hidden_layer_config import AnnHiddenLayerConfig
from blackfox_restapi.models.ann_layer_config import AnnLayerConfig
from blackfox_restapi.models.ann_optimization_config import AnnOptimizationConfig
from blackfox_restapi.models.ann_optimization_status import AnnOptimizationStatus
from blackfox_restapi.models.ann_model import AnnModel
from blackfox_restapi.models.ann_series_optimization_config import AnnSeriesOptimizationConfig
from blackfox_restapi.models.ann_optimization_engine_config import AnnOptimizationEngineConfig
from blackfox_restapi.models.optimization_algorithm import OptimizationAlgorithm
# import rnn models
from blackfox_restapi.models.rnn_hidden_layer_config import RnnHiddenLayerConfig
from blackfox_restapi.models.rnn_optimization_config import RnnOptimizationConfig
from blackfox_restapi.models.rnn_optimization_status import RnnOptimizationStatus
from blackfox_restapi.models.rnn_model import RnnModel
# import random forest models
from blackfox_restapi.models.random_forest_optimization_config import RandomForestOptimizationConfig
from blackfox_restapi.models.random_forest_optimization_status import RandomForestOptimizationStatus
from blackfox_restapi.models.random_forest_model import RandomForestModel
from blackfox_restapi.models.random_forest_series_optimization_config import RandomForestSeriesOptimizationConfig
from blackfox_restapi.models.random_forest_model_type import RandomForestModelType

# import xgboost models
from blackfox_restapi.models.xg_boost_optimization_config import XGBoostOptimizationConfig
from blackfox_restapi.models.xg_boost_optimization_status import XGBoostOptimizationStatus
from blackfox_restapi.models.xg_boost_model import XGBoostModel
from blackfox_restapi.models.xg_boost_series_optimization_config import XGBoostSeriesOptimizationConfig

from blackfox.black_fox import BlackFox
from blackfox.log_writer import LogWriter
from blackfox.csv_log_writer import CsvLogWriter