import numpy as np
import pandas as pd

from config import possible_technologies


def add_experience_column(data_frame: pd.DataFrame) -> pd.DataFrame:
    data_frame["experience"] = "Junior"
    experience_levels = ["Middle", "Senior", "Lead"]

    for experience_level in experience_levels:
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
    df_junior = data_frame[data_frame["experience"] == experience_level]
    count_of_technologies = pd.DataFrame(columns=["technology", "count"])

    for technology in possible_technologies:
        count = (
            df_junior["job_description"]
            .str.contains(technology, case=False)
            .sum()
        )
        count_of_technologies.loc[len(count_of_technologies)] = {
            "technology": technology,
            "count": count,
        }

    return count_of_technologies
