"""
This class is for all common utils used across the project
"""
import inspect
import logging
import time
import pytest
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
from pageObjects.CommonObjects import CommonObjects
from pageObjects.AmazonPageObjects import AmazonPage

@pytest.mark.usefixtures("setup")
class BaseClass:

    def getLogger(self):
        loggerName = inspect.stack()[1][3]
        logger = logging.getLogger(loggerName)
        fileHandler = logging.FileHandler('logfile.log')
        formatter = logging.Formatter("%(asctime)s :%(levelname)s : %(name)s :%(message)s")
        fileHandler.setFormatter(formatter)

        logger.addHandler(fileHandler)  # filehandler object

        logger.setLevel(logging.DEBUG)
        return logger

    def googleSearch(self,text_to_search):
        """
        This function enters the text in serach bar and searches, by returning the links of the search results
        displayed in first page

        :param text_to_search:
        :return: list of links appeared in search
        """
        self.driver.find_element(*CommonObjects.google_searchbox).send_keys(text_to_search)
        self.driver.find_element(*CommonObjects.google_searchbox).send_keys(Keys.ENTER)
        time.sleep(2)
        search_results = self.driver.find_elements_by_xpath("//div[@class='yuRUbf']//a")
        links = []
        for h in search_results:
            links.append(h.get_attribute("href"))
        return links


    def verifyLinkPresence(self, text):
        element = WebDriverWait(self.driver, 10).until(
        EC.presence_of_element_located((By.LINK_TEXT, text)))

    def selectOptionByText(self,locator,text):
        sel = Select(locator)
        sel.select_by_visible_text(text)


    def processingSearchResultsCount(self,results_match):
        if results_match:
            if "," in results_match[0].split(" results")[0]:
                replaced_str = results_match[0].split(" results")[0].replace(",","")
            else:
                replaced_str = results_match[0].split(" results")[0]
            extract_result_cnt = int(replaced_str)
        else:
            extract_result_cnt = 0

        return extract_result_cnt