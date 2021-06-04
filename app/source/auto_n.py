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
    for index, bd in enumerate(body_list):
        result += f"{title_list[index]}\n\n"
        bd = bd.replace('et al.', '『et al』')
        bd = bd.replace('Eqn. ', '『Eqn』')
        bd = bd.replace('Eq. ', '『Eq』')
        s_list = bd.split('. ')
        for idx, string in enumerate(s_list):
            string = string.replace('『et al』', 'et al.')
            string = string.replace('『Eqn』', 'Eqn. ')
            string = string.replace('『Eq』', 'Eq. ')
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
