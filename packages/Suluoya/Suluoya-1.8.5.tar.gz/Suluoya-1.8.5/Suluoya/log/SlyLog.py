import time


class SlyLog(object):
    def __init__(self, filename='log'):
        self.filename = filename
        self.Time = time.asctime(time.localtime(time.time()))
        with open(f'{self.filename}.txt', 'w', encoding='utf8') as f:
            f.write(self.Time+'\n')
            f.write("(｡･∀･)ﾉﾞ嗨!\n\n")

    def write(self, contents='', title=''):
        with open(f'{self.filename}.txt', 'a', encoding='utf8') as f:
            f.write(f'\n{title}\n')
            f.write(contents)

    def easy_write(self, contents=''):
        with open(f'{self.filename}.txt', 'a', encoding='utf8') as f:
            f.write('\n'+contents)

    def warning(self, contents='warning'):
        print(f'\033[1;32;40m{contents}')
        self.write(contents, 'warning  o(≧口≦)o\n♛♛♛♛♛♛♛♛♛♛♛♛♛♛♛♛♛♛♛')

    def error(self, contents='error'):
        print(f'\033[1;31;40m{contents}')
        self.write(contents, 'error  ≧ ﹏ ≦\n♛♛♛♛♛♛♛♛♛♛♛♛♛♛♛♛♛♛♛')

    def info(self, contents='info'):
        print(f'\033[1;36;40m{contents}')
        self.write(contents, 'info  ヾ(≧▽≦*)o\n♛♛♛♛♛♛♛♛♛♛♛♛♛♛♛♛♛♛♛')

    def black(self, contents='black'):
        '''
        Black
        '''
        print(f'\033[1;30;40m{contents}')
        self.easy_write(contents)

    def red(self, contents='red'):
        print(f'\033[1;31;40m{contents}')
        self.easy_write(contents)

    def green(self, contents='green'):
        print(f'\033[1;32;40m{contents}')
        self.easy_write(contents)

    def yellow(self, contents='yellow'):
        print(f'\033[1;33;40m{contents}')
        self.easy_write(contents)

    def blue(self, contents='blue'):
        print(f'\033[1;34;40m{contents}')
        self.easy_write(contents)

    def pink(self, contents='pink'):
        print(f'\033[1;35;40m{contents}')
        self.easy_write(contents)

    def cyan(self, contents='cyan'):
        print(f'\033[1;36;40m{contents}')
        self.easy_write(contents)

    def white(self, contents='white'):
        print(f'\033[1;37;40m{contents}')
        self.easy_write(contents)

