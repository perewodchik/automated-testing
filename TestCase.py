import unittest
from allure_commons.types import AttachmentType
import allure
from selenium import webdriver
from YandexPage import YandexMainPage, YandexImagesPage, YandexImageSearchPage, YandexSearchPage
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

@allure.severity(allure.severity_level.NORMAL)
class YandexTestSuite(unittest.TestCase):
    """YandexTestSuite"""

    def setUp(self):
        options = webdriver.ChromeOptions()
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        self.driver = webdriver.Chrome(options=options)

    def test_search_result_contains_tensor_link(self):
        """Проверяет, существует ли ссылка на 
            официальный сайт ТЕНЗОР в первых пяти результатах запроса
        """
        
        LINK = "tensor.ru"

        with allure.step("Открывается главная страница яндекс"):
            page = YandexMainPage(self.driver)

        with allure.step("Работаем с поисковой строкой"):
            search = page.get_search_field()
            with allure.step("Вводим данные"):
                search.send_keys("тензор")

            with allure.step("Проверяем, появилась ли окно с подсказками"):
                assert page.is_suggest_visible(), "Окно с подсказками не появилось"
            
            search.submit()

        with allure.step("Проверяем страницу с запросом"):
            page = YandexSearchPage(self.driver)
            results = page.get_results()
            allure.attach(self.driver.get_screenshot_as_png(), name="searchScreen", attachment_type=AttachmentType.PNG)

            with allure.step("Смотрим, ведут ли ссылки на официальный сайт ТЕНЗОР"):
                for result in results:
                    result_link_href = result.find_element(By.TAG_NAME, "a").get_attribute("href")
                    if LINK in result_link_href:
                        return

                assert False,"Ссылки из запроса не ведут на официальный сайт ТЕНЗОР"

        

    def test_yandex_images(self):
        """Тестирует функциональность изображений
        """
        
        with allure.step("Открываем главную страницу яндекса"):
            page = YandexMainPage(self.driver)
        
        with allure.step("Переходим по кнопке Картинки"):
            page = page.redirect_to_yandex_images()
        
        with allure.step("Переходим по первой категории из картинок"):
            categories = page.get_image_categories()
            categories[0].click()
            page = YandexImageSearchPage(self.driver)

            assert page.get_current_search_request() == categories[0].text, \
                "Данные в поисковой строке и в названиях категорий не совпадают"

        with allure.step("Кликаем по картинке"):
            images = page.get_images()
            images[0].click()
        
            assert page.is_image_open, "Картинка не открылась"

        first_image_url = page.get_modal_image()

        with allure.step("Переходим на следующую картинку"):
            ActionChains(self.driver).send_keys(Keys.RIGHT).perform()
            assert first_image_url != page.get_modal_image(), "Картинка не изменилась"

        with allure.step("Возвращаемся на предыдущую и сравниваем результаты"):
            ActionChains(self.driver).send_keys(Keys.LEFT).perform()
            assert first_image_url == page.get_modal_image(), "Картинка не совпадает с исходной"

    def tearDown(self):
        self.driver.close()

if __name__ == "__main__":
    unittest.main()