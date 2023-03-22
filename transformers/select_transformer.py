from typing import List
from typing import Union

from sklearn.base import BaseEstimator, TransformerMixin
import pandas as pd

class SelectTransformer(BaseEstimator, TransformerMixin):
    """
    Selects given columns/rows corresponding to boolian data seires (should be with same number of rows as the transform target)
    """
    def __init__(self, selection: Union[List[str], pd.Series], target: str = None) -> None:
        self.selection = selection
        self.target = target
    

    def fit(self, X, y=None):
        return self
    
    def transform(self, X, y=None):
        result = None
        if self.target != None:
            result = X.copy()
            result[self.target] = X[self.target][self.selection]
        else:
            result = X[self.selection]
        return result