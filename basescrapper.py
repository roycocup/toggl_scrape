import os
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class BaseScrapper:
    driver = None
    
    def __init__(self, options:list = []):
        try:
            geckoPath = './geckodriver'
            fireFoxOptions = webdriver.FirefoxOptions()
            
            if 'headless' in options:
                fireFoxOptions.headless = True
            self.driver = webdriver.Firefox(executable_path=geckoPath, firefox_options=fireFoxOptions)
        except:
            raise Exception("Cannot start firefox webdriver.", self.driver)
        
        self.driver.implicitly_wait(10)
    
    def get_source_code(self):
        source = self.driver.page_source
        with open('source.txt', "w") as f:
            f.write(source)

    def screenshot(self, filename='default.png'):
        self.driver.save_screenshot(filename=filename)

    def goto(self, url):
        self.driver.get(url)
    
    def quit(self):
        self.driver.quit()

    def get_by_text(self, text=""):
        return self.driver.find_elements_by_xpath("//*[contains(text(), \'"+text+"\')]")

    def wait_for(self, time=60, id=None):
        element = WebDriverWait(self.driver, time).until(EC.visibility_of_element_located((By.Id, id)))
        return element
