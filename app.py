import sys
from modules.preprocess import preprocess
from modules.skipgram import skipgram

if __name__ == '__main__':
    ARGS = sys.argv
    if len(ARGS) == 1 or len(ARGS) > 2:
        print('処理の第一内容を引数に記載してください。')
    elif ARGS[1] == 'preprocess':
        preprocess()
    elif ARGS[1] == 'skipgram':
        skipgram()
    else:
        print('処理の内容を第一引数に記載してください。')
