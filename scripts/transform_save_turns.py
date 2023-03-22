import pandas as pd
from sklearn.pipeline import Pipeline
import sys
from os.path import normpath, join, dirname
sys.path.append(normpath(join(dirname(__file__), '..'))) # add scrabble folder to path so import will work

from transformers.extract_set_column_transformer import ExtractSetColumnsTransformer
from transformers.select_by_index_transformer import SelectByIndexTransformer
from transformers.my_turns_transformation import MyTurnsTransformation
from transformers.select_by_mask_transformer import SelectByMaskTransformer

from functions.is_bot_extractor import IsBotExtarctor

from builders.preprocessor_builder import PreprocessorBuilder


'''
arg1: games path
arg2: train path
arg3: turns path
arg4: path to save to
'''
if __name__ == "__main__":
    games = pd.read_csv(sys.argv[1], index_col='game_id')
    train = pd.read_csv(sys.argv[2], index_col='game_id')
    turns = pd.read_csv(sys.argv[3], index_col='game_id')

    G_NAME = 'games'
    T_NAME = 'turns'
    DATA_NAME = 'train'

    names = ['BetterBot', 'STEEBot', 'HastyBot']

    prePipe = Pipeline([
                        ('get_relavent_turns', SelectByIndexTransformer(train.index.unique(), target=T_NAME)),
                        ('get_relavent_games',  SelectByIndexTransformer(train.index.unique(), target=G_NAME)),
                        ('train_set_is_player', ExtractSetColumnsTransformer({'is_player': IsBotExtarctor(names, 'nickname', True)},
                                                                            src=DATA_NAME, dest=DATA_NAME)),
                        ('get_bot_rating', ExtractSetColumnsTransformer({'bot_rating': lambda train: train[~train['is_player']]['rating']},
                                                                        src=DATA_NAME, dest=G_NAME)),
                        ('get_bots_names', ExtractSetColumnsTransformer({'bot_name': lambda train: train[~train['is_player']]['nickname']},
                                                                        src=DATA_NAME, dest=G_NAME)),
                        ('data_drop_bot_rating', SelectByMaskTransformer('is_player', target=DATA_NAME)),
                        ])
    preprocessor = PreprocessorBuilder(games, G_NAME, turns, T_NAME, prePipe).build()
    n_games, n_turns, n_ratings = preprocessor.process(train, DATA_NAME)
    t_turns = MyTurnsTransformation().transform(n_turns)
    t_turns.to_csv(sys.argv[4], index_label='game_id')
