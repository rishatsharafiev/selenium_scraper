import os, unittest
from datetime import datetime
from selenium import webdriver
from pyvirtualdisplay import Display
from selenium.common.exceptions import WebDriverException, NoSuchElementException

import requests

class TestEdaDealSite(unittest.TestCase):

    def setUp(self):
        self.display = Display(visible=0, size=(800,600))
        # self.display.start()

        self.current_path = os.path.dirname(os.path.realpath(__file__))
        self.chromedriver_path = os.path.join(self.current_path, 'chromedriver')
        self.driver = webdriver.Chrome(self.chromedriver_path)

    def test_get_offers_list(self):
        driver = self.driver
        driver.implicitly_wait(10)
        try:
            product_counter = 1
            for page in range(1, 250):
                try:
                    page_url = 'https://edadeal.ru/naberezhnye-chelny/offers?page={}'.format(page)
                    print('<---- Page #{} ---->'.format(page))
                    driver.get(page_url)
                    elements = driver.find_elements_by_class_name('b-offer__root')
                    # driver.find_element_by_class_name('b-pagination')
                    for element in elements:
                        image_url = element.find_element_by_class_name('b-image__img').get_attribute('src')
                        request = requests.get(image_url, stream=True, timeout=30)
                        filename = image_url.split(os.sep)[-1]
                        with open(os.path.join('images', filename), 'wb') as image:
                            image.write(request.content)
                        product_counter +=1
                except NoSuchElementException:
                    driver.implicitly_wait(10)
                    driver.get(page_url)
                    elements = driver.find_elements_by_class_name('p-offers__offer')
                    print('Increase wait to 10')
                except WebDriverException as err:
                    print('Error is happened: <{}>'.format(str(err)))
        finally:
            driver.quit()


if __name__ == "__main__":
    unittest.main()
