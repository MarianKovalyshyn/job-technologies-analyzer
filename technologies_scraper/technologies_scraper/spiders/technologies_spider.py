import time

import scrapy
from scrapy.exceptions import CloseSpider
from scrapy.http import Response
from selenium import webdriver
from selenium.webdriver.common.by import By


class TechnologiesSpider(scrapy.Spider):
    name = "technologies"
    allowed_domains = ["robota.ua"]
    start_urls = ["https://robota.ua/zapros/python-developer/ukraine"]

    def __init__(self, *args, **kwargs) -> None:
        super(TechnologiesSpider, self).__init__(*args, **kwargs)
        self.driver = webdriver.Chrome()

    def parse(self, response: Response, **kwargs):
        page_number = 0

        while True:
            page_number += 1
            page_link = self.start_urls[0] + f"?page={page_number}"
            yield from self.parse_single_page(page_link)

    def parse_single_page(self, page_link: str):
        self.driver.get(page_link)

        if (self.driver.find_elements(By.CSS_SELECTOR, "h3.santa-typo-h3")[0]
                .text == "За вашим запитом поки немає вакансій"):
            raise CloseSpider("Condition met")

        self.scroll_to_bottom(speed=10)

        for job_card in self.driver.find_elements(
            By.CSS_SELECTOR, "div.santa--mb-20"
        ):
            yield {
                "job_title": job_card.find_element(
                    By.CSS_SELECTOR, "h2.santa-typo-h3"
                ).text,
                "link": job_card.find_element(By.CSS_SELECTOR, "a.santa-mb-20")
                .get_attribute("href"),
            }

    def closed(self) -> None:
        self.driver.quit()

    def scroll_to_bottom(self, speed: int = 1) -> None:
        time.sleep(7)
        total_height = self.driver.execute_script(
            "return Math.max(document.body.scrollHeight, "
            "document.body.offsetHeight, "
            "document.documentElement.clientHeight, "
            "document.documentElement.scrollHeight, "
            "document.documentElement.offsetHeight);"
        )
        prev_height = 0

        while True:
            step_size = total_height // speed

            for i in range(prev_height, total_height, step_size):
                self.driver.execute_script("window.scrollTo(0, {});".format(i))
                time.sleep(0.1)

            current_height = self.driver.execute_script(
                "return Math.max(document.body.scrollHeight, "
                "document.body.offsetHeight, "
                "document.documentElement.clientHeight, "
                "document.documentElement.scrollHeight, "
                "document.documentElement.offsetHeight);"
            )

            if current_height == total_height:
                break

            prev_height = total_height
            total_height = current_height

        time.sleep(2)
