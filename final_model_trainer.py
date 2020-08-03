'''
Outputs a model trained on all of the data.
@author: Timothy Wu, William Zhang  
'''
#imports
import pandas as pd
import numpy as np
import os
import datetime
import xgboost as xgb
import sklearn
from xgboost.sklearn import XGBClassifier
from sklearn import metrics
from sklearn.model_selection import cross_validate
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
from numpy import sort
from sklearn.feature_selection import SelectFromModel
from sklearn.preprocessing import StandardScaler
# Optimal Parameters: {'objective': 'binary:logistic', 'base_score': 0.5, 'booster': 'gbtree', 'colsample_bylevel': 1, 'colsample_bynode': 1, 'colsample_bytree': 0.6, 'gamma': 0.0, 'gpu_id': -1, 'importance_type': 'gain', 'interastraints': '', 'learning_rate': 0.01, 'max_delta_step': 0, 'max_depth': 3, 'min_child_weight': 4, 'missing': nan, 'monotone_constraints': '()', 'n_estimators': 2340, 'n_jobs': 0, 'num_parallel_tree': 1, 'random_state': _alpha': 0.1, 'reg_lambda': 100, 'scale_pos_weight': 1, 'subsample': 0.85, 'tree_method': 'exact', 'validate_parameters': 1, 'verbosity': None, 'seed': 812}

def to_int(num):
    return int(num)


df = pd.read_csv("updatedtrainingdata.csv")
#df = pd.read_csv("trainingdata50minutes20102020.csv", encoding='utf-8')
#df = df.drop(df.index[0])
#df = df.drop(["GameID"], axis=1)
y = df['Homewin']
features = list(df.columns[1:-1])
X = df[features]
y = y.apply(to_int)

model = XGBClassifier(
                max_depth=3,
                learning_rate=0.01,
                verbosity=None, # might throw an error, just put it as 0 if it does
                objective= 'binary:logistic',
                booster='gbtree',
                tree_method='exact',
                n_jobs=0,
                gamma=0.0,
                min_child_weight=4,
                max_delta_step=0,
                subsample=.85, 
                colsample_bytree=0.6,
                colsample_bynode=1,
                reg_alpha=0.1,
                reg_lambda=100,
                scale_pos_weight=1,
                base_score=0.5,
                random_state=812)

model = model.fit(X, y, eval_metric='auc')

'''
thresh = 0.01702188141644001

selection = SelectFromModel(model, threshold=thresh, prefit=True)
select_X = selection.transform(X)


model = XGBClassifier(
                max_depth=3,
                learning_rate=0.01,
                verbosity=None, # might throw an error, just put it as 0 if it does
                objective= 'binary:logistic',
                booster='gbtree',
                tree_method='exact',
                n_jobs=0,
                gamma=0.0,
                min_child_weight=4,
                max_delta_step=0,
                subsample=.85, 
                colsample_bytree=0.6,
                colsample_bynode=1,
                reg_alpha=0.1,
                reg_lambda=100,
                scale_pos_weight=1,
                base_score=0.5,
                random_state=812)

model = model.fit(select_X, y, eval_metric='auc')
'''

model.save_model('FULLNBAMODEL2010-2020test.model')
print("model complete")