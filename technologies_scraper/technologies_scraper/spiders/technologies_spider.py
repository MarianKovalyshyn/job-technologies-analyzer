import time

import scrapy
from scrapy import Selector
from scrapy.exceptions import CloseSpider
from scrapy.http import Response
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait


class TechnologiesSpider(scrapy.Spider):
    name = "technologies"
    allowed_domains = ["robota.ua"]
    main_url = "https://robota.ua/zapros/python-developer/ukraine"

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self.driver = Chrome()

    def close(self, reason: str) -> None:
        self.driver.quit()
        super().close(self, reason)

    def start_requests(self) -> scrapy.Request:
        page_number = 0

        while True:
            page_number += 1
            url_to_parse = self.main_url + f"?page={page_number}"
            html_content = self.get_full_html_page(url_to_parse)

            yield scrapy.Request(
                url=url_to_parse,
                callback=self.parse,
                meta={"html_content": html_content},
            )

    def parse(self, response: Response, **kwargs):
        html_content = response.meta["html_content"]
        selector = Selector(text=html_content)
        job_cards = selector.css("div.santa-min-h-0")

        for job_card in job_cards:
            parsed_job_card = self.parse_job_card(job_card)
            yield {
                "job_title": parsed_job_card["job_title"],
                "job_link": parsed_job_card["job_link"],
                "job_description": parsed_job_card["job_description"],
            }

    def parse_job_card(self, job_card: Selector) -> dict[str, str]:
        job_title = job_card.css("h2.santa-typo-h3::text").get()
        job_link = (
            "https://robota.ua"
            + job_card.css("a.santa-mb-20::attr(href)").get()
        )
        job_description = self.get_job_description(job_link)
        return {
            "job_title": job_title,
            "job_link": job_link,
            "job_description": job_description,
        }

    def get_job_description(self, job_link: str) -> str:
        self.driver.get(job_link)
        WebDriverWait(self.driver, timeout=10).until(
            lambda driver_inside: driver_inside.execute_script(
                'return document.readyState == "complete"'
            )
        )
        time.sleep(1)
        html_content = self.driver.page_source
        selector = Selector(text=html_content)
        job_description = selector.css("#description-wrap").get()
        return job_description

    def get_full_html_page(self, url: str) -> str:
        self.driver.get(url)
        WebDriverWait(self.driver, timeout=10).until(
            lambda driver_inside: driver_inside.execute_script(
                'return document.readyState == "complete"'
            )
        )

        if (
            self.driver.find_element(By.CSS_SELECTOR, "h3.santa-typo-h3").text
            == "За вашим запитом поки немає вакансій"
        ):
            raise CloseSpider("No jobs found")

        self.scroll_to_bottom(self.driver)
        html_content = self.driver.page_source
        return html_content

    @staticmethod
    def scroll_to_bottom(driver: Chrome) -> None:
        scroll_increment = 500
        current_scroll = 0
        sleep_time = 0.25

        while True:
            driver.execute_script(f"window.scrollBy(0, {scroll_increment});")
            time.sleep(sleep_time)
            current_scroll += scroll_increment

            if current_scroll >= driver.execute_script(
                "return Math.max(document.body.scrollHeight, "
                "document.body.offsetHeight, "
                "document.documentElement.clientHeight, "
                "document.documentElement.scrollHeight, "
                "document.documentElement.offsetHeight);"
            ):
                break
