import pandas as pd

from config import experience_levels
from technologies_analysis.utils import visualize_technologies


vacancies_df = pd.read_csv("technologies_scraper/vacancies.csv")

for level in experience_levels:
    visualize_technologies(vacancies_df, level)
