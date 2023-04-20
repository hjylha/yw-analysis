
import numpy as np
import pandas as pd

from constants import habit_path, habit_cols_path


def ask_for_inclusion(name):
    # while True:
    ans = input(f"Include {name}? (y/n) ")
    if ans.lower() == "y":
        return True
    return False


def ask_for_inclusion_for_all(list_of_names):
    included_names = []
    for name in list_of_names:
        if ask_for_inclusion(name):
            included_names.append(name)
    return included_names


if __name__ == "__main__":
    habits_df = pd.read_csv(habit_path)
    cols = ask_for_inclusion_for_all(habits_df.columns)
    print(cols)
    with open(habit_cols_path, "w") as f:
        f.write(",".join(cols))
        
