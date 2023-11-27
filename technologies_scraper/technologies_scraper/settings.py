BOT_NAME = "technologies_scraper"

SPIDER_MODULES = ["technologies_scraper.spiders"]
NEWSPIDER_MODULE = "technologies_scraper.spiders"

ROBOTSTXT_OBEY = True

REQUEST_FINGERPRINTER_IMPLEMENTATION = "2.7"
TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"
FEED_EXPORT_ENCODING = "utf-8"
