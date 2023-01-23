
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
# from fake_useragent import UserAgent
# import re
import time
import csv
import datetime


products = []
# -------------- USER INPUT
customer = '27-687380'
un = "tanu@herbspro.com"
pw = "nb1826hp"
starting_page = 2    # extract data starting page  up to nth
last_page_no = 4       # last page to scrape TYPE: 0 to check for the last page
headless = 'F'       # t or f | T or F
url = "https://connect-identity-server.kehe.com/Account/Login?ReturnUrl=%2Fconnect%2Fauthorize%2Fcallback%3Fclient_id%3Dconnect-retailer-web%26redirect_uri%3Dhttps%253A%252F%252Fconnectretailer.kehe.com%252Fcallback%26response_type%3Dcode%26scope%3Dopenid%2520profile%2520order-management-api%2520kehe-api%26state%3Dcddd47e34af54943bf0d5c96bc3b351b%26code_challenge%3DNlwkpxM67eK9IhTOwlPIjg01rpN41xD7LmeII48T_-g%26code_challenge_method%3DS256%26response_mode%3Dquery"
filename = 'test1'
# ---------------------

# fix xpaths
results_flag_sel = "//span[@class='col-6 text-left']//span[@class='ng-star-inserted']"


curPage = 1
count = 0

def chr_driver(url):
    op = webdriver.ChromeOptions()
    op.add_argument("window-size=1920x1080")
    op.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36")
    serv = Service('/home/m3wt/enzo/chromedriver')
    if headless == 't' or headless == 'T':
        op.headless = True
    elif headless == 'f' or headless == 'F':
        op.headless = False
    else:
        op.headless = False
        print('running headless')
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

def checkLastPage(last_page_no):
    if last_page_no == 0:
        last_page_button_sel = "//kendo-datapager[@class='k-pager-wrap k-pager k-widget ng-star-inserted']//span[@aria-label='Go to the last page']"
        last_page_button = WebDriverWait(driver, 120).until(
            EC.element_to_be_clickable((By.XPATH, last_page_button_sel))
            )
        last_page_button.click()
        results_flag_sel = "//span[@class='col-6 text-left']//span[@class='ng-star-inserted']"
        WebDriverWait(driver, 120).until(
                EC.presence_of_element_located((By.XPATH, results_flag_sel))
            )
        last_page_text_sel = "//kendo-datapager[@class='k-pager-wrap k-pager k-widget ng-star-inserted']//ul[@class='k-pager-numbers k-reset']/li[last()]/button"
        last_page_text_elem = driver.find_element(By.XPATH,last_page_text_sel)
        last_page_text =last_page_text_elem.get_attribute("textContent")
        print(f'total pages: {last_page_text}')

        #go back to first page
        fist_page_sel = "//kendo-datapager[@class='k-pager-wrap k-pager k-widget ng-star-inserted']//span[@aria-label='Go to the first page']"
        first_page = driver.find_element(By.XPATH,fist_page_sel)
        first_page.click()
        WebDriverWait(driver, 120).until(
                EC.presence_of_element_located((By.XPATH, results_flag_sel))
            )

        return int(last_page_text )
    else:
        return last_page_no


