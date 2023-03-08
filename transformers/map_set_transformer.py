import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin
from typing import Dict, Callable, Tuple
from transformers.columns_setter_transformer import ColumnsSetterTransformer


class MapSetTransformer(BaseEstimator, TransformerMixin):
    def __init__(self, columns: Dict[str, Tuple[Callable[[any], any], str]], target: str = None) -> None:
        self.columns = columns
        self.target = target
    

    def fit(self, X, y=None):
        return self
    
    def transform(self, X, y=None):
        result = None
        if self.target != None:
            result = X.copy()
            result[self.target] = ColumnsSetterTransformer({new_col: lambda df, mapper=mapper, old_col=old_col: df[old_col].apply(mapper)
                                         for new_col, (mapper, old_col) in self.columns.items()}).transform(X[self.target])
        else:
            result = ColumnsSetterTransformer({new_col: lambda df, mapper=mapper, old_col=old_col: df[old_col].apply(mapper)
                                         for new_col, (mapper, old_col) in self.columns.items()}).transform(X)
        return result