import glob
import os
import re
from bs4 import BeautifulSoup

CORPUS_MODULE_PATH = os.path.abspath(os.path.dirname(__file__))
WIKI_FILES_DIRECTORY = CORPUS_MODULE_PATH + '/../../data/wikipedia/*/*'


class WikiProcessing():
    ''' Wikipedia関連の処理を行うclass '''
    def __init__(self):
        return

    def get_files(self):
        return glob.glob(WIKI_FILES_DIRECTORY)

    def separate_paragraph_array(self, document):
        contents = document.read()
        # docタグ以外のタグは削除
        contents = re.sub(r'\<((?!doc).)*?\>', '', contents)
        contents = re.sub(r'\</((?!doc).)*?\>', '', contents)
        # BeautifulSoupの仕様?頭に何かタグを入れないと、<doc>タグを最初の一つしか読まない
        contents = '<docs>\n' + contents + '</docs>'
        soup = BeautifulSoup(contents, "xml")
        wiki_items = soup.find_all('doc')

        wiki_text = ''
        for wiki_item in wiki_items:
            wiki_text += wiki_item.get_text()
        return wiki_text.split('\n')
