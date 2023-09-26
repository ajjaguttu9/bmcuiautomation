from selenium.webdriver.common.by import By


class AmazonPage:

    def __init__(self, driver):
        self.driver = driver

    # signin related xpaths
    amazon_signin_homepage = [By.XPATH,"//a[@data-nav-ref='nav_ya_signin']"]
    amazon_username = [By.ID,"ap_email"]
    amazon_password = [By.ID,"ap_password"]
    amazon_continue = [By.ID,"continue"]
    amazon_signin = [By.ID, "signInSubmit"]
    amazon_home = [By.ID,"nav-logo"]

    # Home page related xpath
    amazon_search_dropdown = [By.XPATH,"//select[@name='url']/option"]
    amazon_search_box = [By.ID,"twotabsearchtextbox"]
    amazon_search_results_text = [By.XPATH,"//div[@cel_widget_id='UPPER-RESULT_INFO_BAR-0']"]
    amazon_price_filter_min = [By.ID,'low-price']
    amazon_price_filter_max = [By.ID, 'high-price']
    amazon_price_filter_go_button = [By.XPATH,"//span[contains(text(),'Go')]/preceding-sibling::input"]

    # Filtered results related xpath
    amazon_filter_item_price = [By.XPATH,"//div[contains(@class,'sg-row')]//span[@class='a-price']//span[@class='a-price-whole']"]
    amazon_goto_page_2 = [By.XPATH,"//a[@aria-label='Go to page 2']"]
    amazon_five_star_rating = [By.XPATH,"//span[@aria-label='5.0 out of 5 stars']"]
    amazon_fivestar_text = [By.XPATH, "//span[@aria-label='5.0 out of 5 stars']//..//..//preceding-sibling::div[contains(@class,'s-title')]"]
