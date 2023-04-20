
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
            habit_df.insert(col_index, f"{column}_{value}", habit_df.apply(lambda r: 1 if r[column] == value else 0, axis=1))
        habit_df = habit_df.drop(column, axis=1)
    return habit_df

def modify_yes_no_columns(habit_df, yes_no_columns):
    habit_df.loc[:, yes_no_columns] = habit_df.loc[:, yes_no_columns].replace({"no": 0, "yes": 1, "i-dont-know": float("nan")})
    return habit_df


def modify_rate_column_value(rate_col_value, replacement_col_value):
    try:
        int(rate_col_value)
        return rate_col_value
    except ValueError:
        if replacement_col_value == 0:
            return replacement_col_value
        return float("nan")


def modify_rate_columns(habit_df):
    cols = ["Shower-Leak", "Toilet-Leak", "Basin-Tap-Leak", "Bath-Tap-Leak", "Kitchen-Tap-Leak"]
    for col in cols:
        rate_col = f"{col}-Rate"
        habit_df[rate_col] = habit_df.loc[:, [col, rate_col]].apply(lambda r: modify_rate_column_value(r[rate_col], r[col]), axis=1)
    
    return habit_df


