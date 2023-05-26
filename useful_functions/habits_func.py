
from itertools import combinations

import pandas as pd

# get different types of columns from a text
def get_column_modifiers(text):
    dict_of_column_types = dict()
    listable_column_types = ["drop", "yes-no", "classification"]
    lines = text.split("\n")
    column_type = None
    column = None
    for line in lines:
        l = line.strip()
        if "### " in l:
            column_type = l.split(" ")[-1]
            if column_type in listable_column_types and dict_of_column_types.get(column_type) is None:
                dict_of_column_types[column_type] = []
            else:
                dict_of_column_types[column_type] = dict()
        if l and "#" not in l and "=" not in l:
            column = l
            if column_type in listable_column_types:
                dict_of_column_types[column_type].append(column)
            else:
                if dict_of_column_types[column_type].get(column) is None:
                    dict_of_column_types[column_type][column] = dict()
        if "=" in l and "#" not in l:
            key, item = l.split("=")
            try:
                dict_of_column_types[column_type][column][key] = float(item)
            except ValueError:
                dict_of_column_types[column_type][column][key] = float("nan")

    return dict_of_column_types


def read_column_modifiers(path):
    with open(path, "r") as f:
        text = f.read()
    return get_column_modifiers(text)


def modify_values_using_dict(habit_df, column_dict):
    for column, replacements in column_dict.items():
        habit_df[column] = habit_df[column].replace(replacements)
    return habit_df


def add_classifier_columns(habit_df, list_of_class_columns):
    for column in list_of_class_columns:
        values = habit_df[column].dropna().unique()
        col_index = habit_df.columns.get_loc(column)
        for value in values:
            habit_df.insert(
                col_index, f"{column}_{value}", habit_df.apply(
                    lambda r: 1 if r[column] == value else 0, axis=1))
        habit_df = habit_df.drop(column, axis=1)
    return habit_df


# turn yes or no values to 1 or 0 (and "i dont know" to nan)
def modify_yes_no_columns(habit_df, yes_no_columns):

    habit_df.loc[:, yes_no_columns] = habit_df.loc[:, yes_no_columns].replace(
        {"no": 0, "yes": 1, "i-dont-know": float("nan")})

    return habit_df


def modify_rate_column_value(rate_col_value, replacement_col_value):
    try:
        int(rate_col_value)
        return rate_col_value
    except ValueError:
        if replacement_col_value == 0:
            return replacement_col_value
        return float("nan")


def modify_leak_rate_columns(habit_df):
    cols = [
        "Shower-Leak",
        "Toilet-Leak",
        "Basin-Tap-Leak",
        "Bath-Tap-Leak",
        "Kitchen-Tap-Leak"]
    for col in cols:
        rate_col = f"{col}-Rate"
        habit_df[rate_col] = habit_df.loc[:, [col, rate_col]].apply(
            lambda r: modify_rate_column_value(r[rate_col], r[col]), axis=1)
        habit_df.drop(col, inplace=True, axis=1)
    return habit_df


# try to measure impact of different columns in model.fit(X, Y)
def get_column_impact_df(model, X):
    columns_with_impact = []
    for col, coef in zip(X.columns, model.coef_):
        columns_with_impact.append({"column": col,
                                    "mean_impact": abs(X[col].mean() * coef),
                                    "max_impact": abs(coef) * (X[col].max() - X[col].min())})
    return pd.DataFrame(columns_with_impact)
    # return pd.DataFrame(columns_ordered).sort_values("mean_impact", ascending=False)


def fit_models_based_on_score(model, X_train, X_test, Y_train, Y_test, up_to=10):
    final_cols = []
    max_score = 0
    cols_to_check = X_train.columns
    not_done = True
    while not_done:
        not_done = False
        next_col = None
        for col in cols_to_check:
            cols = final_cols + [col]
            model.fit(X_train.loc[:, cols], Y_train)
            score = model.score(X_test.loc[:, cols], Y_test)
            if score > max_score:
                next_col = col
                max_score = score
                not_done = True
        if next_col is not None:
            final_cols.append(next_col)
        if len(final_cols) >= up_to:
            not_done = False

    return final_cols


# key = max or mean
def fit_models_based_on_impact(model, X_orig, Y, key="max"):
    impact_col = f"{key}_impact"
    results = []
    X = X_orig.copy()
    while list(X.columns):
        model.fit(X, Y)
        results.append({"columns": list(X.columns), "num_of_columns": len(X.columns), "score": model.score(X, Y)})
        impact_df = get_column_impact_df(model, X).sort_values(impact_col, ascending=False)
        X.drop(impact_df["column"].iloc[-1], axis=1, inplace=True)
    return pd.DataFrame(results).set_index("num_of_columns")


# fit(X[...], Y), where X is restricted to k columns
def fit_models_w_k_columns(model, X, Y, k):
    col_collections = combinations(X.columns, k)
    max_score = 0.26
    best_cols = None
    for cols in col_collections:
        model.fit(X.loc[:, list(cols)], Y)
        score = model.score(X.loc[:, list(cols)], Y)
        if score > max_score:
            # print(f"{score} > {max_score}: {cols} = {best_cols}")
            max_score = score
            best_cols = cols
    return (best_cols, max_score)


# waste time fitting models
def fit_everything(model, X, Y, up_to=2):
    up_to = min(up_to, len(X.columns))
    results = []
    for k in range(1, up_to + 1):
        cols, score = fit_models_w_k_columns(model, X, Y, k)
        results.append({"num_of_columns": k, "columns": cols, "score": score})
    return pd.DataFrame(results).set_index("num_of_columns")
