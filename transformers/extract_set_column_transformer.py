import pandas as pd
from typing import Callable, Dict
from sklearn.base import BaseEstimator, TransformerMixin
from transformers.columns_setter_transformer import ColumnsSetterTransformer

class ExtractSetColumnsTransformer(BaseEstimator, TransformerMixin):
    def __init__(self, extarctors: Dict[str, Callable[[pd.DataFrame], pd.Series]]) -> None:
        self.extarctors = extarctors 
    
    def transform(self, X, y=None):
        columns = {}
        for name in self.extarctors:
            columns[name] = self.extarctors[name](X)
        return ColumnsSetterTransformer(columns).transform(X)