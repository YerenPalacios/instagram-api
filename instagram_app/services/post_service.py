import functools

from instagram_app.repositories.post_repository import PostRepository

from selenium import webdriver
from bs4 import BeautifulSoup
import time
import requests

def match_class(target):
    def do_match(tag):
        classes = tag.get('class', [])
        return all(c in classes for c in target)
    return do_match


def get_bytes(url):
    import base64
    content = requests.get(url).content
    return base64.b64encode(content).decode('utf-8')

class PostScrapper:

    def get_raw_data(self):
        driver = webdriver.Edge()
        url = "https://www.instagram.com/instagram/reels/"
        driver.get(url)
        time.sleep(5)
        html = driver.page_source
        soup = BeautifulSoup(html, "html.parser")
        driver.quit()
        soup.findAll('_abq3')
        return soup

    @functools.lru_cache(maxsize=None)
    def get_clean_post(self):
        soup = self.get_raw_data()
        raw_posts = soup.findAll(match_class(['_abq3', '_al5o']))
        post_dict = [{
            'id': i,
            'images': [{'image': get_bytes(post.find(match_class(['_aag6', '_aajx'])).attrs.get('style').split('"')[1])}],
            # 'likes_count': post.find(match_class(
            #     'x1lliihq x1plvlek xryxfnj x1n2onr6 x193iq5w xeuugli '
            #     'x1fj9vlw x13faqbe x1vvkbs x1s928wv xhkezso x1gmr53x x1cpjm7i'
            #     ' x1fgarty x1943h6x x1i0vuye xl565be x1xlr1w8 x9bdzbf x10wh9bi'
            #     ' x1wdrske x8viiok x18hxmgj'
            # ))
        } for i, post in enumerate(raw_posts)]

        return post_dict


class PostService:
    def __init__(self):
        self._repository = PostRepository()

    def get_posts(self, user_id: int = None, priority: bool = None):
        if user_id:
            return self._repository.get_posts_for_user(user_id, priority)
        return self._repository.get_general_posts()

    def get_scraper_posts(self):
        scraper = PostScrapper()
        return scraper.get_clean_post()
