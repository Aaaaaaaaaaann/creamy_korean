from celery import chain
from celery.schedules import crontab

from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

from cosdna_scraper.cosdna_scraper.spiders.cosdna import CosdnaSpider
from sifo_scraper.sifo_scraper.spiders.sifo import SifoSpider
from .celery_app import celery_app

spiders = [SifoSpider, CosdnaSpider]


@celery_app.task
def run_spider(spider):
    process = CrawlerProcess(get_project_settings())
    process.crawl(spider)
    process.start()


@celery_app.on_after_finalize.connect
def setup_periodic_tasks(sender, **kwags):
    sender.add_periodic_tasks(crontab(hour=0, minute=0, day_of_week=1), 
                              chain(*[run_spider.s(spider) for spider in spiders]))
