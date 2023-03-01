from sklearn.base import BaseEstimator, TransformerMixin
import pandas as pd

class SelectRowsTransformer(BaseEstimator, TransformerMixin):
    def __init__(self, selection: pd.Index) -> None:
        self.selection = selection
    

    def fit(self, X, y=None):
        return self
    
    def transform(self, X, y=None):
        return X.loc[self.selection, :]