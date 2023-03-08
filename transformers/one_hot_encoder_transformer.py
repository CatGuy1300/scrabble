from typing import List
from sklearn.base import BaseEstimator, TransformerMixin
import pandas as pd

class OneHotEncoderTransformer(BaseEstimator, TransformerMixin):
    def __init__(self, columns: List[str], target: str = None) -> None:
        self.columns = columns
        self.target = target
    

    def fit(self, X, y=None):
        return self
    
    def transform(self, X, y=None):
        result = None
        arg_target = None
        if self.target != None:
            arg_target = X[self.target]
        else:
            arg_target = X
    
        for column in self.columns:
            dummies = pd.get_dummies(arg_target[column], prefix=column, dummy_na=True)
            arg_target = arg_target.merge(dummies, left_index=True, right_index=True)

        if self.target != None:
            result = X.copy()
            result[self.target] = arg_target
        else:
            result = arg_target
        
        return result
    