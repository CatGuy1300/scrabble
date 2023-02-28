import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin
from typing import Dict


class ColumnsSetterTransformer(BaseEstimator, TransformerMixin):
    def __init__(self, columns: Dict[str, pd.Series]) -> None:
        self.columns = columns
    

    def fit(self, X, y=None):
        return self
    
    def transform(self, X, y=None):
        for name in self.columns:
            X = X.assign(**{name: self.columns[name]})
        return X