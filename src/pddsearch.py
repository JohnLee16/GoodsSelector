import requests
import re
from prettytable import PrettyTable
import prettytable as pt
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import csv

def getHtmlText(url):
    try:
        header = {
            'cache-control': 'max-age=0',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36 Edg/91.0.864.41',
            'sec-fetch-user': '?1',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-dest': 'document',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'zh-CN,zh;q=0.9',
            "Referer": "http://mobile.pinduoduo.com/",
            'cookie': '',
        }
        r = requests.get(url, headers=header)
        r.raise_for_status()
        r.encoding = r.apparent_encoding

        return r.text
    except:
        print("爬取失败")
        return ""


def parsePage(ilist, html):
    try:
        goods_info = re.findall('VGc5+Y0S a9bD-5Ut *', html)
        plt = re.findall(r'"view_price":"\d+.\d*"', html)
        tlt = re.findall(r'"raw_title":".*?"', html)
        slt = re.findall(r'"nick":".*?"', html)
        addlt = re.findall(r'"item_loc":".*?"', html)
        qlt = re.findall(r'"view_sales":".*?"', html)
        # print(tlt)
        print(len(plt))
        for i in range(len(plt)):
            price = eval(plt[i].split(':')[1])
            title = eval(tlt[i].split(':')[1])
            shop = eval(slt[i].split(':')[1])
            address = eval(addlt[i].split(':')[1])
            quality = eval(qlt[i].split(':')[1])
            ilist.append([title, price, shop, address, quality])

        # print(ilist)
    except:
        print("解析出错")


def printGoodsList(ilist, num):
    table = PrettyTable(["序号", "商品名称", "价格", "商家名称", "商家地址", "销量"])# add more info here
    count = 0
    for g in ilist:
        count += 1
        if count <= num:
            table.add_row([count,g[0],g[1],g[2],g[3],g[4]])
    print(table)


def search_product(driver, keywords):
    driver.maximize_window()
    # click text box 2022.01.05
    driver.find_element_by_class_name('_18v23kPu').click()
    time.sleep(0.5)

    # find text box and fill QahmZDd2
    search_text = driver.find_element_by_class_name('QahmZDd2')
    search_text.send_keys(keywords)
    search_text.send_keys(Keys.ENTER)
    count = 0
    time.sleep(0.5)
    items_titles = driver.find_elements_by_class_name('PWKq3gf1')

    # find item info via find elements by class name
    items_names = driver.find_elements_by_class_name('fnpJrQyt KbqLm0ek')
    # items_price = driver.find_elements_by_class_name('_9D91bFn1')
    # items_salecount = driver.find_elements_by_class_name('jmOJMlWq')

    # find items info via xpath
    # page = driver.find_elements_by_xpath('//*[@id="main"]')[0].text
    # print(page)
    page = driver.find_elements_by_xpath('//*[@class="RIo5XeMZ"]')[0].text
    itemsname_list = []
    time.sleep(0.5)
    # fnpJrQyt
    items_names = driver.find_elements_by_xpath('//*[@class="RIo5XeMZ"]')
    for item in items_names:
        print(item.text)
        itemsname_list.append(item.text)


    
    search_html = driver.find_element_by_tag_name('html')#获取对应标签
    height=search_html.size['height'] * 21#获取html页面的总高度
 
    for i in range(700,height,700):
        s=f'window.scrollBy(0,700)'#每次划700的单位
        driver.execute_script(s)   #向下滚动，0在第一位是向上向下，0在第二位是向左向右，负号决定具体方向
        time.sleep(1.5)

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


def pddSearch(name):
    infoList = []
    # initialize driver
    while 1:
        try:
            driver = webdriver.Chrome()
            break
        except Exception:
            time.sleep(1)

    # request page
    driver.get("https://mobile.pinduoduo.com/")
    search_product(driver, name)
    # 通过page_source获取网页源代码
    print(driver.page_source)


    print("开始保存")
    with open("testdddddd" + 'data.csv', 'a', encoding='utf-8-sig', newline='') as f:
        w = csv.writer(f)
        for v in infoList:
            # print(v)
            w.writerow(v)
    print("结束保存")

pddSearch("充电宝")