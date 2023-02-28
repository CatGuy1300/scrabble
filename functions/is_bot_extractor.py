from typing import Iterable
import pandas as pd

class IsBotExtarctor:
    """
    A class that extarcts a seires mappimg game_id corresponding to
    name (meaning there could be duplicated game_ids) to wether it is a bot
    """
    def __init__(self, bot_names: Iterable[str]) -> None:
        self.bot_names = bot_names
    

    def __call__(self, data: pd.DataFrame) -> pd.Series:
        name_col = 'nickname'
        return data[name_col].isin(self.bot_names)