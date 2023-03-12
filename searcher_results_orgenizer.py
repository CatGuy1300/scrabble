import pandas as pd
from typing import Dict, Tuple, Set
from sklearn.model_selection import GridSearchCV


class SearcherResultsOrgenizer:
    def __init__(self, redo_scores = True) -> None:
        self.redo_scores = redo_scores
        
    def orgenize(self, gcvs: Dict[Tuple[str, str], GridSearchCV]) -> pd.DataFrame:
        gcvs_df = self.__to_df_y(gcvs) if self.redo_scores else self.__to_df_n(gcvs)
        orgenized = self.__remove_all_redundent(gcvs_df)
        orgenized = orgenized.set_index(['model_name', 'scorer'] if self.redo_scores else ['model_name'])
        return orgenized.drop(columns=['params', 'rank_test_score'] if self.redo_scores else ['params'])


    def __to_df_y(self, gcvs: Dict[Tuple[str, str], GridSearchCV]) -> pd.DataFrame:
        list = []
        for name, scorer in gcvs:
            results = pd.DataFrame(gcvs[(name, scorer)].cv_results_)
            results['model_name'] = name
            results['scorer'] = scorer
            list.append(results)
        return pd.concat(list, ignore_index=True)
    
    
    def __to_df_n(self, gcvs: Dict[Tuple[str, str], GridSearchCV]) -> pd.DataFrame:
        list = []
        for name in gcvs:
            results = pd.DataFrame(gcvs[name].cv_results_)
            results['model_name'] = name
            list.append(results)
        return pd.concat(list, ignore_index=True)
    
    def __get_params(self, ds: pd.Series) -> Set:
        return {param.split('__')[1] for dict in ds.values for param in dict}

    
    def __remove_all_redundent(self, df: pd.DataFrame) -> pd.DataFrame:
        for param in self.__get_params(df['params']):
            df = self.__remove_reduntent(df, param)
        return df

    def __remove_reduntent(self, df: pd.DataFrame, name: str) -> pd.DataFrame:
        rel = []
        for column in df.columns:
            if column.endswith(name):
                rel.append(df[column])
                df = df.drop(columns=column)
        new_col = pd.concat(rel)
        df[name] = new_col[~new_col.astype(str).isin(['NaN', 'nan'])] # drop values that are NaN but doesn't drop None
        return df