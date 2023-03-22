from typing import Iterable
import pandas as pd

class IsBotExtarctor:
    """
    Extarcts a seires mappimg game_id corresponding to
    name (meaning there could be duplicated game_ids) to wether it is a bot
    """
    def __init__(self, bot_names: Iterable[str], name_col='nickname', neg=False) -> None:
        self.bot_names = bot_names
        self.name_col = name_col
        self.neg = neg

    def __call__(self, data: pd.DataFrame) -> pd.Series:
        result = data[self.name_col].isin(self.bot_names)
        if(self.neg):
            result = ~result
        return result