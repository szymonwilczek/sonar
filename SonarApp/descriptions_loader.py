import pandas as pd
import os

def get_descriptions_dict():
    csv_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'description.csv')

    if not os.path.exists(csv_path):
        return {}

    try:
        df = pd.read_csv(csv_path)
        return dict(zip(df['fish_class'], df['description']))
    except Exception as e:
        print(f"Could not load descriptions: {e}")
        return {}
