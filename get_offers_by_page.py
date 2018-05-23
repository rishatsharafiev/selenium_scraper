import os
from selenium import webdriver
from pyvirtualdisplay import Display

current_path = os.path.dirname(os.path.realpath(__file__))
chromedriver_path = os.path.join(current_path, 'chromedriver')

display =Display(visible=0, size=(800,600))
display.start()

driver = webdriver.Chrome(chromedriver_path)
try:
    product_counter = 1
    for i in range(1, 237):
        print('<---- Page #{} ---->'.format(i))
        driver.get('https://edadeal.ru/naberezhnye-chelny/offers?page={}'.format(i))
        driver.implicitly_wait(10)
        elements = driver.find_elements_by_class_name('b-offer__root')
        for element in elements:
            print('<---- Product #{} ---->'.format(product_counter))
            print(element.text)
            product_counter +=1

finally:
    driver.quit()
