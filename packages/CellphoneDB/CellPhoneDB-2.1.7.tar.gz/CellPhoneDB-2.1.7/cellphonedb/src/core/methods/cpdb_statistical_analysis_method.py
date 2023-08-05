import pandas as pd

from cellphonedb.src.core.methods import cpdb_statistical_analysis_complex_method


def call(meta: pd.DataFrame,
         count: pd.DataFrame,
         counts_data: str,
         interactions: pd.DataFrame,
         genes: pd.DataFrame,
         complex_expanded: pd.DataFrame,
         complex_composition: pd.DataFrame,
         iterations: int,
         threshold: float,
         threads: int,
         debug_seed: int,
         result_precision: int,
         pvalue: float,
         separator: str
         ) -> (pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame):

    pvalues, means, significant_means, deconvoluted = \
        cpdb_statistical_analysis_complex_method.call(meta.copy(),
                                                      count.copy(),
                                                      counts_data,
                                                      interactions,
                                                      genes,
                                                      complex_expanded,
                                                      complex_composition,
                                                      pvalue,
                                                      separator,
                                                      iterations,
                                                      threshold,
                                                      threads,
                                                      debug_seed,
                                                      result_precision,
                                                      )


    max_rank = significant_means['rank'].max()
    significant_means['rank'] = significant_means['rank'].apply(lambda rank: rank if rank != 0 else (1 + max_rank))
    significant_means.sort_values('rank', inplace=True)

    return deconvoluted, means, pvalues, significant_means
