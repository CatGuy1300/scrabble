from sklearn.pipeline import Pipeline
from typing import Dict, Any, List, Union, Iterator
import pandas as pd
from sklearn.model_selection import GridSearchCV
from sklearn.base import clone


Regressor = Any
ParamGrid = Dict[str, List[Any]]
Scores = Iterator[Any]

class Searcher:
    def __init__(self, pipe: Pipeline, grid: Dict[str, Dict[str, Union[ParamGrid, Scores, Regressor]]],  
                 n_jobs: int = None, redo_scores = True) -> None:
        self.pipe = pipe
        self.grid = grid
        self.n_jobs = n_jobs
        self.result_searchers = {}
        self.redo_scores = redo_scores

    def search(self, X: pd.DataFrame, y: pd.Series) -> None:
        return self.__search_y(X, y) if self.redo_scores else self.__search_n(X, y)

    def __search_y(self, X: pd.DataFrame, y: pd.Series) -> None:
        for name in self.grid:
            pipe = clone(self.pipe)
            pipe.steps.append((name, self.grid[name]['estimator']))
            grid = self.__add_prefix(self.grid[name]['param_grid'], name)
            for score in self.grid[name]['scores']:
                gcv = GridSearchCV(pipe, grid, n_jobs=self.n_jobs, scoring=score)
                gcv.fit(X, y)
                self.result_searchers[(name, score)] = gcv

    
    def __search_n(self, X: pd.DataFrame, y: pd.Series) -> None:
        for name in self.grid:
            pipe = clone(self.pipe)
            pipe.steps.append((name, self.grid[name]['estimator']))
            grid = self.__add_prefix(self.grid[name]['param_grid'], name)
            gcv = GridSearchCV(pipe, grid, n_jobs=self.n_jobs, scoring=self.grid[name]['scores'], refit=False)
            gcv.fit(X, y)
            self.result_searchers[name] = gcv
    
    def get_results(self) -> Iterator[GridSearchCV]:
        return self.result_searchers
            

    def __add_prefix(self, grid: ParamGrid, name: str) -> ParamGrid:
        return {f'{name}__{param}': grid[param] for param in grid}



    
