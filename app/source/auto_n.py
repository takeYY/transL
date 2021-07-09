def escape_special_words(body, swords):
    for sw in swords:
        body = body.replace(sw, f'『{sw}』')
    return body


def back2special_words(body, swords):
    for sw in swords:
        body = body.replace(f'『{sw}』', sw)
    return body


def auto_n():
    # テキストの読み込みパス
    path_r = 'text/english.txt'
    # テキストの書き込みパス
    path_w = 'text/result.txt'
    s_l = []
    body = ''
    title_list = []
    body_list = []
    result = ''
    # txtファイルの読み込み
    with open(path_r) as f:
        s_l = [s.strip() for s in f.readlines()]
    # 章題はtitle_listへ追加、本文はbody_listへ追加
    for index, string in enumerate(s_l):
        if '##' in string:
            title_list.append(string)
            if index != 0:
                body_list.append('='*50)
        else:
            body_list.append(string)
    # 改行をスペースでjoin
    body = ' '.join(body_list)
    body_list = body.split('='*50)
    # エスケープさせる特殊な表現
    special_words = ['et al.', 'Eqn.', 'Eq.', 'Eqs.',
                     'e.g.', 'i.g.', 'Fig.', 'Tab.']
    for index, bd in enumerate(body_list):
        result += f"{title_list[index]}\n\n"
        # 特殊な表現をエスケープ
        bd = escape_special_words(bd, special_words)
        s_list = bd.split('. ')
        for idx, string in enumerate(s_list):
            # エスケープされた特殊な表現を元に戻す
            string = back2special_words(string, special_words)
            while (string.startswith(' ')):
                string = string[1:]
            string = string.replace('- ', '')
            if idx + 1 == len(s_list):
                result += f"{string}\n"
                break
            result += f"{string}.\n"
        result += "\n"
    # ファイルへの書き込み
    with open(path_w, mode='w') as f:
        f.write(result)
    print('auto_n, done!')


if __name__ == '__main__':
    auto_n()
