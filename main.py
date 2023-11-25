import pandas as pd

from config import experience_levels
from technologies_analysis.utils import (
    add_experience_column,
    visualize_technologies,
)

vacancies_df = pd.read_csv("technologies_scraper/vacancies.csv")
vacancies_df = add_experience_column(vacancies_df)


for level in experience_levels:
    visualize_technologies(vacancies_df, level)
