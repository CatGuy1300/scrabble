from typing import List
from typing import Union

from sklearn.base import BaseEstimator, TransformerMixin
import pandas as pd

class SelectTransformer(BaseEstimator, TransformerMixin):
    def __init__(self, selection: Union[List[str], pd.Series]) -> None:
        self.selection = selection
    

    def fit(self, X, y=None):
        return self
    
    def transform(self, X, y=None):
        return X[self.selection]