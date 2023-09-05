from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement

class Selenium():
    def __init__(self, hub_url: str, options: dict = None, headless: bool = True):
        self.hub_url = hub_url
        self.headless = headless
        self.options = Options()
        if options:
            for key, value in options.items():
                setattr(self.options, key, value)
        if headless:
            self.options.add_argument("--headless=new")
        self._driver = None

    @property
    def driver(self) -> WebDriver:
        if self._driver is None:
            print(f'启动浏览器 Chrome headless={self.headless}')
            self._driver = webdriver.Remote(self.hub_url, options=self.options)
        return self._driver

    def get(self, url: str):
        print('打开网页')
        self.driver.get(url)

    def find_element(self, by: str, value: str) -> WebElement:
        print(f'定位元素{by}={value}')
        print('by', type(by), value, type(value))
        try:
            return self.driver.find_element(by, value)
        except Exception:
            raise Exception(f'定位元素{by}={value}失败')

    def click(self, by: str, value: str):
        print(f'点击元素{by}={value}')
        elm = self.find_element(by, value)
        try:
            elm.click()
        except Exception:
            raise Exception(f'点击元素{by}={value}失败')

    def send_keys(self, by: str, value: str, text: str):
        print(f'向元素{by}={value}输入"{text}"')
        elm = self.find_element(by, value)
        try:
            elm.send_keys(text)
        except Exception:
            raise Exception(f'向元素{by}={value}输入"{text}"失败')

    def quit(self):
        print('关闭浏览器')
        self.driver.quit()

