import pandas as pd
from typing import Callable, Dict
from transformers.columns_setter_transformer import ColumnsSetterTransformer

class ExtractSetColumnsTransformer(ColumnsSetterTransformer):
    def __init__(self, extarctors: Dict[str, Callable[[pd.DataFrame], pd.Series]]) -> None:
        ColumnsSetterTransformer.__init__(self, {name: None for name in extarctors})
        self.extarctors = extarctors 
    
    def transform(self, X, y=None):
        for name in self.extarctors:
            self.columns[name] = self.extarctors[name](X)
        return ColumnsSetterTransformer.transform(self, X)