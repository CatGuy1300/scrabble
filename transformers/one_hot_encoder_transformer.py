from typing import List, Dict, Iterable
from sklearn.base import BaseEstimator, TransformerMixin
import pandas as pd

class OneHotEncoderTransformer(BaseEstimator, TransformerMixin):
    """
    add one hot encoding to columns in columns dict.
    The values used for encoding are the values in the series + the values in the dict.

    If target in not none, treats X as a dict.

    Note that indexes of X should be non negative.
    """
    def __init__(self, columns: Dict[str, Iterable[str]], target: str = None) -> None:
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
            # creates seris eith neg indexes, so when contacting won't have dups indexes
            values = pd.Series(self.columns[column],
                                index=(-x-1 for x in range(len(self.columns[column]))))
            
            dummies = pd.get_dummies(pd.concat([arg_target[column], values]), prefix=column, dummy_na=True)
            arg_target = arg_target.merge(dummies, left_index=True, right_index=True)

        if self.target != None:
            result = X.copy()
            result[self.target] = arg_target
        else:
            result = arg_target
        
        return result
    