import csv
import json

from config import possible_technologies


def count_technologies_in_job_description(
    job_description: str,
    technologies_count: dict[str, int],
    technologies: list[str],
) -> None:
    if not job_description:
        return

    for technology in technologies:
        if technology in job_description.lower():
            technologies_count[technology] += 1


def read_json_file(
    file_path: str,
    technologies: list[str],
) -> dict[str, int]:
    with open(file_path, "r", encoding="utf-8") as json_file:
        jobs = json.load(json_file)

    technologies_count = {
        technology: 0 for technology in technologies
    }

    for job in jobs:
        count_technologies_in_job_description(
            job_description=job["job_description"],
            technologies_count=technologies_count,
            technologies=technologies,
        )

    return technologies_count


def write_csv_file(technologies_counted: dict[str, int]) -> None:
    with open("technologies_count.csv", "w", newline="") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=["technology", "count"])
        writer.writeheader()
        writer.writerows(
            [
                {"technology": technology, "count": count}
                for technology, count in technologies_counted.items()
            ]
        )


def get_data(file_path: str) -> None:
    technologies_counted = read_json_file(
        file_path=file_path,
        technologies=possible_technologies,
    )
    write_csv_file(technologies_counted=technologies_counted)
