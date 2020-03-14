#!/usr/bin/env python
# encoding=utf-8
from openpyxl import Workbook
from selenium import webdriver

wb = Workbook()
dest_filename = 'music.xlsx'
ws1 = wb.active  # 当前打开的shell页
ws1.title = "音乐飙升榜"  # 更改默认的sheet名称
DOWNLOAD_URL = 'https://music.163.com/#/discover/toplist'

def main():
    """获取url地址页面内容"""
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.80 Safari/537.36'
    }
    driver = webdriver.Chrome()
    # https://selenium-python.readthedocs.io/installation.html
    driver.get(DOWNLOAD_URL)
    driver.switch_to.frame("g_iframe")
    li_list = driver.find_elements_by_xpath("//tbody/tr")
    content_list = []
    for li in li_list:
        item = {}
        # item["cover"] = li.find_element_by_xpath(".//img[@class='rpic']").get_attribute("src")#只有前三首有封面
        item["num"] = li.find_element_by_xpath(".//span[@class='num']").text
        item["songer"] = li.find_element_by_xpath(".//div[@class='text']").get_attribute("title")
        item["song"] = li.find_element_by_xpath(".//b").get_attribute("title")
        item["song_time"] = li.find_element_by_xpath(".//span[@class='u-dur ']").text
        print(item)
        content_list.append(item)
    ws1['A1'] = "排名"
    ws1['B1'] = "歌手"
    ws1['C1'] = "歌名"
    ws1['D1'] = "歌曲时间"
    for index, it in enumerate(content_list):
        col_a = 'A%s' % (index + 2)
        col_b = 'B%s' % (index + 2)
        col_c = 'C%s' % (index + 2)
        col_d = 'D%s' % (index + 2)
        ws1[col_a] = str(it['num'])
        ws1[col_b] = str(it['songer'])
        ws1[col_c] = str(it['song'])
        ws1[col_d] = str(it['song_time'])
    ws1.column_dimensions['B'].width = 60.0  # 调整列宽
    ws1.column_dimensions['C'].width = 90.0
    wb.save(filename=dest_filename)
    driver.quit()


if __name__ == '__main__':
    main()
