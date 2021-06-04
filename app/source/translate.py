from datetime import datetime as dt
import os
from time import sleep

from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


def get_title_chapter_list():
    # テキストの読み込みパス
    path_r = 'text/result.txt'
    # txtファイルの読み込み
    s_l = []
    with open(path_r) as f:
        s_l = [s.strip() for s in f.readlines()]
    # 章題はtitle_listへ追加、本文はbody_listへ追加
    title_list = []
    chapter_list = []
    body_list = []
    for index, string in enumerate(s_l):
        if '##' in string:
            title_list.append(string)
            if index != 0:
                chapter_list.append(body_list)
                body_list = []
        elif string:
            body_list.append(string)
        if index + 1 == len(s_l):
            chapter_list.append(body_list)
    return title_list, chapter_list


def translate(input_text):
    driver = webdriver.Remote(
        command_executor=os.environ['SELENIUM_URL'],
        desired_capabilities=DesiredCapabilities.FIREFOX.copy()
    )
    driver.set_window_size('1200', '1000')
    driver.get('https://www.deepl.com/ja/translator')

    driver.implicitly_wait(3)
    sleep(5)

    input_selector = '#dl_translator > div.lmt__text > div.lmt__sides_container > div.lmt__side_container.lmt__side_container--source > div.lmt__textarea_container > div.lmt__inner_textarea_container > textarea'
    # test
    # input_text = 'This is the test. But I set fire to the rain.'
    driver.find_element_by_css_selector(
        input_selector).send_keys(input_text)

    sleep(5)

    Output_selector = '#dl_translator > div.lmt__text > div.lmt__sides_container > div.lmt__side_container.lmt__side_container--target > div.lmt__textarea_container.lmt__textarea_container_no_shadow > div.lmt__translations_as_text > p.lmt__translations_as_text__item.lmt__translations_as_text__main_translation > button.lmt__translations_as_text__text_btn'
    # '#dl_translator > div.lmt__sides_container > div.lmt__side_container.lmt__side_container--target > div.lmt__textarea_container > div.lmt__translations_as_text > p > button.lmt__translations_as_text__text_btn'
    output_text = driver.find_element_by_css_selector(
        Output_selector).get_attribute('textContent')
    print(output_text)

    # スクショ（確認用）
    # driver.save_screenshot('{0:%Y_%m_%d__%H_%M_%S}'.format(dt.now()) + '.png')

    driver.quit()

    return output_text


if __name__ == '__main__':
    # タイトルと章ごとの本文リストを取得
    title_list, chapter_list = get_title_chapter_list()
    # 最終出力データ
    result = ''
    for index, body_list in enumerate(chapter_list):
        # 章題を追加
        result += f"{title_list[index]}\n"
        for idx, body in enumerate(body_list):
            # 1文ごとに翻訳
            output_text = translate(body)
            # 本文の結果を追加
            result += f"{idx+1}. {body}\n\t- =={output_text}==\n"
        result += "\n"
    # ファイルへの書き込み
    path_w = 'text/translate.txt'
    with open(path_w, mode='w') as f:
        f.write(result)
    print('translation, done!')
