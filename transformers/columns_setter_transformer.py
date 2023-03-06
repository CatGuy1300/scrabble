import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin
from typing import Dict, Union, Callable


class ColumnsSetterTransformer(BaseEstimator, TransformerMixin):
    """
    set the given columns using the given data seires/map.
    If target is not None then treats X as a dictionary and activates on target entry.
    """
    def __init__(self, columns: Dict[str, Union[pd.Series, Callable[[pd.DataFrame], pd.Series]]], target: str = None) -> None:
        self.columns = columns
        self.target = target
    

    def fit(self, X, y=None):
        return self
    
    def transform(self, X, y=None):
        result = None
        if self.target != None:
            result = X.copy()
            result[self.target] = X[self.target].assign(**self.columns)
        else:
            result = X.assign(**self.columns)
        return result