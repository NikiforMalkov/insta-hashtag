from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from src.helper import get_url_collection
from selenium import webdriver
from src.postPdo import PostPdo


class Parser(object):

    def __init__(self, driver: webdriver, selector_collection: dict, post: PostPdo):
        self.driver = driver
        self.cookie_collection = None
        self.selector_collection = selector_collection
        self.post = post

    def login(self, user_login: str, user_password: str):
        self.driver.get("https://www.instagram.com/")
        try:
            element = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, self.selector_collection["loginButton"]))
            )
            login_button = self.driver.find_element_by_css_selector(self.selector_collection["loginButton"])
            login_button.click()
        finally:
            assert "No results found." not in self.driver.page_source

        try:
            element = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, self.selector_collection["loginField"]))
            )
            login_filed = self.driver.find_element_by_css_selector(self.selector_collection["loginField"])
            password_field = self.driver.find_element_by_css_selector(self.selector_collection["passwordField"])
            sing_in_button = self.driver.find_element_by_css_selector(self.selector_collection["singInButton"])
            login_filed.send_keys(user_login)
            password_field.send_keys(user_password)
            sing_in_button.click()
            element = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((
                    By.CSS_SELECTOR,
                    "#react-root > section > main > section > div.COOzN > div.m0NAq > div > div.RR-M-._2NjG_"
                ))
            )
        finally:
            assert "No login text selector found"

    def get_post_row(self, link: str):
        self.driver.get(link)
        try:
            element = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, self.selector_collection["publication"]))
            )
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            publication_collection = self.get_publication_list()
            publication_div = publication_collection[0].find_element_by_css_selector(
                self.selector_collection["publicationDiv"]
            )
            publication_div.click()
            element = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, self.selector_collection["publicationTime"]))
            )
            is_last = False
            while not is_last:
                is_last = self.get_pagination_arrow()
        finally:
            assert "No publications on the page"

    def get_pagination_arrow(self):
        result = False
        try:
            element = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, self.selector_collection["paginationArrow"]))
            )
            result = self.get_post()
            return result
        finally:
            return result

    def get_publication_list(self):
        publication_collection = self.driver.find_elements_by_css_selector(
            self.selector_collection["publicationCollection"]
        )
        return publication_collection

    def get_post(self):
        link = self.driver.current_url
        date = self.driver.find_element_by_css_selector(self.selector_collection["publicationTime"])
        image_tag = self.driver.find_element_by_css_selector(self.selector_collection["publicationImage"])
        url_collection = get_url_collection(image_tag.get_attribute("srcset"))
        user_login = self.driver.find_element_by_css_selector(self.selector_collection["publicationUserLogin"])
        next_button = self.driver.find_element_by_css_selector(self.selector_collection["paginationArrow"])

        if self.post.one_by_link(link) is None:
            self.post.add_post(
                user_login.get_attribute("innerHTML"),
                None,
                url_collection[0],
                link,
                date.get_attribute("datetime")
            )
            next_button.click()
            print("Add new post")
            return False
        else:
            print("Skip")
            next_button.click()
            return True
