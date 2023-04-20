
from pathlib import Path

daily_path = Path(__file__).parent.parent / "data" / "Daily m3 1315.csv"
habit_path = Path(__file__).parent.parent / "data" / "Yorkshire Water consumer habits.csv"

habit_cols_path = Path(__file__).parent.parent / "data" / "habits_columns.csv"
habit_mod_path = daily_path = Path(__file__).parent.parent / "data" / "habits_column_modifiers.txt"
