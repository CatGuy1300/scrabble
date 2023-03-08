import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin
from typing import Dict


class AddToDictTransformer(BaseEstimator, TransformerMixin):
    """
    Adds given dfs to X dictionary (if not a dict, make it so)
    """
    def __init__(self, dfs: Dict[str, pd.DataFrame], original: str = 'games') -> None:
        self.dfs = dfs
        self.original = original
    

    def fit(self, X, y=None):
        return self
    
    def transform(self, X, y=None):
        result = None
        if type(X) == dict:
            result = X.copy()
        else:
            result = {self.original: X}
        result.update(self.dfs)
        return result