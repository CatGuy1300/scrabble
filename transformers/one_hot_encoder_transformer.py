from typing import List
from sklearn.base import BaseEstimator, TransformerMixin
import pandas as pd

class OneHotEncoderTransformer(BaseEstimator, TransformerMixin):
    def __init__(self, columns: List[str]) -> None:
        self.columns = columns
    

    def fit(self, X, y=None):
        return self
    
    def transform(self, X, y=None):
        for column in self.columns:
            dummies = pd.get_dummies(X[column], prefix=column, dummy_na=True)
            X = X.merge(dummies, left_index=True, right_index=True)
        return X