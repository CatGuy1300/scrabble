from sklearn.base import BaseEstimator, TransformerMixin
import pandas as pd

class SelectByIndexTransformer(BaseEstimator, TransformerMixin):
    """
    selects the rows corresponding to given indexes.
    if target is not none then treats X as a dict, and selects rows of target.
    """
    def __init__(self, selection: pd.Index, target: str = None) -> None:
        self.selection = selection
        self.target = target
    

    def fit(self, X, y=None):
        return self
    
    def transform(self, X, y=None):
        result = None
        if self.target != None:
            result = X.copy()
            result[self.target] = X[self.target].loc[self.selection, :]
        else: 
            result = X.loc[self.selection, :]
        return result