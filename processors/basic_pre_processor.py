import pandas as pd
from sklearn.pipeline import Pipeline
from typing import Union, Tuple


class BasicPreProcessor:
    """
    Preprocesses the data using given pipleline, games and turns dfs.
    Assumes that pipline returns dict contained processed games, turns, train dfs.
    
    returns proccesed games, turns and ratings.
    """
    def __init__(self, pipeline: Pipeline, games: pd.DataFrame, turns: pd.DataFrame, g_name: str = 'games', t_name: str = 'turns') -> None:
        self.pipeline = pipeline
        self.games = games
        self.turns = turns
        self.g_name = g_name
        self.t_name = t_name

    
    def process(self, data: Union[pd.DataFrame, pd.Series], data_name: str) -> Tuple[pd.DataFrame, pd.DataFrame, pd.Series]:
        new_data_dict = self.pipeline.transform({data_name: data, self.g_name: self.games, self.t_name: self.turns})
        new_data_dict[self.g_name]['score'] = new_data_dict[data_name]['score']
        return new_data_dict[self.g_name], new_data_dict[self.t_name], new_data_dict[data_name]['rating']