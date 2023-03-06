import pandas as pd
from typing import Callable, Dict
from sklearn.base import BaseEstimator, TransformerMixin
from transformers.columns_setter_transformer import ColumnsSetterTransformer

class ExtractSetColumnsTransformer(BaseEstimator, TransformerMixin):
    """
    A transformer that extracts data series from df using using given extractors and assignes them to the df.
    if src and dest are both not none, that treats X as a dictionary, extracts info from src and assignes to dest.
    """
    def __init__(self, extarctors: Dict[str, Callable[[pd.DataFrame], pd.Series]], src: str = None, dest: str = None) -> None:
        self.extarctors = extarctors
        self.src = src
        self.dest = dest 
    
    def transform(self, X, y=None):
        result = None
        if self.src != None and self.dest !=None:
            arg_src = X[self.src]
        else:
            arg_src = X

        columns = {}
        for name in self.extarctors:
            columns[name] = self.extarctors[name](arg_src)

        if self.src != None and self.dest !=None:
            result = X.copy()
            result[self.dest] = ColumnsSetterTransformer(columns).transform(X[self.dest])
        else:
            result = ColumnsSetterTransformer(columns).transform(X)

        return result