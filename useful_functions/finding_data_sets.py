

import numpy as np
import pandas as pd

from constants import daily_path


# find indices of columns names (args)
def find_col_indices(df, *args):
    return tuple(df.columns.get_loc(label) for label in args)



def find_largest_contiguous_data(df, start_index=0, end_index=None):
    if end_index is None:
        df_to_look_into = df.iloc[:, start_index:]
        end_index = len(df.columns) - 1
    else:
        df_to_look_into = df.iloc[:, start_index:end_index+1]
    df_to_return = None
    max_values = 0
    full_l = end_index - start_index + 1
    for l in range(full_l, -1, -1):
        if l * len(df_to_look_into) < max_values:
            break
        for s in range(full_l - l + 1):
            curr_df = df_to_look_into.iloc[:, s: s+l].dropna()

            if (num_values := (len(curr_df) * l)) > max_values:
                max_values = num_values
                df_to_return = curr_df
        # print(max_values)
    return df_to_return



if __name__ == "__main__":

    df = pd.read_csv(daily_path)

    # df.info()

    


    # ultimate_df = find_largest_contiguous_data(df, 3, len(df.columns) - 1)
    # ultimate_df.info()
    # Int64Index: 1453 entries, 973 to 2595
    # Columns: 1114 entries, 02/04/2012 to 20/04/2015
    # dtypes: float64(1114)
    # memory usage: 12.4 MB

    df = df[df["DMA"] == 1]

    # df.info()

    ultimate_df = find_largest_contiguous_data(df.iloc[:, 3:])
    ultimate_df.info()
    # Int64Index: 960 entries, 0 to 972
    # Columns: 520 entries, 09/09/2013 to 10/02/2015
    # dtypes: float64(520)
    # memory usage: 3.8 MB

    print(len(ultimate_df))

