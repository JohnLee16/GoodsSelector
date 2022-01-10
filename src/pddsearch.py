import requests
import re
from prettytable import PrettyTable
import prettytable as pt
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import csv
import itertools

def login_page(driver):
    user_name = '18682468446'
    #footer-item-icon-wrap
    footer_items = driver.find_elements_by_xpath('//*[@class="footer-item-icon-wrap"]')
    footer_items[len(footer_items) - 1].click()
    driver.find_element_by_xpath('//*[@class="phone-login"]').click()

    driver.find_element_by_id('user-mobile').send_keys(user_name)
    driver.find_element_by_id('code-button').click()
    pincode_input = driver.find_element_by_id('input-code')
    

def search_product(driver, keywords):
    username = "18682468446"

    driver.maximize_window()
    # click text box 2022.01.05
    driver.find_element_by_class_name('_18v23kPu').click()
    time.sleep(0.5)

    # find text box and fill QahmZDd2
    search_text = driver.find_element_by_class_name('QahmZDd2')
    search_text.send_keys(keywords)
    search_text.send_keys(Keys.ENTER)

    time.sleep(0.5)
    items_titles = driver.find_elements_by_class_name('PWKq3gf1')

    # find item info via find elements by class name
    # items_names = driver.find_elements_by_class_name('fnpJrQyt KbqLm0ek')
    # items_price = driver.find_elements_by_class_name('_9D91bFn1')
    # items_salecount = driver.find_elements_by_class_name('jmOJMlWq')

    # find items info via xpath
    # page = driver.find_elements_by_xpath('//*[@id="main"]')[0].text
    # print(page)

    # get all items only 22, one page 
    items = driver.find_elements_by_xpath('//*[@class="RIo5XeMZ"]')
    for item in items:
        item.click()
        time.sleep(0.5)
        # find the "发起拼单" Qzax7E1w
        pindan = driver.find_element_by_xpath('//*[@class="Qzax7E1w"]')
        pindan.click()
        time.sleep(0.5)
        # various classification: r-mksVqr
        skus = driver.find_elements_by_xpath('//*[@class="sku-specs-key"]') #sku-specs-key sku for goods
        for sku in skus:
        # color classification: qK4302ba
        # selected specific type:tWGpNA2Y
            ssr = sku.find_elements_by_xpath('.//div/*')
            
            # price of specific product: _27FaiT3N
            price = driver.find_elements_by_xpath('//*[@class="_27FaiT3N"]')

        
    itemsname_list = []
    time.sleep(0.5)
    # fnpJrQyt
    items_names = driver.find_elements_by_xpath('//*[@class="RIo5XeMZ"]')
    for item in items_names:
        print(item.text)
        itemsname_list.append(item.text)

    # region  lazy load
    # get labels
    search_html = driver.find_element_by_tag_name('html')
    # get html page height
    height=search_html.size['height'] * 21 
    for i in range(700,height,700):
        s=f'window.scrollBy(0,700)'#每次划700的单位
        driver.execute_script(s)   #向下滚动，0在第一位是向上向下，0在第二位是向左向右，负号决定具体方向
        time.sleep(1.5)
    #endregion


    items_specs = driver.find_elements_by_xpath('//*[@class="NA5750pm"]')
    itemsspecs_list = []
    for spec in items_specs:
        itemsspecs_list.append(spec.text)
    items_price = driver.find_elements_by_xpath('//*[@class="_9D91bFn1"]')
    price_list = []
    for price in items_price:
        price_list.append(price.text.replace('\n',''))


    page = re.findall('(\d+)',page)[0]#提取page中的数字
    return int(page)

# def pddlogin(username, password):


def pddSearch(name, brand="", serial_number="", size="", color=""):
    infoList = []
    # initialize driver
    option=webdriver.ChromeOptions()
    user_data_dir=r'C:\Users\Home_JLI\AppData\Local\Google\Chrome\User Data'
    option.add_argument(f'--user-data-dir={user_data_dir}')
    while 1:
        try:
            driver = webdriver.Chrome(options=option)
            break
        except Exception:
            time.sleep(1)
    # get all info can be type in searchbox
    keyword = name + brand + serial_number
    # request page
    driver.get("https://mobile.pinduoduo.com/")
    login_page(driver)
    search_product(driver, keyword)
    # 通过page_source获取网页源代码
    print(driver.page_source)


    print("开始保存")
    with open("testdddddd" + 'data.csv', 'a', encoding='utf-8-sig', newline='') as f:
        w = csv.writer(f)
        for v in infoList:
            # print(v)
            w.writerow(v)
    print("结束保存")

pddSearch("充电宝", "华为", "60W", "快充")