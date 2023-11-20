from config import possible_technologies
from technologies_scraper.technologies_scraper.utils import read_file


file_path = "technologies_scraper/technologies.json"
technologies_counted = read_file(
    file_path=file_path,
    possible_technologies=possible_technologies,
)
