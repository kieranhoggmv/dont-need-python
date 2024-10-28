import glob
from bs4 import BeautifulSoup

from dotenv import load_dotenv
import os

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from chromedriver_py import binary_path

load_dotenv()

LOCAL_USER = os.getenv("LOCAL_USER")
CHROME_PROFILE = os.getenv("CHROME_PROFILE")


class Browser:

    def __init__(self):
        os.system("taskkill /f /im chrome.exe")
        options = webdriver.ChromeOptions()
        options.add_argument("--log-level=3")
        options.add_experimental_option("detach", True)
        options.add_argument("--disable-infobars")
        profile_path = rf"C:\Users\{LOCAL_USER}\AppData\Local\Google\Chrome\User Data"
        profile_name = "Profile 1"
        profiles = glob.glob(f"{profile_path}/Profile*")
        if len(profiles) > 1:
            profile_name = profiles[-1].split(os.sep)[-1]
            print(
                f'Warning: multiple Chrome profiles found. Using {profile_name}, if this is incorrect, add e.g. "CHROME_PROFILE = Profile 1" to .env'
            )
        options.add_argument(f"--user-data-dir={profile_path}")
        options.add_argument(f"--profile-directory={profile_name}")
        svc = webdriver.ChromeService(
            executable_path=binary_path,
            capabilities=options.to_capabilities(),
        )

        options.add_experimental_option("detach", True)
        self.driver = webdriver.Chrome(service=svc, options=options)

    def get_url_source(self, url):
        self.driver.get(url)
        self.driver.minimize_window()
        return BeautifulSoup(self.driver.page_source, features="html.parser")
