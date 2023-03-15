from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.feature_selection import SelectFromModel
from xgboost import XGBRegressor

class SelectFeaturesWrapper(BaseEstimator, TransformerMixin):
 
    def __init__(self, regressor: XGBRegressor, threshold=None) -> None:
        self.regressor = regressor
        self.threshold = threshold
    

    def fit(self, X, y=None):
        return self
    
    def transform(self, X, y=None):
        selection = SelectFromModel(self.regressor, threshold=self.threshold, prefit=True)
        return selection.transform(X)