from sklearn.base import BaseEstimator, TransformerMixin
import pandas as pd

class SeriesFromGroupTransformer(BaseEstimator, TransformerMixin):
    '''
    Makes a new series by grouping by groupby str, and indexing each entry 
    in the new series by indexby.
    '''
    def __init__(self, groupby: str, indexby: str) -> None:
        self.groupby = groupby
        self.indexby = indexby
    

    def fit(self, X, y=None):
        return self
    
    def transform(self, X, y=None):
        return pd.Series({game_id: turns.set_index(self.indexby) for game_id, turns in X.groupby(self.groupby)})