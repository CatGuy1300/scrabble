import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.pipeline import Pipeline

from functions.is_bot_extractor import IsBotExtarctor

import numpy as np

from tsfresh.feature_extraction import extract_features
from tsfresh.feature_extraction.settings import from_columns
from tsfresh.utilities.dataframe_functions import impute

from transformers.extract_set_column_transformer import ExtractSetColumnsTransformer
from transformers.name_dropper_transformer import NameDropperTransformer
from transformers.map_set_transformer import MapSetTransformer
from transformers.one_hot_encoder_transformer import OneHotEncoderTransformer

class MyTurnsTransformation(BaseEstimator, TransformerMixin): 
    def fit(self, X, y=None):
        return self
    
    def transform(self, X, y=None):
        turns = self.__initial_transformation(X)
        return self.__to_tsfresh_features(turns)
    
    def __initial_transformation(self, X):
        letters = ['Z', 'A', 'I', '.', 'e', 'l']
        turns = X.reset_index()
        names = ['BetterBot', 'STEEBot', 'HastyBot']
        initial_pipe = Pipeline([
                      ('hot', OneHotEncoderTransformer({'turn_type': turns['turn_type'].unique()})),
                      ('count_letters_used',
                        MapSetTransformer({letter: (lambda x, letter=letter: x.count(letter) if type(x) == str else 0, 'move') for letter in letters})),
                      ('turns_word_info_mappers', MapSetTransformer({
                                                                    'move_len': (lambda x: len(x) if type(x) == str else 0, 'move'), 
                                                                    'jokers_num': (lambda x: sum(1 for c in x if c.islower()) if (type(x) == str) and (x not in ['(challenge)', '(time)']) else 0, 'move'),
                                                                     }),),
                      ('set_is_player', ExtractSetColumnsTransformer({'is_player': IsBotExtarctor(names, 'nickname', True)},)), 
                      ('bool_to_int', ExtractSetColumnsTransformer({'is_player': lambda turns: turns['is_player'].astype(int)})),
                      ('drops', NameDropperTransformer(['turn_type', 'nickname', 'move', 'location', 'rack'])),
                    ])
        return initial_pipe.transform(turns)
    
    def __to_tsfresh_features(self, X):
        features = np.load('../feature_selection_consts/columns.npy', allow_pickle=True)

        a_extracted = self.__extract_features(X, features, 'a_')
        p_extracted = self.__extract_features(X[X['is_player']==1], features, 'p_')
        b_extracted = self.__extract_features(X[X['is_player']==0], features, 'b_')
        
        return a_extracted.merge(p_extracted, left_index=True, right_index=True).merge(b_extracted, left_index=True, right_index=True)

    def __extract_features(self, X, features, prefix):
        kind_to_fc_parameters = from_columns([feature for feature in features if feature.startswith(prefix)])
        turns = X.rename(columns={column: prefix + column for column in X.columns})
        extracted = extract_features(turns, kind_to_fc_parameters=kind_to_fc_parameters,
                                column_id=prefix+'game_id', column_sort=prefix+'turn_number')
        impute(extracted)
        return extracted

