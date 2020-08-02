'''
Given a dataset create a xgboost model and optimize parameters, print out the feature importance after
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

# function that fits the model through cross validation, predicts and prints out the model summary of the model
def modelfit(model, X_train, X_test, y_train, y_test, cv_folds=5, early_stopping_rounds=50, featureimportance=False):
    #get parameters
    xgb_param = model.get_xgb_params()
    #create Data Matrix for xgboost model
    xgtrain = xgb.DMatrix(X_train, label=y_train)
    #cross validate the model and find ideal n_estimators
    cvresult = xgb.cv(xgb_param, xgtrain, num_boost_round=model.get_params()['n_estimators'], nfold=cv_folds, metrics='auc',
                        early_stopping_rounds=early_stopping_rounds, verbose_eval=False)
    #set n_estimators
    model.set_params(n_estimators=cvresult.shape[0])
    #fit the model
    model.fit(X_train, y_train, eval_metric='auc')
    #predict with training and testing data as well as the probability of each happening
    trainpred = model.predict(X_train)
    testpred = model.predict(X_test)
    trainprob = model.predict_proba(X_train)[:,1]
    testprob = model.predict_proba(X_test)[:,1]

    #only print out model report if not checking feature importance
    if not featureimportance:
        print("\nModel Report")
        print(f"Parameters: {model.get_params()}")
        print(f"Accuracy (Train): {metrics.accuracy_score(y_train, trainpred) * 100} %")
        print(f"AUC Score (Train): {metrics.roc_auc_score(y_train, trainprob)}")
        print(f"Accuracy (Test): {metrics.accuracy_score(y_test, testpred) * 100} %")
        print(f"AUC Score (Test): {metrics.roc_auc_score(y_test, testprob)}")
    return model

#function that edits the final output csv for win%, allowing for closer analysis on what went wrong with the model
def savewinprob(model, X, y):
    winprob = model.predict_proba(X)[:,1]
    X['HomeWinProb'] = winprob
    X['HomeWin'] = y
    X['Round'] = winprob.round()
    index = (X['HomeWin'] == X['Round'])
    X['Correct'] = 0
    X.loc[index, ['Correct']] = 1
    X.to_csv('NBAwithWinprob.csv')
    model.save_model('FULLNBAMODEL2010-2020.model')

#gridsearch with given parameters to find best ones
def optimizeparams(initialmodel, params, X_train, y_train):
    gsearch = GridSearchCV(initialmodel, param_grid = params, scoring='roc_auc', n_jobs=4, cv=5)
    gsearch.fit(X_train, y_train)
    print(gsearch.best_params_)
    print(gsearch.best_score_)
    return gsearch.best_estimator_

#iterate through features to print their importance and also how each model does with n features
def featureimportance(model, X_train, X_test, y_train, y_test):
    thresholds = sort(model.feature_importances_)
    bestthresh = 0
    bestN = 0
    bestaccuracy = 0
    for thresh in thresholds:
        # select features using threshold
        selection = SelectFromModel(model, threshold=thresh, prefit=True)
        select_X_train = selection.transform(X_train)
        select_X_test = selection.transform(X_test)
        # train model
        #selection_model = XGBClassifier(model.get_xgb_params())
        selection_model = model
        selection_model = modelfit(selection_model, select_X_train, select_X_test, y_train, y_test, featureimportance=True)
        # eval model
        y_pred = selection_model.predict(select_X_test)
        predictions = [round(value) for value in y_pred]
        accuracy = metrics.accuracy_score(y_test, predictions)
        print(f"Thresh={thresh}, n={select_X_train.shape[1]}, Accuracy: {accuracy*100}%")
        if accuracy > bestaccuracy:
            bestthresh = thresh
            bestN = select_X_train.shape[1]
            bestaccuracy = accuracy

    print(f"Best Run: Thresh={bestthresh}, n={bestN}, Accuracy: {bestaccuracy*100}%")
    '''
    xgb.plot_importance(model, height=2)
    plt.tick_params(axis='y', which='major', labelsize=5)
    plt.show()
    '''

#main function that runs through functions through each hyperparameter
def makemodel(X, y):
    print("started", end="")
    print(datetime.datetime.now())
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, shuffle=False)
    #scale everything
    sc = StandardScaler()
    X_train_temp = sc.fit_transform(X_train)
    X_test_temp = sc.fit_transform(X_test)
    X_train = pd.DataFrame(X_train_temp, columns=X_train.columns)
    X_test = pd.DataFrame(X_test_temp, columns=X_test.columns)
    
    initialmodel = XGBClassifier(
                learning_rate=0.1,
                n_estimators=1000,
                #default 5
                max_depth=5,
                #default 1
                min_child_weight=1,
                #default 0
                gamma=0,
                #default 0.8
                subsample=0.8,
                #default 0.8
                colsample_bytree=0.8,
                #default 0
                reg_alpha=0,
                #default 1
                reg_lambda=1,
                objective= 'binary:logistic',
                scale_pos_weight=1,
                seed=812)

    model = modelfit(initialmodel, X_train, X_test, y_train, y_test)

    #optimize max_depth and min_child_weight
    params = {'max_depth':[3,5,7,9], 'min_child_weight':[1,3,5]}
    model = optimizeparams(model, params, X_train, y_train)
    bestmaxdepth = model.get_params()['max_depth']
    bestminchildweight = model.get_params()['min_child_weight']
    params = {'max_depth':[bestmaxdepth-1, bestmaxdepth, bestmaxdepth+1], 'min_child_weight':[bestminchildweight-1,bestminchildweight,bestminchildweight+1]}
    model = optimizeparams(model, params, X_train, y_train)
    model.set_params(n_estimators=1000)
    model = modelfit(model, X_train, X_test, y_train, y_test)

    #optimize gamma
    params = {'gamma':[i/10.0 for i in range(0,5)]}
    model = optimizeparams(model, params, X_train, y_train)
    bestgamma = model.get_params()['gamma']
    if bestgamma == 0:
        bestgamma = 0.05
    params = {'gamma':[i/100.0 for i in range(int(bestgamma*100-5.0), int(bestgamma*100+10.0), 5)]}
    model = optimizeparams(model, params, X_train, y_train)
    model.set_params(n_estimators=1000)
    model = modelfit(model, X_train, X_test, y_train, y_test)

    #optimize subsample and colsample_bytree
    params = {'subsample':[i/10.0 for i in range(6,10)], 'colsample_bytree':[i/10.0 for i in range(6,10)]}
    model = optimizeparams(model, params, X_train, y_train)
    bestsub = model.get_params()['subsample']
    bestcol = model.get_params()['colsample_bytree']
    params = {'subsample':[i/100.0 for i in range(int(bestsub*100-5.0), int(bestsub*100+10.0), 5)], 
            'colsample_bytree':[i/100.0 for i in range(int(bestcol*100-5.0), int(bestcol*100+10.0), 5)]}
    model = optimizeparams(model, params, X_train, y_train)
    model.set_params(n_estimators=1000)
    model = modelfit(model, X_train, X_test, y_train, y_test)

    #optimize reg_alpha and reg_lambda
    params = {'reg_alpha':[1e-5, 1e-2, 0, 1, 100], 'reg_lambda':[1e-5, 1e-2, 0, 1, 100]}
    model = optimizeparams(model, params, X_train, y_train)
    bestalpha = model.get_params()['reg_alpha']
    bestlambda = model.get_params()['reg_lambda']
    alp = bestalpha
    lamb = bestlambda
    if bestalpha == 0:
        alp = 1
    if bestlambda == 0:
        lamb = 1
    params = {'reg_alpha':[alp/100.0, alp/10.0, bestalpha, alp*10, alp*100], 
                'reg_lambda':[lamb/100.0, lamb/10.0, bestlambda, lamb*10, lamb*100]}
    model = optimizeparams(model, params, X_train, y_train)
    model.set_params(n_estimators=1000)
    model = modelfit(model, X_train, X_test, y_train, y_test)

    #set n_estimators up and learning_rate lower
    model.set_params(n_estimators=5000, learning_rate=0.01)
    model = modelfit(model, X_train, X_test, y_train, y_test)
    savewinprob(model, X, y)

    #check which features are important and print finish time
    featureimportance(model, X_train, X_test, y_train, y_test)
    print("finished", end="")
    print(datetime.datetime.now())

#where things are run
#change this area for different data sets
os.getcwd()

minutes_threshold = [50]

def to_int(num):
    return int(num)
#for min in minutes_threshold:
if True:
    df = pd.read_csv("updatedtrainingdata.csv")
    print(df)
    #df = df.drop(df.index[0])
    #df = df.drop(["GameID"], axis=1)
    y = df['Homewin']
    features = list(df.columns[1:-1])
    X = df[features]
    y = y.apply(to_int)
    makemodel(X, y)