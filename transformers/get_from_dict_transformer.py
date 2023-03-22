import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin
from typing import Dict


class GetFromDictTransformer(BaseEstimator, TransformerMixin):
    """
    returns requires entry from the dict.
    """
    def __init__(self, target: str) -> None:
        self.target = target
    

    def fit(self, X, y=None):
        return self
    
    def transform(self, X, y=None):
        result = None
        if type(X) == dict:
            result = X[self.target]
        else:
            result = X
        return result