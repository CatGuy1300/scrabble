from typing import List
from sklearn.base import BaseEstimator, TransformerMixin

class NameDropperTransformer(BaseEstimator, TransformerMixin):
    def __init__(self, columns: List[str]) -> None:
        self.columns = columns
    

    def fit(self, X, y=None):
        return self
    
    def transform(self, X, y=None):
        return X.drop(columns=self.columns)