import time
import traceback
from pyvirtualdisplay import Display


from selenium.webdriver.common.by import By
from seleniumbase import Driver


def close_windows(driver):
    while True:
        if len(driver.window_handles) > 1:
            try:
                driver.switch_to.window(driver.window_handles[1])
                driver.close()
                time.sleep(1)
            except Exception as e:
                traceback.print_exc()
                print(e)
        else:
            break

if __name__ == '__main__':
        # Start virtual display
        display = Display(visible=0, size=(1920, 1080))
        display.start()

        driver = Driver(headless=True , extension_dir='MetaMask')
        time.sleep(5)
        close_windows(driver)
        driver.switch_to_window(driver.window_handles[0])
        driver.get('https://ofc.onefootball.com/s2?referral=mMYdExLOn8ad')
        time.sleep(2)
        driver.wait_for_element(By.CSS_SELECTOR, 'body > main > header > div > div > div > button',
                                timeout=30).click()
        time.sleep(2)
        driver.wait_for_element(
            '#privy-modal-content > div > div.sc-fUnMCh.itSONO > div.sc-eldPxv.jZzOQY > div > button:nth-child(1)',
            timeout=30).click()
        print(driver.window_handles)
        time.sleep(10)
        print(driver.window_handles)
        time.sleep(2)

        # Stop virtual display
        driver.quit()
        display.stop()
        