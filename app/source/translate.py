from datetime import datetime as dt
import os
import re
from time import sleep

from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


def get_title_chapter_list():
    # テキストの読み込みパス
    path_r = 'text/format.txt'
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

    output_selector = '#dl_translator > div.lmt__text > div.lmt__sides_container > div.lmt__side_container.lmt__side_container--target > div.lmt__textarea_container > div.lmt__translations_as_text > p > button.lmt__translations_as_text__text_btn'
    output_text = driver.find_element_by_css_selector(
        output_selector).get_attribute('textContent')

    # スクショ（確認用）
    # driver.save_screenshot('{0:%Y_%m_%d__%H_%M_%S}'.format(dt.now()) + '.png')

    driver.quit()

    return output_text


def formula2eqs(body):
    # 変換する辞書（key: 変換後の文字列, value: 変換前の文字列）
    formula_dict = {}
    # markdown記法の数式パターン
    formula_pattern = '\$.*?\$'
    formula_body = re.findall(formula_pattern, body)
    # 変換する文字列を辞書に登録
    for i, fb in enumerate(formula_body):
        formula_dict[f'<<EQS{i}>>'] = repr(fb)
        body = re.sub(formula_pattern, f'<<EQS{i}>>', body, 1)
    return body, formula_dict


def eqs2formula(body, formula_dict):
    for key, value in formula_dict.items():
        body = body.replace(key, eval(value))
    return body


if __name__ == '__main__':
    # タイトルと章ごとの本文リストを取得
    title_list, chapter_list = get_title_chapter_list()
    # 最終出力データ
    result = ''
    try:
        for index, body_list in enumerate(chapter_list):
            # 章題を追加
            result += f"{title_list[index]}\n"
            # 章題を出力
            print('*'*100)
            print(
                f'({str(index+1).zfill(len(str(len(chapter_list))))}/{len(chapter_list)}): {title_list[index]}')
            print('*'*100)
            for idx, body in enumerate(body_list):
                # 数式コードを<<EQS{N}>>へ変換
                new_body, formula_dict = formula2eqs(body)
                # 1文ごとに翻訳（結果がなければ最大10回繰り返して翻訳にかける）
                loop_num = 0
                output_text = ''
                while(not output_text and loop_num < 5):
                    try:
                        output_text = translate(new_body)
                    except:
                        print(f'翻訳失敗！（残りtry回数：{5-loop_num+1}）')
                    loop_num += 1
                    # 5回tryして失敗した場合、例外を発生させ、途中結果を出力
                    if 5 <= loop_num:
                        raise Exception
                # 数式文字列を元に戻す
                output_text = eqs2formula(output_text, formula_dict)
                # 翻訳結果出力
                print(
                    f'({str(idx+1).zfill(len(str(len(body_list))))}/{len(body_list)}): {output_text}')
                # 本文の結果を追加
                result += f"{idx+1}. {body}\n\t- =={output_text}==\n"
            result += "\n"
    except:
        # ファイルへの書き込み
        path_w = 'text/translate_not_completed.txt'
        with open(path_w, mode='w') as f:
            f.write(result)
        print('translation is not completed... Try again.')
    # ファイルへの書き込み
    path_w = 'text/translate.txt'
    with open(path_w, mode='w') as f:
        f.write(result)
    print('translation, done!')
