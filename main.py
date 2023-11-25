import pandas as pd

from technologies_analysis.utils import add_experience_column

vacancies_df = pd.read_json("vacancies.json")
vacancies_df = add_experience_column(vacancies_df)
print(vacancies_df.head())
