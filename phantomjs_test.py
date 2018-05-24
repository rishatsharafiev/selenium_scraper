import os, unittest
from selenium import webdriver

class TestOne(unittest.TestCase):

    def setUp(self):
        current_path = os.path.dirname(os.path.realpath(__file__))
        phantomjs_path = os.path.join(current_path, 'phantomjs')
        self.driver = webdriver.PhantomJS(phantomjs_path)
        self.driver.set_window_size(1120, 550)

    def test_search_in_python_org(self):
        self.driver.get("http://duckduckgo.com/")
        self.driver.find_element_by_id(
            'search_form_input_homepage').send_keys("realpython")
        self.driver.find_element_by_id("search_button_homepage").click()
        self.assertIn(
            "https://duckduckgo.com/?q=realpython", self.driver.current_url
        )

    def tearDown(self):
        self.driver.quit()

if __name__ == "__main__":
    unittest.main()