def main():
    global curPage
    global lastPage
    global starting_page
    global count

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


    lastPage = checkLastPage(last_page_no)
    # results_flag_sel = "//span[@class='col-6 text-left']//span[@class='ng-star-inserted']"
    results_flag = WebDriverWait(driver, 120).until(
        EC.presence_of_element_located((By.XPATH, results_flag_sel))
    )
    
    print(f'current page: {curPage} catalog: {results_flag.text} last page to scrape: {lastPage}')
    while curPage <= lastPage: #pagination
        try:
            if curPage < starting_page: # skip pages to curPage
                pagination()
                curPage+=1
                results_flag = WebDriverWait(driver, 120).until(
                    EC.presence_of_element_located((By.XPATH, results_flag_sel))
                )
                print(f'current page: {curPage} catalog: {results_flag.text} last page to scrape: {lastPage}')

            elif curPage >= starting_page and curPage <= lastPage: # iterate range
                image_links = driver.find_elements(By.XPATH,'//tbody/tr/td[3]//img/parent::div') # image divs in the catalog
                i = 1
                
                for image in image_links:
                # for image in range(1,3): # TEST ITERATION
                # for image in enumerate(image_links[1:3]): #TEST ITERATION
                    image = driver.find_element(By.XPATH,f'//tbody/tr[{i}]/td[3]//img/parent::div') # avoid stale element
                    link = image.find_element(By.XPATH,f'//tbody/tr[{i}]/td[3]//img/parent::div')
                    try:
                        link.click()
                    except:
                        pass
                    try:
                        WebDriverWait(driver, 120).until(
                                EC.presence_of_element_located((By.XPATH, "//img[@id='edo-product-details-modal-image']"))
                            )
                    except:
                        pass
                        cancel_btn_sel = "//div[contains(text(),'Cancel')]" # lose pop up when times out
                        cancel_btn = driver.find_element(By.XPATH, cancel_btn_sel)
                        cancel_btn.click()
                    # extract data
                    pcode = driver.find_element(By.XPATH,"//span[@id='edo-product-details-modal-item-num']").get_attribute("textContent")
                    upc = driver.find_element(By.XPATH,"//span[@id='edo-product-details-modal-upc']").get_attribute("textContent")
                    brand = driver.find_element(By.XPATH,"//a[@id='edo-product-details-modal-brand']").get_attribute("textContent")
                    country = driver.find_element(By.XPATH,"//span[@id='edo-product-details-modal-country']").get_attribute("textContent")
                    try:
                        image = driver.find_element(By.XPATH,"//img[@id='edo-product-details-modal-image']").get_attribute("src")
                    except NoSuchElementException:
                        image = ''
                    product_name = driver.find_element(By.XPATH,"//span[@id='edo-product-details-modal-title']").get_attribute("textContent")
                    try:
                        description = driver.find_element(By.XPATH,"//app-every-day-product-specifications[@class='ng-star-inserted']/div/div[1]").get_attribute("innerHTML")
                    except NoSuchElementException:
                        description = ''
                    try:
                        category_manager = driver.find_element(By.XPATH,"//span[@id='edo-product-details-modal-contact-manager-name']").get_attribute("textContent")
                    except NoSuchElementException:
                        category_manager = ''
                    try:
                        buyer = driver.find_element(By.XPATH,"//span[@id='edo-product-details-modal-buyer-name']").get_attribute("textContent")
                    except NoSuchElementException:
                        buyer = ''
                    try:
                        kehe_srp = driver.find_element(By.XPATH,"//span[@id='edo-product-details-modal-kehe-srp-price']").get_attribute("textContent")
                    except NoSuchElementException:
                        kehe_srp = ''
                    try:
                        wholesale = driver.find_element(By.XPATH,"//span[@id='edo-product-details-modal-wholesale-price']").get_attribute("textContent")  
                    except NoSuchElementException:
                        wholesale = ''
                    try:
                        qty_on_hand = driver.find_element(By.XPATH,"//span[@id='edo-product-details-modal-total-on-hand']").get_attribute("textContent") + ' ea'
                    except NoSuchElementException:
                        qty_on_hand = ''
                    try:
                        conversion = driver.find_element(By.XPATH,"//span[@id='edo-product-details-modal-eaches-to-cases']").get_attribute("textContent") + ' ea'
                    except NoSuchElementException:
                        conversion = ''
                    customer_no = driver.find_element(By.XPATH,"//div[@class='customer-number ng-star-inserted']").get_attribute("textContent")
                    customer_name = driver.find_element(By.XPATH,"//div[@class='customer-name']").get_attribute("textContent")
                    try:
                        status = driver.find_element(By.XPATH,"//div[@class='status-banner-text']").get_attribute("textContent")
                    except NoSuchElementException:
                        status = ''
                    try:
                        product_traits = driver.find_element(By.XPATH,"//span[@class='product-traits-list']").get_attribute("textContent")
                    except NoSuchElementException:
                        product_traits = ''
                    current_url = driver.current_url
                    try:
                        net_price = driver.find_element(By.XPATH,"//span[@id='edo-product-details-modal-net-price']").get_attribute("textContent")
                    except NoSuchElementException:
                        net_price = ''
                    today = datetime.datetime.today()
                    scrape_date = today.strftime("%d/%m/%Y")       
                    product_info = {
                        'product_code': pcode,
                        'upc': upc,
                        'brand': brand,
                        'country': country,
                        'product_name': product_name,
                        'description': description,
                        'image1': image,
                        'category_manager': category_manager,
                        'buyer': buyer,
                        'kehe_srp': kehe_srp,
                        'wholesale': wholesale,
                        'qty_on_hand': qty_on_hand,
                        'conversion': conversion,
                        'customer_name': customer_name,
                        'customer_no': customer_no,
                        'status': status,
                        'product_traits': product_traits,
                        'page_url': current_url,
                        'your_net_price': net_price,
                        'scrape_date': scrape_date
                    }
                    products.append(product_info)
                    count +=1
                    cancel_btn_sel = "//div[contains(text(),'Cancel')]" # lose pop up when times out
                    cancel_btn = driver.find_element(By.XPATH, cancel_btn_sel)
                    cancel_btn.click()
                    i = i+1
                    time.sleep(1)
                    print(f'count: {count} - item_no: {pcode} | product_name: {product_name} | wholesale: {wholesale}')
                # iterate pagination
                pagination()
                curPage +=1
                results_flag = WebDriverWait(driver, 120).until(
                    EC.presence_of_element_located((By.XPATH, results_flag_sel))
                )
                print(f'current page: {curPage} catalog: {results_flag.text} last page to scrape: {lastPage}')
            else:
                print("last page")
                break # break loop
        except NoSuchElementException:
            print('element exception - NoSuchElementException')
            break
    time.sleep(1)
    return products

def pagination():
    global lastPage
    global curPage
    if curPage <= lastPage:
        nextPage_selector = "//kendo-datapager[@class='k-pager-wrap k-pager k-widget ng-star-inserted']//span[@aria-label='Go to the next page']"
        nextPage = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, nextPage_selector))
        )
        if curPage < lastPage:
            print('clicking next page')
            nextPage.click()
        else:
            print('Last Page')
            return
    else:
        print('Out of bounds')
        return
    time.sleep(1)

def save(data):
    #save to csv
    with open(f'{filename}_{starting_page}-{curPage}.csv', 'w', newline='',encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=['product_code', 'upc', 'brand', 'country', 'product_name', 'description', 'image1', 'category_manager', 'buyer', 'kehe_srp', 'wholesale', 'qty_on_hand','conversion','customer_name','customer_no', 'status', 'product_traits','page_url','your_net_price','scrape_date'])
        writer.writeheader()
        writer.writerows(products)
    print('data saved')

if __name__ == '__main__':
    driver = chr_driver(url)
    login(un,pw)
    data = main()
    save(data)
    driver.quit()
