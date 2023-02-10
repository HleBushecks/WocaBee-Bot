import csv
import sys

from googletrans import Translator
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as CService
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service as FService

import config

TRANSLATOR = Translator()


def get_mode():
    modes = []
    ids = ['translateWord', 'chooseWord', 'findPair', 'completeWord', 'transcribe']

    for i in ids:
        modes.append(driver.find_element(By.ID, i))

    for i in modes:
        if 'none' not in i.get_attribute('style'):
            return i.find_element(By.CLASS_NAME, 'methodDesc').text


def get_word_for_translate(identifier):
    return driver.find_element(By.ID, identifier).text


def translate_word(word):
    with open('correct_words.csv', 'r') as f:
        reader = csv.reader(f)
        for i in reader:
            if i[0] == word:
                return i[1]

    if TRANSLATOR.detect(word).lang == config.first_lang:
        return TRANSLATOR.translate(word, dest=config.second_lang).text
    else:
        return TRANSLATOR.translate(word, dest=config.first_lang).text


def enter_word():
    driver.find_element(By.ID, 'translateWordAnswer').send_keys(translate_word(get_word_for_translate('q_word')))
    driver.find_element(By.ID, 'translateWordSubmitBtn').click()


def chose_option():
    word = translate_word(get_word_for_translate("ch_word"))
    buttons = driver.find_element(By.ID, 'chooseWords').find_elements(By.CLASS_NAME, 'chooseWordAnswer')
    for btn in buttons:
        if btn.text == word:
            btn.click()
            return
    buttons[0].click()


def repair_wrong_word():
    word = translate_word(get_word_for_translate('completeWordQuestion'))
    wrong_word = driver.find_element(By.ID, 'completeWordAnswer').text

    buttons = driver.find_element(By.ID, 'characters').find_elements(By.CLASS_NAME, 'char')
    clicks = wrong_word.count('_')

    if len(word) != len(wrong_word):
        for i in range(clicks):
            buttons[i].click()
    else:
        for i, j in zip(word, wrong_word):
            if j == '_':
                for btn in buttons:
                    if btn.text == i and 'hidden;' not in btn.get_attribute('style'):
                        btn.click()
                        break

    driver.find_element(By.ID, 'completeWordSubmitBtn').click()


def choose_pair():
    q_buttons = driver.find_element(By.ID, 'q_words').find_elements(By.CLASS_NAME, 'btn')
    words = []
    for btn in q_buttons:
        words.append(btn.text)

    translated_words = []
    for word in words:
        translated_words.append(translate_word(word))

    a_buttons = driver.find_element(By.ID, 'a_words').find_elements(By.CLASS_NAME, 'btn')
    example_words = []
    for btn in a_buttons:
        example_words.append(btn.text)

    for q in range(3):
        for a in range(3):
            if translated_words[q] == example_words[a]:
                q_buttons[q].click()
                a_buttons[a].click()
                return
    q_buttons[0].click()
    a_buttons[0].click()


def autologin():
    driver.find_element(By.ID, 'login').send_keys(config.login)
    driver.find_element(By.ID, 'password').send_keys(config.password)
    driver.find_element(By.ID, 'submitBtn').click()


if __name__ == "__main__":

    if config.browser == 'firefox':
        driver = webdriver.Firefox(service=FService(executable_path=config.driver))
        driver.get('https://www.wocabee.app/app/?lang=CZ')
    else:
        driver = webdriver.Chrome(service=CService(executable_path=config.driver))
        driver.get('https://www.wocabee.app/app/?lang=CZ')

    if '--autologin' in sys.argv:
        autologin()

    try:
        while True:
            try:
                mode = get_mode()

                if mode == 'Translate':
                    enter_word()

                elif mode == 'Choose the correct translation':
                    chose_option()

                elif mode == 'Fill in the missing characters':
                    repair_wrong_word()

                elif mode == 'Select the correct pair':
                    choose_pair()

                elif mode == 'Listen and write':
                    driver.find_element(By.ID, 'transcribeSkipBtn').click()

                # block for getting correct and incorrect words and saving to file
                if 'none' not in driver.find_element(By.ID, 'incorrect').get_attribute('style'):
                    correct_word_1 = driver.find_element(By.CLASS_NAME, 'correctWordQuestion').text
                    correct_word_2 = driver.find_element(By.CLASS_NAME, 'correctWordAnswer').text
                    with open('correct_words.csv', 'a') as file:
                        writer = csv.writer(file)
                        writer.writerow([correct_word_1, correct_word_2])
                        writer.writerow([correct_word_2, correct_word_1])
                    driver.find_element(By.ID, 'incorrect-next-button').click()
            except Exception:
                pass

    finally:
        driver.close()
        driver.quit()
