import os

from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from selenium.common.exceptions import ElementNotInteractableException, NoSuchElementException

PROMISED_DOWNLOAD = os.getenv('upload')
PROMISED_UPLOAD = os.getenv('download')
TWITTER_LOGIN = os.getenv('login')
TWITTER_PASSWORD = os.getenv('password')
INTERNET_PROVIDER = os.getenv('internet_provider_handle')

download_speed = None
upload_speed = None


class InternetSpeedTwitterBot:
    def __init__(self):
        self.chrome_options = webdriver.ChromeOptions()
        self.chrome_options.add_experimental_option('detach', True)
        self.driver = webdriver.Chrome(options=self.chrome_options)
        self.up = PROMISED_UPLOAD
        self.down = PROMISED_DOWNLOAD

    def get_speed(self):
        self.driver.get('https://www.speedtest.net/')
        time.sleep(1)

        internet_speed_start = self.driver.find_element(By.CSS_SELECTOR, 'span.start-text')
        time.sleep(3)
        internet_speed_start.click()

        time.sleep(40)

        close_ad = self.driver.find_element(By.CSS_SELECTOR, 'a.notification-dismiss')
        try:
            close_ad.click()
        except ElementNotInteractableException:
            pass

        global upload_speed, download_speed
        download_speed = self.driver.find_element(By.XPATH, '//*[@id="container"]/div/div[3]/div/div/div/div[2]/div['
                                                           '3]/div[3]/div/div[3]/div/div/div[2]/div[1]/div['
                                                           '1]/div/div[2]/span').text

        upload_speed = self.driver.find_element(By.XPATH, '//*[@id="container"]/div/div[3]/div/div/div/div[2]/div['
                                                         '3]/div[3]/div/div[3]/div/div/div[2]/div[1]/div[2]/div/div['
                                                         '2]/span').text

        time.sleep(5)
        self.driver.close()

    def tweet_at_provider(self):
        self.driver = webdriver.Chrome(options=self.chrome_options)
        self.driver.get('https://x.com/i/flow/login')
        # time.sleep(2)
        #
        # sign_in = self.driver.find_element(By.XPATH, '/html/body/div/div/div/div[2]/main/div/div/div[1]/div/div/div[3]/div[4]/a')
        # sign_in.click()

        time.sleep(4)

        enter_username = self.driver.find_element(By.NAME, 'text')
        enter_username.click()
        enter_username.send_keys(TWITTER_LOGIN)
        time.sleep(1)

        next_button = self.driver.find_element(By.XPATH, '//*[@id="layers"]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div/div/div/button[2]/div')
        next_button.click()
        time.sleep(2)

        self.driver.switch_to.active_element.send_keys(TWITTER_PASSWORD)

        login = self.driver.find_element(By.XPATH, '//*[@id="layers"]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[2]/div/div/div/div/button/div')
        login.click()
        time.sleep(3)

        tweet = self.driver.find_element(By.CLASS_NAME, 'public-DraftStyleDefault-block')
        tweet.send_keys(f'Hey @{os.getenv("internet_provider_handle")}, why is my internet speed {download_speed}down/{upload_speed}up when '
                        f'I pay for {PROMISED_DOWNLOAD}down/{PROMISED_UPLOAD}up?')
        time.sleep(2)
        post = self.driver.find_element(By.XPATH, '/html/body/div[1]/div/div/div[2]/main/div/div/div/div/div/div[3]/div/div[2]/div[1]/div/div/div/div[2]/div[2]/div[2]/div/div/div/button/div')
        post.click()

        try:
            close_ad = self.driver.find_element(By.XPATH, '//*[@id="layers"]/div[2]/div/div/div/div/div/div[2]/div['
                                                      '2]/div/div[1]/div/div/div/div[1]/div/div/svg')
            close_ad.click()
        except NoSuchElementException:
            pass


while True:
    bot = InternetSpeedTwitterBot()
    bot.driver.maximize_window()

    bot.get_speed()

    if PROMISED_DOWNLOAD > int(round(float(download_speed))) or PROMISED_UPLOAD > int(round(float(upload_speed))):
        bot.tweet_at_provider()
    time.sleep(60*60*24)
