import requests
from bs4 import BeautifulSoup

class Crawling:
    def __init__(self):
        self.url_dict = [
                            {'url': "https://news.yahoo.co.jp/topics/domestic", 'class': "newsFeedTab_item"},
                            {'url': "https://www.asahi.com/national/list/", 'class': "NavInner"},
                            {'url': "https://www.yomiuri.co.jp/life/", 'class': "p-header-category-list__sibling"},
                            {'url': "https://www.nikkei.com/business/archive/", 'class': "subpage-gnav__list"},
                            {'url': "https://news.nicovideo.jp/categories/70?news_ref=top_header", 'class': "tabs"},
                        ]

        self.news_list_dict = [
                            "newsFeed_item",
                            "List",
                            "p-list-item",
                            "m-miM09_title",
                        ]

        self.base = [ "https://news.yahoo.co.jp","https://www.asahi.com/", "","https://www.nikkei.com", "https://news.nicovideo.jp"]


    def get_category(self, site_id):
        category = {}
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
            li_list = soup.select("ul.tabs li")
        else:   
            li_list = soup.find_all(class_=self.url_dict[site_id]['class'])

        for li in li_list:
            if site_id == 1 or site_id == 3:
                if li.string != 'トップ' and li.string != "連載" and li.string != "オピニオン" and li.string != "スポーツ" and li.string != "医療・健康" and li.string != "地域":
                    if site_id == 3:
                        if li.string != '速報' and li.string != 'ライフ':
                            category.setdefault(li.string, self.base[site_id] + li.get('href')+ 'archive/' )
                        elif li.string == '速報':
                            category.setdefault(li.string, self.base[site_id] + li.get('href') )

                    else:
                        category.setdefault(li.string, self.base[site_id] + li.get('href').split('?')[0] )

            elif site_id == 4:
                try:
                    if li.get_text() != "トップ":
                        category.setdefault(li.get_text(), self.base[site_id] + li.find('a').get('href') )
                except:
                    print('error')
            else:
                try:
                    category.setdefault(li.get_text(), self.base[site_id] + li.find('a').get('href') )
                except:
                    print('error')

        print(category)
        return category

    def get_article_list(self,site_id ,category_url):
        news_list = {}
        html = requests.get(category_url)
        soup = BeautifulSoup(html.content, 'html.parser')
        if site_id == 1:   
            soup = soup.select("ul.List li")
        elif site_id == 3:
            article = []
            article += soup.select(".m-miM09_title")
            article += soup.select(".m-miM32_itemTitle")
            soup = article
        elif site_id == 4:
            soup = soup.select("div.news-news-articles-list")
        else:
            soup = soup.find_all(class_= self.news_list_dict[site_id])

        for row in soup:
            try:
                if(site_id == 1):
                    news_list.setdefault(row.find('a').get_text(), {"url": self.base[site_id] +row.find('a').get('href'), "fee": row.find("img")} )
                elif(site_id == 2):
                    split_list = row.find('a').get('href').split('/')
                    if((len(split_list) == 6 or len(split_list) == 7) and '=' not in split_list[-1]):
                        news_list.setdefault(row.find('a').string,{"url": row.find('a').get('href'), "fee": row.find(class_="c-list-member-only")})
                elif(site_id == 3):
                    news_list.setdefault(row.find('a').get_text(), {"url":'https://r.nikkei.com' +row.find('a').get('href'), "fee": row.find(class_="m-iconMember")})
                elif(site_id == 4):
                    news_list.setdefault(row.find(class_='news-title').get_text(), {"url": self.base[site_id] +row.get('href') } )
                else:
                    news_list.setdefault(row.find(class_="newsFeed_item_title").get_text(), {"url": row.find('a').get('href')})
            except:
                print(row)
        
        print(news_list)
        return news_list

    def get_article(self,site_id ,category_url):
        html = requests.get(category_url)
        soup = BeautifulSoup(html.content, 'html.parser')
        article_body= ""
        if site_id == 0:
            soup = soup.find(class_="pickupMain_detailLink")
            html = requests.get(soup.find('a').get('href'))
            soup = BeautifulSoup(html.content, 'html.parser')
            article = soup.find(id="uamods")
            title = article.select('header h1')[0].get_text()
            soup = soup.select('.article_body div')
            for row in soup:
                try:
                    content = row.find(class_='yjDirectSLinkTarget').string
                    article_body += content
                except:
                    print("error")
        elif site_id == 1:
            article = soup
            title = article.select('.ArticleTitle .Title h1')[0].get_text()
            soup = soup.select(".ArticleText p")
            for row in soup:
                article_body += row.string
                print(article_body)

        elif site_id == 2:
            article = soup
            title = article.select('.article-content .article-header h1')[0].get_text()
            print(title)
            soup = soup.select(".p-main-contents p")
            for row in soup:
                article_body += row.string
                print(article_body)

        elif site_id == 3:
            article = soup
            title = article.select('article header h1')[0].get_text()
            soup = soup.select(".article__body .article__snippet p")
            for row in soup:
                article_body += row.string

        return {"title": title, "body": article_body}



