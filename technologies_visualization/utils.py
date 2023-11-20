import matplotlib.pyplot as plt
import pandas as pd


def read_data() -> pd.DataFrame:
    tech_count = pd.read_csv("technologies_count.csv")
    tech_count = tech_count.sort_values(by="count", ascending=False)[:10]
    return tech_count


def visualize_data() -> None:
    technologies_df = read_data()
    plt.bar(technologies_df["technology"], technologies_df["count"])
    plt.title("Top 10 technologies for Python developers in Ukraine")
    plt.ylabel("Count")
    plt.xlabel("Technology")
    plt.xticks(rotation=30)
    plt.tight_layout()
    plt.show()
