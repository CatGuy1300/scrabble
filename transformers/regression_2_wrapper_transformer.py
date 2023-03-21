import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.model_selection import train_test_split
from xgboost import XGBRegressor, XGBClassifier


class Regression2WrapperTransformer(BaseEstimator, TransformerMixin):
    """
    making regression using "is 1500" mask
    """
    def __init__(self, classfier=XGBClassifier(), regressor1=XGBRegressor(), regressor2=XGBRegressor(), to_classify=1500) -> None:
        self.classfier = classfier
        self.regressor1 = regressor1
        self.regressor2 = regressor2
        self.to_classify = to_classify

    def fit(self, X, y=None):
        self.regressor1.fit(X[y != self.to_classify], y[y != self.to_classify])
        self.regressor2.fit(X, y)
        self.classfier.fit(X, y == self.to_classify)
        return self
    
    def transform(self, X, y=None):
        mask = self.classfier.predict(X) == 1
        prediction1 = self.regressor1.predict(X)
        prediction2 = self.regressor2.predict(X)
        return mask * prediction2 + (~mask) * prediction1
    

    def predict(self, X, y=None):
        return self.transform(X, y)