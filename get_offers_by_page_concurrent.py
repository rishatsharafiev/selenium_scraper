# -*- coding: utf-8 -*-

import gevent.monkey
gevent.monkey.patch_all()
import gevent
from gevent.queue import Queue, Empty

import os, logging, unittest
from datetime import datetime

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import WebDriverException, NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from pyvirtualdisplay import Display

class TestEdaDealSite(unittest.TestCase):

    def setUp(self):
        self.logger = logging.getLogger(__name__)

        self.tasks = Queue(maxsize=5)

        self.display = Display(visible=0, size=(800,600))
        self.display.start()

        self.current_path = os.path.dirname(os.path.realpath(__file__))
        self.chromedriver_path = os.path.join(self.current_path, 'chromedriver')
        self.times = []
        # TODO: pool of browsers
        # self.drivers = [{'free': True, 'driver': webdriver.Chrome(self.chromedriver_path)} for i in range(5)]

    def parse(self, page):
        now =  datetime.now()

        driver = webdriver.Chrome(self.chromedriver_path)
        driver.implicitly_wait(10)
        page_url = 'https://edadeal.ru/naberezhnye-chelny/offers?page={}'.format(page)
        try:
            driver.get(page_url)
            elements = driver.find_elements_by_class_name('p-offers__offer')
            for element in elements:
                print('<page {}>: '.format(page), element.text)
        except NoSuchElementException:
            driver.implicitly_wait(20)
            driver.get(page_url)
            elements = driver.find_elements_by_class_name('p-offers__offer')
            print('Increase wait to 10')
        except WebDriverException as err:
            print('Error is happened: <{}>'.format(str(err)))
        finally:
            driver.quit()
        timedelta = datetime.now() - now
        self.times.append(timedelta.total_seconds())

    def worker(self, n):
        try:
            while True:
                task = self.tasks.get(timeout=30)
                self.parse(task)
        except Empty:
            print('Quitting time!')

    def main(self):
        for i in range(1, 250):
            self.tasks.put(i)

    def test_get_offers_list(self):
        gevent.joinall([
            gevent.spawn(self.main),
            *[gevent.spawn(self.worker, n) for n in range(5)],
        ])

        total = sum(self.times) or 0
        count = len(self.times) or 1

        print('Average time: {}'.format(total/count))

if __name__ == "__main__":
    unittest.main()
