import time

import scrapy
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
        # for vacancy_detail_link in response.css("a.ng-tns-c224-29"):
        #     yield response.follow(vacancy_detail_link, callback=self.parse_vacancy_detail)

        self.driver.get(response.url)
        self.scroll_to_bottom(speed=10)

        for job_title in self.driver.find_elements(By.CSS_SELECTOR, "h2.santa-typo-h3"):
            yield {"job_title": job_title.text}

    @staticmethod
    def parse_vacancy_detail(response: Response, **kwargs):
        yield {
            "title": response.css("h1.santa-typo-h3::text").get(),
        }

    def closed(self):
        self.driver.quit()

    def scroll_to_bottom(self, speed=1):
        time.sleep(5)
        total_height = self.driver.execute_script("return Math.max(document.body.scrollHeight, document.body.offsetHeight, document.documentElement.clientHeight, document.documentElement.scrollHeight, document.documentElement.offsetHeight);")
        prev_height = 0

        while True:
            step_size = total_height // speed

            for i in range(prev_height, total_height, step_size):
                self.driver.execute_script("window.scrollTo(0, {});".format(i))
                time.sleep(0.1)

            current_height = self.driver.execute_script("return Math.max(document.body.scrollHeight, document.body.offsetHeight, document.documentElement.clientHeight, document.documentElement.scrollHeight, document.documentElement.offsetHeight);")

            if current_height == total_height:
                break

            prev_height = total_height
            total_height = current_height

        time.sleep(1)
