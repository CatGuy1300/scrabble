import pandas as pd
from sklearn.pipeline import Pipeline
from processors.basic_pre_processor import BasicPreProcessor

class PreprocessorBuilder:
    def __init__(self, 
                 games: pd.DataFrame, g_name: str,
                 turns: pd. DataFrame, t_name: str, 
                 preprocessPipe: Pipeline,) -> None:
        self.games = games
        self.g_name = g_name
        self.turns = turns
        self.t_name = t_name
        self.preprocessPipe = preprocessPipe
    

    def build(self) -> BasicPreProcessor:
        return self.__build_preprocessor()
    
    def __build_preprocessor(self) -> BasicPreProcessor:
        return BasicPreProcessor(self.preprocessPipe, self.games, self.turns, self.g_name, self.t_name)
