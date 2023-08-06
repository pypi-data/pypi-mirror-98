import xgboost as xgb
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error as mse
from sklearn.metrics import mean_absolute_error as mae

import numpy as np

default_eval_method_dict = dict()

def xgboost_regressor_eval_method_mse_fast(train_X, train_y, valid_X, valid_y, parameters):

	algo = xgb.XGBRegressor(
		objective='reg:squarederror', 
		learning_rate=parameters['learning_rate_multiplier']/float(parameters['n_estimators']),
		gamma=parameters['gamma'],
		max_depth=int(parameters['max_depth']),
		n_estimators=parameters['n_estimators'],
		min_child_weight=int(parameters['min_child_weight']),
		colsample_bytree=parameters['colsample_bytree'],
		subsample=parameters['subsample'],
		reg_alpha=parameters['reg_alpha'],
		reg_lambda=parameters['reg_lambda'],
		n_jobs=1,
		tree_method='hist')

	algo.fit(train_X, train_y)

	return np.sqrt(mse(algo.predict(valid_X), valid_y))

xgboost_regressor_eval_method_mse_fast_str = \
"""
def xgboost_regressor_eval_method(train_X, train_y, valid_X, valid_y, parameters):

	algo = xgb.XGBRegressor(
		objective='reg:squarederror', 
		learning_rate=parameters['learning_rate_multiplier']/float(parameters['n_estimators']),
		gamma=parameters['gamma'],
		max_depth=int(parameters['max_depth']),
		n_estimators=parameters['n_estimators'],
		min_child_weight=int(parameters['min_child_weight']),
		colsample_bytree=parameters['colsample_bytree'],
		subsample=parameters['subsample'],
		reg_alpha=parameters['reg_alpha'],
		reg_lambda=parameters['reg_lambda'],
		n_jobs=1,
		tree_method='hist')

	algo.fit(train_X, train_y)

	return np.sqrt(mse(algo.predict(valid_X), valid_y))"""

default_eval_method_dict['xgboost_regressor_mse_fast'] = [xgboost_regressor_eval_method_mse_fast, xgboost_regressor_eval_method_mse_fast_str]


def xgboost_regressor_eval_method_mse(train_X, train_y, valid_X, valid_y, parameters):

	algo = xgb.XGBRegressor(
		objective='reg:squarederror', 
		learning_rate=parameters['learning_rate_multiplier']/float(parameters['n_estimators']),
		gamma=parameters['gamma'],
		max_depth=int(parameters['max_depth']),
		n_estimators=parameters['n_estimators'],
		min_child_weight=int(parameters['min_child_weight']),
		colsample_bytree=parameters['colsample_bytree'],
		subsample=parameters['subsample'],
		reg_alpha=parameters['reg_alpha'],
		reg_lambda=parameters['reg_lambda'],
		n_jobs=1)

	algo.fit(train_X, train_y)

	return np.sqrt(mse(algo.predict(valid_X), valid_y))

xgboost_regressor_eval_method_mse_str = \
"""
def xgboost_regressor_eval_method(train_X, train_y, valid_X, valid_y, parameters):

	algo = xgb.XGBRegressor(
		objective='reg:squarederror', 
		learning_rate=parameters['learning_rate_multiplier']/float(parameters['n_estimators']),
		gamma=parameters['gamma'],
		max_depth=int(parameters['max_depth']),
		n_estimators=parameters['n_estimators'],
		min_child_weight=int(parameters['min_child_weight']),
		colsample_bytree=parameters['colsample_bytree'],
		subsample=parameters['subsample'],
		reg_alpha=parameters['reg_alpha'],
		reg_lambda=parameters['reg_lambda'],
		n_jobs=1)

	algo.fit(train_X, train_y)

	return np.sqrt(mse(algo.predict(valid_X), valid_y))"""

default_eval_method_dict['xgboost_regressor_mse'] = [xgboost_regressor_eval_method_mse, xgboost_regressor_eval_method_mse_str]


def sklearn_random_forest_eval_method_mse(train_X, train_y, valid_X, valid_y, parameters):

	algo = RandomForestRegressor(
		n_estimators=parameters['n_estimators'], 
		max_depth=parameters['max_depth'],
		min_samples_split=parameters['min_samples_split'],
		min_samples_leaf=parameters['min_samples_leaf'],
		max_features=parameters['max_features'],
		bootstrap=parameters['bootstrap'],
		n_jobs=1)

	algo.fit(X=train_X, y=train_y.values.ravel())

	return np.sqrt(mse(algo.predict(valid_X), valid_y.values))

sklearn_random_forest_eval_method_mse_str = \
"""
def sklearn_random_forest_eval_method_mse(train_X, train_y, valid_X, valid_y, parameters):

	algo = RandomForestRegressor(
		n_estimators=parameters['n_estimators'], 
		max_depth=parameters['max_depth'],
		min_samples_split=parameters['min_samples_split'],
		min_samples_leaf=parameters['min_samples_leaf'],
		max_features=parameters['max_features'],
		bootstrap=parameters['bootstrap'],
		n_jobs=1)

	algo.fit(X=train_X, y=train_y.values.ravel())

	return np.sqrt(mse(algo.predict(valid_X), valid_y.values))"""

default_eval_method_dict['sklearn_random_forest_regressor_mse'] = [sklearn_random_forest_eval_method_mse, sklearn_random_forest_eval_method_mse_str]

