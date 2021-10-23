from selenium.webdriver.common.by import By
from page import BasePage

class YandexMainPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        self.driver.get("http://www.yandex.ru")
        self.images = self.find_element((By.LINK_TEXT, "Картинки"))

    def is_suggest_visible(self):
        try:
            self.find_element((By.CLASS_NAME, "mini-suggest__popup_visible"))
            return True
        except:
            return False

    def get_search_field(self):
        search = self.find_element((By.ID, "text"))
        return search

    def redirect_to_yandex_images(self):
        self.images.click()
        self.driver.close()
        self.driver.switch_to.window(self.driver.window_handles[0])
        assert "yandex.ru/images" in self.driver.current_url, "Некорректно перешли на картинки"
        return YandexImagesPage(self.driver)

class YandexSearchPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        if "yandex.ru/search" not in self.driver.current_url:
            raise RuntimeError("Illegal URL")

    def get_results(self):
        results = self.find_elements((By.CSS_SELECTOR, ".serp-item.desktop-card"))
        return results

class YandexImagesPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        if "yandex.ru/images" not in self.driver.current_url:
            raise RuntimeError("Illegal URL")

    def get_image_categories(self):
        categories = self.find_elements((By.CLASS_NAME, "PopularRequestList-Item"))
        return categories

class YandexImageSearchPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        if "yandex.ru/images/search" not in self.driver.current_url:
            raise RuntimeError("Illegal URL")

    def get_current_search_request(self):
        search_box = self.find_element((By.CLASS_NAME, "input__control"))
        return search_box.get_attribute("value")

    def get_images(self):
        return self.find_elements((By.CLASS_NAME, "serp-item_type_search"))

    def is_image_open(self):
        try:
            self.find_element((By.CLASS_NAME, "MediaViewer"))
            return True
        except:
            return False

    def get_modal_image(self):
        if not self.is_image_open():
            return ""
        return self.find_element((By.CLASS_NAME, "MMImage-Origin")).get_attribute("src")