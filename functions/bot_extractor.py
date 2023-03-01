from typing import Iterable
import pandas as pd


class BotExtarctor:
    """
    A class that extarcts a seires mappimg game_id to the bot opponet
    """
    def __init__(self, bot_names: Iterable[str], name_col='nickname') -> None:
        self.bot_names = bot_names
        self.name_col = name_col
    

    def __call__(self, data: pd.DataFrame) -> pd.Series:
        return data[data[self.name_col].isin(self.bot_names)][self.name_col]