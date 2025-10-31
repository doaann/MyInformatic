import unittest
from selenium.webdriver.support import expected_conditions as EC

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions

channel_name=input("enter the channel's id please :")

class TestPythonWebsite(unittest.TestCase):
    def setUp(self) -> None:
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

    def test_search_in_python_org(self):
        driver = self.driver
        driver.get(f"https://www.youtube.com/@{channel_name}")
        elem = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, "yt-spec-touch-feedback-shape__fill")))
        elem.click()
        assert "There were no results for" not in driver.title


    def tearDown(self) -> None:
        self.driver.close()
