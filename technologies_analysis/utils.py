from datetime import date

import numpy as np
import pandas as pd
from matplotlib import pyplot as plt

from config import possible_technologies, experience_levels


def add_experience_column(data_frame: pd.DataFrame) -> pd.DataFrame:
    default_level, all_levels = experience_levels[0], experience_levels[1:]
    data_frame["experience"] = default_level

    for experience_level in all_levels:
        data_frame["experience"] = np.where(
            (
                data_frame["job_title"].str.contains(
                    experience_level, case=False
                )
            ),
            experience_level,
            data_frame["experience"],
        )

    return data_frame


def count_technologies(
    experience_level: str, data_frame: pd.DataFrame
) -> pd.DataFrame:
    data_frame = data_frame[data_frame["experience"] == experience_level]
    count_of_technologies = pd.DataFrame(columns=["technology", "count"])

    for technology in possible_technologies:
        count = (
            data_frame["job_description"]
            .str.contains(technology, case=False)
            .sum()
        )
        count_of_technologies.loc[len(count_of_technologies)] = {
            "technology": technology,
            "count": count,
        }

    return count_of_technologies


def visualize_technologies(
    vacancies_df: pd.DataFrame, experience_level: str
) -> None:
    technologies = count_technologies(experience_level, vacancies_df)
    technologies.sort_values(by="count", ascending=False)[:10].plot.bar(
        x="technology", y="count", rot=45
    )
    plt.title(f"Top 10 technologies for {experience_level} Python Developer")
    plt.xlabel("Technology")
    plt.ylabel("Count")
    plt.tight_layout()
    plt.savefig(f"plots/{experience_level.lower()}_technologies_({date.today()}).png")
