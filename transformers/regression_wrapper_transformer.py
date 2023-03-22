import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.model_selection import train_test_split
from xgboost import XGBRegressor, XGBClassifier


class RegressionWrapperTransformer(BaseEstimator, TransformerMixin):
    """
    making regression using "is 1500" mask
    """
    def __init__(self, classfier=XGBClassifier(), regressor=XGBRegressor(), to_classify=1500) -> None:
        self.classfier = classfier
        self.regressor = regressor
        self.to_classify = to_classify

    def fit(self, X, y=None):
        self.regressor.fit(X[y != self.to_classify], y[y != self.to_classify])
        self.classfier.fit(X, y == self.to_classify)
        return self
    
    def transform(self, X, y=None):
        mask = self.classfier.predict(X) == 1
        prediction = self.regressor.predict(X)
        return mask * self.to_classify + (~mask) * prediction
    

    def predict(self, X, y=None):
        return self.transform(X, y)