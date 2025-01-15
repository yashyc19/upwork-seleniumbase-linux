import json
import os
import random
import time
import traceback


from selenium.webdriver.common.by import By
from seleniumbase import Driver
from bip_utils import Bip39MnemonicGenerator, Bip39SeedGenerator, Bip44, Bip44Coins, Bip44Changes
import re


def generate_wallet():
    # Генерація мнемонічної фрази
    mnemonic = Bip39MnemonicGenerator().FromWordsNumber(12)

    # Генерація seed із мнемонічної фрази
    seed = Bip39SeedGenerator(mnemonic).Generate()

    # Створення гаманця з використанням BIP44 (Ethereum)
    bip44_wallet = Bip44.FromSeed(seed, Bip44Coins.ETHEREUM)
    account = bip44_wallet.Purpose().Coin().Account(0).Change(Bip44Changes.CHAIN_EXT).AddressIndex(0)

    return {
        "mnemonic": str(mnemonic),  # Приведення до рядка
        "address": account.PublicKey().ToAddress(),
        "private_key": account.PrivateKey().Raw().ToHex()
    }

def save_wallet_to_file(wallet, filename="wallet.json"):
    with open(filename, "w") as f:
        json.dump(wallet, f, indent=4)

def login_to_metamask(driver, seed_phrase):
    driver.switch_to.window(driver.window_handles[0])
    time.sleep(1)
    driver.get(f'chrome-extension://{extension_id}/home.html#onboarding/welcome')
    time.sleep(1)
    shadow_host = driver.find_element(By.XPATH, '//*[@id="app-content"]/div/div[2]/div/div/div/ul/li[1]/div/input')
    shadow_host.click()
    driver.wait_for_element(By.CSS_SELECTOR,
                            '#app-content > div > div.mm-box.main-container-wrapper > div > div > div > ul > li:nth-child(3) > button').click()
    time.sleep(1)
    driver.wait_for_element(
        '#app-content > div > div.mm-box.main-container-wrapper > div > div > div > div.mm-box.onboarding-metametrics__buttons.mm-box--display-flex.mm-box--gap-4.mm-box--flex-direction-row.mm-box--width-full > button.mm-box.mm-text.mm-button-base.mm-button-base--size-lg.mm-button-secondary.mm-text--body-md-medium.mm-box--padding-0.mm-box--padding-right-4.mm-box--padding-left-4.mm-box--display-inline-flex.mm-box--justify-content-center.mm-box--align-items-center.mm-box--color-primary-default.mm-box--background-color-transparent.mm-box--rounded-pill.mm-box--border-color-primary-default.box--border-style-solid.box--border-width-1').click()
    word_places = [driver.find_element(f'#import-srp__srp-word-{i}') for i in range(12)]
    for index, word_place in enumerate(word_places):
        word_place.send_keys(seed_phrase.split()[index])
        time.sleep(random.randint(1, 10) * 0.05)
    driver.find_element(By.CSS_SELECTOR,
                        '#app-content > div > div.mm-box.main-container-wrapper > div > div > div > div.import-srp__actions > div > button').click()
    time.sleep(1)
    driver.find_element(By.CSS_SELECTOR,
                        '#app-content > div > div.mm-box.main-container-wrapper > div > div > div > div.mm-box.mm-box--margin-top-3.mm-box--justify-content-center > form > div:nth-child(1) > label > input').send_keys(
        '123456789')
    time.sleep(1)
    driver.find_element(By.CSS_SELECTOR,
                        '#app-content > div > div.mm-box.main-container-wrapper > div > div > div > div.mm-box.mm-box--margin-top-3.mm-box--justify-content-center > form > div:nth-child(2) > label > input').send_keys(
        '123456789')
    time.sleep(1)
    driver.find_element(By.CSS_SELECTOR,
                        '#app-content > div > div.mm-box.main-container-wrapper > div > div > div > div.mm-box.mm-box--margin-top-3.mm-box--justify-content-center > form > div.mm-box.mm-box--margin-top-4.mm-box--margin-bottom-4.mm-box--justify-content-space-between.mm-box--align-items-center > label > span.mm-checkbox__input-wrapper > input').click()
    time.sleep(1)
    driver.find_element(By.CSS_SELECTOR,
                        '#app-content > div > div.mm-box.main-container-wrapper > div > div > div > div.mm-box.mm-box--margin-top-3.mm-box--justify-content-center > form > button').click()
    time.sleep(1)
    driver.find_element(By.CSS_SELECTOR,
                        '#app-content > div > div.mm-box.main-container-wrapper > div > div > div > div.mm-box.creation-successful__actions.mm-box--margin-top-6.mm-box--display-flex.mm-box--flex-direction-column.mm-box--justify-content-center.mm-box--align-items-center > button').click()
    time.sleep(1)
    driver.find_element(By.CSS_SELECTOR,
                        '#app-content > div > div.mm-box.main-container-wrapper > div > div > div > div.onboarding-pin-extension__buttons > button').click()
    time.sleep(1)
    driver.find_element(By.CSS_SELECTOR,
                        '#app-content > div > div.mm-box.main-container-wrapper > div > div > div > div.onboarding-pin-extension__buttons > button').click()
    driver.wait_for_element('#app-content > div > div.mm-box.main-container-wrapper > div > div > div > div.account-overview__balance-wrapper > div > div.wallet-overview__balance > div > div > div > div.eth-overview__primary-container > div > span.mm-box.mm-text.currency-display-component__text.mm-text--inherit.mm-text--ellipsis.mm-box--color-text-default',timeout=30)
    driver.save_screenshot('metamask.png')

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
    driver = Driver(headless2=False, extension_dir='MetaMask',window_size='1200,800')
    print(driver.get_window_position())
    print(driver.get_window_size())
    time.sleep(5)
    driver.switch_to_window(driver.window_handles[1])

    extension_url = driver.get_current_url()
    match = re.search(r'chrome-extension://([a-z0-9]+)', extension_url)

    if match:
        extension_id = match.group(1)
        print(extension_id)
    close_windows(driver)
    wallet = generate_wallet()
    save_wallet_to_file(wallet)
    with open('wallet.json', 'r') as f:
        wallet = json.load(f)
        seed_phrase = wallet['mnemonic']
    while True:
        try:
            login_to_metamask(driver, seed_phrase)
            break
        except Exception as e:
            traceback.print_exc()
            print(e)
    driver.switch_to_window(driver.window_handles[0])

    # Print window handles before taking screenshots
    print("Window handles before clicking button:", driver.window_handles)

    driver.get('https://balance.fun/account/deposit')
    time.sleep(5)

    # Take screenshot of the first window
    driver.save_screenshot('window1_screenshot.png')
    print("Screenshot of window 1 saved.")

    driver.wait_for_element(By.CSS_SELECTOR, '#__next > div > div > div.Connect_flex__viPdX.Connect_fixContent__gf23w > div.Connect_hoemFix__YKQdo > div > div',
                            timeout=30).click()

    time.sleep(5)
    try:
        driver.wait_for_element('#__next > div > div > div.Connect_flex__viPdX.Connect_fixContent__gf23w > div:nth-child(2) > div > div.Connect_leftDiv__aKyUD > ul > li:nth-child(2)').click()
    except:
        pass
    time.sleep(5)
    # Print window handles after the new tab opens
    print("Window handles after clicking button:", driver.window_handles)

    # Switch to the new tab (if the window handles increased)
    if len(driver.window_handles) > 1:
        driver.switch_to.window(driver.window_handles[1])  # Switch to the new tab
        driver.save_screenshot('window2_screenshot.png')
        print("Screenshot of window 2 saved.")

    time.sleep(10)
    print(driver.window_handles)
    time.sleep(2)
