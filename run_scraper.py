from scraper import scrape, get_lst_brands

from random import randint
from time import sleep

def run_scrape():
    
    brands_lst, browser = get_lst_brands()

    for brand_name in brands_lst:
        scrape(brand_name, browser)
        sleep(randint(0,2))




run_scrape()