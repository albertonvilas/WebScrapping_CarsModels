from selenium import webdriver

from selenium.webdriver.support.ui import WebDriverWait

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import pandas as pd

from random import randint
from time import sleep

link = "https://www.auto-data.net/en/allbrands"

def get_brand(browser, brand_name):
    
    wait = WebDriverWait(browser,1)
    brands_lst = browser.find_elements_by_class_name('marki_blok')
    for brand_elem in brands_lst:
        brand_name_elem = brand_elem.find_element_by_tag_name('strong').text
        if brand_name_elem.upper() == brand_name.upper():
            link_brand = brand_elem.get_attribute("href")
    
    browser.get(link_brand)

def get_models(browser):
    
    models = []
    wait = WebDriverWait(browser,2)
    models_lst = browser.find_elements_by_class_name('modeli')
    for model_elem in models_lst:
        
        model_name_elem = model_elem.find_element_by_tag_name('strong').text
        model_name_href = model_elem.get_attribute("href")
        models.append([model_name_elem, model_name_href])

    return models

def get_sub_models(browser, models):

    sub_model_dict = {}

    for model in models:

        sleep(randint(0,3))
        browser.get(model[1])
        sub_models_lst = browser.find_elements_by_tag_name('tr')

        versions = []
        for sub_model_elem in sub_models_lst:

            sub_model_description = sub_model_elem.text

            sub_model_description = sub_model_description.replace('\n', '')
            sub_model_description = sub_model_description.replace('\t', '')
            if "adsbygoogle" not in sub_model_description:
                
                sub_model_name = sub_model_elem.find_element_by_tag_name('strong').text
                sub_model_href = sub_model_elem.find_element_by_tag_name('a').get_attribute("href")
                sub_model_scr = sub_model_elem.find_element_by_tag_name('img').get_attribute('src')

                info_version = [model[0], sub_model_name, sub_model_href, sub_model_scr, sub_model_description]
                versions.append(info_version)
        
        sub_model_dict[model[0]] = versions

    return sub_model_dict

def write_sub_model(sub_model_dict, brand_name):
    header = ['Model','Sub_model', 'Sub_model_href', 'Sub_model_scr', 'sub_model_description']

    info_submodel = []
    for key in sub_model_dict:
        info_submodel = info_submodel + sub_model_dict[key]


    sub_model_df = pd.DataFrame(info_submodel, columns=header)
    file_name = "data/" + brand_name + "_submodels.xlsx"
    sub_model_df.to_excel(file_name, index = False)


def scrape(brand_name):
    browser = webdriver.Safari()

    browser.get(link)
    cookies_xpath = "/html/body/div[1]/div[2]"
    try:
        wait = WebDriverWait(browser,1)
        cookies_elem = wait.until(EC.visibility_of_element_located((By.XPATH, cookies_xpath)))
        cookies_elem.click()
        
    except:
        pass

    get_brand(browser, brand_name)
    models = get_models(browser)
    sub_model_dict = get_sub_models(browser, models)

    write_sub_model(sub_model_dict, brand_name)

    print("Brand")
    print(brand_name)
    print("Nr models")
    print(len(models))
    print("Nr versions")
    print(len(sub_model_dict))


    wait = WebDriverWait(browser,4)