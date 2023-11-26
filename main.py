import pandas as pd

from config import experience_levels
from technologies_analysis.utils import visualize_technologies_bar_plot, visualize_technologies_pie_chart

vacancies_df = pd.read_csv("technologies_scraper/vacancies.csv")

for level in experience_levels:
    visualize_technologies_bar_plot(vacancies_df, level)

for level in experience_levels:
    visualize_technologies_pie_chart(vacancies_df, level)
