from typing import List
from typing import Union

from sklearn.base import BaseEstimator, TransformerMixin
import pandas as pd

class SelectByMaskTransformer(BaseEstimator, TransformerMixin):
    """
    Selects given columns/rows corresponding to boolian data seires (should be with same number of rows as the transform target)
    """
    def __init__(self, select_by :str, target: str = None) -> None:
        self.select_by = select_by
        self.target = target
    

    def fit(self, X, y=None):
        return self
    
    def transform(self, X, y=None):
        result = None
        if self.target != None:
            result = X.copy()
            result[self.target] = X[self.target][X[self.target][self.select_by]]
        else:
            result = X[X[self.select_by]]
        return result