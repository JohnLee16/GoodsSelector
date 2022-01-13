from prettytable.prettytable import RANDOM
import requests
import re
from prettytable import PrettyTable
import prettytable as pt
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import csv
from itertools import product

pdddata_goods = []

def write_goods_info(filename, datalist):
    print("--- start write to csv ---")
    with open(filename + 'data.csv', 'a', encoding='utf-8-sig', newline='') as f:
        w = csv.writer(f)
        for v in datalist:
            # print(v)
            w.writerow(v)
    print("--- finished save files ---")

def login_page(driver):
    #footer-item-icon-wrap
    footer_items = driver.find_elements_by_xpath('//*[@class="footer-item-icon-wrap"]')
    try:
        # find "个人中心" to login
        footer_items[len(footer_items) - 1].click()
        time.sleep(0.5)
    except:
        pass

    try :
        driver.find_element_by_class_name('personal-section')
        footer_items = driver.find_elements_by_xpath('//*[@class="footer-item-icon-wrap"]')
        footer_items[0].click()
        time.sleep(0.1)
    except BaseException:
        # click using phone number to login
        driver.find_element_by_xpath('//*[@class="phone-login"]').click()
        time.sleep(0.1)
        # fill mobile number and manually input the pin code
        phonenumber = input('please input your phone number: ')
        driver.find_element_by_id('user-mobile').send_keys(phonenumber)
        driver.find_element_by_id('code-button').click()
        time.sleep(0.1)
        pincode = input('Please input the pin code you have received from your phone: ')
        pincode_input = driver.find_element_by_id('input-code').send_keys(pincode)
        # submit-button
        driver.find_element_by_id('submit-button').click()
        time.sleep(0.2)
        # alert-app-download-head
        try: 
            driver.find_element_by_class_name("alert-app-download-head")
            driver.find_element_by_class_name("alert-goto-app-cancel").click()
            time.sleep(0.2)
        except Exception:
            print("--- No alert app download page show up! ---")
        finally:
            # find "主页" to show
            footer_items = driver.find_elements_by_xpath('//*[@class="footer-item-icon-wrap"]')
            footer_items[0].click()
            time.sleep(0.2)
        


def search_product(driver, keywords):
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

    # get all items only 22, one page "RIo5XeMZ" specific product:VGc5+Y0S a9bD-5Ut
    items = driver.find_elements_by_xpath('//*[@class="VGc5+Y0S a9bD-5Ut"]')
    small_product = True if len(items) != 0 else False
    if not small_product:
        items = driver.find_elements_by_xpath('//*[@class="RIo5XeMZ"]')
        small_product = False    
    
    len_of_items = len(items)
    
    # ** details of product: _2sHFeg0q
    for i in range(len_of_items):
        item_name = items[i].text
        items[i].click()
        time.sleep(0.5)
        try:
            # find the "发起拼单" Qzax7E1w
            pindan = driver.find_element_by_xpath('//*[@class="Qzax7E1w"]')
            pindan.click()
            time.sleep(0.5)
        except Exception:
            continue
        # lSznZClW sku-plus1 exist to process skus, otherwise not necessary to process

        # various classification: r-mksVqr
        skus = driver.find_elements_by_class_name('r-mksVqr') # find_elements_by_xpath('//*[@class="sku-specs-key"]') # sku-specs-key sku for goods
        sku_specs = []
        last_selected = []
        for sku in skus:
            # color classification: qK4302ba
            # selected specific type:tWGpNA2Y  Test contains
            sku_temp = sku.find_elements_by_xpath('.//div[@class = "tWGpNA2Y"]')
            if len(sku_temp) == 0:
                continue
            else:
                sku_specs.append(sku_temp)
                if len(sku_temp) == 1:
                    last_selected.append(sku_temp[0].text)
                else:
                    last_selected.append("")
        
        combin = []
        price_list_diff_spec = []
        spec_names = []
        
        for spec in product(*sku_specs):
            spec_name_temp = ""
            effect = True
            # class name with this: tWGpNA2Y L6GSrkxz, unclickable
            index_of_selected = 0
            for s in spec:
                spec_name_temp += s.text
                if last_selected[index_of_selected] != s.text:
                    last_selected[index_of_selected] = s.text
                    try:
                        s.click()
                    except:
                        effect = False
                        spec_name_temp.replace(s.text, "") 
                        break
                else:
                    index_of_selected += 1
                    continue
                index_of_selected += 1
                
            if effect:
                # price of specific product: _27FaiT3N
                price = driver.find_element_by_xpath('//*[@class="_27FaiT3N"]')
                price_list_diff_spec.append(price.text)
                spec_names.append(spec_name_temp)
                pdddata_goods.append([item_name, spec_name_temp, price.text])
        
        driver.back()
        time.sleep(0.5)        
        items = driver.find_elements_by_xpath('//*[@class="VGc5+Y0S a9bD-5Ut"]') if small_product else driver.find_elements_by_xpath('//*[@class="RIo5XeMZ"]')

    driver.back()
    time.sleep(0.1)
        # return back to product page
        
        
    # price: _27FaiT3N
    # "确定" button
        
    # itemsname_list = []
    # time.sleep(0.5)
    # # fnpJrQyt
    # items_names = driver.find_elements_by_xpath('//*[@class="RIo5XeMZ"]')
    
    # for item in items_names:
    #     print(item.text)
    #     itemsname_list.append(item.text)

    # # region  lazy load
    # # get labels
    # search_html = driver.find_element_by_tag_name('html')
    # # get html page height
    # height=search_html.size['height'] * 21 
    # for i in range(700,height,700):
    #     s=f'window.scrollBy(0,700)'#每次划700的单位
    #     driver.execute_script(s)   #向下滚动，0在第一位是向上向下，0在第二位是向左向右，负号决定具体方向
    #     time.sleep(1.5)
    # #endregion


    # items_specs = driver.find_elements_by_xpath('//*[@class="NA5750pm"]')
    # itemsspecs_list = []
    # for spec in items_specs:
    #     itemsspecs_list.append(spec.text)
    # items_price = driver.find_elements_by_xpath('//*[@class="_9D91bFn1"]')
    # price_list = []
    # for price in items_price:
    #     price_list.append(price.text.replace('\n',''))


    # page = re.findall('(\d+)',page)[0]#提取page中的数字
    # return int(page)


def pddSearch(name, brand="", serial_number="", size="", color=""):

    infoList = []
    # initialize driver
    option=webdriver.ChromeOptions()
    # !! please input path of your user data
    user_data_dir=r'..\AppData\Local\Google\Chrome\User Data'
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
    write_goods_info(keyword, pdddata_goods)
    # 通过page_source获取网页源代码
    print(driver.page_source)


    

pddSearch("液晶电视", "小米", "43寸")