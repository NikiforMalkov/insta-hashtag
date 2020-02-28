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
            index = 0
            # self.get_publication_collection(self, i)
            publication_collection = self.get_publication_list()
            for i in range(0, len(publication_collection)):
                self.get_post(publication_collection[i])
                index = i

            pub_len = self.get_publication_len()
            print("Количество публикаций - " + str(pub_len))
            while index < self.get_publication_len():
                print("Количество публикаций - " + str(pub_len))

                self.driver.implicitly_wait(1)
                publication_collection = self.get_publication_list()
                print("Новое количество публикаций" + str(len(publication_collection)))
                old_index = index
                for i in range(old_index, len(publication_collection)):
                    self.get_post(publication_collection[i])
                    index = i

            # for publication in publication_collection:
            #    self.get_post(publication)
        finally:
            assert "No publications on the page"

    def get_publication_list(self):
        publication_collection = self.driver.find_elements_by_css_selector(
            self.selector_collection["publicationCollection"]
        )
        return publication_collection

    def get_publication_collection(self, i):
        publication_collection = self.get_publication_list()
        for i in range(0, len(publication_collection)):
            self.get_post(publication_collection[i])
        return i

    def get_publication_len(self):
        publication_collection = self.get_publication_list()
        return len(publication_collection)

    def get_post(self, publication):
        publication_div = publication.find_element_by_css_selector(self.selector_collection["publicationDiv"])
        publication_div.click()
        element = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, self.selector_collection["publicationTime"]))
        )
        # description = self.driver.find_element_by_css_selector(self.selector_collection["publicationDescription"])
        link = publication.get_attribute("href")
        date = self.driver.find_element_by_css_selector(self.selector_collection["publicationTime"])
        image_tag = self.driver.find_element_by_css_selector(self.selector_collection["publicationImage"])
        url_collection = get_url_collection(image_tag.get_attribute("srcset"))
        user_login = self.driver.find_element_by_css_selector(self.selector_collection["publicationUserLogin"])

        if self.post.one_by_link(link) is None:
            self.post.add_post(
                user_login.get_attribute("innerHTML"),
                None,
                url_collection[0],
                link,
                date.get_attribute("datetime")
            )
            self.close_popup()
            print("Add new post")
        else:
            self.close_popup()
            return

    def close_popup(self):
        close_popup_button = self.driver.find_element_by_css_selector(
            self.selector_collection["publicationClosePopupButton"]
        )
        close_popup_button.click()
