import requests
from bs4 import BeautifulSoup

class Crawling:
    def __init__(self):
        self.url_dict = [
                            {'url': "https://news.yahoo.co.jp/topics/domestic", 'class': "newsFeedTab_item"},
                            {'url': "https://www.asahi.com/national/list/", 'class': "NavInner"},
                            {'url': "https://www.yomiuri.co.jp/", 'class': "home-2020-prime-topnews"},
                            {'url': "https://www.nikkei.com/business/archive/", 'class': "subpage-gnav__list"},
                            {'url': "https://news.livedoor.com/topics/category/world/", 'class': "navInner"},
                        ]

        self.category_dict = [
                            ["https://news.yahoo.co.jp/articles/"],
                            ["https://www.asahi.com/articles/"],
                            ["https://www.yomiuri.co.jp/"],
                            ["https://www.nikkei.com/article/"],
                            ["https://news.livedoor.com/article/detail/"],
                        ]

    def getCategory(self, site_id):
        category = []
        html = requests.get(self.url_dict[site_id]['url'])
        soup = BeautifulSoup(html.content, 'html.parser')
        li_list = []
        if(site_id == 1):
            soup = soup.find(class_=self.url_dict[site_id]['class'])
            soup = soup.find_all(lambda tag: tag.name == 'li' and len(tag.get('class')) == 2)
            for html in soup:
                li_list.append(html.find('a'))

        elif(site_id == 2):
            li_list = soup.select("nav.home-2020-prime-categorylist.js-home-2020-prime-categorylist ul li")
        elif(site_id == 3):
            soup = soup.find(class_=self.url_dict[site_id]['class'])
            soup = soup.find_all(class_= 'subpage-gnav__listitem--has-sub')
            
            for html in soup:
                li_list.append(html.find("a"))
        elif(site_id == 4):
            li_list= ["主要","国内","海外","IT 経済","芸能","スポーツ","映画","グルメ","女子","トレンド"]

        else:   
            li_list = soup.find_all(class_=self.url_dict[site_id]['class'])

        for li in li_list:
            if site_id != 4:
                category.append(li.string)
            else:
                category = li_list    

        return category


