"""
This class is for all common utils used across the project
"""
import inspect
import logging
import time,re
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.action_chains import ActionChains

from pageObjects.CommonObjects import CommonObjects
from pageObjects.AmazonPageObjects import AmazonPage
from utilities.BaseClass import BaseClass

@pytest.mark.usefixtures("setup")
class AmazonClass(BaseClass):

    def loginToAmazon(self,username,password):
        search_results = self.driver.find_elements_by_xpath("//div[@class='yuRUbf']//a")
        for h in search_results:
            if h.get_attribute("href") == "https://www.amazon.in/":
                h.click()
                break
        time.sleep(2)
        self.driver.find_element(*AmazonPage.amazon_signin_homepage).click()
        self.driver.find_element(*AmazonPage.amazon_username).send_keys("gnana87@gmail.com")
        continue_button = self.driver.find_element(*AmazonPage.amazon_continue)
        if continue_button:
            continue_button.click()

        self.driver.find_element(*AmazonPage.amazon_password).send_keys("chetandiaper")
        self.driver.find_element(*AmazonPage.amazon_signin).click()

    def amazonSelectSearch(self,text_to_select):
        """

        :param text_to_select:
        :return:
        """
        log = self.getLogger()
        options_to_search = self.driver.find_elements(*AmazonPage.amazon_search_dropdown)
        select = Select(self.driver.find_element_by_xpath("//select[@name='url']"))
        time.sleep(1)
        for i in range(1,len(options_to_search)):
            select.select_by_index(i)
            # log.info(f"option text {each_option.text}")
            if options_to_search[i].text == text_to_select:
                return True
        else:
            return False

    def searchForSpecificItem(self,item_to_search):
        self.driver.find_element(*AmazonPage.amazon_search_box).send_keys(item_to_search)
        self.driver.find_element(*AmazonPage.amazon_search_box).send_keys(Keys.ENTER)
        results_box_text = self.driver.find_element(*AmazonPage.amazon_search_results_text).text
        results_match = re.findall(r'\d+[,]?\d+ results for \"'+item_to_search+'\"',results_box_text)
        total_results_cnt = self.processingSearchResultsCount(results_match)
        return total_results_cnt


    def filterSearchResults(self,item_to_search,filter_by,filter_val):
        if filter_by == 'price range':
            min = filter_val[0]
            max = filter_val[1]
            self.driver.find_element(*AmazonPage.amazon_price_filter_min).send_keys(filter_val[0])
            self.driver.find_element(*AmazonPage.amazon_price_filter_max).send_keys(filter_val[1])
            time.sleep(1)
            self.driver.find_element(*AmazonPage.amazon_price_filter_go_button).click()

            results_box_text = self.driver.find_element(*AmazonPage.amazon_search_results_text).text
            results_match = re.findall(r'\d+[,]?\d+ results for \"' + item_to_search + '\"', results_box_text)
            total_results_cnt = self.processingSearchResultsCount(results_match)
            return total_results_cnt

    def validateSearchResults(self,no_of_pages,price_range):
        list_of_prices = []
        for i in range(1,no_of_pages+1):
            prices = self.driver.find_elements(*AmazonPage.amazon_filter_item_price)
            for each_price in prices:
                list_of_prices.append(int(each_price.text.replace(",","")))
            if i == 1:
                time.sleep(5)
                self.driver.find_element(*AmazonPage.amazon_goto_page_2)
                self.driver.find_element(*AmazonPage.amazon_goto_page_2).click()

        for each_price in list_of_prices:
            if each_price < price_range[0] and each_price > price_range[1]:
                return False,f"Price is not in range {each_price}"
        else:
            return True,"success"


    def getFiveStarProducts(self,get_from_pages = 2):
        list_of_5star_products = []
        time.sleep(5)
        self.driver.find_element_by_xpath("//a[contains(@aria-label,'Go to previous page')]").click()
        time.sleep(2)
        for i in range(0,get_from_pages):
            fivestar_products = self.driver.find_elements(*AmazonPage.amazon_fivestar_text)
            for each_product in fivestar_products:
                logging.info(each_product.text)
                list_of_5star_products.append(each_product.text)
            if i == 0:
                time.sleep(5)
                self.driver.find_element(*AmazonPage.amazon_goto_page_2).click()

        if list_of_5star_products:
            return list_of_5star_products, "success"
        return False, f"No five star products {list_of_5star_products}"

    def createWishlist(self,wishlist_name):

        a = ActionChains(self.driver)
        m = self.driver.find_element_by_id("nav-link-accountList-nav-line-1")
        a.move_to_element(m).perform()
        self.driver.find_element_by_xpath("//a//span[text()='Your Wish List']").click()
        self.driver.find_element_by_id("createList").click()
        WebDriverWait(self.driver,5).until(EC.visibility_of_element_located((By.XPATH,"//input[@id='list-name']")))
        self.driver.find_element_by_xpath("//input[@id='list-name']").clear()
        self.driver.find_element_by_xpath("//input[@id='list-name']").send_keys(wishlist_name)
        self.driver.find_element_by_xpath("//span[text()='Create List']/preceding-sibling::input").click()
        time.sleep(1)
        self.driver.find_element(*AmazonPage.amazon_home).click()

    def addProductToWishlist(self,product_to_add):

        time.sleep(5)
        self.driver.find_element_by_xpath("//a[contains(@aria-label,'Go to previous page')]").click()
        time.sleep(2)
        self.driver.find_element_by_xpath("//span[contains(text(),'%s')]" %product_to_add.split("\"")[0]).click()
        time.sleep(3)
        m = self.driver.find_element_by_xpath("//input[@id='add-to-wishlist-button-submit']")
        m.click()
        m.click()
        time.sleep(1)
        message = self.driver.find_element_by_id("huc-atwl-header-section").text
        return message


