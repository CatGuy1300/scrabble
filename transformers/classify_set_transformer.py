import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.model_selection import train_test_split


class ClassifySetTransformer(BaseEstimator, TransformerMixin):
    """
    set the given columns using the given data seires/map.
    If target is not None then treats X as a dictionary and activates on target entry.
    """
    def __init__(self, classfier, column:str, threshold=1600,  prefit=False) -> None:
        self.classfier = classfier
        self.column = column
        self.threshold = threshold
        self.prefit = prefit

    

    def fit(self, X, y=None):
        if not self.prefit:
            train_x, _, train_y, _ = train_test_split(X, y, test_size=0.95, random_state=42)

            self.classfier.fit(train_x, (train_y < self.threshold).astype(int))
        return self
    
    def transform(self, X, y=None):
        return X.assign(**{self.column: self.classfier.predict(X).astype(int)})