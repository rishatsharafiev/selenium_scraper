import os, unittest, csv
from datetime import datetime
from selenium import webdriver
from pyvirtualdisplay import Display
from selenium.common.exceptions import WebDriverException, NoSuchElementException

import requests

class TestEdaDealSite(unittest.TestCase):

    def setUp(self):
        self.display = Display(visible=0, size=(1024,800))
        self.display.start()

        self.current_path = os.path.dirname(os.path.realpath(__file__))
        self.chromedriver_path = os.path.join(self.current_path, 'chromedriver')
        self.driver = webdriver.Chrome(self.chromedriver_path)
        self.write_filename = 'output.csv'

    def test_get_offers_list(self):
        driver = self.driver
        driver.implicitly_wait(15)

        try:
            with open(self.write_filename, 'w', encoding='utf-8') as write_file:
                csv_writer = csv.writer(write_file, delimiter=';', quotechar='|', quoting=csv.QUOTE_MINIMAL, lineterminator='\n')
                col_names = ['Описание', 'Количество', 'Старая цена', 'Новая цена', 'Картинка', ]
                csv_writer.writerow([i.encode('utf8').decode('utf8') for i in col_names])

                for page in range(1, 250):
                    try:
                        page_url = 'https://edadeal.ru/naberezhnye-chelny/offers?page={}'.format(page)
                        driver.get(page_url)
                        elements = driver.find_elements_by_class_name('b-offer__root')
                        for element in elements:
                            image_url = element.find_element_by_class_name('b-image__img').get_attribute('src')
                            request = requests.get(image_url, stream=True, timeout=40)
                            filename = image_url.split(os.sep)[-1]
                            with open(os.path.join('images', filename), 'wb') as image:
                                image.write(request.content)
                            try:
                                description = element.find_element_by_class_name('b-offer__description').text
                            except NoSuchElementException:
                                description = ''
                            try:
                                quantity = element.find_element_by_class_name('b-offer__quantity').text
                            except NoSuchElementException:
                                quantity = ''
                            try:
                                price_old = element.find_element_by_class_name('b-offer__price-old').text
                            except NoSuchElementException:
                                price_old = ''
                            try:
                                price_new = element.find_element_by_class_name('b-offer__price-new').text
                            except NoSuchElementException:
                                price_new = ''

                            csv_writer.writerow([description, quantity, price_old, price_new, filename])
                            print('---> ', description)
                    except NoSuchElementException:
                        print('NoSuchElementException')
                    except WebDriverException as err:
                        print('Error is happened: <{}>'.format(str(err)))
        finally:
            driver.quit()


if __name__ == "__main__":
    unittest.main()
