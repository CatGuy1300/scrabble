from collections.abc import Iterable
import pandas as pd

class BotExtarctor:
    def __init__(self, bot_names: Iterable[str]) -> None:
        self.bot_names = bot_names
    

    def __call__(self, data: pd.DataFrame) -> pd.Series:
        name_col = 'nickname'
        bots = {}
        for _, game in data.iterrows():
            if game[name_col] in self.bot_names:
                bots[game.name] = game[name_col]
        return pd.Series(bots)