import pandas as pd
import os

def get_descriptions_dict():
    csv_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'descriptions.csv')

    if not os.path.exists(csv_path):
        return {}

    try:
        df = pd.read_csv(csv_path)

        descriptions = {}
        for _, row in df.iterrows():
            class_name = row['Class_Name']
            common_name = row.get('Common_Name', '')
            desc = row.get('Description', '')
            habitat = row.get('Habitat', '')
            size = row.get('Average_Size', '')

            full_text = f"Name: {common_name}\nDescription: {desc}\nHabitat: {habitat}\nAverage Size: {size}"
            descriptions[class_name] = full_text

        return descriptions
    except Exception as e:
        print(f"Could not load descriptions: {e}")
        return {}
