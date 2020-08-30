import requests
from bs4 import BeautifulSoup

class Crawling:
    def __init__(self):
        self.url_dict = [
                            {'url': "https://news.yahoo.co.jp/topics/domestic", 'class': "newsFeedTab_item"},
                            {'url': "https://www.asahi.com/national/list/", 'class': "NavInner"},
                            {'url': "https://www.yomiuri.co.jp/life/", 'class': "p-header-category-list__sibling"},
                            {'url': "https://www.nikkei.com/business/archive/", 'class': "subpage-gnav__list"},
                            {'url': "https://news.livedoor.com/topics/category/world/", 'class': "navInner"},
                        ]

        self.news_list_dict = [
                            "newsFeed_item",
                            "List",
                            {'url': "https://www.yomiuri.co.jp/life/", 'class': "p-header-category-list__sibling"},
                            {'url': "https://www.nikkei.com/business/archive/", 'class': "subpage-gnav__list"},
                            {'url': "https://news.livedoor.com/topics/category/world/", 'class': "navInner"},
                        ]

        self.base = [ "https://news.yahoo.co.jp","", "","https://www.nikkei.com", "", ]

        self.category_dict = [
                            ["https://news.yahoo.co.jp/articles/"],
                            ["https://www.asahi.com/articles/"],
                            ["https://www.yomiuri.co.jp/"],
                            ["https://www.nikkei.com/article/"],
                            ["https://news.livedoor.com/article/detail/"],
                        ]

    def get_category(self, site_id):
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
            li_list = soup.select("div.p-header-category-list__sibling ul li ")

        elif(site_id == 3):
            soup = soup.find(class_=self.url_dict[site_id]['class'])
            soup = soup.find_all(class_= 'subpage-gnav__listitem--has-sub')
            
            for html in soup:
                li_list.append(html.find("a"))
        elif(site_id == 4):
            li_list= [
                {"name": "主要", "url": "https://news.livedoor.com/topics/category/main/"},
                {"name": "海外", "url": "https://news.livedoor.com/topics/category/world/"},
                {"name": "IT 経済", "url": "https://news.livedoor.com/topics/category/eco/"},
                {"name": "芸能", "url": "https://news.livedoor.com/topics/category/ent/"},
                {"name": "スポーツ", "url": "https://news.livedoor.com/topics/category/sports/"},
                {"name": "映画", "url": "https://news.livedoor.com/topics/category/52/"},
                {"name": "グルメ", "url": "https://news.livedoor.com/topics/category/gourmet/"},
                {"name": "女子", "url": "https://news.livedoor.com/topics/category/love/"},
                {"name": "トレンド", "url": "https://news.livedoor.com/topics/category/trend/"}]

        else:   
            li_list = soup.find_all(class_=self.url_dict[site_id]['class'])

        for li in li_list:
            if site_id == 1 or site_id == 3:
                if li.string != 'トップ' and li.string != "連載":
                    category.append({'name': li.string, "url": self.base[site_id] + li.get('href').replace('?iref=pc_gnavi', 'list')})
            elif site_id != 4:
                try:
                    category.append({'name': li.get_text(), "url":self.base[site_id] +  li.find('a').get('href')})
                except:
                    print('error')
            else:
                category = li_list   
        print(category) 
        return category

    def getArticleList(self,site_id ,category_url):
        news_list = []
        html = requests.get(category_url)
        soup = BeautifulSoup(html.content, 'html.parser')
        if site_id == 1:   
            soup = soup.select("ul.List li")
        else:
            soup = soup.find_all(class_= self.news_list_dict[site_id])
        for row in soup:
            print('^^^^^^^^^^^^^^^^^^^^')
            try:
                if(site_id == 1):
                    news_list.append({"title": row.find('a').get_text(), "url": row.find('a').get('href'), "fee": row.find("img")})
                else:
                    news_list.append({"title": row.find('a').get_text(), "url": row.find('a').get('href')})

            except:
                print(row)
        print(news_list)



