import pandas as pd
from sklearn.pipeline import Pipeline
import sys
from os.path import normpath, join, dirname


sys.path.append(normpath(join(dirname(__file__), '..'))) # add scrabble folder to path so import will work

from transformers.extract_set_column_transformer import ExtractSetColumnsTransformer
from transformers.select_by_index_transformer import SelectByIndexTransformer
from transformers.select_by_mask_transformer import SelectByMaskTransformer
from transformers.map_set_transformer import MapSetTransformer
from transformers.name_dropper_transformer import NameDropperTransformer
from transformers.turns_transformer import TurnsTransformer
from transformers.one_hot_encoder_transformer import OneHotEncoderTransformer


from functions.is_bot_extractor import IsBotExtarctor

from builders.preprocessor_builder import PreprocessorBuilder

from board_helpers.tiles_counter import TilesCounter
from board_helpers.board_consts import TileType


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
    letters = ['Z', 'A', 'I', '.', 'e', 'l']

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
    

    initial_pipe = Pipeline([
                    ('hot', OneHotEncoderTransformer({'turn_type': turns['turn_type'].unique()})),
                    ('count_letters_used',
                    MapSetTransformer({letter: (lambda x, letter=letter: x.count(letter) if type(x) == str else 0, 'move') for letter in letters})),
                    ('count_tiles_used', 
                    ExtractSetColumnsTransformer(
                        {str(t_type): (lambda turns, t_type=t_type: 
                                       turns.apply(lambda x: 
                                                   TilesCounter(x['location'], x['move'])()[t_type] if type(x['location'])==str and type(x['move'])==str else 0, axis=1)) 
                        for t_type in TileType}
                    )),
                    ('special_tiles', 
                    ExtractSetColumnsTransformer(
                        {'special_type': (lambda turns: turns.apply(lambda x: x['TileType.L2'] + x['TileType.L3'] + x['TileType.W2'] + x['TileType.W3'], axis=1))}
                    )),
                    ('turns_word_info_mappers', MapSetTransformer({'move_len': (lambda x: len(x) if type(x) == str else 0, 'move'), 
                                                                   'jokers_num': (lambda x: sum(1 for c in x if c.islower()) if (type(x) == str) and (x not in ['(challenge)', '(time)']) else 0, 'move'),
                                                    }),),
                    ('set_is_player', ExtractSetColumnsTransformer({'is_player': IsBotExtarctor(names, 'nickname', True)},)), 
                    # ('bool_to_int', ExtractSetColumnsTransformer({'is_player': lambda turns: turns['is_player'].astype(int)})),
                    ('drops', NameDropperTransformer(['turn_type', 'nickname', 'move', 'location', 'rack'])),
                ])
    preprocessor = PreprocessorBuilder(games, G_NAME, turns, T_NAME, prePipe).build()
    n_games, n_turns, n_ratings = preprocessor.process(train, DATA_NAME)
    turns_transformer = TurnsTransformer(
                                            initial_pipe=initial_pipe, 
                                            # mappers=mapings
                                        )
    t_turns = turns_transformer.transform(n_turns)
    t_turns.to_csv(sys.argv[4], index_label='game_id')
