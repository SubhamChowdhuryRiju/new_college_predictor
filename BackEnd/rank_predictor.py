import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split

rvp = pd.read_csv('BackEnd/rvp_cleaned.csv')
# print('Create regressors', flush=True)


def create_regressor(rvp_):
    X = rvp_['PERCENTILE'].values.reshape(-1, 1)
    y = rvp_['RANK'].values.reshape(-1, 1)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)
    regressor = LinearRegression()
    regressor.fit(X_train, y_train)
    return regressor


categories = ['GEN', 'EWS', 'SC', 'ST', 'OBC-NCL']
regressors = {
    category: [
        create_regressor(rvp[rvp['CATEGORY'] == category]),
        create_regressor(rvp[rvp['CATEGORY'] == category + '-PwD'])
    ] for category in categories
}


def pvr(perc, pwd, category):
    x = pd.Series([perc])
    z = regressors[category][pwd == 'YES'].predict(x.values.reshape(-1, 1))
    k = float(np.round(z[0]))
    if k <= 0:
        k = 13
    return k


# print(pvr(78.2, 'NO', 'GEN'))
