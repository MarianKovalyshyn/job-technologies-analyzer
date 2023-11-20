from config import possible_technologies
from technologies_scraper.technologies_scraper.utils import (
    read_json_file,
    write_csv_file,
)
from technologies_visualization.utils import visualize_data

file_path = "technologies_scraper/technologies.json"
technologies_counted = read_json_file(
    file_path=file_path,
    possible_technologies=possible_technologies,
)
write_csv_file(technologies_counted=technologies_counted)
visualize_data()
