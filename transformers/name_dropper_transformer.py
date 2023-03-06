from typing import List
from sklearn.base import BaseEstimator, TransformerMixin

class NameDropperTransformer(BaseEstimator, TransformerMixin):
    """
    Drops given columns.
    If target is not None, treats X as dict and drops columns of target.
    """
    def __init__(self, columns: List[str], target: str = None) -> None:
        self.columns = columns
        self.target = target
    

    def fit(self, X, y=None):
        return self
    
    def transform(self, X, y=None):
        result = None
        if self.target != None:
            result = X.copy()
            result[self.target] = X[self.target].drop(columns=self.columns)
        else:
            result = X.drop(columns=self.columns)
        return result