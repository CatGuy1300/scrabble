import pandas as pd
from sklearn.pipeline import Pipeline
from transformers.add_to_dict_transformer import AddToDictTransformer
from transformers.get_from_dict_transformer import GetFromDictTransformer
from typing import Tuple, List

class RegPipeBuilder:
    def __init__(self, 
                 games: pd.DataFrame, g_name: str,
                 turns: pd. DataFrame, t_name: str, 
                 transformSteps: List[Tuple[str, any]],
                 estimator: any) -> None:
        self.games = games
        self.g_name = g_name
        self.turns = turns
        self.t_name = t_name
        self.transformSteps = transformSteps
        self.estimator = estimator
    

    def build(self) -> Pipeline:
        return self.__build_regPipeline()
    
    def __build_regPipeline(self) -> Pipeline:
        steps = [(f'add_{self.t_name}', AddToDictTransformer({self.t_name: self.turns}))]
        steps.extend(self.transformSteps)
        steps.append((f'get_{self.g_name}', GetFromDictTransformer(self.g_name)))
        steps.append(('estimator', self.estimator))
        return Pipeline(steps)