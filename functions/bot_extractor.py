from typing import Iterable
import pandas as pd


class BotExtarctor:
    """
    A class that extarcts a seires mappimg game_id to the bot opponet
    """
    def __init__(self, bot_names: Iterable[str]) -> None:
        self.bot_names = bot_names
    

    def __call__(self, data: pd.DataFrame) -> pd.Series:
        name_col = 'nickname'
        return data[data[name_col].isin(self.bot_names)][name_col]