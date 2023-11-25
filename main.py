from technologies_scraper.technologies_scraper.utils import get_data
from technologies_visualization.utils import visualize_data


file_path = "technologies_scraper/technologies.json"
get_data(file_path=file_path)
visualize_data()
