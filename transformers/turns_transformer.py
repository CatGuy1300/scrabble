
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.pipeline import Pipeline
from typing import Dict, Callable
import pandas as pd

mapping = Callable[[pd.DataFrame], pd.Series]

class TurnsTransformer(BaseEstimator, TransformerMixin):
    def __init__(self, initial_pipe: Pipeline=None, mappers: Dict[str, mapping]=None) -> None:
        self.initial_pipe=initial_pipe
        self.mappers=mappers


    def fit(self, X, y=None):
        return self
    

    def transform(self, X, y=None):
        if self.initial_pipe:
            X = self.initial_pipe.transform(X)
        if self.mappers:
            result = pd.DataFrame(index=X.index.unique())
            for mapping in self.mappers:
                result[mapping] = self.mappers[mapping](X)
            X = result
        return X
    