import scrapy
from enum import Enum

class Config:

    _PERSIAN = "fa/service/"
    NAME = "Tasnim"
    ROOT = "https://www.tasnimnews.com/"
    PAGE = "?page="
    ROOT_PERSIAN = ROOT + _PERSIAN

    LIST_CSS = 'article.list-item a::attr(href)'
    TITLE_CSS =  'article.single-news h1.title::text'
    ABSTRACT_CSS = 'article.single-news h3.lead::text'
    BODY_CSS = 'article.single-news div.story p::text'
    TIME_CSS = 'article.single-news div._sticky ul.list-inline li.time::text'

class Category(Enum):

    POLITICS = "سیاسی"
    SOCIAL = "اجتماعی"
    SPORT = "ورزشی"
    ART = "فرهنگی هنری"
    CITY = "استان‌ها"
    ECONOMY = "اقتصادی"
    INTERNATIONAL = "بین الملل"
    MEDIA = "رسانه ها"


class CategoryUrl(Enum):

    POLITICS = Config.ROOT_PERSIAN + "1/"
    SOCIAL = Config.ROOT_PERSIAN + "2/"
    SPORT = Config.ROOT_PERSIAN + "3/"
    ART = Config.ROOT_PERSIAN + "4/"
    CITY = Config.ROOT_PERSIAN + "6/"
    ECONOMY = Config.ROOT_PERSIAN + "7/"
    INTERNATIONAL = Config.ROOT_PERSIAN + "8/"
    MEDIA = Config.ROOT_PERSIAN + "9/"
        

class TasnimSpider(scrapy.Spider):
    
    name = Config.NAME

    PAGE_COUNT = 100

    def __init__(self):
        self._set_start_urls()
        
    def _set_start_urls(self):
        self.start_urls = [f"{base_url.value}{Config.PAGE}{i}" for base_url in list(CategoryUrl) \
                     for i in range(1, self.PAGE_COUNT)]


    def _get_category(self, response):
        for category_url, category in zip(list(CategoryUrl), list(Category)):
            if response.url.startswith(category_url.value):
                return category.value

    def parse(self, response):
    
        category = self._get_category(response)
        for news in response.css(Config.LIST_CSS).getall():
            request=scrapy.Request(
                Config.ROOT+news, 
                callback=self.parse_news,
                cb_kwargs=dict(category=category))
            yield request 


    def parse_news(self, response, category):
        item = {
            'category': category,
            'title': response.css(Config.TITLE_CSS).get(),
            'abstract': response.css(Config.ABSTRACT_CSS).get(),
            'body': ' '.join(response.css(Config.BODY_CSS).getall()),
            'time': response.css(Config.TIME_CSS).get()
        }
        
        yield item