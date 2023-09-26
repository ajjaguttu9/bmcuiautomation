import pytest
from selenium import webdriver
import time,os,logging,configparser

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from testdata.AmazonData import AmazonData
from utilities.AmazonClass import AmazonClass

# @pytest.fixture(scope="class")
# def setup(request):


class TestAmazon(AmazonClass):

    cwd = os.getcwd()
    config = configparser.ConfigParser("")
    config.read( cwd+"\\testdata\\config.ini")

    @pytest.mark.parametrize('value', AmazonData.getTestData())
    def test_e2e(self,value):
        logging.info(value)
        logging.info("Search amazon in google")
        self.googleSearch("Amazon")
        logging.info("Login to amazon")
        self.loginToAmazon(self.config['Credentials']['username'],self.config['Credentials']['password'])
        # self.createWishlist("testing")
        self.amazonSelectSearch(value['Search_Category'])
        item_search = self.searchForSpecificItem(value['Search_Product'])
        filtered_search = self.filterSearchResults(value['Search_Product'],value['Filter_By'],[value['Min'],value['Max']])
        assert item_search > filtered_search,f"Actual Search Result count {item_search} " \
            f"Filtered Serach Count {filtered_search}"
        result_validate,msg = self.validateSearchResults(2,[value['Min'],value['Max']])
        assert result_validate,f"Failed due to prices are not falling in the range {msg}"
        logging.info("All prices are falling in the price")
        fivestarproducts,msg = self.getFiveStarProducts(2)
        assert msg == "success",f"There are no five star prdoucts"
        message = self.addProductToWishlist(fivestarproducts[0])
        assert "This item was already intesting's Wish List" in message,f"Item is not added to the wish list {message}"




