''' corpusからwordデータを抜き出して、model作成するための前処理 '''
import re
from collections import Counter
import MeCab
from tqdm import tqdm
from modules.models.DbModel import DbModel
from modules.corpus_processing.WikiProcessing import WikiProcessing
from config.config import CONFIG


class WordProcessing():
    ''' 文章から単語の出現頻度を求めたり、単語をindexにしたりするclass '''
    def __init__(self, corpus, docs_files):
        self.corpus = corpus
        self.docs_files = docs_files
        self.file_num = len(docs_files)
        # 日本語の表層系でなく、基本形を使用するためにOchasenを使用
        self.tagger = MeCab.Tagger('-Ochasen')

    def extract_words_fequency(self):
        words_frequency = Counter({})
        unnecessary_words = []

        pbar = tqdm(total=self.file_num)
        pbar.set_description('extract words fequency')
        for docs_file in self.docs_files:
            pbar.update(1)
            with open(docs_file) as doc:
                paragraph_sentence_list =\
                    self.corpus.separate_paragraph_array(doc)
                words_list = []
                for paragraph_sentence in paragraph_sentence_list:
                    node = self.tagger.parseToNode(paragraph_sentence)
                    paragraph_words = []
                    while node:
                        word = node.feature.split(",")[6]
                        # 日本語の表現だけを抽出
                        if re.search(r'[ぁ-んァ-ヶ一-龥]+', word):
                            paragraph_words.append(word)
                        else:
                            if word not in unnecessary_words:
                                unnecessary_words.append(word)
                        node = node.next
                    words_list.extend(paragraph_words)

                words_frequency += Counter(words_list)
        pbar.close()
        return words_frequency

    def _create_word2idx_dict(self, words_info):
        word_stoi = {}
        for word_info in words_info:
            word_stoi[word_info[1]] = word_info[0]
        return word_stoi

    def transfer_sentence_word2idx(self, words_info, db_model):
        word_stoi = self._create_word2idx_dict(words_info)

        pbar = tqdm(total=self.file_num)
        pbar.set_description('transfer sentence word2idx')
        for wiki_file in self.docs_files:
            pbar.update(1)
            with open(wiki_file) as doc:
                inserted_info = []

                paragraph_sentence_list =\
                    self.corpus.separate_paragraph_array(doc)
                for paragraph_sentence in paragraph_sentence_list:
                    node = self.tagger.parseToNode(paragraph_sentence)
                    paragraph_words = []
                    while node:
                        word = node.feature.split(",")[6]
                        # 日本語の表現だけを抽出
                        if re.search(r'[ぁ-んァ-ヶ一-龥]+', word):
                            paragraph_words.append(word_stoi[word])
                        node = node.next

                    if paragraph_words:
                        inserted_info.append((
                            wiki_file, paragraph_sentence, str(paragraph_words)
                        ))

                # 文章情報のDB登録
                db_model.insert_records_sentences_table(inserted_info)
        pbar.close()


def preprocess():
    wiki = WikiProcessing()
    wiki_files = wiki.get_files()
    wiki_word_processing = WordProcessing(wiki, wiki_files)
    wiki_words_frequency = wiki_word_processing.extract_words_fequency()
    # 単語情報のDB登録
    db_model = DbModel(CONFIG['db_file_name'])
    db_model.insert_records_words_table(wiki_words_frequency)

    words_info = db_model.select_all_records_words_table()
    wiki_word_processing.transfer_sentence_word2idx(words_info, db_model)
    db_model.close_connection()
