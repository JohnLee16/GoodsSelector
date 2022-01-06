import csv
import requests
import re
from prettytable import PrettyTable
import prettytable as pt

def getHtmlText(url):
    try:
        header = {
            'authority': 'www.taobao.com',
            'cache-control': 'max-age=0',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36 Edg/91.0.864.41',
            'sec-fetch-user': '?1',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-mode': 'navigate',
            'referer': 'https://s.taobao.com/search?s=44',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'zh-CN,zh;q=0.9',
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



def taobaoSearch():
    goods = "猫包"

    depth = 4
    start_url = "https://s.taobao.com/search?q=" + goods
    infoList = []
    num = 300
    for i in range(depth):
        try:
            url = start_url + '$S=' + str(44 * i)
            html = getHtmlText(url)
            parsePage(infoList, html)
        except:
            continue

    printGoodsList(infoList, num)
    print("开始保存")
    with open("testdddddd" + 'data.csv', 'a', encoding='utf-8-sig', newline='') as f:
        w = csv.writer(f)
        for v in infoList:
            # print(v)
            w.writerow(v)
    print("结束保存")

taobaoSearch()