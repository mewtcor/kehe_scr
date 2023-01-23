from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import datetime


# -- user input
customer = '27-687380'
un = "tanu@herbspro.com"
pw = "nb1826hp"
url = "https://connect-identity-server.kehe.com/Account/Login?ReturnUrl=%2Fconnect%2Fauthorize%2Fcallback%3Fclient_id%3Dconnect-retailer-web%26redirect_uri%3Dhttps%253A%252F%252Fconnectretailer.kehe.com%252Fcallback%26response_type%3Dcode%26scope%3Dopenid%2520profile%2520order-management-api%2520kehe-api%26state%3Dcddd47e34af54943bf0d5c96bc3b351b%26code_challenge%3DNlwkpxM67eK9IhTOwlPIjg01rpN41xD7LmeII48T_-g%26code_challenge_method%3DS256%26response_mode%3Dquery"

def chr_driver(url):
    op = webdriver.ChromeOptions()
    op.headless = True
    op.add_argument("window-size=1920x1080")
    op.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36")
    serv = Service('/home/m3wt/enzo/chromedriver')
    browser = webdriver.Chrome(service=serv, options=op)
    browser.get(url)
    return browser

def login(un, pw):
    next_btn_sel = "//button[@value='login'][contains(.,'Next')]"
    next_btn = WebDriverWait(driver, 120).until(
            EC.presence_of_element_located((By.XPATH, next_btn_sel))
        )
    user_sel = "//input[@id='username']"
    username = driver.find_element(By.XPATH,user_sel)
    # next_btn.click()
    username.send_keys(un)
    next_btn.click()

    login_sel = "//button[@value='login'][contains(.,'Log In')]"
    login_btn = WebDriverWait(driver, 120).until(
            EC.presence_of_element_located((By.XPATH, login_sel))
        )
    pass_sel = "//input[@id='password']"
    password = driver.find_element(By.XPATH, pass_sel)
    password.send_keys(pw)
    login_btn.click()
    # blocked here


def main():
    # backup_url = 'https://connectretailer.kehe.com/every-day'
    # driver.get(backup_url)
    shop_everyday_sel = "//em[@class='fas fa-shopping-basket']"
    shop_everyday = WebDriverWait(driver, 120).until(
            EC.presence_of_element_located((By.XPATH, shop_everyday_sel))
        )
    shop_everyday.click()
    cust_flag ="//div[@class='customer-number ng-star-inserted']"
    WebDriverWait(driver, 120).until(
            EC.presence_of_element_located((By.XPATH, cust_flag))
        )

    # select customer 
    cust_container_sel = '//div[@class="cid-wrap list-closed"]'
    driver.find_element(By.XPATH,cust_container_sel).click()
    cust_no_sel = f'//div[@class="cid-wrap list-open"]/div[2]//span[@class="cid-dc"][contains(.,"DC {customer}")]'
    driver.find_element(By.XPATH, cust_no_sel).click()

    time.sleep(1)
    # -- shop all categories
    products_menu_sel = '//a[normalize-space()="Products"]'
    products_cat = WebDriverWait(driver, 120).until(
            EC.element_to_be_clickable((By.XPATH, products_menu_sel))
        )
    products_cat.click()
    time.sleep(1)
    shop_all_sel = '//ul[@id="k-menu0-child1"]//a[normalize-space()="Shop All Categories"]'
    shop_all = driver.find_element(By.XPATH, shop_all_sel)
    shop_all.click()
    time.sleep(5)

    last_page_button_sel = "//kendo-datapager[@class='k-pager-wrap k-pager k-widget ng-star-inserted']//span[@aria-label='Go to the last page']"
    last_page_button = WebDriverWait(driver, 120).until(
            EC.element_to_be_clickable((By.XPATH, last_page_button_sel))
        )
    # actions = ActionChains(driver)
    # driver.execute_script("arguments[0].scrollIntoView();", last_page_button)
    last_page_button.click()
    results_flag_sel = "//span[@class='col-6 text-left']//span[@class='ng-star-inserted']"
    results_flag = WebDriverWait(driver, 120).until(
            EC.presence_of_element_located((By.XPATH, results_flag_sel))
        ) 

    last_page_text_sel = "//kendo-datapager[@class='k-pager-wrap k-pager k-widget ng-star-inserted']//ul[@class='k-pager-numbers k-reset']/li[last()]/button"
    last_page_text_elem = driver.find_element(By.XPATH,last_page_text_sel)
    last_page_text =last_page_text_elem.get_attribute("textContent")
    today = datetime.datetime.today()
    scrape_date = today.strftime("%d/%m/%Y")
    print(f'date: {scrape_date} | last page: {last_page_text} | results: {results_flag.text}')

    driver.quit()


if __name__ == '__main__':
    driver = chr_driver(url)
    login(un,pw)
    main()