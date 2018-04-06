import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

train = pd.read_csv("train.csv")
validation = pd.read_csv("validation.csv")

######### NEGATIVE DOWNSAMPLING ###############
# Negative downsample to try and balance click/non-clicks better in the training data
print("negative downsampling")
from sklearn.utils import resample
majority = train[train.click == 0]
minority = train[train.click == 1]
majorityResampled = resample(majority, replace=False, n_samples=400000)
train = pd.concat([minority, majorityResampled])

fullData = pd.concat([train, validation]).reset_index(drop=True)

# Need to know for the index to split the validation/train data after feature engineering
trainLength = len(train)
del train
del validation

############ DUMMIES #########################
# Columns not wanted for the CTR prediction
columnsToDrop = ['bidid', 'userid', 'IP', 'url', 'urlid', 'slotid', 'keypage', 'bidprice',
                 'click', 'domain']
fullData = fullData.drop(columnsToDrop, axis=1)

# Create dummy variables for these columns
columnsForDummies = ['weekday', 'city', 'hour', 'region', 'slotwidth', 'slotheight', 'advertiser', 'creative',
                     'slotprice', 'adexchange', 'slotformat', 'slotvisibility', 'useragent']

print("creating fullData dummmies")
for i in columnsForDummies:
    print("completing: " + i)
    dummies = pd.get_dummies(fullData[i], prefix=i)
    joined = pd.concat([fullData, dummies], axis=1)
    fullData = joined.drop(i, axis=1)

# Usertag needs some extra work
print("completing: usertag")
fullData['usertag'].fillna(value="null", inplace=True)
usertags = fullData.usertag.str.split(',').tolist()
usertagDf = pd.DataFrame(usertags)
del usertags
usertagDummies = pd.get_dummies(usertagDf,prefix='usertag')
del usertagDf
usertagDummies = usertagDummies.groupby(usertagDummies.columns, axis=1).sum()
fullData = pd.concat([fullData, usertagDummies], axis=1)
fullData = fullData.drop('usertag', axis=1)
print("finished dummies")
del usertagDummies

# Split the train and validation data
train = fullData[0:trainLength]
validation = fullData[trainLength:]
fullData = 0
##########################################


##### SPLIT DATA FOR TRAINING ############
print("X/y preparation")
X_train = train.drop('payprice', axis=1)
y_train = train['payprice']
X_validation = validation.drop('payprice', axis=1)
y_validation = validation['payprice']
train = 0
validation = 0
###########################################


##### TRY DIFFERENT MODELS ################
from sklearn.metrics import explained_variance_score, r2_score
#
from sklearn.linear_model import Lasso
for a in [1, 0.1, 0.01, 0.001, 0.0001]:
    print("fitting lasso (alpha:" + str(a) + "): ")
    lassoModel = Lasso(alpha=a, precompute=True)
    lassoModel.fit(X_train, y_train)
    predictions = lassoModel.predict(X_validation)
    print(explained_variance_score(y_validation, predictions))

from sklearn.svm import LinearSVR
for strength in [100, 10, 1, 0.1, 0.01]:
    print("fitting svr (C:" + str(strength) + "): ")
    svrModel = LinearSVR(C=strength)
    svrModel.fit(X_train, y_train)
    predictions = svrModel.predict(X_validation)
    print(explained_variance_score(y_validation, predictions))
print("finished regression fitting")

lassoModel = Lasso(precompute=True)
lassoModel.fit(X_train, y_train)
predictions = lassoModel.predict(X_validation)
predictionData = pd.DataFrame(data=predictions, columns=['Payprediction'])
predictionData.to_csv("Paypredictions.csv", index=False)
#
# print("saving to disk")
# predictionData = pd.DataFrame(data=predictions, columns=['Payprediction'])
# predictionData.to_csv("Paypredictions.csv", index=False)

# plt.scatter(predictions, y_validation, s=0.1)
# plt.xlabel("predicted payprice")
# plt.ylabel("actual payprice")
# # plt.savefig("lasso")
# plt.show()
