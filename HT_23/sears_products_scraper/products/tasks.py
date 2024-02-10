from scraper_services.products_scraper import save_or_update_scraped_products_data
from sears_products_scraper.celery import app as celery_app


@celery_app.task(name='sears_products_scraper')
def sears_products_scraper_task(**kwagrs):
    print(kwagrs)
    return save_or_update_scraped_products_data(kwagrs.get('scraping_task_instance_id'))